bash加载配置文件
==========

1. login shell都是interactive shell?

login shell (interactive login shell & non-interactive shell with --login)
-----------------
### start
1. source /etc/profile anyway
2. source the first one available in the following order:
	1. ~/.bash_profile
	2. ~/.bash_login
	3. ~/.profile

*inhibit this behavior by `--noprofile`*

### exit
1. source ~/.bash_logout

non-login shell
--------------------
### interactive
1. source /etc/bash.bashrc
2. source ~/.bashrc

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

