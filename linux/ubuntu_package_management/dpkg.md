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


#### dpkg-query
显示conffiles
conffiles不会作为单独的control files保存，也不会由`dpkg-query --control-list`显示
dpkg-query -s PACKAGE_NAME
dpkg-query -f '${Conffiles}\n' -W PACKAGE_NAME
