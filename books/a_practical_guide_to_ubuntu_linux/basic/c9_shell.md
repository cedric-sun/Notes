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

控制bash的特性和选项
------------
### CLI参数
--posix			以posix兼容模式启动bash
-O opt / +O opt		打开/关闭shopt选项opt

### set
set是POSIX标准
`set -o` or `set +o`获取两种不同版本的当前选项开关情况
set -o opt打开opt，set +o opt关闭opt
通常opt会有对应的单选项，比如`set -o xtrace`等价于`set -x`，`set +o xtrace`等价于`set +x`

### shopt
shopt不是POSIX标准，shopt管理着另一套选项，但是shopt也可以操作set选项

shopt			show all options status
shopt opt		show opt status
shopt -s opt		set
shopt -u opt		unset
shopt -o		操作set选项

e.g.
```
cedric@TR:~$ set -o | grep noclobber
noclobber      	on
cedric@TR:~$ shopt -o -u noclobber
cedric@TR:~$ set -o | grep noclobber
noclobber      	off
```

bash工作过程
-----------------
### 0.0 历史展开
如!!运行上一条命令
set histexpand
### 0.1 别名替换
shopt expand_aliases
### 0.2 Tokenization
### 1 花括号生成展开
e.g. `echo chap_{one,two,three}.txt`
set braceexpand
注意花括号展开的条件：
```
cedric@TR:~$ echo aa_{123}
+ echo 'aa_{123}'
aa_{123}
cedric@TR:~$ echo aa_{123,}
+ echo aa_123 aa_
aa_123 aa_
cedric@TR:~$ echo aa_{123,456}
+ echo aa_123 aa_456
aa_123 aa_456
```

注意[]的展开和{}的展开不同，[]的展开发生在路径名展开层，即vrs[A-E]只能匹配到**已经存在的**vrsA, vrsB, ..., vrsE中，即遵循“若没有匹配到已存在的文件就不生成”的原则。
```
cedric@TR:~/Desktop/test$ touch test{0..9}
+ touch test0 test1 test2 test3 test4 test5 test6 test7 test8 test9
cedric@TR:~/Desktop/test$ ls
+ ls --color=auto
test0  test1  test2  test3  test4  test5  test6  test7  test8  test9
cedric@TR:~/Desktop/test$ rm test4
+ rm test4
cedric@TR:~/Desktop/test$ ls test[0-9]
+ ls --color=auto test0 test1 test2 test3 test5 test6 test7 test8 test9
test0  test1  test2  test3  test5  test6  test7  test8  test9
cedric@TR:~/Desktop/test$ ls test{0..9}
+ ls --color=auto test0 test1 test2 test3 test4 test5 test6 test7 test8 test9
ls: cannot access 'test4': No such file or directory
test0  test1  test2  test3  test5  test6  test7  test8  test9
```

同时注意上面{}展开和[]展开中，表示范围的语法的不同，以下是错误示范：
```
cedric@TR:~/Desktop/test$ ls test[0..9] # "test0" or "test." or "test." or "test9"
+ ls --color=auto test0 test9
test0  test9
cedric@TR:~/Desktop/test$ ls test{0-9}
+ ls --color=auto 'test{0-9}'
ls: cannot access 'test{0-9}': No such file or directory
```

### 2 代字符(~)展开
当~出现在某个token的起始处时：
1. 后面紧跟一个合法login name时，展开成该login name的home
e.g.
```
cedric@TR:~/Desktop/test$ echo ~tonystark
+ echo /home/tonystark
/home/tonystark
```

login name不存在时，不展开
e.g.
```
cedric@TR:/$ echo ~xx
+ echo '~xx'
~xx
```
2. ~+展开成$PWD，~-展开成$OLDPWD
3. 展开为$HOME

### 3 参数展开 & 变量展开
参数
	命令行
	位置参数
	特殊参数
变量
	用户变量
	关键字变量

### 4 算数展开
`$((expression))`
整数运算，结果向下取整

#### let也可以进行算术运算
```
cedric@TR:~$ let a=33+22*4
cedric@TR:~$ echo $a
121
```

如果表达式有空格，则需要使用引号
```
cedric@TR:~$ let "a = 3 * 2 + 344"
cedric@TR:~$ echo $a
350
```

同一行上可以有多个表达式
```
cedric@TR:~$ let a=3+2 b=99/4
cedric@TR:~$ echo $a $b
5 24
```

((expression))和let expression是同义词

在$(())和let中引用变量时，都不需要带上$

### 5 命令替换
`$(command)`
command将在子shell中执行

bash支持
```
`command`
```
的语法，但是存在各种缺陷，比如不能嵌套，以及标点处理的歧义

### 6 IFS分词
在前面几层的展开完成之后，再按IFS对被展开的部分进行分词

### 7 路径名（模糊文件名引用）展开
即替换* ? []
使用set -o noglob关闭这一层展开，通配符本身将作为参数传递给程序
shopt -s nullglob可以在通配符匹配不到任何文件时，将通配符转换为null，而不是把通配符本身传递给程序作为参数。

双引号会阻止这一层的展开，但不阻止变量&参数展开
单引号会阻止所有展开

需注意在变量赋值这一上下文中，虽然没有单双引号，但上下文仍然阻止了这一层展开：
```
cedric@TR:~/Desktop/test$ ls
test0  test1  test2  test3  test5  test6  test7  test8  test9
cedric@TR:~/Desktop/test$ somevar=test*
cedric@TR:~/Desktop/test$ set | grep somevar
somevar='test*'
```

下面的例子更好地展示了无引号、双引号和单引号的展开层级的不同：
```
cedric@TR:~/Desktop/test$ echo $somevar
test0 test1 test2 test3 test5 test6 test7 test8 test9
cedric@TR:~/Desktop/test$ echo "$somevar"
test*
cedric@TR:~/Desktop/test$ echo '$somevar'
$somevar
```

### 8 进程替换（bash特有）
```
<(command)
>(command)
```
将command的stdout/stdin管道文件作为文件名参数
e.g.
diff <(command1) <(command2)

TODO
---------------
man getty mingetty
#### bash init script: where is PATH set?

