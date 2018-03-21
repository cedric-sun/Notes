进程组
=============
进程组主要是为了分发信号而存在的
当进程组收到一个信号时，该信号会被进程组的所有成员进程收到

e.g. shell上的一个pipeline组成一个进程组
- 如果是前景进程组，Ctrl-C发送SIGINT会终止整个job，而不仅仅是pipeline上的某个命令
- background jobs也是一样的，kill %1会导致JOBSPEC为1的pipeline中的所有命令的进程收到SIGTERM

进程组不能从一个session迁移到另一个session
进程不能创建属于另一个session的进程组(?)


当进程执行exec替换image时，新images的进程继续属于老images的进程组和session
