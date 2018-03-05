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


dpkg - Debian PacKaGe
---------------

### History
dpkg was originally created by Ian Murdock in January 1994 as a Shell script, Matt Welsh, Carl Streeter and Ian Murdock then rewrote it in Perl, and then later the main part was rewritten in C by Ian Jackson in 1994. The name dpkg was originally the short for "Debian package", but the meaning of that phrase has evolved significantly, as dpkg the software is orthogonal to the deb package format as well as the Debian Policy Manual which defines how Debian packages behave in Debian.

### CLI Interfaces
#### dpkg
dpkg [option...] action

1. dpkg is a tool to **install, build, remove and manage** Debian packages (.deb)
2. dpkg的user-friendly的前端wrapper是aptitude
3. dpkg本身完全靠命令行参数控制（没有任何配置文件？）
4. Each invocation consist of **exactly one action** and **zero or more options**.
5. action告诉dpkg做什么，options控制action的行为
6. dpkg本身也是dpkg-deb和dpkg-query的前端：

对于每个包，dpkg关心并维护3个属性：
package states:
	not-installed		该包未安装
	config-files		系统上只存在该包的配置文件
	half-installed		该包的安装已开始，但出于某些原因还未完成
	unpacked		该包已经unpack，但是还没配置
	half-configured		该包已经unpack，并且配置已经开始，但出于某些原因还未完成
	triggers-awaited	该包在等待另一个包的触发器
	triggers-pending	该包已经被触发
	installed		该包已经正确地unpack并配置

Package selection states:
	install			该包被选中安装(installation)
	hold			被标记为hold的包不会被dpkg处理，除非用--force-hold强制覆盖
	deinstall		该包被选中卸载(deinstallation)，即删除所有文件，但保留配置文件
	purge			The  package  is selected to be purged (i.e. we want to remove everything from system directories, even configuration files).  

Package flags
	reinst-required		A package marked reinst-required is broken  and  requires  rein‐ stallation. These packages cannot be removed, unless forced with option --force-remove-reinstreq.




apt - Advanced Packaging Tool
---------------
