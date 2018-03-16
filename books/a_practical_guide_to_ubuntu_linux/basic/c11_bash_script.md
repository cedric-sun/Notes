控制结构
================
条件
-----------

### if
```
if test-command
	then
		commands
fi
```

### if ... else ...
```
if test-command
	then
		commands
	else
		commands
fi
```

```
if test-command ; then
		commands
	else
		commands
fi
```

### if ... else if ... else
```
if test-command
	then
		commands
	elif test-command
		then
			commands
...
	else
		commands
fi
```

利用shell builtin `true` & `false`生成返回值
------------
```
cedric@TR:~/Desktop$ true
cedric@TR:~/Desktop$ echo $?
0
cedric@TR:~/Desktop$ false
cedric@TR:~/Desktop$ echo $?
1
```

loop
----------------
### for
#### for ... in
```
for loop-index in list
do
	commands
done
```

e.g.
```
#!/bin/bash

for fruit in apple banana orange
do
	echo $fruit
done
exit 0
```

Note: 用`$(seq first last)`或`{first..last}`来生成list

当省略list时，默认为"$@"
e.g.
```
#!/bin/bash

for fruit
do
	echo $fruit
done
exit 0
```

```
cedric@TR:~/Desktop$ ./print-fruits.sh apple watermelon citrus
apple
watermelon
citrus
```

#### C-like for
```
for (( expr1 ; expr2 ; expr3 ))
do
	commands
done
```

### whlie
```
while test-command
do
	commands
done
```

e.g.
```
#!/bin/bash

declare -i i=0
while [ "$i" -lt 100 ]
do
	echo "yes"
	let i+=1
done
exit 0
```

```
cedric@TR:~/Desktop$ ./while-test.sh | wc
    100     100     400
```

### until
相当于while的反面
```
until test-command
do
	commands
done
```

### break & continue

case
---------------
```
case test-string in
	pattern-1)
		commands-1
		;;
	pattern-2)
		commands-2
		;;
	...
esac
```

;;相当于break，不会继续执行

### pattern中可用的匹配
`*`	匹配任意串
`?`	匹配任意单字符
`[...]`
`|`	or


select
----------------
从KSH继承来的特性
```
select var [in args...]
do
	commands
done
```

忽略args时默认"$@"

do和done之间的逻辑不会主动停止，需要用条件语句判断当前var的取值并触发break或exit事件

Here Document
------------
```
cedric@TR:~$ cat <<+
> great
> +
great
cedric@TR:~$ cat <<+
> $(ls)
> +
141310223.txt
Desktop
Documents
Downloads
examples.desktop
Music
Pictures
Public
ss-config
Templates
tmuxconf.backup
Videos
```

相当于把stdin重定向到了某个管道，而这个管道的stdin的内容直接由命令行输入
<<后的那个字符用来界定here document
可以看到，当在here document使用命令替换的时候，和bash进程替换的特性是一样的。

sh也支持here document

参数 & 变量
=============
特殊参数
------------
$#		参数数量（不包括$0）
$0		调用名
$n		参数n
$?		最近一条在foreground运行的pipeline的返回值
$$		当前shell的pid
$!		最近放入后台的job的pid（如果是管道的话是最后那个命令的pid？）
$* and $@	都代表参数集合，但是$@被双引号引用的时候（"$@"）仍然会展开成多个tokens
对于如下脚本：

```
#!/bin/bash

set -x

echo $*
echo $@
echo "$*"
echo "$@"
```

在命令行上调用时
```
cedric@TR:~/Desktop$ ./gao.sh 1 2 3 4
+ echo 1 2 3 4
1 2 3 4
+ echo 1 2 3 4
1 2 3 4
+ echo '1 2 3 4'
1 2 3 4
+ echo 1 2 3 4
1 2 3 4
```

shift [n]
----------------
左移参数n次：$2变成$1，$3变成$2，...
省略n默认为1
没有unshift命令，已经shift掉的参数无法找回
$#也会相应减少

set
----------------
设置位置参数
```
cedric@TR:~$ set a b c
cedric@TR:~$ echo $1 $2 $3
a b c
```

set可以和命令替换联用，来格式化一个命令的输出
```
#!/bin/bash

set $(date)
echo "$2, $3, $6"	# Mar, 15, 2018
```

数组
------------
name=(ele0 ele1 ele2 ...)

```
cedric@TR:~$ great=(make america great again)
cedric@TR:~$ declare -p great
declare -a great='([0]="make" [1]="america" [2]="great" [3]="again")'
```

下标索引访问 & 赋值：
```
cedric@TR:~$ echo ${great[1]}
america
edric@TR:~$ great[1]=china
cedric@TR:~$ echo ${great[@]}
make china great again
```

'*'和'@'作为下标可以表示所有元素的集合，两者的区别同"$*"和"$@"
```
cedric@TR:~$ print-args "${great[*]}"
Total arguments: 2
0: print-args
1: make america great again
cedric@TR:~$ print-args "${great[@]}"
Total arguments: 5
0: print-args
1: make
2: america
3: great
4: again
```

数组长度：
```
cedric@TR:~$ echo ${#great[*]}
4
```

注意${great}引用的是great的0号元素，${#great}也是0号元素的字符串长度

`${#var}`对于普通变量而言是求字符串长度：
```
cedric@TR:~$ a=fuck
cedric@TR:~$ echo ${#a}
4
```

函数变量作用域
---------
在函数中用`declare var[=value]`来声明一个函数局部变量

变量默认值
-----------
当变量值为空串或null时，有三种方式处理：
1. `${var:-fallback}`: 使用fallback作为该表达式的值
2. `${var:=fallback}`: 使用fallback作为该表达式的值，并将var赋值为fallback
3. `${var:?message}`: 终止pipeline的执行，提示错误信息message，并返回1

```
cedric@TR:~$ echo ${fuck:-lll}
lll
cedric@TR:~$ echo $fuck

cedric@TR:~$ echo ${fuck:=lll}
lll
cedric@TR:~$ echo $fuck
lll
cedric@TR:~$ echo ${var:?"error message"}
bash: var: error message
```

如果希望在一个变量为空时为其设置默认值
```
${var:=fallback}
```
会导致var被赋值之后，fallback被当做一个命令执行，此时可以
```
: ${var:=fallback}
```

内置命令
==============
read
--------
read [var]			# 如果未指定变量，则保存在`$REPLY`中
### options
-p "prompt: "		# 带提示信息
-a array		# 以数组形式读入array
-n num			# 读入num个字母后立即返回
-s			# 无回显
-uFD			# 从FD读入，而不是stdin。单独使用read时相当于`read <&FD`，但是在循环结构中，后者每次重定向都会将current指针置于文件头。
-d delim		# 使用delim来代替换行符终止输入（delim按下后立即停止read）

### policy
如果输入的token (word)数量大于参数变量数量，多余的token会全部赋给最后一个变量:
```
cedric@TR:~$ read a b
This is a long long long sentence.    
cedric@TR:~$ echo $a
This
cedric@TR:~$ echo $b
is a long long long sentence.
```

### return value
读到EOF时返回1
否则返回0

### 从文件循环读入的注意事项
每次进行重定向时，FD的current指针都会被置于文件头，如果这么写循环读入的重定向：
```
while read line < file.txt
do
	echo $line
	sleep 1
done
```
则read每次总能从文件头开始读到line，永远不会读到EOF（除非文件本身为空），陷入死循环

#### Solution 1 可以为整个循环结构设置重定向
```
while read line
do
	echo $line
	sleep 1
done < file.txt
```

#### Solution 2 显式启动子shell，对子shell整体进行重定向
```
(
while read line
do
	echo $line
	sleep 1
done
) < file.txt
```

#### Solution 3 使用-u参数从事先打开的FD读入
```
cedric@TR:~$ exec 100<file.txt 
cedric@TR:~$ while read -u100 line
> do
> echo $line
> sleep 1
> done
Viva La Gloria!
Welcome to paradise
Boulevard of Broken Dream
American Idiot

```

exec
--------------
`/dev/tty`总是代表当前正在使用的工作屏幕

trap
--------------
trap			打印当前trap配置
trap -p [SIG]		打印SIG的trap配置，省略SIG时打印所有信号，即同上
trap -l			打印可用的信号，同`kill -l`
trap SIG...		重置SIG配置
trap 'command' SIG...	设置SIG的trap：收到SIG时执行command
	如果用单引号引用command，则command中的shell变量会在收到信号时展开

trap常用来在脚本被信号中断时清除临时文件

kill
--------------

getopts
---------------

wait
----------

times
----------

Expression
==================
```
cedric@TR:~$ a=10 b=12			# 一行内多变量赋值
cedric@TR:~$ let "a = a + 2" b=b-3	# let后表达式可连写，有空格的表达式要引号
cedric@TR:~$ echo $a $b
12 9
cedric@TR:~$ ((a = b - 22 , b += 55))	# 逗号分隔(())内的表达式
cedric@TR:~$ echo $a $b
-13 64
```

关于test [], let (()), 以及 [[]]
-----------
### 首先let是可以用来做逻辑判断的
```
cedric@TR:~$ if let '1 < 9 && 10 > 2'
> then
>       echo "pass"
> fi
pass
```
这是因为let后的表达式将按照man bash中的ARITHMETIC EVALUATION一节的规则进行运算，也就是单纯的算数求值。此时"<" ">" "&&"都是bash合法的算术运算符。根据let的规则，当let后的最后一个表达式求值为0时返回false，否则返回true。所以let是能够进行基于算数的逻辑判断的。但是遇到非算数的判断，比如字符串的字典序大小，文件是否存在，是否可执行等，let就无法处理了。

### 其次关于test和[[]]
`[]`同义与test，读作test，是POSIX标准
`[[]]`读作new test，仅在Bash, Zsh和Ksh中受到支持，功能更为强大。

尽量用new test代替test

### 作为独立程序的test & 保持后向兼容的builtin
在上古时代test是个独立的程序，该程序评估作为命令行参数传进来的表达式，返回true (0) 或false (1)，以便配合shell中的控制结构使用（事实上现在也是/usr/bin/test，只不过在bash里会先调用内建的test，但是也要保持后向兼容性，模仿独立test程序的行为），所以必须确保test程序能如实收到参数，因此必须对很多shell保留字符进行转义，调用起来也十分的不方便

e.g. 希望比较字符串"a"和"b"的字典序
```shell
cedric@TR:~/Desktop/sandbox$ ls
comptest.sh
cedric@TR:~/Desktop/sandbox$ cat comptest.sh 
#!/bin/bash

if [ a \> b ]
then
	echo "String comparison: a > b"		# you should never see this
else
	echo "String comparison: a <= b"
fi
cedric@TR:~/Desktop/sandbox$ ./comptest.sh 
String comparison: a <= b
cedric@TR:~/Desktop/sandbox$ ls
comptest.sh
```

如果一不小心忘了转义，不但比较会出错，而且会被理解为重定向，在当前目录生成b
```
cedric@TR:~/Desktop/sandbox$ ls
comptest.sh
cedric@TR:~/Desktop/sandbox$ cat comptest.sh 
#!/bin/bash

if [ a > b ]
then
	echo "String comparison: a > b"		# you should never see this
else
	echo "String comparison: a <= b"
fi
cedric@TR:~/Desktop/sandbox$ ./comptest.sh 
String comparison: a > b
cedric@TR:~/Desktop/sandbox$ ls
b  comptest.sh
```

说到底，带来如此多的麻烦问题的根源是，test是一个独立程序，就算现代shell将其作为builtin来实现，它的行为也应该像一个独立程序，i.e. 无论如何shell的展开要先进行，因此无法根据上下文来对操作符进行独立处理，一个很好的例子就是命令行上的"<"和">"在[[ ]]中会被当做比较字符串字典序的操作符，而在[ ]中却无法将其和输入输出重定向区分开来

而[[ ]]是shell的关键字

#### 使用-le等操作符比较数值
注意不管在[]还是在[[]]中，大于号(<)和小于号(>)都是用来比较字符串的字典序的，如果用于比较数字则会出错：
```
cedric@TR:~/Desktop/sandbox$ cat comptest2.sh 
#!/bin/bash

if [ 30 \< 4 ]
then
	echo "30 < 4"		# you should never see this
else
	echo "30 >= 4"
fi
cedric@TR:~/Desktop/sandbox$ ./comptest2.sh 
30 < 4
```

控制语句块的重定向
===========
可以为控制语句块单独进行重定向
e.g.
```
cedric@TR:~$ echo $$
17009
cedric@TR:~$ for i in 1 2 3
> do
> lsof -p $$ -d 0,1,2 -a
> echo $$
> echo
> done <141310223.txt 
COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
bash    17009 cedric    0r   REG   8,21       17 318702 /home/cedric/141310223.txt
bash    17009 cedric    1u   CHR  136,2      0t0      5 /dev/pts/2
bash    17009 cedric    2u   CHR  136,2      0t0      5 /dev/pts/2
17009

COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
bash    17009 cedric    0r   REG   8,21       17 318702 /home/cedric/141310223.txt
bash    17009 cedric    1u   CHR  136,2      0t0      5 /dev/pts/2
bash    17009 cedric    2u   CHR  136,2      0t0      5 /dev/pts/2
17009

COMMAND   PID   USER   FD   TYPE DEVICE SIZE/OFF   NODE NAME
bash    17009 cedric    0r   REG   8,21       17 318702 /home/cedric/141310223.txt
bash    17009 cedric    1u   CHR  136,2      0t0      5 /dev/pts/2
bash    17009 cedric    2u   CHR  136,2      0t0      5 /dev/pts/2
17009

```

控制结构并没有运行在子shell里。对于控制结构的重定向会使当前shell的FDs临时进行重定向，在控制结构退出后恢复。
