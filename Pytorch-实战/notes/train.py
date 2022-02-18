#!/usr/bin/python3

import torch
import torch.nn as nn
import torchvision
from vggnet import VGGNet
from resnet import ResNet
from mobilenetv1 import MobileNetV1_small
from pre_resnet import pytorch_resnet34
from cifar10_dataloader import train_data_loader, test_data_loader
import os
import tensorboardX

# 能用 GPU 就用
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(device)
print(torch.__version__)
epoch_num = 200
lr = 1e-3
batch_size = 128

net = pytorch_resnet34().to(device)

# loss
loss_func = nn.CrossEntropyLoss()

# 优化器
optimizer = torch.optim.SGD(params=net.parameters(), lr=lr,
                            momentum=0.9, weight_decay=5e-4)

# 动态调整学习率
scheduler = torch.optim.lr_scheduler.StepLR(optimizer, 
                                    step_size=5,# 5个 epoch 调整一次学习率
                                    gamma=0.9)
model_path = "models/pytorch_resnet18"
log_path = "log"
if not os.path.exists(log_path):
        os.mkdir(log_path)
if not os.path.exists(model_path):
    os.mkdir(model_path)

writer = tensorboardX.SummaryWriter("log")

step_n = 0
for epoch in range(epoch_num):
    net.train()

    for i, data in enumerate(train_data_loader):
        # 取数据
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)

        # 训练网络
        outputs = net(inputs)
        loss = loss_func(outputs, labels)

        # 参数初始化
        optimizer.zero_grad()
        # 反向传播
        loss.backward()
        # 更新参数
        optimizer.step()

        # 记录预测对的
        _, pred = torch.max(outputs.data, dim=1)
        correct = pred.eq(labels.data).cpu().sum()

        # 图片可视化
        im = torchvision.utils.make_grid(inputs)
        writer.add_image("train_img", im, global_step=step_n)

        print(f"epoch is {epoch+1}")
        print("train lr is ", optimizer.state_dict()["param_groups"][0]["lr"])
        print(f"train step is {i}, ", f"loss is {loss.item()}, ",
                f"mini-batch correct is {100.0 * correct / batch_size}%")

        # loss，corr 记录到 tensorboard
        writer.add_scalar("train_loss", loss.item(), global_step=step_n)
        writer.add_scalar("train_correct", 
                            100.0 * correct.item() / batch_size,
                            global_step=step_n)
        step_n += 1
    
    # 保存模型

    torch.save(net.state_dict(), f"{model_path}/{epoch+1}.pth")

    # 更新学习率
    scheduler.step()

    # 测试
    sum_loss = 0
    sum_correct = 0
    for i, data in enumerate(test_data_loader):
        net.eval()
        # 取数据
        inputs, labels = data
        inputs, labels = inputs.to(device), labels.to(device)

        # 使用网络
        outputs = net(inputs)
        loss = loss_func(outputs, labels)
        sum_loss += loss.item()

        # 记录预测对的
        _, pred = torch.max(outputs.data, dim=1)
        correct = pred.eq(labels.data).cpu().sum()
        sum_correct += correct.item()

        # 图片可视化
        im = torchvision.utils.make_grid(inputs)
        writer.add_image("test_img", im, global_step=step_n)

        writer.add_scalar("test_loss", loss.item(), global_step=step_n)
        writer.add_scalar("test_correct", 
                            100.0 * correct.item() / batch_size,
                            global_step=step_n)

    test_loss = sum_loss / len(test_data_loader)
    test_correct = sum_correct / len(test_data_loader) / batch_size

    print("epoch is ", epoch+1, ", test loss is ", test_loss, 
            ", mini-batch correct is ", 100.0 * test_correct, "%")

writer.close()