INDEX
============
1. 归档 & 压缩
2. 打印控制
3. 终端相关
4. 进程管理
5. 字符流处理
6. Shell辅助工具
7. 多用户 & 用户管理
8. X
9. Disk Management
10. 环境
11. Booting

tail. Miscellaneous

归档 & 压缩
=================
ar
----------
ar只能提取到当前目录

### USE
ar x FILE	提取
ar t FILE	显示

zip, unzip
----------

gzip, gunzip, zcat
-----------
gunzip = gzip -d
zcat = gunzip -c = gzip -dc

bzip, bunzip, bzcat
-----------

xz, unxz, xzcat, lzma
-----------

tar
-----------

md5sum
-----------
md5sum [option]... [FILE]...

打印控制
==================
lpr (line printer) - 打印
----------
lpr FILE	打印FILE。将使用默认打印机。
lpr -P NAME	指定打印机名。注意-P不带NAME参数单独使用时有别的含义。

lpstat
----------

cups (not a executable? man 1 cups)
----------

lpq - 显示打印队列状态
--------

lprm - 取消打印任务
----------

cancel - 取消打印任务
----------

终端相关
================
stty
----------
stty -echo	关闭回显

tset & reset
---------

tput & reset
--------------
tput clear	清除tty内容

tty
---------
显示自身进程的stdin指向的设备名
一般直接从shell里调用

trap
----------

进程管理
================
ps
----------
ps -C cmdlist		显示进程命令名在cmdlist之中的进程
ps PID			显示pid为PID的进程
	ps -PID			ditto
	ps -p PIDLIST		ditto	# PIDLIST支持空格（需要引号）和","作为分隔符
	ps p PIDLIST		ditto
	ps --pid PIDLIST	ditto

lsof
--------------
-p PID
-d FDs-LIST

kill (/bin/kill, and also a bash-builtin)
--------------
send a signal to a process

字符流处理
===============
tr
--------
DOS line end (\r\n)向Linux line end (\n)转换：
tr -d '\r' FILE

pr
---------

dos2unix & unix2dos
--------

Shell辅助工具
================
script
-----------
fork一个新shell，记录新shell中的一切交互（输入输出），并写入指定文件（默认./typescript）。
随着新shell的退出(exit or C-D)而返回

date
-----------
输出日期
TODO: 控制格式

cal
-----------
日历

calendar
------------
历史上的今天 - wtf

多用户 & 用户管理
=============
who
-----------
显示已登录的用户

w
--------

finger
----------
存在安全隐患？
finger会搜索用户目录的.plan, .project, pgpkey文件？

write
-------------
w

mesg
-----------

wall
------------
write to all

chsh
------------
改变login shell

X
=============
xmodmap
-------------
修改X的按键映射

### 列出当前pointer map
xmodmap -pp

鼠标按键的编号：
- 左键 = 1
- 中键 = 2	// 通常为按下滑轮
- 右键 = 3
- 滚轮上滚 = 4
- 滚轮下滚 = 5

### 交换鼠标左右键
xmodmap -e 'pointer = 3 2 1 4 5'
对于没有滑轮的鼠标（i.e. 没有2 4 5）:
xmodmap -e 'pointer = 2 1'

Disk Management
==============

环境
============
printenv
-------------

env
-------------

Booting
================
runlevel
------------
显示当前runlevel

telinit
-----------
改变runlevel

Miscellaneous
=============
aspell
--------
TODO: vim spell check

basename
------------

readlink
-----------

dirname
-----------

realpath
-----------
