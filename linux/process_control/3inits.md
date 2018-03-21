SysVInit
============
/etc/init.d/		脚本
/etc/rc?.d/		链接
/etc/rc.local

update-rc.d SERVICE enable	create symlink in /etc/rc?.d/service to /etc/init.d/service

service SERVICE stop/start

systemd
==========
/lib/systemd/system/	脚本
/etc/systemd/system/	链接

systemctl
-----------
### Service Admin
start
stop
reload			if the service unit support this
reload-or-restart	do this when you are not sure whether reload is supported
enable			create symlink
disable
status
is-active
is-enabled
is-failed
kill
restart

### System Overview
LOAD	ACTIVE	ENABLED	SUB
