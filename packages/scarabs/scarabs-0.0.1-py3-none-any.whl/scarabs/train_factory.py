# -*- coding: utf-8 -*-
# @Time   : 2024/08/30 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition

from __future__ import absolute_import, division, print_function

import os
import sys
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import torch
from loguru import logger
from torch.utils.data import Dataset, RandomSampler
from transformers.trainer import (
    TRAINER_STATE_NAME,
    DebugOption,
    EvalPrediction,
    HPSearchBackend,
    ParallelMode,
    Trainer,
    TrainerState,
    TrainOutput,
    accelerate_version,
    deepspeed_init,
    deepspeed_load_checkpoint,
    denumpify_detensorize,
    dist,
    get_model_param_count,
    has_length,
    hp_params,
    is_accelerate_available,
    is_apex_available,
    is_torch_xla_available,
    math,
    nested_concat,
    nested_detach,
    nn,
    shutil,
    skip_first_batches,
    speed_metrics,
    time,
    version,
)
from transformers.trainer_callback import (
    IntervalStrategy,
    TrainerCallback,
)

if is_apex_available():
    from apex import amp  # type: ignore
if is_torch_xla_available():
    import torch_xla.core.xla_model as xm  # type: ignore
    import torch_xla.debug.metrics as met  # type: ignore
if is_accelerate_available():
    from accelerate import __version__ as accelerate_version
    from accelerate import skip_first_batches

    DATA_SAMPLERS = [RandomSampler]
    if version.parse(accelerate_version) > version.parse("0.23.0"):
        from accelerate.data_loader import SeedableRandomSampler

        DATA_SAMPLERS += [SeedableRandomSampler]


# EvalData Early stop callback function
class EarlyStoppingByEvalDataCallback(TrainerCallback):
    """Determine whether to stop early based on evaluation data
    early_stopping_patience: Judgment frequency，
    early_stopping_threshold: Difference, stop if the condition is not met once within the number of judgments
    """

    def __init__(
        self,
        early_stopping_patience: int = 10,
        early_stopping_threshold: Optional[float] = 1e-7,
    ):
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_threshold = early_stopping_threshold
        # early_stopping_patience_counter denotes the number of times validation metrics failed to improve.
        self.early_stopping_patience_counter = 0

    def check_metric_value(self, args, state, control, metric_value):
        # best_metric is set by code for load_best_model
        operator = np.greater if args.greater_is_better else np.less
        if state.best_metric is None or (
            operator(metric_value, state.best_metric)
            and abs(metric_value - state.best_metric) > self.early_stopping_threshold
        ):
            self.early_stopping_patience_counter = 0
        else:
            self.early_stopping_patience_counter += 1

    def on_train_begin(self, args, state, control, **kwargs):
        assert (
            args.load_best_model_at_end
        ), "EarlyStoppingCallback requires load_best_model_at_end = True"
        assert (
            args.metric_for_best_model is not None
        ), "EarlyStoppingCallback requires metric_for_best_model is defined"
        assert (
            args.evaluation_strategy != IntervalStrategy.NO
        ), "EarlyStoppingCallback requires IntervalStrategy of steps or epoch"

    def on_evaluate(self, args, state, control, metrics, **kwargs):
        metric_to_check = args.metric_for_best_model
        # if not metric_to_check.startswith("eval_"):
        #     metric_to_check = f"eval_{metric_to_check}"
        metric_value = metrics.get(metric_to_check)

        if metric_value is None:
            logger.warning(
                f"early stopping required metric_for_best_model, but did not find {metric_to_check} so early stopping"
                " is disabled"
            )
            return

        self.check_metric_value(args, state, control, metric_value)
        if self.early_stopping_patience_counter >= self.early_stopping_patience:
            control.should_training_stop = True


# TrainData Early stop callback function
class EarlyStoppingByTrainDataCallback(TrainerCallback):
    """Determine whether to stop early based on train data
    early_stopping_patience: Judgment frequency，
    early_stopping_threshold: Difference, stop if the condition is not met once within the number of judgments
    """

    def __init__(
        self,
        early_stopping_patience: int = 10,
        early_stopping_threshold: Optional[float] = 1e-7,
    ):
        self.early_stopping_patience = early_stopping_patience
        self.early_stopping_threshold = early_stopping_threshold
        # early_stopping_patience_counter denotes the number of times validation metrics failed to improve.
        self.early_stopping_patience_counter = 0

    def check_metric_value(self, args, state, control, metric_value):
        # best_metric is set by code for load_best_model
        operator = np.greater if args.greater_is_better else np.less
        if state.best_metric is None or (
            operator(metric_value, state.best_metric)
            and abs(metric_value - state.best_metric) > self.early_stopping_threshold
        ):
            self.early_stopping_patience_counter = 0
        else:
            self.early_stopping_patience_counter += 1

    def on_train_begin(self, args, state, control, **kwargs):
        # assert args.load_best_model_at_end, "EarlyStoppingCallback requires load_best_model_at_end = True"
        # assert (
        #     args.metric_for_best_model is not None
        # ), "EarlyStoppingCallback requires metric_for_best_model is defined"
        # assert (
        #     args.evaluation_strategy != IntervalStrategy.NO
        # ), "EarlyStoppingCallback requires IntervalStrategy of steps or epoch"
        pass

    def on_evaluate(self, args, state, control, metrics, **kwargs):
        metric_to_check = args.metric_for_best_model
        # if not metric_to_check.startswith("eval_"):
        #     metric_to_check = f"eval_{metric_to_check}"
        metric_value = metrics.get(metric_to_check)

        if metric_value is None:
            logger.warning(
                f"early stopping required metric_for_best_model, but did not find {metric_to_check} so early stopping"
                " is disabled"
            )
            return

        self.check_metric_value(args, state, control, metric_value)
        if self.early_stopping_patience_counter >= self.early_stopping_patience:
            control.should_training_stop = True


# class Trainer reconstruction
class TrainerFactory(Trainer):
    def _inner_training_loop(
        self,
        batch_size=None,
        args=None,
        resume_from_checkpoint=None,
        trial=None,
        ignore_keys_for_eval=None,
    ):
        ################################################################################
        # Environment Settings
        ################################################################################
        if batch_size is None:
            raise ValueError("batch_size is None")
        if args is None:
            raise ValueError("args is None")

        self.accelerator.free_memory()
        self._train_batch_size = batch_size
        if self.args.auto_find_batch_size:
            self.state.train_batch_size = self._train_batch_size
        logger.debug(
            f"Currently training with a batch size of: {self._train_batch_size}"
        )
        # Data loader and number of training steps
        train_dataloader = self.get_train_dataloader()

        # Setting up training control variables:
        # number of training epochs: num_train_epochs
        # number of training steps per epoch: num_update_steps_per_epoch
        # total number of training steps to execute: max_steps
        total_train_batch_size = (
            self._train_batch_size * args.gradient_accumulation_steps * args.world_size
        )

        len_dataloader = None
        num_train_tokens = None
        if has_length(train_dataloader):
            len_dataloader = len(train_dataloader)
            num_update_steps_per_epoch = (
                len_dataloader // args.gradient_accumulation_steps
            )
            num_update_steps_per_epoch = max(num_update_steps_per_epoch, 1)
            num_examples = self.num_examples(train_dataloader)
            if args.max_steps > 0:
                max_steps = args.max_steps
                num_train_epochs = args.max_steps // num_update_steps_per_epoch + int(
                    args.max_steps % num_update_steps_per_epoch > 0
                )
                # May be slightly incorrect if the last batch in the training dataloader has a smaller size but it's
                # the best we can do.
                num_train_samples = args.max_steps * total_train_batch_size
                if args.include_tokens_per_second:
                    num_train_tokens = (
                        self.num_tokens(train_dataloader, args.max_steps)
                        * args.gradient_accumulation_steps
                    )
            else:
                max_steps = math.ceil(
                    args.num_train_epochs * num_update_steps_per_epoch
                )
                num_train_epochs = math.ceil(args.num_train_epochs)
                num_train_samples = (
                    self.num_examples(train_dataloader) * args.num_train_epochs
                )
                if args.include_tokens_per_second:
                    num_train_tokens = (
                        self.num_tokens(train_dataloader) * args.num_train_epochs
                    )
        # Rely on max_steps when dataloader does not have a working size
        elif args.max_steps > 0:
            max_steps = args.max_steps
            # Setting a very large number of epochs so we go as many times as necessary over the iterator.
            num_train_epochs = sys.maxsize
            num_update_steps_per_epoch = max_steps
            num_examples = total_train_batch_size * args.max_steps
            num_train_samples = args.max_steps * total_train_batch_size
            if args.include_tokens_per_second:
                num_train_tokens = (
                    self.num_tokens(train_dataloader, args.max_steps)
                    * args.gradient_accumulation_steps
                )
        else:
            raise ValueError(
                "args.max_steps must be set to a positive value if dataloader does not have a length, was"
                f" {args.max_steps}"
            )

        delay_optimizer_creation = self.is_fsdp_xla_enabled or self.is_fsdp_enabled

        # We need to reset the scheduler, as its parameters may be different on subsequent calls
        if self._created_lr_scheduler:
            self.lr_scheduler = None
            self._created_lr_scheduler = False

        if self.is_deepspeed_enabled:
            self.optimizer, self.lr_scheduler = deepspeed_init(
                self, num_training_steps=max_steps
            )

        if not delay_optimizer_creation:
            self.create_optimizer_and_scheduler(num_training_steps=max_steps)

        self.state = TrainerState()
        self.state.is_hyper_param_search = trial is not None
        self.state.train_batch_size = self._train_batch_size

        # Compute absolute values for logging, eval, and save if given as ratio
        if args.logging_steps is not None:
            if args.logging_steps < 1:
                self.state.logging_steps = math.ceil(max_steps * args.logging_steps)
            else:
                self.state.logging_steps = args.logging_steps
        if args.eval_steps is not None:
            if args.eval_steps < 1:
                self.state.eval_steps = math.ceil(max_steps * args.eval_steps)
            else:
                self.state.eval_steps = args.eval_steps
        if args.save_steps is not None:
            if args.save_steps < 1:
                self.state.save_steps = math.ceil(max_steps * args.save_steps)
            else:
                self.state.save_steps = args.save_steps

        # Activate gradient checkpointing if needed
        if args.gradient_checkpointing:
            if args.gradient_checkpointing_kwargs is None:
                gradient_checkpointing_kwargs = {}
            else:
                gradient_checkpointing_kwargs = args.gradient_checkpointing_kwargs

            self.model.gradient_checkpointing_enable(
                gradient_checkpointing_kwargs=gradient_checkpointing_kwargs
            )

        model = self._wrap_model(self.model_wrapped)

        # as the model is wrapped, don't use `accelerator.prepare`
        # this is for unhandled cases such as
        # FSDP-XLA, SageMaker MP/DP, DataParallel, IPEX
        use_accelerator_prepare = True if model is self.model else False

        if delay_optimizer_creation:
            self.create_optimizer_and_scheduler(num_training_steps=max_steps)

        # prepare using `accelerator` prepare
        if use_accelerator_prepare:
            self.model.train()
            if hasattr(self.lr_scheduler, "step"):
                if self.use_apex:
                    model = self.accelerator.prepare(self.model)
                else:
                    model, self.optimizer = self.accelerator.prepare(
                        self.model, self.optimizer
                    )
            else:
                # to handle cases wherein we pass "DummyScheduler" such as when it is specified in DeepSpeed config.
                model, self.optimizer, self.lr_scheduler = self.accelerator.prepare(
                    self.model, self.optimizer, self.lr_scheduler
                )

        if self.is_fsdp_enabled:
            self.model = self.model_wrapped = model

        # for the rest of this function `model` is the outside model, whether it was wrapped or not
        if model is not self.model:
            self.model_wrapped = model

        # backward compatibility
        if self.is_deepspeed_enabled:
            self.deepspeed = self.model_wrapped

        # ckpt loading
        if resume_from_checkpoint is not None:
            if self.is_deepspeed_enabled:
                deepspeed_load_checkpoint(self.model_wrapped, resume_from_checkpoint)
            elif self.is_fsdp_enabled:
                self._load_from_checkpoint(resume_from_checkpoint, self.model_wrapped)

        # Check if saved optimizer or scheduler states exist
        self._load_optimizer_and_scheduler(resume_from_checkpoint)

        ################################################################################
        # Train! Settings
        ################################################################################
        # important: at this point:
        # self.model         is the Transformers Model
        # self.model_wrapped is DDP(Transformers Model), Deepspeed(Transformers Model),
        # FSDP(Transformers Model), Dynamo Optimized Module(Transformers Model) etc.

        logger.info("***** Running training *****")
        logger.info(f"  Num examples = {num_examples:,}")
        logger.info(f"  Num Epochs = {num_train_epochs:,}")
        logger.info(
            f"  Instantaneous batch size per device = {self.args.per_device_train_batch_size:,}"
        )
        if self.args.per_device_train_batch_size != self._train_batch_size:
            logger.info(
                f"  Training with DataParallel so batch size has been adjusted to: {self._train_batch_size:,}"
            )
        logger.info(
            f"  Total train batch size (w. parallel, distributed & accumulation) = {total_train_batch_size:,}"
        )
        logger.info(
            f"  Gradient Accumulation steps = {args.gradient_accumulation_steps}"
        )
        logger.info(f"  Total optimization steps = {max_steps:,}")
        logger.info(
            f"  Number of trainable parameters = {get_model_param_count(model, trainable_only=True):,}"
        )

        self.state.epoch = 0
        start_time = time.time()
        epochs_trained = 0
        steps_trained_in_current_epoch = 0
        steps_trained_progress_bar = None

        # Check if continuing training from a checkpoint
        if resume_from_checkpoint is not None and os.path.isfile(
            os.path.join(resume_from_checkpoint, TRAINER_STATE_NAME)
        ):
            self.state = TrainerState.load_from_json(
                os.path.join(resume_from_checkpoint, TRAINER_STATE_NAME)
            )
            epochs_trained = self.state.global_step // num_update_steps_per_epoch
            if not args.ignore_data_skip:
                steps_trained_in_current_epoch = self.state.global_step % (
                    num_update_steps_per_epoch
                )
                steps_trained_in_current_epoch *= args.gradient_accumulation_steps
            else:
                steps_trained_in_current_epoch = 0

            logger.info(
                "  Continuing training from checkpoint, will skip to saved global_step"
            )
            logger.info(f"  Continuing training from epoch {epochs_trained}")
            logger.info(
                f"  Continuing training from global step {self.state.global_step}"
            )
            if not args.ignore_data_skip:
                logger.info(
                    f"  Will skip the first {epochs_trained} epochs then the first"
                    f" {steps_trained_in_current_epoch} batches in the first epoch."
                )

        # Update the references
        self.callback_handler.model = self.model
        self.callback_handler.optimizer = self.optimizer  # type: ignore
        self.callback_handler.lr_scheduler = self.lr_scheduler  # type: ignore
        self.callback_handler.train_dataloader = train_dataloader  # type: ignore

        if self.hp_name is not None and self._trial is not None:
            # use self._trial because the SigOpt/Optuna hpo only call `_hp_search_setup(trial)` instead of passing trial
            # parameter to Train when using DDP.
            self.state.trial_name = self.hp_name(self._trial)
        if trial is not None:
            assignments = (
                trial.assignments
                if self.hp_search_backend == HPSearchBackend.SIGOPT
                else trial
            )
            self.state.trial_params = hp_params(assignments)

        # This should be the same if the state has been saved but in case the training arguments changed, it's safer
        # to set this after the load.
        self.state.max_steps = max_steps
        self.state.num_train_epochs = num_train_epochs
        self.state.is_local_process_zero = self.is_local_process_zero()
        self.state.is_world_process_zero = self.is_world_process_zero()

        # tr_loss is a tensor to avoid synchronization of TPUs through .item()
        tr_loss = torch.tensor(0.0).to(args.device)
        # _total_loss_scalar is updated everytime .item() has to be called on tr_loss and stores the sum of all losses
        self._total_loss_scalar = 0.0
        self._globalstep_last_logged = self.state.global_step
        model.zero_grad()

        self.control = self.callback_handler.on_train_begin(
            args, self.state, self.control
        )

        ################################################################################
        # Train Start
        ################################################################################

        ################################################################################
        # reconstuct start
        ################################################################################
        self.train_metrics = None
        ################################################################################
        # reconstuct end
        ################################################################################
        total_batched_samples = 0
        for epoch in range(epochs_trained, num_train_epochs):
            epoch_iterator = train_dataloader
            if hasattr(epoch_iterator, "set_epoch"):
                epoch_iterator.set_epoch(epoch)  # type: ignore

            # Reset the past mems state at the beginning of each epoch if necessary.
            if args.past_index >= 0:
                self._past = None

            steps_in_epoch = (
                len(epoch_iterator)
                if len_dataloader is not None
                else args.max_steps * args.gradient_accumulation_steps
            )

            self.control = self.callback_handler.on_epoch_begin(
                args, self.state, self.control
            )

            if (
                epoch == epochs_trained
                and resume_from_checkpoint is not None
                and steps_trained_in_current_epoch == 0
            ):
                self._load_rng_state(resume_from_checkpoint)

            rng_to_sync = False
            steps_skipped = 0
            if steps_trained_in_current_epoch > 0:
                epoch_iterator = skip_first_batches(
                    epoch_iterator, steps_trained_in_current_epoch
                )
                steps_skipped = steps_trained_in_current_epoch
                steps_trained_in_current_epoch = 0
                rng_to_sync = True

            ############################################################################
            # reconstuct start
            ############################################################################
            self.all_preds = None
            self.all_labels = None
            ############################################################################
            # reconstuct end
            ############################################################################

            step = -1
            for step, inputs in enumerate(epoch_iterator):
                total_batched_samples += 1

                if self.args.include_num_input_tokens_seen:
                    main_input_name = getattr(
                        self.model, "main_input_name", "input_ids"
                    )
                    if main_input_name not in inputs:
                        logger.warning(
                            "Tried to track the number of tokens seen, however the current model is "
                            "not configured properly to know what item is the input. To fix this, add "
                            "a `main_input_name` attribute to the model class you are using."
                        )
                    else:
                        self.state.num_input_tokens_seen += self.accelerator.gather(
                            inputs[main_input_name]
                        ).numel()  # type: ignore
                if rng_to_sync:
                    self._load_rng_state(resume_from_checkpoint)
                    rng_to_sync = False

                # Skip past any already trained steps if resuming training
                if steps_trained_in_current_epoch > 0:
                    steps_trained_in_current_epoch -= 1
                    if steps_trained_progress_bar is not None:
                        steps_trained_progress_bar.update(1)
                    if steps_trained_in_current_epoch == 0:
                        self._load_rng_state(resume_from_checkpoint)
                    continue
                elif steps_trained_progress_bar is not None:
                    steps_trained_progress_bar.close()
                    steps_trained_progress_bar = None

                if step % args.gradient_accumulation_steps == 0:
                    self.control = self.callback_handler.on_step_begin(
                        args, self.state, self.control
                    )

                ########################################################################
                # reconstuct start
                ########################################################################
                with self.accelerator.accumulate(model):
                    out = self.training_step(model, inputs)
                    outputs = None
                    labels = None
                    if isinstance(out, Tuple):
                        tr_loss_step, outputs, labels = out
                    else:
                        tr_loss_step = out
                ########################################################################
                # reconstuct end
                ########################################################################

                if (
                    args.logging_nan_inf_filter
                    and not is_torch_xla_available()
                    and (torch.isnan(tr_loss_step) or torch.isinf(tr_loss_step))
                ):
                    # if loss is nan or inf simply add the average of previous logged losses
                    tr_loss += tr_loss / (
                        1 + self.state.global_step - self._globalstep_last_logged
                    )
                else:
                    tr_loss += tr_loss_step

                self.current_flos += float(self.floating_point_ops(inputs))
                is_last_step_and_steps_less_than_grad_acc = (
                    steps_in_epoch <= args.gradient_accumulation_steps
                    and (step + 1) == steps_in_epoch
                )
                if (
                    total_batched_samples % args.gradient_accumulation_steps == 0
                    or
                    # last step in epoch but step is always smaller than gradient_accumulation_steps
                    is_last_step_and_steps_less_than_grad_acc
                ):
                    # the `or` condition of `is_last_step_and_steps_less_than_grad_acc` is not covered
                    # in accelerate. So, explicitly enable sync gradients to True in that case.
                    if is_last_step_and_steps_less_than_grad_acc:
                        self.accelerator.gradient_state._set_sync_gradients(True)

                    # Gradient clipping
                    if args.max_grad_norm is not None and args.max_grad_norm > 0:
                        # deepspeed does its own clipping
                        if self.use_apex:
                            # Revert to normal clipping otherwise, handling Apex or full precision
                            nn.utils.clip_grad_norm_(
                                amp.master_params(self.optimizer),
                                args.max_grad_norm,
                            )
                        else:
                            self.accelerator.clip_grad_norm_(
                                model.parameters(),
                                args.max_grad_norm,
                            )

                    # Optimizer step
                    self.optimizer.step()  # type: ignore
                    optimizer_was_run = not self.accelerator.optimizer_step_was_skipped
                    if optimizer_was_run:
                        # Delay optimizer scheduling until metrics are generated
                        if not isinstance(
                            self.lr_scheduler,
                            torch.optim.lr_scheduler.ReduceLROnPlateau,
                        ):
                            self.lr_scheduler.step()  # type: ignore

                    model.zero_grad()
                    self.state.global_step += 1
                    self.state.epoch = (
                        epoch + (step + 1 + steps_skipped) / steps_in_epoch
                    )
                    self.control = self.callback_handler.on_step_end(
                        args, self.state, self.control
                    )

                    self._maybe_log_save_evaluate(
                        tr_loss,
                        model,
                        trial,
                        epoch,
                        ignore_keys_for_eval,
                        outputs,
                        labels,
                    )
                else:
                    self.control = self.callback_handler.on_substep_end(
                        args, self.state, self.control
                    )

                if self.control.should_epoch_stop or self.control.should_training_stop:
                    break

            if step < 0:
                logger.warning(
                    "There seems to be not a single sample in your epoch_iterator, stopping training at step"
                    f" {self.state.global_step}! This is expected if you're using an IterableDataset and set"
                    f" num_steps ({max_steps}) higher than the number of available samples."
                )
                self.control.should_training_stop = True

            self.control = self.callback_handler.on_epoch_end(
                args, self.state, self.control
            )
            self._maybe_log_save_evaluate(
                tr_loss, model, trial, epoch, ignore_keys_for_eval, outputs, labels
            )

            if DebugOption.TPU_METRICS_DEBUG in self.args.debug:
                if is_torch_xla_available():
                    # tpu-comment: Logging debug metrics for PyTorch/XLA (compile, execute times, ops, etc.)
                    xm.master_print(met.metrics_report())
                else:
                    logger.warning(
                        "You enabled PyTorch/XLA debug metrics but you don't have a TPU "
                        "configured. Check your training configuration if this is unexpected."
                    )
            if self.control.should_training_stop:
                break

        if args.past_index and hasattr(self, "_past"):
            # Clean the state at the end of training
            delattr(self, "_past")

        logger.info("\n\nTraining completed =)\n\n")
        if args.load_best_model_at_end and self.state.best_model_checkpoint is not None:
            # Wait for everyone to get here so we are sure the model has been saved by process 0.
            if is_torch_xla_available():
                xm.rendezvous("load_best_model_at_end")
            elif args.parallel_mode == ParallelMode.DISTRIBUTED:
                dist.barrier()

            self._load_best_model()

        # add remaining tr_loss
        # self._total_loss_scalar += tr_loss.item()
        # train_loss = self._total_loss_scalar / self.state.global_step
        train_loss = self._total_loss_scalar
        metrics = speed_metrics(
            "train",
            start_time,
            num_samples=num_train_samples,
            num_steps=self.state.max_steps,
            num_tokens=num_train_tokens,
        )
        self.store_flos()
        metrics["total_flos"] = self.state.total_flos
        metrics["train_loss"] = train_loss

        ################################################################################
        # reconstuct start
        ################################################################################
        if self.train_metrics is not None:
            metrics.update(self.train_metrics)
        ################################################################################
        # reconstuct end
        ################################################################################

        self.is_in_train = False

        self._memory_tracker.stop_and_update_metrics(metrics)

        self.log(metrics)

        run_dir = self._get_output_dir(trial)
        checkpoints_sorted = self._sorted_checkpoints(
            use_mtime=False, output_dir=run_dir
        )

        # Delete the last checkpoint when save_total_limit=1 if it's different from the best checkpoint and process allowed to save.
        if (
            self.args.should_save
            and self.state.best_model_checkpoint is not None
            and self.args.save_total_limit == 1
        ):
            for checkpoint in checkpoints_sorted:
                if not os.path.samefile(checkpoint, self.state.best_model_checkpoint):
                    logger.info(
                        f"Deleting older checkpoint [{checkpoint}] due to args.save_total_limit"
                    )
                    shutil.rmtree(checkpoint)

        self.control = self.callback_handler.on_train_end(
            args, self.state, self.control
        )

        # Wait for the checkpoint to be uploaded.
        self._finish_current_push()

        # After training we make sure to retrieve back the original forward pass method
        # for the embedding layer by removing the forward post hook.
        if self.neftune_noise_alpha is not None:
            self._deactivate_neftune(self.model)

        return TrainOutput(self.state.global_step, train_loss, metrics)

    def _maybe_log_save_evaluate(
        self, tr_loss, model, trial, epoch, ignore_keys_for_eval, outputs, labels
    ):
        ################################################################################
        # reconstuct start
        ################################################################################
        if outputs is not None and labels is not None:
            logits = outputs.get("logits", None)
            logits = self.accelerator.pad_across_processes(
                logits, dim=1, pad_index=-100
            )
            labels = self.accelerator.pad_across_processes(
                labels, dim=1, pad_index=-100
            )

            if self.preprocess_logits_for_metrics is not None:
                logits = self.preprocess_logits_for_metrics(logits, labels)  # type: ignore

            logits = self.gather_function((logits))
            self.all_preds = (
                logits
                if self.all_preds is None
                else nested_concat(self.all_preds, logits, padding_index=-100)
            )

            labels = self.gather_function((labels))
            self.all_labels = (
                labels
                if self.all_labels is None
                else nested_concat(self.all_labels, labels, padding_index=-100)
            )
        ################################################################################
        # reconstuct end
        ################################################################################
        if self.control.should_log:
            if is_torch_xla_available():
                xm.mark_step()

            logs: Dict[str, float] = {}

            # all_gather + mean() to get average loss over all processes
            tr_loss_scalar = self._nested_gather(tr_loss).mean().item()  # type: ignore

            # reset tr_loss to zero
            tr_loss -= tr_loss

            logs["loss"] = round(
                tr_loss_scalar
                / (self.state.global_step - self._globalstep_last_logged),
                4,
            )
            logs["learning_rate"] = self._get_learning_rate()

            ############################################################################
            # reconstuct start
            ############################################################################
            # self._total_loss_scalar += tr_loss_scalar
            self._total_loss_scalar = logs["loss"]
            ############################################################################
            # reconstuct end
            ############################################################################
            self._globalstep_last_logged = self.state.global_step
            self.store_flos()

            ############################################################################
            # reconstuct start
            ############################################################################
            if (
                self.compute_metrics is not None
                and self.all_preds is not None
                and self.all_labels is not None
            ):
                # For exceeding the length, remove the previous values
                current_length = len(self.all_preds)
                if current_length > 100000:
                    self.all_preds = self.all_preds[-100000:]
                    self.all_labels = self.all_labels[-100000:]

                tr_metrics = self.compute_metrics(
                    EvalPrediction(
                        predictions=self.all_preds,  # type: ignore
                        label_ids=self.all_labels,  # type: ignore
                    )
                )

                preds_mean = self._nested_gather(self.all_preds).float().mean().item()  # type: ignore
                labels_mean = self._nested_gather(self.all_labels).float().mean().item()  # type: ignore
                logs.update(
                    {
                        "train_preds_mean": round(preds_mean, 6),
                        "train_labels_mean": round(labels_mean, 6),
                    }
                )
                tr_metrics = denumpify_detensorize(tr_metrics)
                if isinstance(tr_metrics, dict):
                    for key in list(tr_metrics.keys()):
                        tr_metrics[f"train_{key}"] = round(tr_metrics.pop(key), 6)
                    logs.update(tr_metrics)
                    self.train_metrics = tr_metrics
                    self.train_metrics.update(
                        {
                            "train_preds_mean": round(preds_mean, 6),
                            "train_labels_mean": round(labels_mean, 6),
                        }
                    )
            ############################################################################
            # reconstuct end
            ############################################################################
            self.log(logs)

        metrics = None
        if self.control.should_evaluate:
            if isinstance(self.eval_dataset, dict):
                metrics = {}
                for eval_dataset_name, eval_dataset in self.eval_dataset.items():
                    dataset_metrics = self.evaluate(
                        eval_dataset=eval_dataset,
                        ignore_keys=ignore_keys_for_eval,
                        metric_key_prefix=f"eval_{eval_dataset_name}",
                    )
                    metrics.update(dataset_metrics)
            else:
                metrics = self.evaluate(ignore_keys=ignore_keys_for_eval)
            self._report_to_hp_search(trial, self.state.global_step, metrics)

            # Run delayed LR scheduler now that metrics are populated
            if isinstance(
                self.lr_scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau
            ):
                metric_to_check = self.args.metric_for_best_model
                if not metric_to_check.startswith("eval_"):  # type: ignore
                    metric_to_check = f"eval_{metric_to_check}"
                self.lr_scheduler.step(metrics[metric_to_check])  # type: ignore

        if self.control.should_save:
            self._save_checkpoint(model, trial, metrics=metrics)
            self.control = self.callback_handler.on_save(
                self.args, self.state, self.control
            )

    def evaluate(
        self,
        eval_dataset: Optional[Dataset] = None,
        ignore_keys: Optional[List[str]] = None,
        metric_key_prefix: str = "eval",
    ) -> Dict[str, float]:
        # memory metrics - must set up as early as possible
        self._memory_tracker.start()

        eval_dataloader = self.get_eval_dataloader(eval_dataset)
        start_time = time.time()

        eval_loop = (
            self.prediction_loop
            if self.args.use_legacy_prediction_loop
            else self.evaluation_loop
        )
        output = eval_loop(
            eval_dataloader,
            description="Evaluation",
            # No point gathering the predictions if there are no metrics, otherwise we defer to
            # self.args.prediction_loss_only
            prediction_loss_only=True if self.compute_metrics is None else None,
            ignore_keys=ignore_keys,
            metric_key_prefix=metric_key_prefix,
        )
        if output.metrics is None or output.num_samples is None:
            raise ValueError("You cannot use `evaluate` and `predict` not metrics")

        total_batch_size = self.args.eval_batch_size * self.args.world_size
        if f"{metric_key_prefix}_jit_compilation_time" in output.metrics:
            start_time += output.metrics[f"{metric_key_prefix}_jit_compilation_time"]
        output.metrics.update(
            speed_metrics(
                metric_key_prefix,
                start_time,
                num_samples=output.num_samples,
                num_steps=math.ceil(output.num_samples / total_batch_size),
            )
        )

        ################################################################################
        # reconstuct start
        ################################################################################

        preds_mean = float(np.mean(self._nested_gather(output.predictions)))  # type: ignore
        labels_mean = float(np.mean(self._nested_gather(output.label_ids)))  # type: ignore
        output.metrics.update(
            {
                "eval_preds_mean": round(preds_mean, 6),
                "eval_labels_mean": round(labels_mean, 6),
            }
        )
        self.log(output.metrics)
        ################################################################################
        # reconstuct end
        ################################################################################

        if DebugOption.TPU_METRICS_DEBUG in self.args.debug:
            # tpu-comment: Logging debug metrics for PyTorch/XLA (compile, execute times, ops, etc.)
            xm.master_print(met.metrics_report())

        self.control = self.callback_handler.on_evaluate(
            self.args, self.state, self.control, output.metrics
        )

        self._memory_tracker.stop_and_update_metrics(output.metrics)

        return output.metrics

    def training_step(
        self, model: torch.nn.Module, inputs: Dict[str, Union[torch.Tensor, Any]]
    ):
        """ """
        model.train()
        inputs = self._prepare_inputs(inputs)

        outputs = None
        labels = None
        with self.compute_loss_context_manager():
            out = self.compute_loss(
                model, inputs, return_outputs=False, return_labels=False
            )
            if isinstance(out, Tuple) and len(out) == 3:
                loss, outputs, labels = out
            elif isinstance(out, Tuple) and len(out) == 2:
                loss, outputs = out
            else:
                loss = out

        if self.args.n_gpu > 1:
            loss = loss.mean()  # mean() to average on multi-gpu parallel training

        self.accelerator.backward(loss)

        if outputs is None:
            return loss.detach() / self.args.gradient_accumulation_steps

        return loss.detach() / self.args.gradient_accumulation_steps, outputs, labels

    def compute_loss(self, model, inputs, return_outputs=False, return_labels=False):
        """
        How the loss is computed by Trainer. By default, all models return the loss in the first element.
        """
        has_labels = (
            False
            if len(self.label_names) == 0
            else all(inputs.get(k) is not None for k in self.label_names)
        )

        # labels may be popped when computing the loss (label smoothing for instance) so we grab them first.
        if has_labels:
            labels = nested_detach(tuple(inputs.get(name) for name in self.label_names))
            if len(labels) == 1:
                labels = labels[0]
        else:
            labels = None

        outputs = model(**inputs)
        # Save past state if it exists
        # TODO: this needs to be fixed and made cleaner later.
        if self.args.past_index >= 0:
            self._past = outputs[self.args.past_index]

        if isinstance(outputs, dict) and "loss" not in outputs:
            raise ValueError(
                "The model did not return a loss from the inputs, only the following keys: "
                f"{','.join(outputs.keys())}. For reference, the inputs it received are {','.join(inputs.keys())}."
            )
        # We don't use .loss here since the model may return tuples instead of ModelOutput.
        loss = outputs["loss"] if isinstance(outputs, dict) else outputs[0]
        if not return_labels and return_outputs:
            return loss, outputs
        if return_labels and return_outputs:
            return loss, outputs, labels

        return loss


# LLM Pre training
class TrainerFactoryWithPretrain(TrainerFactory):
    def training_step(
        self, model: torch.nn.Module, inputs: Dict[str, Union[torch.Tensor, Any]]
    ):
        """ """
        model.train()
        inputs = self._prepare_inputs(inputs)

        outputs = None
        labels = None
        with self.compute_loss_context_manager():
            out = self.compute_loss(
                model, inputs, return_outputs=False, return_labels=False
            )
            if isinstance(out, Tuple) and len(out) == 3:
                loss, outputs, labels = out
            elif isinstance(out, Tuple) and len(out) == 2:
                loss, outputs = out
            else:
                loss = out

        if self.args.n_gpu > 1:
            loss = loss.mean()  # mean() to average on multi-gpu parallel training

        self.accelerator.backward(loss)

        if outputs is None:
            return loss.detach() / self.args.gradient_accumulation_steps

        return loss.detach() / self.args.gradient_accumulation_steps, outputs, labels


# Classification
class TrainerFactoryWithLLMClassification(TrainerFactory):
    def training_step(
        self, model: torch.nn.Module, inputs: Dict[str, Union[torch.Tensor, Any]]
    ):
        """
        Classification tasks require displaying evaluation metrics during the training process
        include the following indicators:
        1. Loss
        2. Accuracy
        3. F1
        4. Precision
        5. Recall
        """
        model.train()
        inputs = self._prepare_inputs(inputs)

        outputs = None
        labels = None
        with self.compute_loss_context_manager():
            out = self.compute_loss(
                model, inputs, return_outputs=True, return_labels=True
            )
            if isinstance(out, Tuple) and len(out) == 3:
                loss, outputs, labels = out
            elif isinstance(out, Tuple) and len(out) == 2:
                loss, outputs = out
            else:
                loss = out

        if self.args.n_gpu > 1:
            loss = loss.mean()  # mean() to average on multi-gpu parallel training

        self.accelerator.backward(loss)
        if outputs is None:
            return loss.detach() / self.args.gradient_accumulation_steps

        return loss.detach() / self.args.gradient_accumulation_steps, outputs, labels


# Tabular tasks
class TrainerFactoryWithTabular(TrainerFactory):
    def training_step(
        self, model: torch.nn.Module, inputs: Dict[str, Union[torch.Tensor, Any]]
    ):
        model.train()
        inputs = self._prepare_inputs(inputs)

        outputs = None
        labels = None
        with self.compute_loss_context_manager():
            out = self.compute_loss(
                model, inputs, return_outputs=True, return_labels=True
            )

            if isinstance(out, Tuple) and len(out) == 3:
                loss, outputs, labels = out
            elif isinstance(out, Tuple) and len(out) == 2:
                loss, outputs = out
            else:
                loss = out

        if self.args.n_gpu > 1:
            loss = loss.mean()  # mean() to average on multi-gpu parallel training

        self.accelerator.backward(loss)
        if outputs is None:
            return loss.detach() / self.args.gradient_accumulation_steps

        return loss.detach() / self.args.gradient_accumulation_steps, outputs, labels
