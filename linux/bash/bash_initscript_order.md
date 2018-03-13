bash加载配置文件
==========
login shell都是interactive shell
Q: what if I `bash -l some_script.sh`?

login shell (or with -l option)
-----------------
### on start
1. source /etc/profile anyway
2. source the first one available in the following order:
	1. `~/.bash_profile`
	2. `~/.bash_login`
	3. `~/.profile`

*inhibit this behavior by `--noprofile`*

Usually `~/.bash_profile` will source `~/.bashrc` too, so that a login shell can also obtain features provided by the non-login shell init script.

### on exit
source `~/.bash_logout`

non-login shell
--------------------
### interactive (e.g. terminal emulator)
1. source /etc/bash.bashrc
2. source ~/.bashrc

The book *A Practical Guide to Ubuntu Linux* mentioned that one should source `/etc/bashrc` (which doesn't even exist in 16.04.03 LTS, I guess they've changed it to `/etc/bash.bashrc`) in `~/.bashrc`, I don't think this make sense anyway. According to the man page, these 2 files will both be sourced without mentioning the order of execution.

*inhibit this behavior by `--norc`*
*`--rcfile FILE` force bash to source FILE instead of the 2 file mentioned above*

### non-interactive (e.g. to execute script)
1. source $BASH_ENV, as if :
```
if [ -n "$BASH_ENV" ]; then . "$BASH_ENV"; fi
```

if invoked as `sh` symlink
==============
以"sh"这一名字调用bash的时候，bash会尽量模仿sh的行为，并尽量遵守POSIX

login shell
-------------
1. source /etc/profile
2. source ~/.profile

*--noprofile works too*

