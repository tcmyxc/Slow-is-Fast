#!/usr/bin/python3

import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.modules import batchnorm

class VGGBase(nn.Module):
    def __init__(self):
        super().__init__()

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=64, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU()
        )
        self.max_pooling1 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv2_1 = nn.Sequential(
            nn.Conv2d(in_channels=64, out_channels=128, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU()
        )
        self.conv2_2 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=128, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU()
        )
        self.max_pooling2 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.conv3_1 = nn.Sequential(
            nn.Conv2d(in_channels=128, out_channels=256, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )
        self.conv3_2 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=256, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU()
        )
        self.max_pooling3 = nn.MaxPool2d(kernel_size=2, stride=2, padding=1)

        self.conv4_1 = nn.Sequential(
            nn.Conv2d(in_channels=256, out_channels=512, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.conv4_2 = nn.Sequential(
            nn.Conv2d(in_channels=512, out_channels=512, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(512),
            nn.ReLU()
        )
        self.max_pooling4 = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc = nn.Linear(in_features=512*4, out_features=10)


    def forward(self, x):
        batchsize = x.size(0)
        out = self.conv1(x)
        out = self.max_pooling1(out)

        out = self.conv2_1(out)
        out = self.conv2_2(out)
        out = self.max_pooling2(out)

        out = self.conv3_1(out)
        out = self.conv3_2(out)
        out = self.max_pooling3(out)

        out = self.conv4_1(out)
        out = self.conv4_2(out)
        out = self.max_pooling4(out)

        # 进入 FC 层之前先平铺
        # batchsize * c * h *w --> batchsize * n
        out = out.view(batchsize, -1)
        out = self.fc(out)

        # softmax
        out = F.log_softmax(out, dim=1)

        return out
    
def VGGNet():
    return VGGBase()