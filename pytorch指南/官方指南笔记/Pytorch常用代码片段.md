# Pytorch注意事项
- 学习率调度器的更新应该在一个完整的 epoch 之后

# Pytorch常用代码片段

## 数据集和数据加载相关

### 包相关


```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader,Dataset

import torchvision
import torchvision.transforms as transforms
from torchvision import datasets
```

### 数据加载迭代器


```python
train_dataloader = DataLoader(custom_dataset, batch_size=64, shuffle=True)  # DataLoader 是可迭代的

# 定义一个迭代器
train_iterator = iter(train_dataloader)
# 取一批样本
train_features, train_labels = next( train_iterator)
```

## 使用CUDA


```python
# Get cpu or gpu device for training.
device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using {device} device")
```

## 训练和测试通用代码

### 分类任务


```python
# 通用训练代码
def train(dataloader, model, loss_fn, optimizer):
    size = len(dataloader.dataset)
    model.train()
    for batch, (X, y) in enumerate(dataloader):
        X, y = X.to(device), y.to(device)

        # Compute prediction error
        pred = model(X)
        loss = loss_fn(pred, y)

        # Backpropagation
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:
            loss, current = loss.item(), batch * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
```


```python
# 通用测试代码
def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")
```

## 保存模型

### 一般保存


```python
torch.save(model.state_dict(), "model.pth")
print("Saved PyTorch Model State to model.pth")
```


```python
# 加载模型参数
# 1、加载模型结构
# 2、加载模型参数
model = NeuralNetwork()
model.load_state_dict(torch.load("model.pth"))
```

### 保存其他信息


```python
torch.save(
    {
        'model_state_dict': net.state_dict(),  # 必须
        'optimizer_state_dict': optimizer.state_dict(),  # 必须
        'epoch': EPOCH,
        'loss': LOSS,
        # 其他的合理信息都可
    },
    PATH
)

# 之后如果想从这个状态继续训练，
#（1）定义和原来一样的模型变量和优化器变量
#（2）加载保存时间点的参数
model = Net()
optimizer = optim.SGD(net.parameters(), lr=0.001, momentum=0.9)

checkpoint = torch.load(PATH)
model.load_state_dict(checkpoint['model_state_dict'])
optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
epoch = checkpoint['epoch']
loss = checkpoint['loss']

model.eval()
# - or -
model.train()
```

# 模型结构和参数

### 打印模型结构

```python
print("Model structure: ", model)
```

### 打印模型参数


```python
for name, param in model.named_parameters():
    print(f"Layer: {name} | Size: {param.size()} | Values : {param[:2]} \n")
```
