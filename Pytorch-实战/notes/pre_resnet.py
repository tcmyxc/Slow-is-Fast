#!/usr/bin/python3
# coding=utf-8
# @Author : 徐文祥
# @Time : 2021/8/14 22:53

import torch.nn as nn
# 模型放在 torchvision
from torchvision import models

class ResNet34(nn.Module):
    def __init__(self):
        super(ResNet34, self).__init__()
        self.model = models.resnet34(pretrained=True)
        self.num_features = self.model.fc.in_features
        self.model.fc = nn.Linear(self.num_features, 10)

    def forward(self, x):
        out = self.model(x)

        return out

def pytorch_resnet34():
    return ResNet34()