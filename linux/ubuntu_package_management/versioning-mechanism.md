.deb package versioning mechanism
------------------
[epoch:]UpstreamVersion[-DebianRevision]

### epoch
epoch字段的意义是，更新epoch可以从新开始版本号系统，这样就不必为过去的版本号错误而纠缠
该字段只能使用无符号数字

### UpstreamVersion
上游版本号，代表.deb包的第一手发布者指定的版本，通常这一字段会和上游发布者指定的格式保持一致，但是有时需要进行改写，以符合版本号比较机制。
该字段必须存在，且应由一个数位打头
可以使用alphanumerics(A-Za-z0-9)和五个特殊符号：
. + - : ~
在不提供epoch字段的时候，UpstreamVersion字段不能包含":"，因为一旦包含，划分字段就会出现歧义
在不提供DebianRevision字段的时候，UpstreamVersion字段不能包含"-"，理由同上

### DebianRevision
Debian的Revision，通常是为Debian系统修改过的版本
可以使用alphanumerics和+ . ~
该字段是可选的：忽略该字段代表该包只打过一次补丁(进行debianization)，因此可忽略
每次更新UpstreamVersion，DebianRevision就会重新从1开始。
dpkg会使用整个version string最后的hyphen来分割UpstreamVersion和DebianRevision
如果两个同样的UpstreamVersion，一个有DebianRevision，另一个没有，则没有的那个视为更早的包

### TODO: 比较机制
划分出三个字段之后，对于UpstreamVersion和Debian


