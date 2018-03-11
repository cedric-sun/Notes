Package Management in Ubuntu
==============

.deb file format
----------
以chrome的.deb包为例：
```
Desktop/google-chrome-stable_current_amd64.deb
├── control.tar.gz
│   ├── control
│   ├── postinst
│   ├── postrm
│   └── prerm
├── data.tar.xz (filesystem tar-file)
└── debian-binary
```

.deb文件是普通的ar归档包，文件头magic number: "!<arch>"

也支持tar归档包，但是并不推荐。详细支持的tar格式见manpage

包内第一个成员是名为debian-binary的文件，包含了一系列行，目前只使用了一行，是deb文件格式的版本号，应为2.0

包内第二个必须的成员是control.tar。这是包含包的控制信息的tar归档包，并允许使用gzip或xz压缩（此时扩展名为.tar.gz或.tar.xz）。包内应是一系列文本文件，其中名为control的文件是必须的，包含了核心的控制信息。

第三个成员，也是最后一个必须的成员是data.tar，支持gzip (.tar.gz), xz (.tar.xz), bzip2 (.tar.bz2), lzma (.tar.lzma)压缩

包内成员必须严格按照上述顺序排列。目前的实现要求忽略data.tar后的一切成员，之后文件格式的版本更新也会将新成员追加在上述三者之后。

control.tar包内可以包含一个"conffiles"文件，内容如：
```
/etc/init.d/shadowsocks
/etc/shadowsocks/config.json
/etc/default/shadowsocks
```
是该包需要的配置文件的名称，dpkg会将data.tar中的上述三个文件视为配置文件（作用是e.g. remove不会删除配置文件，purge才会）

### control file
"#"开头的行是注释
#### 4个必选
Package: package-name

Version: version-string

Maintainer: fullname-email
格式应为：`Joe Bloggs <jbloggs@foo.com>`
通常是.deb包的制作者（区别于该软件本身的作者）

Description: short-description
 long-description
跟tag在同一行上的是短描述，通常会被apt-cache search之类的程序用于简略描述该包
换行之后是长描述，长描述的每一行**必须**由一个空格打头，空行必须包含一个"."

#### 描述性字段
##### Section: section
代表包的种类
e.g. utils, net, mail, text, x11, ...

##### Priority: priority
该包在系统中的重要性
e.g. required, standard, optional, extra, ...

*Section & Priority的合法值参见debian-policy包所提供的手册*

##### Essential: yes | no
是否关系到系统的正常运作
dpkg等包管理工具不允许移除Essential package（除非带上force选项）
通常只有yes的时候该字段才需要出现...

##### Build-Essential: yes | no
是否关系到构建系统的正常工作
通常只有yes的时候该字段才需要出现...

##### Architecture: ARCH | all
all代表architecture independent

##### Origin: distro-name
该包来自的发行版的名称

##### Source: source-package-name
该包的源码包的名字

#### 依赖
##### Depends
若包A依赖包B, C, D
	安装中：B C D的postinst会在A的postinst之前执行
	卸载中：A的prerm会在B C D的prerm之前执行

##### Pre-Depends
场景：包A的preinst脚本需要包B安装并配置好才能运行。

##### Recommends
正常安装需要的依赖包。若用户选择不安装Recommends包，则会弹出警告

##### Suggests
安装这些包会提供增强的功能，但是不安装也是完全合理的

上述4个字段的格式是：group0, group1, ...
每个group的格式是：pack0 | pack1 ...
一个group内的包可以互相替换，so 管道号读作"OR"

每个包名后可以跟一个可选的":ARCHITECTURE"指定架构（对应依赖包的Architecture字段）
ARCHITECTURE可以为any。如果省略，则默认和本包的Architecture字段相同

每个包名后可以跟一个可选的"(VERSION-QUALIFIER)"指定该依赖的版本要求

VERSION-QUALIFIER format:
`>>VERSION`	大于VERSION		# 任何VERSION之后的版本都可接受
`>=VERSION`	大于等于		# 同上，且包含VERSION
`<<VERSION`	小于			# 任何VERSION之前的版本都可接受
`<=VERSION`	小于			# 等于同上，且包含VERSION

*VERSION可以忽略Debian Revision号*

#### 冲突
##### Breaks: package-list
该包将破坏的包
e.g. 安装该包将使package-list中的某个包产生bug
包管理系统将不会允许package-list中的包被配置

##### Conflicts: package-list
e.g. 包含同名文件
冲突的两个包应该互相在该字段中提到对方

##### Replaces: package-list
该包有能力替换package-list中的包提供的某些文件
常见用法是，如果该字段和Conflicts字段中都提到了某个包S，那么包S会被卸载

上述3个字段的格式是：package0, package1, ...
可选的":Architecture"，但默认值是any，而不是本包的Architecture
可选的"(VERSION)"，格式同依赖的4个字段

#### 虚拟包 Provides: package-list
e.g. "sendmail"和"exim"两个包都能当mail server用，所以它们都提供了一个名为"mail-transport-agent"的虚拟包。这样别的包就能把"mail-transport-agent"当做依赖，而无需关心邮件服务器到底是用哪个包实现的
注意，尽管“依赖一个邮件服务器”的包可以在它们的Depends字段中使用"|"写出所有满足条件的邮件服务器实现的包名，但是显然没有使用虚拟包机制简洁。

package-list的格式是：vpackage0, vpackage1, ...
可选的":Architecture"，默认值本包的Architecture
可选的"(VERSION)"，严格等于。

#### 构建信息 Built-Using: package-list
声明该包构建时所使用的额外源码包名
package-list中的包名必须跟着严格的"=VERSION"限制符

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

##### 包信息
// 应指出：available和status是两个数据库，尽管它们对每个包维护的信息差不多
对于每个available的包，dpkg关心并维护3个属性，对应dpkg -l的前三列flag：
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
###### dpkg native
short	long			arguments		note
-i	--install		package-files(R)
	--unpack		package-files(R)		unpack but do not configure
	--configure		packages*
	--triggers-only 	packages*
-r	--remove		packages*
-P	--purge			packages*
-V	--verify		[packages]		verify all packages if no packages specified
	--update-avail		[Packages-file]		replace old info with new one. 
							read from stdin if no Packages-file specified
	--merge-avail		[Packages-file]		combine old info with new one
							read from stdin if no Packages-file specified
-A	--record-avail		package-files(R)
	--forget-old-unavail				TODO
	--clear-avail
-C	--audit			packages*		perform db sanity & consistency checks for "packages"
							check all packages if no package specified
	--get-selection		[package-name-pattern]	non-installed will not be shown if no arg
	--set-selection					read from stdin only
							unknown packages (not in avail) are ignored
	--clear-selections				将所有包的selection变为deinstall(remove)
							通常用在-set-selection之前以清除环境
							真是个危险的命令...
	--yet-to-unpack					Searches for packages selected for installation, but which for some reason still haven't been installed.
	--predep-package				TODO
	--add-architecture	architecture-name
	--remove-architecture	architecture-name
	--print-architecture
	--print-foreign-architecture
	--assert-feature				TODO
	--compare-version	ver1 op ver2
-?	--help
	--force-help					Give help about the --force-thing options

*当参数为-a或--pending时，dpkg数据库中所有列为“等待该操作”的包会被执行对应操作
(R) 参数可为目录，此时带上-R参数会递归作用于目录内所有文件

TODO: what does unpack mean?
###### dpkg-deb actions
-b	--build
-c	--contents
-e	--control
-x	--extract
-X	--vextract
-f	--field
	--ctrl-tarfile
	--fsys-tarfile
-I	--info

###### dpkg-query actions
-l	--list
-s	--status
-L	--listfiles
-S	--search
-p	--print-avail

##### TODO: dpkg options

#### dpkg-deb
dpkg-deb packs, unpacks and provides information about Debian archives.
对于多数接受一个archive名作为参数的命令，使用"-"可以让dpkg-deb读stdin
man 1 dpkg-deb中提到：
> You  can  also  invoke  dpkg-deb  by calling dpkg with whatever options you want to pass to dpkg-deb. dpkg will spot that you wanted dpkg-deb and run it for you.
但是dpkg-deb有些参数，比如-W，如果直接调用dpkg -W，则会提示未知参数。可见此处的"whatever options"并不正确。


short	long		args					note
-b	--build		directory [archive|directory]
-I	--info		deb-archive [control-file-name]		c-f-n is the name of a file in the "control.tar" tarball, e.g. "control", "preinst".
								If no c-f-n specified, a summury is printed and "control" is used by default.
-W	--show		deb-archive				see also: --showformat
-f	--field		deb-archive [control-field-name]	if no c-field-n specified, print the whole "control" file
-c	--contents	deb-archive				list all files that will be installed on the filesystem (everything in the "data.tar" tarball)
-x	--extract	archive directory			extract all file that will be installed to "directory".
								Note that extracting a package to the root directory will NOT result in a correct installation!
-X	--vextract	archive directory			verbose output extract
-R	--raw-extract	archive directory			extract control infomation files also, to a directory named "DEBIAN"
	--ctrl-tarfile	archive					pipe "archive"'s "control.tar" to stdout. This is meant to be used together with `tar` on the pipeline
	--fsys-tarfile	archive					pipe "archive"'s "data.tar" to stdout. This is meant to be used together with `tar` on the pipeline. "data.tar" is also called "filesystem tar-file"
-e	--control	archive [directory]			extract the content of the "control.tar" of the archive to "directory".
								If no "directory" specified, create & use "DEBIAN" by default.

#### dpkg-query
dpkg-query显示dpkg数据库中的信息
short	long		args				note
-l	--list		[package-name-pattern]
-W	--show		[package-name-pattern]
-s	--status	package-name...
-L	--listfiles	package-name...
	--control-list	package-name			不包含原deb包里的"control"文件
	--control-show	package-name control-file	打印指定控制文件的内容。某个包的可用的"control-file"名可以通过--control-list得到
-c	--control-path	package-name [control-file]	打印指定包的[指定]控制文件的路径
-S	--search	filename-pattern		f-p来自哪个包。注意文件必须来自包本身，安装后由安装脚本创建的文件（配置文件等）不会维护在数据库中，因此也不会找到。
-p	--print-avail	package-name...			打印available文件中关于p-n的信息

deb安装到系统时，会核验包内的control/md5sums文件，并作为控制信息的一部分存入数据库。
如果没有这个文件，则安装时就无法核验文件的完整性了，但是dpkg仍会计算并生成该文件存入数据库，用以维护一致性。不论如何，包内的md5sums和数据库内的md5sums应当完全一致。

### Files
/var/lib/dpkg/available
dpkg和dselect用该文件记录所有可用的包的信息。
该文件相当于dselect的online repo的index文件，只是dpkg也提供查询该文件的操作，可见dpkg设计之初是面向dselect提供支持的。
只使用dpkg作为后端，apt作为前端时，这个无用的文件确实会对理解dpkg的工作方式带来一些困惑。
通常该文件由`dselect update`维护。APT前端**不会更新**也**不会使用**该文件作为数据库。因此所有操作available文件的Actions，在APT作为前端的系统上基本毫无作用。

/var/lib/dpkg/status
dpkg用该文件记录所有未purge的包的信息。

### USE
#### 
dpkg -s PACKAGE_NAME		show the status of installed package PACKAGE_NAME
dpkg -S FILE_NAME		determine which package provides file FILE_NAME
dpkg -L PACKAGE_NAME		show all the files provided by PACKAGE_NAME // the output of `dpkg -L` and the file list on the packages.ubuntu.com vary only in that `dpkg -L` will also display directories

dpkg --set-selection		read file from stdin, whose content should be in the format "package state", and modify the selection state of the "package" to "state". Legal value of "state" are: "install", "hold", "deinstall" or "purge". Utilities provided by package "dlocate", such as "dpkg-remove" or "dpkg-purge" provides a convenient way to change these states marker. Speculation: maybe the change of package selection state is not usually (or not meant to be) invoked directly by user, so such a batch-operation design is efficiency-oriented, and is meant to be used by sysadmins.
dpkg --info DEB_FILE		Examine DEB_FILE (meta-information)// =dpkg-deb --info
dpkg --content DEB_FILE		list the content of DEB_FILE // =dpkg-deb --content

TODO: see more commands provided by package "dlocate"
```
cedric@MS:~$ dpkg -L dlocate | grep bin
/usr/sbin
/usr/sbin/dpkg-purge
/usr/sbin/dpkg-unhold
/usr/sbin/dpkg-hold
/usr/sbin/dpkg-remove
/usr/sbin/update-dlocatedb
/usr/bin
/usr/bin/dlocate
```


### dpkg-deb

apt - Advanced Packaging Tool
---------------
### Determine what files a online package contains
This is possibly impossible via local apt interface, for store the info about the content of each package is not necessary, maintaining the content list does not help any aspects about solving the dependencies or installing the package

### apt-cache
apt-cache depends PACKAGE_NAME		show all the dependencies of PACKAGE_NAME
apt-cache rdepends PACKAGE_NAME		show all packages that depends on PACKAGE_NAME
apt-cache showpkg PACKAGE_NAME		show all the available version of PACKAGE_NAME from official repo	// apt show -a PACKAGE_NAME can also do this
apt-cache unmet [-i]

### TODO: determine which remote package provides specific file (esp. executable)
Why bash know which pacakge to be prompt for you to install when you type a command that does not exist on local machine yet provided by a package in the online repo?

### Downgrade
sudo apt-get install <package-name>=<specific-version-number>

PACKAGE NOTES
==============
1. No pacakge depends on ubuntu-minimal
2. dpkg itself has no knowledge of what "dependency" is. And its output of dpkg -l is somewhat confusing: Desired is called "selection state" elsewhere, althrough this field usually represent the intent of the user about "what do you want to do with this package". So even some package is installed as a dependency (i.e. not because the user explicitly specify it as the argument of apt-get), dpkg will mark the "desired" field of the dependency as "install"
3. !!! vim-common=2:7.4.1689-3ubuntu1.2 disappeared in `apt-cache` after downgrade to 2:7.4.1689-3ubuntu1
4. 
5. `sslocal` binary provided by obsolete package "shadowsocks" is unable to support encryption method "chacha20-ietf-poly1305". The old "shadowsocks" package in official repo (at least in xenial) is implemented using python, and might now be in the state of no-longer-maintained. Use package "shadowsocks-libev" instead.

TODO
==============
1. How does dpkg understand dependencies?
```	
	dpkg: error processing package sogoupinyin (--install):
	 dependency problems - leaving unconfigured
```

