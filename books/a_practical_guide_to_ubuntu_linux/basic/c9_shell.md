C 9
==========
.和source将脚本在当前shell里运行，会影响当前shell环境

echo默认发送到stdout，使用`echo "sdasdsda" 1>&2`来输出错误信息到stderr

Shell Redirection
-----------
>|	ignore "noclobber" and overwrite
[n]<&-	close stdin or fd n if provided
[n]>&-	close stdout or fd n if provided

shell执行命令
-----------
1. fork
2. exec command
	if (succeed) # e.g. command is a binary program
		run
	if (failed) # e.g. command is a shell script, thus cannot be directly exec-ed
		read shebang
		if (right shebang)
			run using specified interpreter
		elseif (no shebang)
			run using shell
		else # interpreter does not exist
			prompt error

& run in background
-----------
可连写a & b & c
a b将在background，而c在foreground

最新的任务用+标识，次新的任务用-标识:
```
cedric@TR:~/Desktop$ jobs
[1]   Running                 sleep 10 &
[2]-  Running                 sleep 20 &
[3]+  Running                 sleep 30 &
```
如果仅输入`fg`，默认将带+号的任务放到foreground
%1和fg 1等价
%string可以前缀匹配，即`fg %f`可以匹配到`find .`
%?string可以任意部分匹配，即`fg %?ace`能匹配到`find . -name ace -type f`

&将前面的管道视为一个job：
```
a | b | c &
```
将作为一整个后台job启动，而不是只有c
```
cedric@TR:~/Desktop$ sleep 200 | sleep 300 | sleep 400 &
[1] 8762
cedric@TR:~/Desktop$ jobs
[1]+  Running                 sleep 200 | sleep 300 | sleep 400 &
cedric@TR:~/Desktop$ ps --pid 8762 u	# ps只会显示管道上最后一条命令？
USER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
cedric    8762  0.0  0.0  14364   680 pts/19   S    14:16   0:00 sleep 400
```

Working Directory Tricks
-----------
`dirs`		显示栈

`pushd /var`	压栈/var并显示当前栈
`pushd +N`	轮转栈，直到从栈顶数第N个栈帧到栈顶[0=栈顶]
`pushd -N`	轮转栈，直到从栈底数第N个栈帧到栈顶[0=栈底]
`pushd`		交换栈顶2个栈帧

`popd`		弹栈
`popd +N`	移除从栈顶数第N个栈帧[0=栈顶]
`popd -N`	移除从栈底数第N个栈帧[0=栈底]

`cd -`		回到先前的的工作目录[仅改变栈顶帧]



*cd仅操作栈顶的那一帧，包括cd -也只会改变栈顶*

Variables
-----------------
如果$var中有空格符，在CLI上展开时，每个空格符将被视为token分隔符。比如var="hit and run"，则echo $var时，echo将看到3个token，而echo "$var"只会让echo看到一个token。
这也不难解释如下的所谓的空格问题：因为所有空白符在shell层就被视为分隔符了。
```
cedric@TR:~$ vara="hit        and         run"
cedric@TR:~$ echo $vara
hit and run
cedric@TR:~$ echo "$vara"
hit        and         run
```
更糟的情况是，如果有vara="f*"之类的变量，那么`echo $vara`实际上是`echo f*`，则echo会输出当前目录下的所有以"f"开头的文件名。

#### 花括号引用变量
变量拼接字符串 & 引用>10的位置参数的时候必须带花括号：
$varb="Hello"
echo "$varbWorld"	# wrong
echo "${varb}World"	# correct

$1	# correct
$9	# correct
$10	# wrong
${10}	# correct

#### 删除变量
unset somevar

#### 变量属性
使变量只读： `readonly somevar`
允许同时声明：`readonly somevar=100`
显示所有只读变量： `readonly`

declare
	name=value	# 设置普通变量，等价于不带declare
	-r name=value	# 设置只读变量，等价于readonly
	-a		# 数组
	-i		# 整数
	-f		# 函数
	-x		# export，等价于export

-换成+可以删除某个属性。e.g. `declare -x -r SOMEVAR=123`声明一个全局只读变量，`declare +x SOMEVAR`将其变为非全局变量，但仍是只读。

关键字变量
-----------------
关键字变量是指那些对bash有特殊意义的变量，bash会主动读取它们，它们会影响bash的行为
关键字变量不一定是环境变量。

### CDPATH
扩大cd的搜索范围，可以直接用CDPATH中目录的子目录名作为cd参数

e.g.
```
cedric@TR:~$ CDPATH=$HOME
cedric@TR:~$ echo $CDPATH
/home/cedric
cedric@TR:~$ cd /
cedric@TR:/$ cd Desktop/
/home/cedric/Desktop
cedric@TR:~/Desktop$ 
```

### PS[1234]
可用的转义字符见man/info bash的PROMPTING一节

### IFS - Internal Field Separator
IFS变量决定了bash展开一个变量时，将哪些字符视为分割符
e.g.
```
cedric@TR:~$ LFS=p
cedric@TR:~$ a=lsp/
cedric@TR:~$ $a
bin    core  home	     lib	 media	proc  sbin  sys  var
boot   dev   initrd.img      lib64	 mnt	root  snap  tmp  vmlinuz
cdrom  etc   initrd.img.old  lost+found  opt	run   srv   usr
```
注意只有当“变量展开”这件事发生时，IFS才会起作用，在上面的例子中，如果手动在命令行上输入`lsp/`，p是**不会**作为分隔符的。
```
cedric@TR:~$ lsp/
bash: lsp/: No such file or directory
```

### HISTFILE & HISTSIZE & HISTFILESIZE
HISTFILE: bash history文件位置
HISTFILESIZE: bash history文件中保存的历史命令数
HISTSIZE: `history`命令保存的历史命令数

### COLUMNS & LINES
列数（宽度）和行数（高度）
通常select命令会使用这两个变量

### LANG & LC_*
TODO: man -f locale
```
cedric@TR:~$ declare | grep ^LC
LC_ADDRESS=en_US.UTF-8
LC_IDENTIFICATION=en_US.UTF-8
LC_MEASUREMENT=en_US.UTF-8
LC_MONETARY=en_US.UTF-8
LC_NAME=en_US.UTF-8
LC_NUMERIC=en_US.UTF-8
LC_PAPER=en_US.UTF-8
LC_TELEPHONE=en_US.UTF-8
LC_TIME=en_US.UTF-8
```

### PROPMT_COMMAND
在每条提示符弹出之前执行的命令

Process
----------------
### pstree
打印进程树
see also: ps --forest

### 执行命令
在shell中调用程序时，shell先fork一个子进程，然后exec那个程序，随后shell本身进入睡眠，子进程开始执行。子进程执行完毕后，通过其退出状态通知其父进程，也就是shell，shell被唤醒。

可以看到，后台任务（&）和前台任务的区别仅仅是：启动后台任务时shell本身不进入睡眠。

shell内置命令不会启动新进程执行。
See the "SHELL BUILTIN COMMANDS" chapter in `man 1 bash` and `man 7 bash-builtin` for more.

history
-------------
history命令的buffer中保存的是当前shell进程的历史命令。
当shell退出时，buffer中的命令才会写入$HISTFILE指定的文件，对于bash一般是~/.bash_history。
启动新shell时，将会用$HISTFILE来初始化history的buffer

### fc - fix command
#### 列出历史命令
fc -l [first [last]]
	不带first和last：	默认最近16条
	带first不带last：	从first开始到最近
	都带：			[first, last]
其中first和last可以是字符串，匹配最近的相同前缀

#### 批量修改 & 执行历史命令
fc [-e editor] [first [last]]
	不带first和last：	上一条
	带first：		first
	带first和last：		[first, last]
其中first和last可以是字符串，匹配最近的相同前缀
编辑器优先级： `-e editor` > `$FCEDIT` > `$EDITOR`

退出编辑器时shell将会执行该临时文件中的所有命令，如果不想执行，必须在退出前清空编辑器buffer

#### 直接执行
fc -s [id|prefix]
支持简单的替换:
```
cedric@TR:~$ ls 141310223.txt 
141310223.txt
cedric@TR:~$ fc -s ls=cat
cat 141310223.txt 
My name is sunce
```

### lib Readline
bash使用GNU Readline库(https://tiswww.case.edu/php/chet/readline/rltop.html)来处理输入输出。Readline库会读取$INPUTRC指定的文件，如果没有设定$INPUTRC则默认~/.inputrc，来获取按键绑定和配置信息。
e.g. 让Readline库使用vi风格的按键，在~/.inputrc里加入：
```
set editing-mode vi
```
See `man 3 readline` and the `READLINE` chapter of `man 1 bash` for more

修改~/.inputrc会导致所有使用Readline库的程序改变其行为，如果只想在bash里使用vi模式，则修改~/.bashrc:
```
set -o vi
```

#### vi模式历史命令处理
jk	上一条/下一条
?	反向搜索历史
/	正向搜索历史

alias & unalias
--------------
变量展开在别名这一情景中的例子：
```
cedric@TR:~$ alias acA="echo $PWD"
cedric@TR:~$ alias acB='echo $PWD'
cedric@TR:~$ ncA="echo $PWD"
cedric@TR:~$ ncB='echo $PWD'

cedric@TR:~$ cd /
cedric@TR:/$ acA
/home/cedric
cedric@TR:/$ acB
/
cedric@TR:/$ $ncA
/home/cedric
cedric@TR:/$ $ncB
$PWD
```

可以看到变量的展开只发生一次，即如果变量值中仍有形如对变量的引用，则不会递归地进行二次展开。

shell只对简单命令应用别名展开，比如ls会展开成ls --color=auto，但是/bin/ls不会

function
--------------
```
[function] function_name() {
	...
}
```

TODO
---------------
man getty mingetty
#### bash init script: where is PATH set?
#### () subshell: stdin and stdout stuff?
```
(cd ~/Desktop ; ls) | (cd / ; cat)
```

