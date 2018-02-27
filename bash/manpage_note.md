CLI options
==================
-c		该选项后的第一个non-option argument将被视为在新bash进程里执行的命令。
		执行完成后将退出bash。

-i		start a **interactive** shell

-l		make the newly-invoked bash work as if it is a login shell

-r		invoke a **restricted** bash shell

-s		if bash is invoked without a script file (no more token remains after argument processing) or with -s, it take commands from STDIN.
		This allow positional parameter to be set when invoking an interactive shell.  // -si?

-v		equivalent to --verbose
		show more infomation on each command / step that bash executes

Arguments
==============
if
	1. arguments remains after option processing, and
	2. neither `-c` nor `-s` option has been specified

pipelines
===============
pipeline connection establishs before any redirection.

command | command2		command's stdout to command2's stdin
command |& command2		command's stdout and stderr to command2's stdin
