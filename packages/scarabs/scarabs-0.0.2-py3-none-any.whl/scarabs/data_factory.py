# -*- coding: utf-8 -*-
# @Time   : 2024/07/30 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition
from __future__ import absolute_import, division, print_function

import os
from itertools import chain
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, Tuple, Union

import torch
from datasets import Dataset, DatasetDict, load_dataset, load_from_disk
from loguru import logger
from transformers import (
    PreTrainedTokenizer,
    PreTrainedTokenizerFast,
    TrainingArguments,
)

from scarabs.args_factory import DataArguments
from scarabs.mora.utils.feature_utils import Feature2Transformer


class DataFactory:
    def __init__(
        self,
        data_args: DataArguments,
        training_args: TrainingArguments,
        tokenizer: PreTrainedTokenizer | PreTrainedTokenizerFast | None = None,
    ):
        self.data_args = data_args
        self.training_args = training_args

        if tokenizer is not None:
            self.tokenizer = tokenizer
            try:
                self.pad_id = self.tokenizer.pad_token_id
                if self.pad_id is None:
                    raise
            except Exception:
                logger.warning(
                    f"The pad_token_id is not set. We set it to {self.tokenizer.eos_token_id}."
                )
                self.pad_id = self.tokenizer.eos_token_id

            if self.pad_id is None:
                raise ValueError("pad_token_id is not set")
            os.makedirs(data_args.dataset_cache, exist_ok=True)

            if (
                data_args.max_seq_length is None
                or data_args.max_seq_length > tokenizer.model_max_length
            ):
                logger.warning(
                    f"The max_seq_length passed ({data_args.max_seq_length}) is larger than the maximum length for the "
                    f"model ({tokenizer.model_max_length}). Using max_seq_length={tokenizer.model_max_length}."
                )
                data_args.max_seq_length = tokenizer.model_max_length
            self.max_seq_length = min(
                data_args.max_seq_length, tokenizer.model_max_length
            )

    def get_dataset(self, files=None, template=None):
        if files is not None:
            dataset = self._prepare_dataset(files, template, "test")
            return dataset, None

        train_dataset = None
        validation_dataset = None
        if self.data_args.train_file is not None:
            train_file = self._get_all_files_abs_path(self.data_args.train_file)
            train_dataset = self._prepare_dataset(train_file, template, "train")

        if self.data_args.validation_file is not None:
            validation_file = self._get_all_files_abs_path(
                self.data_args.validation_file
            )
            validation_dataset = self._prepare_dataset(validation_file, template, "val")

        if train_dataset is None and validation_dataset is None:
            raise ValueError("No dataset is provided")
        if train_dataset is not None and validation_dataset is not None:
            return train_dataset, validation_dataset
        elif train_dataset is not None:
            return train_dataset, None
        else:
            return None, validation_dataset

    def _prepare_dataset(self, files=None, template=None, dtype=None):
        dataset_cache = self.data_args.dataset_cache
        if dtype is not None:
            dataset_cache = os.path.join(dataset_cache, dtype)

        try:
            if self.data_args.overwrite_cache:
                logger.info(f"Overwrite cache")
                raise
            dataset = load_from_disk(dataset_cache, keep_in_memory=False)
            logger.info(f"Finished loading from cache")
            if dataset[0].get("input_ids") is not None:  # type: ignore
                self._sanity_check(
                    dataset[0]["input_ids"][:10][:-1], dataset[0]["input_ids"][:10][1:]
                )
        except Exception:
            if self.data_args.extension is None:
                raise ValueError("no extension is provided")
            dataset = load_dataset(
                self.data_args.extension, data_files=files, split="train"
            )
            logger.info(f"dataset basic info: \n {dataset}")
            if not isinstance(dataset, Dataset):
                raise ValueError(f"dataset is not a Dataset, but {type(dataset)}")
            dataset = self._process(dataset, template)
            logger.info(f"after format_torch dataset[0] info: \n {dataset[0]} \n")
            if dataset[0].get("input_ids") is not None:
                self._sanity_check(
                    dataset[0]["input_ids"][:10][:-1], dataset[0]["input_ids"][:10][1:]
                )
            dataset.save_to_disk(dataset_cache)

        if isinstance(dataset, DatasetDict):
            raise ValueError(f"dataset is not a Dataset, but {type(dataset)}")
        return dataset

    def _sanity_check(self, tokens: List, target: List):
        logger.info("\n Sanity Check >>>>>>>>>>>>> \n")
        for t, m in zip(tokens, target):
            decoded = self.tokenizer.decode([t])
            logger.info("\n %20s: %6d -> %6d \n" % (repr(decoded), t, m))
        logger.info("\n <<<<<<<<<<<<< Sanity Check \n")

        assert len(tokens) == len(
            target
        ), f"length mismatch: {len(tokens)} vs {len(target)}"

    def _get_all_files_abs_path(self, path):
        if isinstance(path, list):
            return [os.path.abspath(p) for p in path]
        elif os.path.isdir(path):
            return [
                os.path.abspath(os.path.join(root, fi))
                for root, dirs, files in os.walk(path)
                for fi in files
            ]
        elif os.path.isfile(path):
            return [os.path.abspath(path)]
        else:
            raise ValueError("Invalid path or unsupported type")

    def _process(self, dataset: Dataset, template: Optional[str] = None):
        if self.data_args.line_by_line:
            # When using line_by_line, we just tokenize each nonempty line.
            padding = "max_length" if self.data_args.pad_to_max_length else False

            def tokenize_function(examples):
                # Remove empty lines
                examples["text"] = [
                    line
                    for line in examples["text"]
                    if len(line) > 0 and not line.isspace()
                ]
                if template is not None:
                    examples["text"] = [
                        template.format(line) for line in examples["text"]
                    ]

                return self.tokenizer(
                    examples["text"],
                    padding=padding,
                    truncation=True,
                    max_length=self.max_seq_length,
                )

            with self.training_args.main_process_first(desc="dataset map tokenization"):
                tokenized_datasets = dataset.map(
                    tokenize_function,
                    batched=True,
                    num_proc=self.data_args.preprocessing_num_workers,
                    remove_columns=["text"],
                    load_from_cache_file=not self.data_args.overwrite_cache,
                    desc="Running tokenizer on dataset line_by_line",
                )

        else:
            # Otherwise, we tokenize every text, then concatenate them together before splitting them in smaller parts.
            def tokenize_function(examples):
                if template is not None:
                    examples["text"] = [
                        template.format(line) for line in examples["text"]
                    ]
                logger.info(f"tokenized_examples len: {len(examples)}")
                return self.tokenizer(examples["text"])

            with self.training_args.main_process_first(desc="dataset map tokenization"):
                tokenized_datasets = dataset.map(
                    tokenize_function,
                    batched=True,
                    num_proc=self.data_args.preprocessing_num_workers,
                    remove_columns="text",
                    load_from_cache_file=not self.data_args.overwrite_cache,
                    desc="Running tokenizer on every text in dataset",
                )

            # Main data processing function that will concatenate all texts from our dataset and generate chunks of
            # max_seq_length.
            def group_texts(examples):
                # Concatenate all texts.
                concatenated_examples = {
                    k: list(chain(*examples[k])) for k in examples.keys()
                }
                total_length = len(concatenated_examples[list(examples.keys())[0]])
                # We drop the small remainder, and if the total_length < max_seq_length  we exclude this batch and return an empty dict.
                # We could add padding if the model supported it instead of this drop, you can customize this part to your needs.
                total_length = (
                    total_length // self.max_seq_length
                ) * self.max_seq_length
                # Split by chunks of max_len.
                result = {
                    k: [
                        t[i : i + self.max_seq_length]
                        for i in range(0, total_length, self.max_seq_length)
                    ]
                    for k, t in concatenated_examples.items()
                }
                return result

            # Note that with `batched=True`, this map processes 1,000 texts together, so group_texts throws away a
            # remainder for each of those groups of 1,000 texts. You can adjust that batch_size here but a higher value
            # might be slower to preprocess.
            #
            # To speed up this part, we use multiprocessing. See the documentation of the map method for more information:
            # https://huggingface.co/docs/datasets/process#map

            with self.training_args.main_process_first(desc="grouping texts together"):
                tokenized_datasets = tokenized_datasets.map(
                    group_texts,
                    batched=True,
                    num_proc=self.data_args.preprocessing_num_workers,
                    load_from_cache_file=not self.data_args.overwrite_cache,
                    desc=f"Grouping texts in chunks of {self.max_seq_length}",
                )

        return tokenized_datasets

    def data_collator_fn(self):
        raise NotImplementedError


class DataFactoryWithPretrain(DataFactory):
    """your data ,data name is suffix .jsonl or .json

    {"text": "your text"}
    {"text": "your text"}

    """

    def _process(self, dataset: Dataset, template: Optional[str] = None):
        if self.data_args.line_by_line:
            # When using line_by_line, we just tokenize each nonempty line.
            padding = "max_length" if self.data_args.pad_to_max_length else False

            def tokenize_function(examples):
                # Remove empty lines
                examples["text"] = [
                    line
                    for line in examples["text"]
                    if len(line) > 0 and not line.isspace()
                ]
                if template is not None:
                    examples["text"] = [
                        template.format(line) for line in examples["text"]
                    ]

                return self.tokenizer(
                    examples["text"],
                    padding=padding,
                    truncation=True,
                    max_length=self.max_seq_length,
                )

            with self.training_args.main_process_first(desc="dataset map tokenization"):
                tokenized_datasets = dataset.map(
                    tokenize_function,
                    batched=True,
                    num_proc=self.data_args.preprocessing_num_workers,
                    remove_columns=["text"],
                    load_from_cache_file=not self.data_args.overwrite_cache,
                    desc="Running tokenizer on dataset line_by_line",
                )

        else:
            # Otherwise, we tokenize every text, then concatenate them together before splitting them in smaller parts.
            def tokenize_function(examples):
                if template is not None:
                    examples["text"] = [
                        template.format(line) for line in examples["text"]
                    ]
                return self.tokenizer(examples["text"])

            with self.training_args.main_process_first(desc="dataset map tokenization"):
                tokenized_datasets = dataset.map(
                    tokenize_function,
                    batched=True,
                    batch_size=3,
                    num_proc=self.data_args.preprocessing_num_workers,
                    remove_columns="text",
                    desc="Running tokenizer on every text in dataset",
                )

            # Main data processing function that will concatenate all texts from our dataset and generate chunks of
            # max_seq_length.
            def group_texts(examples):
                # Concatenate all texts.
                concatenated_examples = {
                    k: list(chain(*examples[k])) for k in examples.keys()
                }
                total_length = len(concatenated_examples[list(examples.keys())[0]])

                # We drop the small remainder, and if the total_length < max_seq_length  we exclude this batch and return an empty dict.
                # We could add padding if the model supported it instead of this drop, you can customize this part to your needs.
                total_length = (
                    total_length // self.max_seq_length
                ) * self.max_seq_length
                # Split by chunks of max_len.
                result = {
                    k: [
                        t[i : i + self.max_seq_length]
                        for i in range(0, total_length, self.max_seq_length)
                    ]
                    for k, t in concatenated_examples.items()
                }
                return result

            # Note that with `batched=True`, this map processes 1,000 texts together, so group_texts throws away a
            # remainder for each of those groups of 1,000 texts. You can adjust that batch_size here but a higher value
            # might be slower to preprocess.
            #
            # To speed up this part, we use multiprocessing. See the documentation of the map method for more information:
            # https://huggingface.co/docs/datasets/process#map

            # with self.training_args.main_process_first(desc="grouping texts together"):
            #     tokenized_datasets = tokenized_datasets.map(
            #         group_texts,
            #         batched=True,
            #         num_proc=self.data_args.preprocessing_num_workers,
            #         desc=f"Grouping texts in chunks of {self.max_seq_length}",
            #     )

        return tokenized_datasets

    def data_collator_fn(self, batch_examples):
        lengths = max(
            [len(x["input_ids"]) for x in batch_examples if x["input_ids"] is not None]
        )
        batch_max_len = min(lengths, self.max_seq_length)

        input_ids_batch, attention_mask_batch, labels_batch = [], [], []
        for example in batch_examples:
            input_ids = example["input_ids"]
            attention_mask = example["attention_mask"]

            # truncate
            input_ids = input_ids[-batch_max_len:]
            attention_mask = attention_mask[-batch_max_len:]

            # padding
            input_ids_real_len = len(input_ids)
            padding_len = batch_max_len - input_ids_real_len
            input_ids = input_ids + [self.pad_id] * padding_len
            attention_mask = attention_mask + [0] * padding_len

            input_ids_batch.append(input_ids)
            attention_mask_batch.append(attention_mask)
            labels_batch.append(input_ids)

        # to tensor
        input_ids_batch = torch.tensor(input_ids_batch, dtype=torch.long)
        attention_mask_batch = torch.tensor(attention_mask_batch, dtype=torch.long)
        labels_batch = torch.tensor(labels_batch, dtype=torch.long)

        inputs = {
            "input_ids": input_ids_batch,
            "attention_mask": attention_mask_batch,
            "labels": labels_batch,
        }

        return inputs


class DataFactoryWithLLMClassification(DataFactory):
    """your data ,data name is suffix .jsonl or .json

    {"text": "your text", "label": "class"}
    {"text": "your text", "label": "class"}

    """

    def _process(self, dataset: Dataset, template: Optional[str] = None):
        # When using line_by_line, we just tokenize each nonempty line.
        padding = "max_length" if self.data_args.pad_to_max_length else False

        def tokenize_function(examples):
            # Remove empty lines
            examples["text"] = [
                line
                for line in examples["text"]
                if len(line) > 0 and not line.isspace()
            ]

            out = self.tokenizer(
                examples["text"],
                padding=padding,
                truncation=True,
                max_length=self.max_seq_length,
            )

            out["labels"] = examples["label"]

            return out

        with self.training_args.main_process_first(desc="dataset map tokenization"):
            tokenized_datasets = dataset.map(
                tokenize_function,
                batched=True,
                num_proc=self.data_args.preprocessing_num_workers,
                remove_columns=["text"],
                load_from_cache_file=not self.data_args.overwrite_cache,
                desc="Running tokenizer on dataset line_by_line",
            )

        return tokenized_datasets

    def data_collator_fn(self, batch_examples):
        lengths = max(
            [len(x["input_ids"]) for x in batch_examples if x["input_ids"] is not None]
        )
        batch_max_len = min(lengths, self.max_seq_length)

        input_ids_batch, attention_mask_batch, labels_batch = [], [], []
        for example in batch_examples:
            input_ids = example["input_ids"]
            attention_mask = example["attention_mask"]
            labels = example["labels"]

            # truncate
            input_ids = input_ids[-batch_max_len:]
            attention_mask = attention_mask[-batch_max_len:]

            # padding
            input_ids_real_len = len(input_ids)
            padding_len = batch_max_len - input_ids_real_len
            input_ids = input_ids + [self.pad_id] * padding_len
            attention_mask = attention_mask + [0] * padding_len

            input_ids_batch.append(input_ids)
            attention_mask_batch.append(attention_mask)
            labels_batch.append(labels)

        # to tensor
        input_ids_batch = torch.tensor(input_ids_batch, dtype=torch.long)
        attention_mask_batch = torch.tensor(attention_mask_batch, dtype=torch.long)
        labels_batch = torch.tensor(labels_batch, dtype=torch.long)

        inputs = {
            "input_ids": input_ids_batch,
            "attention_mask": attention_mask_batch,
            "labels": labels_batch,
        }

        return inputs


class DataFactoryWithTabular(DataFactory):
    def create_feature2transformer(self, config):
        self.FT = Feature2Transformer(
            os.path.join(self.data_args.dataset_cache, "meta")
        )
        self.FT.creat_meta(config)
        if self.data_args.extension is None:
            raise ValueError("no extension is provided")
        train_file = self._get_all_files_abs_path(self.data_args.train_file)
        dataset = load_dataset(
            self.data_args.extension, data_files=train_file, split="train"
        )
        logger.info(f"dataset basic info: \n {dataset}")
        if not isinstance(dataset, Dataset):
            raise ValueError(f"dataset is not a Dataset, but {type(dataset)}")
        valid_columns = list(self.FT.feature2meta.keys())
        dataset = dataset.remove_columns(
            [col for col in dataset.column_names if col not in valid_columns]
        )
        logger.info(f"dataset basic info: \n {dataset}")
        dataset.map(self.FT.build_meta)
        for item in self.FT.feature2meta.items():
            logger.info(f"【{item[0]}】 vocab size: {len(item[1].vocab)}")

        # self.FT.save_meta()

    def load_feature2transformer(self, config):
        try:
            self.FT = Feature2Transformer(
                os.path.join(self.data_args.dataset_cache, "meta")
            )
        except Exception:
            self.FT = Feature2Transformer()
        self.FT.load_meta(config)
        for item in self.FT.feature2meta.items():
            logger.info(f"【{item[0]}】 vocab size: {len(item[1].vocab)}")

    def get_feature2meta(self):
        return self.FT.feature2meta

    def _process(self, dataset: Dataset, template: Optional[str] = None):
        label_names = (
            []
            if self.training_args.label_names is None
            else self.training_args.label_names
        )
        valid_columns = list(self.FT.feature2meta.keys()) + label_names
        dataset = dataset.remove_columns(
            [col for col in dataset.column_names if col not in valid_columns]
        )
        logger.info(f"dataset basic info: \n {dataset}")

        dataset = dataset.map(self.FT.handle)
        logger.info(f"after handle example:  \n {dataset[0]}")
        return dataset

    def data_collator_fn(self, batch_examples):
        X = {}
        for example in batch_examples:
            for name, value in example.items():
                if name not in X:
                    X[name] = []
                X[name].append(value)

        label_names = (
            []
            if self.training_args.label_names is None
            else self.training_args.label_names
        )
        for name in X:
            if name in label_names:
                X[name] = torch.tensor(X[name], dtype=torch.float32)
            else:
                X[name] = torch.tensor(X[name], dtype=torch.long)

        return X
