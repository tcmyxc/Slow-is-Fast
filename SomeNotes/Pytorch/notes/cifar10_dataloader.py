from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image
import numpy as np
import glob


# 标签名
label_name = ["airplane", "automobile", "bird", "cat", "deer",
                "dog", "frog", "horse", "ship", "truck"]


label_dict = {}

# 将标签转换为数字
for idx, name in enumerate(label_name):
    label_dict[name] = idx


def default_loader(path):
    """根据图片路径打开图片

    :param path: 图片路径
    """
    return Image.open(path).convert("RGB")

# 定义数据增强(仅训练集需要)
train_transfrom = transforms.Compose([
    transforms.RandomResizedCrop([28, 28]),
    transforms.RandomHorizontalFlip(),
    transforms.RandomVerticalFlip(),
    transforms.RandomRotation(90),
    transforms.RandomGrayscale(0.1), # 0.1 的概率变成灰度图
    transforms.ToTensor()
])


class MyDataset(Dataset):
    """自定义数据集"""

    def __init__(self, im_list, transform=None, loader=default_loader):
        super().__init__()
        imgs = []

        for im_item in im_list:
            # 倒数第二个是标签名
            # win 的分割符是 \\，linux 是 /
            im_label_name = im_item.split("\\")[-2] 
            # 列表中追加图片路径，图片类别
            imgs.append([im_item, label_dict[im_label_name]]) 
        
        self.imgs = imgs
        self.transform = transform
        self.loader = loader

    def __getitem__(self, index):
        im_path, im_label = self.imgs[index]
        im_data = self.loader(im_path)

        # 判断是否有数据增强
        if self.transform is not None:
            im_data = self.transform(im_data)

        return im_data, im_label
    
    def __len__(self):
        return len(self.imgs)


im_train_list = glob.glob("dataset/cifar-10/train/*/*.png")

im_test_list = glob.glob("dataset/cifar-10/test/*/*.png")

train_dataset = MyDataset(im_train_list, transform=train_transfrom)

test_dataset = MyDataset(im_test_list, transform=transforms.ToTensor())

# 定义 dataloader
train_data_loader = DataLoader(dataset=train_dataset,
                                batch_size=128,
                                shuffle=True)

test_data_loader = DataLoader(dataset=test_dataset,
                                batch_size=128,
                                shuffle=False)

print("num of train", len(train_dataset))
print("num of test", len(test_dataset))


