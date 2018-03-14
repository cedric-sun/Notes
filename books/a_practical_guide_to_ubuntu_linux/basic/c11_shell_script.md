参数访问
-------------
$#		参数数量（不包括$0）
$0		调用名
$n		参数n
$?		最近一条在foreground运行的pipeline的返回值
$$		当前shell的pid
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


Control Flow
----------------

### 条件

#### if
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

Note: 用`seq first last`或`{first..last}`来生成list

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

`*)`表示default case


integer变量(declare -i)
--------------
```
cedric@TR:~$ a=6/3
cedric@TR:~$ echo $a
6/3
cedric@TR:~$ declare -i b
cedric@TR:~$ b=6/3
cedric@TR:~$ echo $b
2
```
