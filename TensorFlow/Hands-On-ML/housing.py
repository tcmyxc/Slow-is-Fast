#!/usr/bin/python3
# coding=utf-8
# @Author : 徐文祥

import os
import tarfile
import urllib.request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DOWNLOAD_ROOT = "https://raw.githubusercontent.com/ageron/handson-ml2/master/"
HOUSING_PATH = os.path.join("datasets", "housing")
HOUSING_URL = DOWNLOAD_ROOT + "datasets/housing/housing.tgz"

# 取数据的函数
def fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH):
    os.makedirs(housing_path, exist_ok=True)
    tgz_path = os.path.join(housing_path, "housing.tgz")
    urllib.request.urlretrieve(housing_url, tgz_path)
    housing_tgz = tarfile.open(tgz_path)
    housing_tgz.extractall(path=housing_path)
    housing_tgz.close()

def load_housing_data(housing_path=HOUSING_PATH):
    csv_path = os.path.join(housing_path, "housing.csv")
    return pd.read_csv(csv_path)

def split_train_test(data, test_ratio=0.2):
    """
    根据给定比例划分训练集、测试集
    :param data: 数据集
    :param test_ratio: 测试集比例
    :return: 训练集、测试集
    """
    np.random.seed(42)
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    return data.iloc[train_indices], data.iloc[test_indices]

if __name__ == '__main__':
    # fetch_housing_data(housing_url=HOUSING_URL, housing_path=HOUSING_PATH)
    housing = load_housing_data()

    # print(housing.head())
    # print(housing.info())
    # print(housing.describe())

    # housing.hist(bins=50, figsize=(20, 15))
    # plt.show()

    train_set, test_set = split_train_test(housing, 0.2)
    print(len(train_set), len(test_set))

    print(train_set.head())

