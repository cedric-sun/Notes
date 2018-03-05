几个关键文件
======================
/etc/passwd
----------------
man 5 passwd
/etc/passwd一行对应一个用户

```
	cedric:x:1000:1000:Cedric,,,:/home/cedric:/bin/bash
```

7 fields, delimited by colons (:)
	1. login name			[cedric]
	2. (optional) encrypted passwd	[x]
	3. numeriacl UID		[1000]
	4. numerical GID		[1000]
	5. user name or comment field		[Cedric,,,]
	6. user home directory		[/home/cedric]
	7. (optional) user command interpreter	[/bin/bash]

### field 2 - encrypted passwd
field 2可以为空，此时鉴别该login name不需要密码。但是某些应用程序读了/etc/passwd之后，可能不会允许field 2为空的账户进行任何操作。

如果field 2是一个小写的x，代表加密后的密码存储在/etc/shadow。此时shadow文件中**必须**存在对应的行，否则该用户账户就无效。

除了上述情况，field 2中任何其他值都会被视为加密后的密码。加密详情见man 3 crypt。

### field 5 - user name or comment field
各种system utilities会field 5，比如finger (man 1 finger)

### field 6 home
field 6代表初始工作目录。`login`程序会用这一信息来设置$HOME环境变量。

### field 7
代表用户命令语言解释器的名称，or the name of the initial program to execute. `login`程序使用该field设置$SHELL环境变量。如果为空，默认为/bin/sh

/etc/shadow
----------------
man 5 shadow

cedric:$1$PBKIfx8v$ZST8PMxsGdUcA5u6zJpCH/:17570:0:99999:7:::

9 fields:
	1. login name	[cedric]
	2. encrypted passwd	[$1$PBKIfx8v$ZST8PMxsGdUcA5u6zJpCH/]
		如果此处的值不是crypt(3)的合法结果，则该用户无法使用unix密码登录（但是可以以其他方式登录）。
		此field可以为空，此时不需要密码来鉴别该login name，但是某些应用程序读了/etc/shadow之后（wcnm这权限够高的）可能会决定不允许该账户进行任何操作。
		如果该field以感叹号!打头，代表密码被锁，感叹号以外剩余的字符代表密码被锁之前的密码。（密码或账户过期？）
	3. 上次改密码的日期	[17570]
		从1980年1月1日起的天数
		用于配合min pa和max pa计算相关过期天数。
	4. minimum password age		[0]
		number of days
		empty field或者0代表没有minimum password age
	5. maximum password age		[99999]
		number of days
		empty field或者0代表没有maximum password age、没有password warning period & 没有password inactivity period
		过期后密码仍可以有效，用户下次登录应被要求更改密码。
		如果field 5 < filed 4，则用户无法更改密码。
		e.g. 每5天必须修改一次密码（max），每两次修改密码却不得小于10天(min)
	6. password warning period	[7]
		maximum password age过期之前多久（天数），用户该得到修改密码的警告提示。
		e.g. mpa = 10 days, pwp = 3 days，则用户在某次修改密码7天之后会得到“请在3天内修改密码“的提示
		empty field或者0代表没有pwp
	7. password inactivity period		(empty)
		密码过期后(after max-pa)仍然有效的天数。用户在此期间的下次登录会被要求修改密码。如果pip也过期，则用户无法使用密码登录，应当联系管理员。
		empty field代表没有对pip的强制要求（无限期？）
	8. account expiration date	(empty)
		账户过期的日期 - 从1970.1.1起的天数
		账户过期和密码过期不同：
			账户过期之后，用户不允许登录
			密码过期之后，用户不允许通过密码登录
		empty field代表账户永不过期
		不应使用0，0值可能产生歧义：要么不会过期，要么在1970.1.1过期
	9. 保留字段	(empty)
		This field is reserved for future use.

/etc/group
-----------------
4 fields:
	1. group name
	2. (encrypted) group password
	3. GID
	4. user list

/etc/gshadow
---------------------
4 fields:
	1. group name
	2. encrypted passwd
		如果此处的字符串不是crypt(3)的合法结果，如!或*，则非该组的用户无法使用密码访问该组（该组的组内用户并不需要密码）
		组密码通常是用来使一个用户获得自己不属于的某个用户组的权限。
			e.g. 一个非admin用户组的用户获得admin的权限（如执行sudo）
		如果该域为空，则只有组成员才能享有组权限。（不可能有别的用户使用密码提权）
		!代表密码被锁，剩余字符代表上锁之前的密码。
		此处的密码会覆盖/etc/group中的密码。
	3. administrators
		一个逗号分隔的用户名列表
		administrators享有普通组员的权限以外，还可以更改组密码、修改组成员。
	4. members
		一个逗号分隔的用户名列表
		members可以不用密码就访问用户组
		该field应和/etc/group中的user list (field 4)保持一致


/etc/login.defs
----------------------
### UID
		default value if not specified in /etc/login.defs
UID_MAX		60000
UID_MIN		1000

### GID
GID_MAX		60000
GID_MIN		1000

### SYS_UID
SYS_UID_MAX	UID_MIN - 1
SYS_UID_MIN	101

### SYS_GID
SYS_GID_MAX	GID_MIN - 1
SYS_GID_MIN	101

CREATE_HOME	no	是否自动为新用户创建home目录。只对普通用户有效，system user会无视该选项，统一不创建home目录。

几个相关命令
===============
chage [options] LOGIN
-------------
* ROOT is required.
* 0就代表0，-1往往代表empty field

-d, --lastday LAST_DAY		修改/etc/shadow的field 3。值为1970.1.1起的天数。

-E, --expiredate EXPIRE_DATE	修改shadow的field 8。EXPIRE_DATE为1970.1.1起的天数。
				也可以使用YYYY-MM-DD的格式。
				EXPIRE_DATE = -1代表移除expiration date。

-I, --inactive INACTIVE		修改shadow的field 7。INACTIVE为天数。
				INACTIVE = -1代表移除inactivity period。

-l, --list			显示账户的aging infomation。COOL.

-m, --mindays MIN_DAYS		修改shadow的field 4
				MIN_DAYS = 0代表用户可以随时修改密码。

-M, --maxdays MAX_DAYS		修改shadow的field 5
				-1代表密码永久有效。

-R, -root CHROOT_DIR		使用CHROOT_DIR/作为/，来寻找相应的配置文件。
				e.g.	/etc/passwd -> CHROOT_DIR/etc/passwd

-W, --warndays WARN_DAYS	修改shadow的field 6

chgrp
-------------
modify user group to which a file belong
* 只能chgrp到自己所在的某个用户组，否则需要root。

-R, --recursive		递归。

chown
---------------
* 修改文件owner必须要root账户。
* `chown :GROUP xxx`仅修改组的时候同`chgrp`: GROUP必须为自己所在的某个用户组，否则需要root

useradd
-------------
-s, --shell SHELL	指定用户的login shell
-g, --gid GROUP		用户的initial group的名称或gid。
			如果未指定，则：
				在自动创建了同名用户组的情况下，使用同名用户组
				在未自动创建同名用户组的情况下，使用/etc/default/useradd的GROUP变量。如果GROUP变量也没有设置，默认使用gid = 100。
-G, --groups GROUP1[,GROUP2,...]	设置额外的supplementary groups。可使用名称或gid，用逗号分隔。
-m, --create-home	为用户创建home目录
-M			不要为用户创建home目录。用来覆盖CREATE_HOME。
-k, --skel SKEL_DIR	依照骨架目录创建home。只有配合-m时才有效。
			不指定该选项时默认使用/etc/default/useradd中的SKEL变量
			SKEL变量也未指定时，默认使用/etc/skel作为骨架
			SKEL_DIR = /dev/null可以不生成任何骨架。
-u, --uid UID		指定用户UID。
-U, --user-group	为即将创建的用户建立一个同名用户组。
			不指定该项时，默认值是USERGROUPS_ENAB变量（一般是yes）。
-N, --no-user-group	Contrary to -U. Use this to override USERGROUPS_ENAB.
-r, --system		创建一个system account。默认情况下不会创建home目录（即使CREATE_HOME = yes），除非手动指定-m。system account uid的范围取决于SYS_UID_MIN和SYS_UID_MAX，而不是普通用户的UID_MIN和UID_MAX。

* useradd的行为会受到/etc/login.defs这个配置文件的影响，比如该文件中的CREATE_HOME变量设为yes的情况下，即使不指定-m也会默认创建home目录（但是仍可以用-M覆盖）

userdel
--------------
-f, --force		强制删除账户，即使用户已登录。同时删除用户的home目录（即使多个用户都在使用该目录）和mail spool

-r, --remomve		删除用户的home目录，同时删除mail spool

usermod
---------------
* usermod = user modify, but chmod = change mode
`usermod [options] LOGIN`

-g, --gid GROUP		改变initial login group。可用group name或gid。
-G, --groups GROUP1[,GROUP2,...]	设置额外的supplementary groups。可使用名称或gid，用逗号分隔。注意这只是赋值，会覆盖现有的用户组，如果要追加用户组，需要配合-a。
-a, --append		追加用户组，而不是覆盖。必须配合-G。
-c, --comment		修改/etc/passwd的comment field。通常应使用chfn工具修改。
-d, --home HOME_DIR	修改home目录路径。并不会移动现有目录内容，仅是修改/etc/passwd
-m, --move-home		修改home目录路径的同时移动现有目录。必须配合-d。
-e, --expiredate EXPIRE_DATE	修改账户过期时间。同`chage -E`
-f, --inactive INACTIVE		修改账户inactive时间。同`chage -I`
-l, --login NEW_LOGIN	修改用户的登录名，仅此而已。如果需要，需要手动更新用户的home目录或者mail spool。

groupadd
-------------
`groupadd [options] group`

-g, --gid GID		指定group's ID
-r, --system		创建一个system group。system gid的范围取决于SYS_GID_MIN和SYS_GID_MAX，而不是普通用户的GID_MIN和GID_MAX。

groupdel
-------------
`groupdel [options] GROUP`

无法删除一个既存用户的primary group，i.e. 必须先删除所有以GROUP作为primary group的用户，才能删除GROUP

*  primary group = initial login group?

groupmod
--------------
`groupmod [options] GROUP`

-g, --gid GID		更改gid
			以GROUP作为primary group的用户的/etc/passwd中的gid也会自动更新
			但是如果有必要，文件系统上的文件inode中记录的所属的gid必须手动更新
-n, --new-name NEW_GROUP	更改group name为NEW_GROUP

* primary group被记录在/etc/passwd的field 4中，但是supplementary groups被以/etc/group (& /etc/gshadow)的user list (field 4 for both files)的形式记录（反向mapping）

diff user* *user
----------------------
useradd, userdel, usermod是binary
adduser, deluser是perl脚本，后端仍是useradd

第4个权限位
===============
linux的默认权限机制通过12个bit来记录权限：
	前3个是suid(4) sgid(2) sticky_bit(1)
	剩下9个就是user group other每个的rwx

suid - setuid - set user ID upon execution
--------------
任何用户可以直接以文件属主的身份执行该文件（但是首先该用户要本身拥有x权限）
* 只适用于文件

e.g. /bin/passwd
```
	cedric@ubuntu:~/Desktop/permtest$ ls -l $(type passwd | cut -d ' ' -f 3)
	-rwsr-xr-x 1 root root 54256 May 16  2017 /usr/bin/passwd
```

即cedric可以直接在bash中使用`passwd`来以root身份执行passwd，修改自己(cedric)的密码

如果passwd是`-rwsr-xr--`，则other无法以root身份执行passwd，因为other没有x

### 关于脚本的setuid
如果脚本是executable shell script，即由magic number `#!/PATH_TO_INTERPRETER`开头，则直接从bash里以`./script arg1 arg2 ...`的形式调用的时候，script文件本身上设置的setuid位会起作用，但是如果以`INTERPRETER script arg1 arg2`调用的时候，则解释器本身被调用读取script，此时script被当做普通文本文件对待，因此script上的setuid位不会起作用。

More about executable shell script:
http://www.faqs.org/faqs/unix-faq/faq/part4/section-7.html

假设一个脚本foo:
```
	echo 123
```

此时在shell里执行`./foo`（首先foo要有x权限），此时没有#!这一magic number，或者OS无法识别`#!`后指定的解释器，则OS会向shell返回一个缺少解释器的错误码，此时shell会尝试用/bin/sh作为解释器运行该脚本（/bin/sh通常为指向真正解释器 - 如bash等 - 的symlink）

可以看到这是一个shell的行为，而不是OS ABI层的行为，所以与“直接调用executable shell script可以使脚本文件上的setuid生效”不同，此时OS看到的实际上是`/bin/sh script arg1 arg2 ...`这样的形式，因此script上的setuid此时不会生效。

sgid - setgid - set group ID upon execution
-------------
* 适用于文件时类似于setuid，相当于任何拥有x权限的用户(u g o)都以组用户身份执行。

适用于目录时，任何在该目录下创建的文件的owner仍然是文件的创建者，但是文件的group将和该目录的group保持一致。

场景：Alice, Bob, Carol三个用户都属于admins用户组，希望共享admins_dir/文件夹，但是Alice在该目录下创建的文件将拥有alice:alice的owner和group，必须要开other的w权限（文件默认664），或者手动修改成alice:admins才能使其他admins写入。这样显然过于麻烦。如果将admins_dir/设为sgid，则任何在该目录下创建的文件都被设为:admins，这样就方便的实现了用户组的设置。

sticky bit
-----------------
* sticky bit在用chmod字母法设置的时候只需要`chomd +t xxx`
* 只适用于目录

设置为sticky的目录，只有该目录的owner，以及目录中文件的创建者，能够删除或重命名该文件。

sticky bit是为了解决w权限过于宽泛的问题的，即w代表了创建+删除+修改，但是在有些场景下，我们希望多个用户都可以在某个目录下创建文件，但是用户不能随便修改/删除别的用户建立的文件。

e.g. /tmp
```
	cedric@ubuntu:~$ ls -ld /tmp
	drwxrwxrwt 14 root root 4096 Feb 12 19:21 /tmp
```

登录系统的每个用户都可以在/tmp里存储临时文件，但是不允许删除别人的临时文件。

显示问题
---------------
虽然文件系统中这12 bits一定是分开存储的，但是在ls等程序显示的时候格却是叠加的。

setuid会在owner的x位上显示s，由于会覆盖原来的x：
	原来owner有x的时候，显示s
	原来owner没有x的时候，显示S

setgid会在group的x位上显示s，由于会覆盖原来的x：
	原来group有x的时候，显示s
	原来group没有x的时候，显示S

sticky bit会在other的x尾上显示t，由于会覆盖原来的x：
	原来other有x的时候，会显示t
	原来other没有x的时候，会显示T
