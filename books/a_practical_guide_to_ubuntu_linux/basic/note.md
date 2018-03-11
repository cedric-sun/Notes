C 1 2 3
----------
苹果的产品线曾使用IBM POWER PC处理器架构

/boot存放Linux内核，可单独使用ext2文件系统存放于独立分区，因为该目录的内容不常变化，没有必要使用ext3及以上的日志功能。

/var存放经常改变的内容（如日志），频繁的读写代表着适合将其独立出来成为一个分区，和其余文件系统的隔离也确保了/var分区被写满时不会影响别的文件系统

/usr是第二主文件层次，可以将/usr单独挂载，然后在多个系统之间共享

独立挂载/home，更换系统时保留用户的文件

.iso映像文件的etymology是ISO 9660标准，它定义了CD文件系统。

过去，用户都是在文本界面tty登录shell，然后再启动X服务器。现在，大多数系统都能提供图形化登录界面，被称为display manager。

C 4
----------------
gksudo是sudo的图形化前端
diff sudo gksudo:
https://superuser.com/questions/202676/sudo-vs-gksudo-difference
用sudo提权命令行程序
用gksudo提权图形程序

TODO: 建立管理员帐号 & 锁定（已解锁的）root账号

GNOME是GNU项目之一

nautilus的move to trash将文件存放在~/.local/share/Trash

pidgin是一个即时通讯软件

copy buffer和selection buffer (aka primary buffer)

xeyes	跟踪鼠标的X应用demo

从/usr/src/linux/Documentation和/usr/share/doc中同样可以找到文档，这些文档往往是面向开发者的

/etc/issue记录了shell登录时，显示在登录提示之前的字符串
可以使用当前机器上的getty的实现所支持的转义序列，详见man getty（通常是agetty？）的ISSUE ESCAPES一节

man 7 term
TERM环境变量通常包含了当前用户使用的终端的类型名，该变量对于所有screen-oriented的程序都很重要。
telnet和ssh等程序会将本地TERM环境变量传递给远端服务器。当远端服务器上的terminfo和termcap与本地不兼容时（即对同一个终端类型名存在着不同的能力认定），这会产生一些问题，但是很少见，并总是能通过将TERM显式地设置为"vt100"来解决——这是最简易的终端。
termcap已经过时，新系统应当使用terminfo作为TERM数据库

stty - set teletypewriter
pty = pseudo tty

进程在运行时可以接受操作系统向其发送的信号，这种机制称为signal (man 7 signal)

kill %1		其中%1用来代指后台编号为1的任务？

C 5
--------------
C-V C-?		在shell中插入控制字符	e.g. `C-V C-U`

od类似hexdump，用来进行dump
e.g.	od -c FILE	显示FILE的每个独立字符
e.g.	echo "abc(C-V C-U)" | od -t x1z
x=hex		1=1 byte per integer	z=display printable chars

lpr - line printer

扩展名在Linux下没有特殊意义，但是某些应用程序（如gcc编译器驱动会用扩展名决定具体调用C编译器还是C++编译器）
此外，遵守扩展名的约定可以最大限度地利用通配符或正则:
```
ls *.txt
```

C7
---------------
chsh改变自己的login shell，修改完成后会立即调用指定新shell的一个实例，但是仍是在shell中嵌套新shell。只有完全注销，并重新登录，才能使用新的login shell

当一个job包含多个命令（如带有管道的job）时，建立后台任务的提示中的pid是第一个命令的pid

### wildcard: ? *
如果wildcard的展开能匹配到已存在的文件，那么shell会展开wildcard，命令相当于直接接收到了各个文件名的全名。如果无法匹配到存在的文件，则shell会把wildcard原封不动当做普通字符传递给命令。
```
cedric@TR:~$ ls -d s*
ss-config
cedric@TR:~$ ls -d sk*
ls: cannot access 'sk*': No such file or directory
```
所以不能简单地认为wildcard的展开一定是发生在shell层，或总是程序本身行为
shell层展开wildcard的过程又被称为globbing
see shell option "nullglob" for more
// TODO: diff term (clobber, etc.)
关于bash统配的几点注意：
	a[0-39]可以匹配a0 a1 a2 a3 a9
	a[a-zA-Z]可以匹配所有大小写字母
	a[0-9]会在命令行上填入a0 ... a9中已存在的文件名
	a{0..9}是并不会参考已存在的文件，而是简单的生成字符串a0, a1 ..., a39并填入命令行

C8 - X!
------------------

### Relative Executables
X (/usr/bin/X)往往是指向Xorg(/usr/bin/Xorg)的软连接
```
cedric@TR:~$ ls -al $(which X Xorg)
lrwxrwxrwx 1 root root   4 Mar  4 12:22 /usr/bin/X -> Xorg
-rwxr-xr-x 1 root root 274 Jul 25  2017 /usr/bin/Xorg
```

而Xorg是启动/usr/lib/xorg/Xorg.wrap或/usr/lib/xorg/Xorg的脚本：
```
cedric@TR:~$ cat $(which Xorg)
#!/bin/sh
#
# Execute Xorg.wrap if it exists otherwise execute Xorg directly.
# This allows distros to put the suid wrapper in a separate package.

basedir=/usr/lib/xorg
if [ -x "$basedir"/Xorg.wrap ]; then
	exec "$basedir"/Xorg.wrap "$@"
else
	exec "$basedir"/Xorg "$@"
fi
```

startx是xinit的简单封装，用来启动X一个服务器实例：
```
cedric@TR:~$ which startx xinit
/usr/bin/startx
/usr/bin/xinit

cedric@TR:~$ file $(which startx xinit)
/usr/bin/startx: POSIX shell script, ASCII text executable
/usr/bin/xinit:  ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 2.6.32, BuildID[sha1]=b96dcc673f37ad0245c0a8b6e90af64999733ab3, stripped

cedric@TR:~$ head -n 20 /usr/bin/startx
#!/bin/sh

#
# This is just a sample implementation of a slightly less primitive
# interface than xinit. It looks for user .xinitrc and .xserverrc
# files, then system xinitrc and xserverrc files, else lets xinit choose
# its default. The system xinitrc should probably do things like check
# for .Xresources files and merge them in, start up a window manager,
# and pop a clock and several xterms.
#
# Site administrators are STRONGLY urged to write nicer versions.
#

unset DBUS_SESSION_BUS_ADDRESS
unset SESSION_MANAGER
userclientrc=$HOME/.xinitrc
sysclientrc=/etc/X11/xinit/xinitrc

userserverrc=$HOME/.xserverrc
sysserverrc=/etc/X11/xinit/xserverrc
```

### 若希望在分布式的环境中使用X
1. 服务器启用对tcp的监听: -listen tcp
2. 服务器允许指定主机连接监听: xhost +[...]

由于X的设计，图形程序不必要依赖Xserver在本地的安装。

Q: X服务器和客户端如何交互？通信内容是什么？
G: 服务器向客户端发送事件（e.g. 用户点击了某个坐标上的按钮、用户按下了某个按键），而客户端（应用程序）接收到该事件之后，向服务器指示该如何反馈（e.g. 显示该坐标处的按钮的“按下”动画、在文本框中回显渲染按下的按键对应的字符）

Q: 图形库是否必须同时安装在客户端和服务器？

### DISPLAY
环境变量DISPLAY唯一指定/标识了一个X服务器的实例，许多X程序也接受-display这个参数在命令行上指定X服务器。
格式为：
[hostname:]display-number[.screen-number]

