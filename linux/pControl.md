信号分发与session & process group之间的关系？

当session leader不存在时，session的foreground process group应当处理hangup信号

setsid()
==============
创建一个新session，使calling process成为一个其session leader，以及该session中唯一的新process group中的唯一进程，当然，此时calling process是session leader & group leader (of the only group)

calling process不能是一个group leader，因为这并不符合设计。否则calling process成为了新session中的一个新group的group leader，这个新group用calling process的pid作为pgid，这样新旧sessoin中存在使用同一个pgid的两个process group，乱套了。

为了确保这一点，通常：
```
p = fork();
if (p) exit(0);
pid = setsid();
```

process group可以没有group leader，但是自然情况下一个process group总是由一个leader fork出来的

session id是session leader的process group id
(POSIX)不允许session leader改变process group id


setpgid(pid_t pid, pid_t pgid)
=============
- 要么使`pid`加入（当前session）一个已存在的process group `pgid`
- 要么在当前session创建一个新process group，使calling process成为其group leader

```
setpgrp() = setpgid(0,0)
```



当process group id = ID的process group仍存在（组中仍有进程）的时候，系统中新进程不得reuse ID作为自己的PID（即使PID = ID的进程（原来的process group leader）已经死亡） - 因为这样该新进程有可能成为group leader的时候就会产生冲突（他会用自己的pid作为new group id)，旧的process group也不会把这个新进程误认为自己的group leader


信号机制
==============
kill (2)- <signal.h> <sys/types.h>
---------------
system call `kill` 既能够向individual process发送信号，也能向process group发送信号

raise (3)
---------------
raise library function call可以向进程自身发送信号

处理信号
---------------
use signal(2) or sigaction(2) to set traps

默认处理也有2种可选：SIG_IGN忽略	SIG_DFL使用默认handler

SIGKILL & SIGSTOP cannot be intercepted

`sigprocmask(2)` to block & unblock the delivery of signals.
SIGKILL & SIGSTOP cannot be blocked.

Session
==============
在textual user interface登陆的时候，一个login session在内核中的表示是一个真正的kernel session
在图形终端登录时，一个login session对应一个由display manager拉起的指定进程的life span

Session Leader Exit
-------------
用户登出时
- 没有前台进程组
- 对于后台进程组
  - 对于login shell，后台进程组是否收到SIGHUP取决于bash的huponexit选项(TODO)
  - 对于终端模拟器中的interactive non-login shell，后台进程组不会收到SIGHUP

shell (controlling process / session leader)被SIGHUP时
- 前台进程组收到SIGHUP(此时nohup的前台进程组继续运行)（虽然nohup好像只支持单命令的)
- 后台进程组收到SIGHUP(!)

shell被SIGTERM时
**前台有进程时忽略SIGTERM**
- 前台进程收到SIGTERM(TODO: is it really SIGTERM or other signal that also terminate the process?)
- 后台进程组不收到任何信号，过继给init

Conclusion: 当session leader收到SIGHUP的时候，session中所有进程组都会收到SIGHUP

foreground process group
=========
一个session同时最多存在一个foreground process group，也可以没有fpg

可以看到内核中会话和前后台进程组的概念是为了shell的"作业控制"这一特性而对应实现的

stty
===========
stty tostop控制着：当一个background process group向tty发起输出的时候，是否向其发送SIGTTOU信号
进程收到SIGTTOU信号应当停止，但是如果进程选择无视，那么write()会返回EIO (Error IO)

disown
============
对于作为controlling process的shell而言，如果使用disown将一个job移除出`jobs`显示的列表，则当shell收到SIGHUP时不会向该job对应的process group发送SIGHUP


EXIT!?
=============
用exit命令退出terminal emulator和直接关闭emulator的窗口，后果是不一样的
exit会保留后台进程
直接关闭会杀死process group

GUESS: 直接关闭terminal emulator发送了SIGHUP

session leader shell收到SIGHUP的时候，会向jobs列表中的process groups发送SIGHUP
因此process group不受shell job control控制的进程不会收到SIGHUP（即使它仍在当前session中）
比如从shell运行用户的程序a.out
a.out本身fork一个子进程然后立即退出，子进程不受shell管理，也不会收到SIGHUP
这样的子进程所在的process group就成为orphan process group

Daemonize
==============
对于一个daemon所处的独立session，我们真的并不需要一个controlling process
怎么优雅怎么来 显然是fork setsid fork更舒服
