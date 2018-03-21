unit的别名机制
==================
unit的aliasing的实现只是简单的在enable的时候在/etc/systemd/system/下建立一个符号链接
e.g.
rsyslog.service有alias=syslog.service

则systemctl enable rsyslog.service之后，/etc/systemd/system/下多了一个syslog.service的symlink

当rsyslog.service是disabled的状态时，也就不存在syslog.service这个symlink，因此`systemctl enable syslog.service`或者`systemctl is-enabled syslog.service`均会失败：因为没有名为syslog.service的服务

但是当rsyslog.service是enabled的状态时，存在syslog.service，因此`systemctl disable syslog.service`是合法的，并且实际上disable的是rsyslog.service
