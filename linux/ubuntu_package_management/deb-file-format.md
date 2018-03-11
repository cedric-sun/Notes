.deb file format
=============
.deb文件是普通的ar归档包，文件头magic number: `!<arch>`

也支持tar归档包，但是并不推荐。详细支持的tar格式见man page

包内第一个成员是名为"debian-binary"的文件，包含了一系列行，目前只使用了一行，是deb文件格式的版本号，应为`2.0`

包内第二个必须的成员是"control.tar"。这是包含包的控制信息的tar归档包，并允许使用gzip或xz压缩（此时扩展名为.tar.gz或.tar.xz）。包内应是一系列文本文件，其中名为control的文件是必须的，包含了核心的控制信息。

第三个成员，也是最后一个必须的成员是data.tar，支持gzip (.tar.gz), xz (.tar.xz), bzip2 (.tar.bz2), lzma (.tar.lzma)压缩

包内成员必须严格按照上述顺序排列。目前的实现要求忽略data.tar后的一切成员，之后文件格式的版本更新也会将新成员追加在上述三者之后。

control files - control.tar
---------------
control.tar中可以包含以下7个控制文件：
control conffiles
preinst postinst
prerm postrm
triggers

### conffiles - 配置文件声明
conffiles声明该包提供的配置文件
e.g.
```
/etc/init.d/shadowsocks
/etc/shadowsocks/config.json
/etc/default/shadowsocks
```
dpkg会将data.tar中的上述三个文件视为配置文件（作用是e.g. remove不会删除配置文件，purge才会）

### preinst postinst


### prerm postrm

### triggers

### control
"#"开头的行是注释
#### 4个必选
1. Package: package-name
2. Version: version-string
3. Maintainer: fullname-email
格式应为：`Joe Bloggs <jbloggs@foo.com>`
通常是.deb包的制作者（区别于该软件本身的作者）
4. Description: short-description
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
