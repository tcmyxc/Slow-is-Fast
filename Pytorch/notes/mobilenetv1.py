#!/usr/bin/python3

import torch
import torch.nn as nn
import torch.nn.functional as F

# 主要是深度课分离卷积的思想

class MobileNetV1(nn.Module):

    # 核心单元
    def conv_dw(self, in_channel, out_channel, stride):
        # 分组卷积
        return nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=in_channel, 
                        kernel_size=3, stride=stride, padding=1,
                        groups=in_channel, bias=False),
            nn.BatchNorm2d(in_channel),
            nn.ReLU(),

            # 点卷积
            nn.Conv2d(in_channels=in_channel, out_channels=out_channel, 
                        kernel_size=1, stride=1, padding=0, bias=False),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(),
        )

    def __init__(self):
        super().__init__()
        
        # 第一个卷积一般使用标准的卷积层
        self.conv_1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU()
        )
        self.conv_dw2 = self.conv_dw(32, 32, 1)
        self.conv_dw3 = self.conv_dw(32, 64, 2)

        self.conv_dw4 = self.conv_dw(64, 64, 1)
        self.conv_dw5 = self.conv_dw(64, 128, 2)

        self.conv_dw6 = self.conv_dw(128, 128, 1)
        self.conv_dw7 = self.conv_dw(128, 256, 2)

        self.conv_dw8 = self.conv_dw(256, 256, 1)
        self.conv_dw9 = self.conv_dw(256, 512, 2)

        self.fc = nn.Linear(in_features=512, out_features=10)

        

    
    def forward(self, x):
        out = self.conv_1(x)
        out = self.conv_dw2(out)
        out = self.conv_dw3(out)
        out = self.conv_dw4(out)
        out = self.conv_dw5(out)
        out = self.conv_dw6(out)
        out = self.conv_dw7(out)
        out = self.conv_dw8(out)
        out = self.conv_dw9(out)

        out = F.avg_pool2d(out, 2)
        out = out.view(-1, 512)
        out = self.fc(out)
        return out


def MobileNetV1_small():
    return MobileNetV1()