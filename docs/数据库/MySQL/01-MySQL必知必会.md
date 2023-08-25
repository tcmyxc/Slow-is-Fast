# MySQL必知必会

# 第一章：了解SQL

主键的好习惯：

- 不更新、不重用主键列的值
- 不使用可能会更改的值作为主键

# 第二章：MySQL简介

```mysql
mysql -u root -p
```

回车之后会提示输入密码，输入即可

注意：

- 命令用分号 `;` 或者 `\g` 结束

# 第三章：使用

## 选择数据库

```mysql
USE 数据库名; # 选择数据库
```

## 查看各种信息

```mysql
show databases; # 查看可用的数据库
show tables; # 查看某个数据库中可用的表

show columns from 表名; # 显示表的列信息

# 查看建库、建表语句
show create database 数据库名;
show create table 表名;
```

# 第四章：检索数据

> 想选择什么，从哪里选择

## 建议

- 关键词大写
- 也不一定大写，保持一致性就好

## 限制结果

返回第一行或者前几行，可使用 `limit` 子句

```mysql
select prod_name
from products
limit 5;
```



可以指定开始行和总共要多少行

```mysql
select prod_name
from products
limit 3, 5;# 从行3开始（索引以0开始），查5行
```

等价于

```mysql
select prod_name
from products
limit 3 offset 5;
```

## 完全限定名

表名和列名有完全限定名，在多表查询的时候有用