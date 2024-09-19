# -*- coding: utf-8 -*-
# @Time   : 2024/07/30 10:24
# @Author : zip
# @Moto   : Knowledge comes from decomposition

from __future__ import absolute_import, division, print_function

from dataclasses import dataclass
from typing import Optional

import torch
from transformers import PretrainedConfig, PreTrainedModel
from transformers.utils import ModelOutput


@dataclass
class CtrModelOutput(ModelOutput):
    loss: Optional[torch.Tensor] = None
    logits: Optional[torch.Tensor] = None


class CtrWithDNNConfig(PretrainedConfig):
    model_type = "CtrWithDNN"

    def __init__(
        self,
        features=None,
        embedding_size=64,
        feature_hidden_size=[64, 64],
        mlp_hidden_size=[64, 64],
        label_name="label",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.features = features
        self.embedding_size = embedding_size
        self.feature_hidden_size = feature_hidden_size
        self.mlp_hidden_size = mlp_hidden_size
        self.label_name = label_name


class CtrWithDNN(PreTrainedModel):
    """
    模型：feature-mutli-tower-mlp
    结构：
    fea1     fea2      fea3     fea4
     |         |         |        |
    mlp       mlp       mlp      mlp
     |_________|_________|________|
                    |
                  concat
                    |
                   mlp
                    |
                   out
    """

    def __init__(self, config: PretrainedConfig):
        super().__init__(config)
        self.embedding_size = config.embedding_size
        self.feature_hidden_size = config.feature_hidden_size
        self.mlp_hidden_size = config.mlp_hidden_size
        self.label_name = config.label_name
        self.features = config.features

        #  define embedding layer
        self.feature_layer = torch.nn.ModuleDict()
        input_len = 0
        for name, feature in self.features.items():
            if feature["shared_embed_name"] is not None:
                continue

            f_layer = torch.nn.Sequential()
            f_layer.add_module(
                name + "_emb",
                torch.nn.Embedding(
                    len(feature["vocab"]),
                    self.embedding_size,
                ),
            )
            for i in range(len(self.feature_hidden_size)):
                if i == 0:
                    f_layer.add_module(
                        name + "_nn_" + str(i),
                        torch.nn.Linear(
                            self.embedding_size,
                            self.feature_hidden_size[i],
                        ),
                    )
                else:
                    f_layer.add_module(
                        name + "_nn_" + str(i),
                        torch.nn.Linear(
                            self.feature_hidden_size[i - 1],
                            self.feature_hidden_size[i],
                        ),
                    )
                f_layer.add_module(name + "_relu_" + str(i), torch.nn.LeakyReLU())

            input_len += self.feature_hidden_size[-1]
            self.feature_layer[name] = f_layer

        # net
        self.hidden = torch.nn.Sequential()
        for i in range(len(self.mlp_hidden_size)):
            if i == 0:
                self.hidden.add_module(
                    "dnn_hidden_" + str(i),
                    torch.nn.Linear(input_len, self.mlp_hidden_size[i]),
                )
            else:
                self.hidden.add_module(
                    "dnn_hidden_" + str(i),
                    torch.nn.Linear(
                        self.mlp_hidden_size[i - 1], self.mlp_hidden_size[i]
                    ),
                )
            self.hidden.add_module("dnn_relu_" + str(i), torch.nn.LeakyReLU())

        # out
        self.out = torch.nn.Linear(self.mlp_hidden_size[-1], 1)

        # loss
        self.criterion = torch.nn.BCELoss()

        self._init_weight_()

    def _init_weight_(self):
        for m in self.feature_layer.values():
            if isinstance(m, torch.nn.Embedding):
                torch.nn.init.normal_(m.weight, std=0.01)
            if isinstance(m, torch.nn.Linear):
                torch.nn.init.xavier_normal_(m.weight)
                torch.nn.init.zeros_(m.bias)

        for m in self.hidden:
            if isinstance(m, torch.nn.Linear):
                torch.nn.init.xavier_normal_(m.weight)
                torch.nn.init.zeros_(m.bias)
        torch.nn.init.kaiming_uniform_(self.out.weight, a=1, nonlinearity="sigmoid")
        torch.nn.init.zeros_(self.out.bias)

    def forward(self, **kwargs):
        inputs = []
        for name, feature in self.features.items():
            if feature["shared_embed_name"] is None:  # shared_embed
                tmp = self.feature_layer[name](kwargs[name])
            else:
                tmp = self.feature_layer[feature["shared_embed_name"]](kwargs[name])
            inputs.append(torch.mean(tmp, dim=1))

        # concat
        out = torch.cat(inputs, dim=-1)
        out = self.hidden(out)

        logits = self.out(out)
        logits = torch.sigmoid(logits)

        labels = None
        if self.label_name in kwargs:
            labels = kwargs[self.label_name]

        if labels is None:
            return CtrModelOutput(logits=logits)

        shift_labels = labels.float().contiguous().view(-1)
        shift_logits = logits.contiguous().view(-1)
        loss = self.criterion(shift_logits, shift_labels)

        return CtrModelOutput(
            loss=loss,
            logits=shift_logits,
        )
