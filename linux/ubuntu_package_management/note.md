Package Management in Ubuntu
==============

.deb file format
----------
.deb文件是普通的ar归档包，文件头magic number: "!<arch>"

也支持tar归档包，但是并不推荐。详细支持的tar格式见manpage

包内第一个成员是名为debian-binary的文件，包含了一系列行，目前只使用了一行，是deb文件格式的版本号，应为2.0

包内第二个必须的成员是control.tar。这是包含包的控制信息的tar归档包，并允许使用gzip或xz压缩（此时扩展名为.tar.gz或.tar.xz）。包内应是一系列文本文件，其中名为control的文件是必须的，包含了核心的控制信息。

第三个成员，也是最后一个必须的成员是data.tar，支持gzip (.tar.gz), xz (.tar.xz), bzip2 (.tar.bz2), lzma (.tar.lzma)压缩

包内成员必须严格按照上述顺序排列。目前的实现要求忽略data.tar后的一切成员，之后文件格式的版本更新也会将新成员追加在上述三者之后。

.deb package versioning mechanism
------------------
[epoch:]UpstreamVersion[-DebianReversion]

### epoch
epoch字段的意义是，更新epoch可以从新开始版本号系统，这样就不必为过去的版本号错误而纠缠
该字段只能使用无符号数字

### UpstreamVersion
上游版本号，代表.deb包的第一手发布者指定的版本，通常这一字段会和上游发布者指定的格式保持一致，但是有时需要进行改写，以符合版本号比较机制。
该字段必须存在，且应由一个数位打头
可以使用alphanumerics(A-Za-z0-9)和五个特殊符号：
. + - : ~
在不提供epoch字段的时候，UpstreamVersion字段不能包含":"，因为一旦包含，划分字段就会出现歧义
在不提供DebianReversion字段的时候，UpstreamVersion字段不能包含"-"，理由同上

### DebianReversion
Debian的Reversion，通常是为Debian系统修改过的版本
可以使用alphanumerics和+ . ~
该字段是可选的：忽略该字段代表该包只打过一次补丁(进行debianization)，因此可忽略
每次更新UpstreamVersion，DebianReversion就会重新从1开始。
dpkg会使用整个version string最后的hyphen来分割UpstreamVersion和DebianReversion
如果两个同样的UpstreamVersion，一个有DebianReversion，另一个没有，则没有的那个视为更早的包

### 比较机制
划分出三个字段之后，对于UpstreamVersion和Debian

dpkg - Debian PacKaGe
---------------

### History
dpkg was originally created by Ian Murdock in January 1994 as a Shell script, Matt Welsh, Carl Streeter and Ian Murdock then rewrote it in Perl, and then later the main part was rewritten in C by Ian Jackson in 1994. The name dpkg was originally the short for "Debian package", but the meaning of that phrase has evolved significantly, as dpkg the software is orthogonal to the deb package format as well as the Debian Policy Manual which defines how Debian packages behave in Debian.

### CLI Interfaces
#### dpkg
dpkg [option...] action

1. dpkg is a tool to **install, build, remove and manage** Debian packages (.deb)
2. dpkg的user-friendly的前端wrapper是aptitude
3. dpkg本身完全靠命令行参数控制（**但是仍有**）
4. 每次只能有1个Action，但可以可以有若干options
5. action告诉dpkg做什么，options控制action的行为
6. dpkg本身也是dpkg-deb和dpkg-query的前端：

对于每个包，dpkg关心并维护3个属性，对应dpkg -l的前三列flag：
package states:		包状态，指该包当前处于什么状态
	not-installed		该包未安装
	config-files		系统上只存在该包的配置文件
	half-installed		该包的安装已开始，但出于某些原因还未完成
	unpacked		该包已经unpack，但是还没配置
	half-configured		该包已经unpack，并且配置已经开始，但出于某些原因还未完成
	triggers-awaited	该包在等待另一个包的触发器
	triggers-pending	该包已经被触发
	installed		该包已经正确地unpack并配置

Package selection states:	选中状态，即用户希望对该包进行什么处理
	install			该包被选中安装(installation)
	hold			被标记为hold的包不会被dpkg处理，除非用--force-hold强制覆盖
	deinstall		该包被选中卸载(deinstallation)，即删除所有文件，但保留配置文件
	purge			The  package  is selected to be purged
				(i.e. we want to remove everything from system
				directories, even configuration files).  

Package flags:		包flag，用来指示错误
	reinst-required		A package marked reinst-required is broken
				and  requires  rein‐ stallation.
				These packages cannot be removed, unless
				forced with option --force-remove-reinstreq.

##### ACTIONS
short	long		arguments	description
-i	--install	deb-file	install
	--unpack	deb-file	unpack (but do not configure)
	--configure	package*	configure
	--triggers-only package*
-r	--remove	package*		remove
-P	--purge		package		purge


apt - Advanced Packaging Tool
---------------
