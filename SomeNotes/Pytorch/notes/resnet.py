#!/usr/bin/python3

import torch
import torch.nn as nn
import torch.nn.functional as F

class ResBlock(nn.Module):
    def __init__(self, in_channel, out_channel, stride=1):
        super().__init__()
        # 主路径
        self.layer = nn.Sequential(
            nn.Conv2d(in_channels=in_channel, out_channels=out_channel, 
                        kernel_size=3, stride=stride, padding=1),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(),
            nn.Conv2d(in_channels=out_channel, out_channels=out_channel, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(out_channel),
            nn.ReLU()
        )

        # 跳连，如果输入输出匹配，那就直连，不匹配就改改
        self.shortcut = nn.Sequential()
        if in_channel != out_channel or stride > 1:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels=in_channel, out_channels=out_channel, 
                            kernel_size=3, stride=stride, padding=1),
                nn.BatchNorm2d(out_channel),
            )
    
    def forward(self, x):
        out1 = self.layer(x)
        out2 = self.shortcut(x)
        out = out1 + out2
        out = F.relu(out)
        return out

class ResNetBase(nn.Module):
    def make_layer(self, block, out_channel, stride, num_block):
        layers_list = []
        for i in range(num_block):
            if i == 0:
                in_stride = stride
            else:
                in_stride = 1
            layers_list.append(
                block(self.in_channel, out_channel, in_stride)
            )
            self.in_channel = out_channel
        
        return nn.Sequential(*layers_list)

    def __init__(self):
        super().__init__()

        self.in_channel = 32

        self.conv1 = nn.Sequential(
            nn.Conv2d(in_channels=3, out_channels=32, 
                        kernel_size=3, stride=1, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU()
        )

        self.layer1 = self.make_layer(ResBlock, 64, 2, 2)
        self.layer2 = self.make_layer(ResBlock, 128, 2, 2)
        self.layer3 = self.make_layer(ResBlock, 256, 2, 2)
        self.layer4 = self.make_layer(ResBlock, 512, 2, 2)
        
        self.fc = nn.Linear(512, 10)

    
    def forward(self, x):
        out = self.conv1(x)
        out = self.layer1(out)
        out = self.layer2(out)
        out = self.layer3(out)
        out = self.layer4(out)
        out = F.avg_pool2d(out, 2)
        # view()的作用相当于numpy中的reshape，重新定义矩阵的形状。
        out = out.view(out.size(0), -1)
        out = self.fc(out)

        return out

def ResNet():
    return ResNetBase()