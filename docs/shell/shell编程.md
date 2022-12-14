# shell编程

shell 是操作系统的最外层。shell 合并编程语言以控制进程和文件，以及启动和控制其它程序。shell 通过提示用户输入，向操作系统解释该输入，然后处理来自操作系统的任何结果输出来管理用户与操作系统之间的交互。

查看操作系统提供的 shell 环境

```bash
cat /etc/shells
```

输出：

```
/bin/bash
/bin/csh
/bin/dash
/bin/ksh
/bin/sh
/bin/tcsh
/bin/zsh
```



通过环境变量查看默认 shell 环境

```bash
echo $SHELL
```

## 1、简单的 hello word

```bash
#!/bin/bash

echo "hello, world"  # 单引号、双引号无所谓
```

第一行，固定套路（起手式），定义脚本使用的解析器



执行脚本的几种方式：

1、使用 `bash [脚本路径]` 执行（不需要赋予脚本可执行权限）

2、先赋予脚本可执行权限（`chmod +x [脚本路径]`），然后运行

3、把第一种方式的 `bash` 换成 `.` 或者 `source` （有的 shell 不支持 `.` 的形式，如 `zsh`）

```bash
$ cat test.sh 
#!/bin/bash 
A=5 
```

```bash
$ sh test.sh 
$ echo $A

$ ./test.sh 
$ echo $A

$ . test.sh 
$ echo $A 
5
```

原因： 

前两种方式都是在当前 shell 中打开一个子 shell 来执行脚本内容，当脚本内容结束，则 子 shell 关闭，回到父 shell 中。 

第三种，也就是使用在脚本路径前加“.”或者 source 的方式，可以使脚本内容在当前 shell 里执行，而无需打开子 shell！这也是为什么我们每次要修改完/etc/profile 文件以后，需 要 source 一下的原因。 

开子 shell 与不开子 shell 的区别就在于，环境变量的继承关系，如在子 shell 中设置的 当前变量，父 shell 是不可见的。

## 2、变量

### 2.1 系统预定义变量

常用的系统变量：

```bash
$HOME
$PWD
$SHELL
$USER
```



直接 `echo` 就好，比如：`echo $USER`

或者使用 `printenv USER`



查看所有预定义变量：`env` 或者 `printenv`

显示当前 Shell 中所有变量：`set`

### 2.2 自定义变量

#### 基本语法

（1）定义变量：`变量=值`（等号前后不能有空格）

（2）撤销变量：`unset 变量名`

（3）声明静态变量：`readonly 变量=值` （不能 `unset`）

变量默认类型都是字符串，不能直接进行数值运算

> `export` 可以把局部变量提升为全局变量，让子 shell 使用
>
> 但是如果子 shell 对变量进行更改的话，不会影响父 shell 中的值

变量命名规则同其他语言

### 2.3 特殊变量

`$n` 

功能描述：n 为数字，`$0` 代表该脚本名称，`$1`-`$9` 代表第一到第九个参数，十以上的参数需要用大括号包含，如`${10}`）

`$#`

 功能描述：获取所有输入参数个数，常用于循环，判断参数的个数是否正确以及 加强脚本的健壮性

`$*`

功能描述：这个变量代表命令行中所有的参数，`$*`把所有的参数看成一个整体

`$@` 

功能描述：这个变量也代表命令行中所有的参数，不过`$@`把每个参数区分对待

`$?` 

功能描述：最后一次执行的命令的返回状态。如果这个变量的值为 0，证明上一 个命令正确执行；如果这个变量的值为非 0（具体是哪个数，由命令自己来决定），则证明上一个命令执行不正确

## 3、运算符

### 基本知识

基本语法：

```bash
$((运算式))
# 或者
$[运算式]  # 推荐
```

运算式中可以有空格

用法：

```bash
$ a=$[1 + 2]
$ echo $a
3
```



也可以使用 `expr`

```bash
$ expr 1 + 2  # 运算符前后必须有空格，相当于传了三个参数给 expr
3

$ expr 1 \* 2  # 乘法
2
```



还可以使用命令替换的方式（用小括号或者反引号），但是不推荐

```bash
$ a=$(expr 2 \* 5)
$ echo $a
10
$ a=`expr 2 \* 5`
x$ echo $a
10
```

### 案例

加法功能

```bash
#!/bin/bash

sum=$[$1 + $2]  # $1 代表第一个变量，$2 代表第二个变量
echo sum=$sum
```

使用：

```bash
$ chmod +x add.sh
$ ./add.sh 1 2
sum=3
```

## 4、条件判断

基本语法：

（1）`test 条件`

（2）`[ 条件 ]` （条件语句前后要有空格，条件非空即为 true）

用法：

```bash
$ a=hello
$ echo $a
hello
$ test $a = hello
$ echo $?  # 条件语句返回值通过特殊变量获得
0  # 测试通过则为0

$ test $a = Hello
$ echo $?
1

[ $a = hello ]  # 等号前后必须有空格，否则会被解析成字符串
$ echo $?
0

$ [ $a = Hello ]
$ echo $?
1

$ [ $a != Hello ]
$ echo $?
0
```



常用判断条件：

（1）两个整数之间比较 

`-eq` 等于（equal） 

`-ne` 不等于（not equal） 

`-lt` 小于（less than） 

`-le` 小于等于（less equal）

 `-gt` 大于（greater than） 

`-ge` 大于等于（greater equal） 

注：如果是字符串之间的比较 ，用等号“=”判断相等；用“!=”判断不等。 

（2）按照文件权限进行判断 

`-r` 有读的权限（read） 

`-w` 有写的权限（write） 

`-x` 有执行的权限（execute） 

（3）按照文件类型进行判断 

`-e` 文件存在（existence） 

`-f` 文件存在并且是一个常规的文件（file） 

`-d` 文件存在并且是一个目录（directory）



多条件判断（`&&` 表示前一条命令执行成功时，才执行后一条命令，`||` 表示上一条命令执行失败后，才执行下一条命令，类似三元运算符）

```bash
$ [ hello ] && echo OK || echo Fail
OK
$ [ ] && echo OK || echo Fail
Fail
```

## 5、流程控制

### if 判断

#### 基本语法

（1）单分支 

```bash
if [ 条件判断式 ];then 
	程序 
fi
```

或者

```bash
if [ 条件判断式 ] 
then
	程序 
fi
```

（2）多分支

```bash
if [ 条件判断式 ] 
then
	程序 
elif [ 条件判断式 ] 
then
	程序 
else
	程序 
fi 
```



注意事项： 

- `[ 条件判断式 ]`，中括号和条件判断式之间必须有空格 
- `if` 后要有空格

#### 案例

```bash
if [ $a -lt 18] && [ $b -gt 50]; then echo OK; fi
# 上面的简写
if [ $a -lt 18 -a $b -gt 50]; then echo OK; fi  # -a 代表 &&, -o 代表 |
```

### case 语句

#### 语法

```bash
case $变量名 in 
"值 1")
	如果变量的值等于值 1，则执行程序 1 
;;
"值 2") 如果变量的值等于值 2，则执行程序 2 
;; 
	…省略其他分支… 
*)  # 缺省条件 
如果变量的值都不是以上的值，则执行此程序 
;;
esac
```



注意事项：

（1）case 行尾必须为单词“in”，每一个模式匹配必须以右括号“)”结束。 

（2）双分号“**;;**”表示命令序列结束，相当于 java 中的 break。 

（3）最后的“*)”表示默认模式，相当于 java 中的 default。

### for循环

#### 语法

```bash
for (( 初始值;循环控制条件;变量变化 ))
do 
	程序 
done

# 或者
for 变量 in 值 1 值 2 值 3… 
do 
	程序 
done
```

示例：

```bash
#!/bin/bash 

sum=0 
for((i=0;i<=100;i++)) 
do 
	sum=$[$sum+$i] 
done 

echo $sum
```

```bash
#!/bin/bash 

for i in cls mly wls
do 
	echo "I love $i" 
done
```

> 注意 `do` 一定要占一行





`$*` 和 `$@` 都表示传递给函数或脚本的所有参数，不被双引号 `""` 包含时，都以 `$1` `$2` …`$n` 的形式输出所有参数。

```bash
$ touch for3.sh 
$ vim for3.sh 

#!/bin/bash 
echo '=============$*=============' 
for i in $* 
do 
echo "I love $i" 
done 

echo '=============$@=============' 
for j in $@ 
do 
echo "I love $j" 
done 

$ chmod 777 for3.sh 
```

```tex
$./for3.sh  java c c++
=============$*=============
I love java
I love c
I love c++
=============$@=============
I love java
I love c
I love c++
```

当它们被双引号`“”`包含时，`$*`会将所有的参数作为一个整体，以“`$1` `$2` …`$n`”的形式输 出所有参数；`$@`会将各个参数分开，以“`$1`” “`$2`”…“`$n`”的形式输出所有参数。

```bash
#!/bin/bash 

echo '=============$*=============' 
for i in "$*"
do 
    echo "I love $i" 
done 

echo '=============$@=============' 
for j in "$@"
do 
    echo "I love $j" 
done 
```

```bash
$./for3.sh  java c c++
=============$*=============
I love java c c++
=============$@=============
I love java
I love c
I love c++
```

### while循环

```bash
while [ 条件判断式 ] 
do 
	程序 
done
```

## 6、从控制台读取输入

### 语法

read (选项) (参数) 

①选项：

`-p`：指定读取值时的提示符； 

`-t`：指定读取值时等待的时间（秒）如果`-t` 不加表示一直等待 

②参数

变量：指定读取值的变量名 

```bash
#!/bin/bash 

read -p "输入你的名字: " -t 10 name
echo "hello, $name"
```

## 7、系统函数

### basename

基本语法：

`basename [string / pathname] [suffix] `

功能描述：basename 命令会删掉所有的前缀包括最后一个（‘/’）字符，然后将字符串显示出来。 可以理解为取路径里的文件名称 

选项： 

`suffix` 为后缀，如果 `suffix` 被指定了，`basename` 会将 `pathname` 或 `string` 中的 `suffix` 去掉

### dirname

语法：

`dirname 文件绝对路径`

可以理解为取文件路径的绝对路径名称

### 自定义函数

语法：

```bash
[ function ] funname[()] 
{ 
	Action; 
	[return int;] 
}
```

技巧：

（1）必须在调用函数地方之前，先声明函数，shell 脚本是逐行运行。不会像其它语言一样先编译。 

（2）函数返回值，只能通过$?系统变量获得，可以显示加 `return` 返回，如果不加，将以最后一条命令运行结果，作为返回值。return 后跟数值 n(0-255)

```bash
#!/bin/bash 
function sum() 
{ 
	s=0 
	s=$[$1+$2] 
	echo "$s" 
}
```

## 8、正则基础

`^`：小尖尖匹配开头

`$`：美元匹配结尾

`.`：点只匹配一个

`*`：星号匹配任意个上一个字符，不能单独用











