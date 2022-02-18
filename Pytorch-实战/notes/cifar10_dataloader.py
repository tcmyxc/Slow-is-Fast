from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image
import numpy as np
import cv2
import glob
from matplotlib import pyplot as plt
#
# # Cifar10 官网辅助函数
# def unpickle(file):
#     import pickle
#     with open(file, 'rb') as fo:
#         dict = pickle.load(fo, encoding='bytes')
#     return dict

# 标签名
label_name = ["airplane", "automobile", "bird", "cat", "deer",
                "dog", "frog", "horse", "ship", "truck"]

# train_list = glob.glob("dataset/cifar-10/data_batch_*")
# test_list = glob.glob("dataset/cifar-10/test_batch")
#
# sava_path = "dataset/cifar-10/train"
# for l in train_list:
#     l_dict = unpickle(l)
#     # print(l_dict)
#     print(l_dict.keys())
#
#     for im_idx, im_data in enumerate(l_dict[b'data']):
#         # print(im_idx)
#         # print(im_data) # 图片数据是个向量，需要 reshape
#
#         im_label = l_dict[b'labels'][im_idx]  # 图片标签
#         im_name = l_dict[b'filenames'][im_idx]  # 图片数据
#
#         # print(im_idx, im_label, im_name, im_data)
#         im_label_name = label_name[im_label]  # 标签的名字
#         im_data = np.reshape(im_data, [3, 32, 32])  # 这个数据集通道在最前面
#         # 把通道放到后面
#         im_data = np.transpose(im_data, [1, 2, 0])
#         # 通过 opencv 可视化
#         # cv2.imshow("im_data", im_data)
#         # cv2.waitKey(0)
#
#         # 判断是否有相应的文件夹，没有则创建
#         if not os.path.exists(f"{sava_path}/{im_label_name}"):
#             os.mkdir(f"{sava_path}/{im_label_name}")
#
#         # 写入图片
#         cv2.imwrite(f"{sava_path}/{im_label_name}/{im_name.decode('utf-8')}",
#                     im_data)
#
# sava_path = "dataset/cifar-10/test"
# for l in test_list:
#     l_dict = unpickle(l)
#     # print(l_dict)
#     print(l_dict.keys())
#
#     for im_idx, im_data in enumerate(l_dict[b'data']):
#         # print(im_idx)
#         # print(im_data) # 图片数据是个向量，需要 reshape
#
#         im_label = l_dict[b'labels'][im_idx]  # 图片标签
#         im_name = l_dict[b'filenames'][im_idx]  # 图片数据
#
#         # print(im_idx, im_label, im_name, im_data)
#         im_label_name = label_name[im_label]  # 标签的名字
#         im_data = np.reshape(im_data, [3, 32, 32])  # 这个数据集通道在最前面
#         # 把通道放到后面
#         im_data = np.transpose(im_data, [1, 2, 0])
#         # 通过 opencv 可视化
#         cv2.imshow("im_data", im_data)
#         cv2.waitKey(0)
#
#         # 判断是否有相应的文件夹，没有则创建
#         if not os.path.exists(f"{sava_path}/{im_label_name}"):
#             os.mkdir(f"{sava_path}/{im_label_name}")
#
#         # 写入图片
#         cv2.imwrite(f"{sava_path}/{im_label_name}/{im_name.decode('utf-8')}",
#                     im_data)

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
                                shuffle=False)

test_data_loader = DataLoader(dataset=test_dataset,
                                batch_size=128,
                                shuffle=False)

print("num of train", len(train_dataset))
print("num of test", len(test_dataset))


