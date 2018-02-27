mvn
	archetype:generate
	-DgroupId=com.mycompany.app
	-DartifactId=my-app
	-DarchetypeArtifactId=maven-archetype-quickstart
	-DinteractiveMode=false
======================

archetype:generate	goal / task (Ant)
	`archetype`		plugin: a collection of goals with a general common purpose.


mvn package
====================
package: phase

phase: a step in the build lifecycle

Although hardly a comprehensive list, these are the most common default lifecycle phases executed.

- validate: validate the project is correct and all necessary information is available
- compile: compile the source code of the project
- test: test the compiled source code using a suitable unit testing framework. These tests should not require the code be packaged or deployed
- package: take the compiled code and package it in its distributable format, such as a JAR.
- integration-test: process and deploy the package if necessary into an environment where integration tests can be run
- verify: run any checks to verify the package is valid and meets quality criteria
- install: install the package into the local repository, for use as a dependency in other projects locally
- deploy: done in an integration or release environment, copies the final package to the remote repository for sharing with other developers and projects.

There are two other Maven lifecycles of note beyond the default list above. They are

- clean: cleans up artifacts created by prior builds
- site: generates site documentation for this project

Phases are actually mapped to underlying goals. The specific goals executed per phase is dependant upon the packaging type of the project. For example, package executes jar:jar if the project type is a JAR, and war:war if the project type is - you guessed it - a WAR.

Dependency
===================
project
	dependencies
		dependency
			groupId
			artifactId
			version
			scope: provided / test / compile?

依赖的version不能省略

在Maven 2里可以用LATEST或者RELEASE来指定使用依赖的最新版或者稳定版，但是考虑到reproducibility，Maven 3取消了对这一特性的支持：

https://stackoverflow.com/questions/30571/how-do-i-tell-maven-to-use-the-latest-version-of-a-dependency

plugin
=================
声明plugin应该详细指定plugin的groupId, artifactId和version，但是version似乎可以省略

在仅声明
```
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
```
的情况下，插件似乎仍然会起作用

可以看出，插件只要在pom.xml里声明其存在，插件就**可以**自动绑定某个lifecycle的某个phase

Q：在pom.xml里声明过的插件是否默认情况下一定会绑定某个phase？**（考虑映射结构图）**
A：

考虑到CLI上直接调用plugin:goal甚至不需要该plugin在pom.xml里声明，这种情况下pom.xml里的plugin是用来进行参数配置和phase绑定的：
```xml
<build>
	<plugins>
		<plugin>
			<artifactId>maven-assembly-plugin</artifactId>
			<configuration>
				<archive>
					<manifest>
						<mainClass>hello.SampleController</mainClass>
					</manifest>
				</archive>
				<descriptorRefs>
					<descriptorRef>jar-with-dependencies</descriptorRef>
				</descriptorRefs>
			</configuration>
		</plugin>
	</plugins>
</build>
```

此时在CLI上调用`mvn clean compile assembly:single`的时候，assembly plugin的single goal就知道如何配置可执行jar的manifest的Main-Class等信息了。

plugin dependency
======================
插件本身也有依赖，比如maven-antrun-plugin 1.2依赖Ant 1.6.5，但是如果用户想强制使用最新版ant，比如ant 1.7.1，可以为`<plugin>`加上`<dependencies>`的约束：
```
<project>
	...
	<build>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-antrun-plugin</artifactId>
				<version>1.2</version>
				...
				<dependencies>
					<dependency>
						<groupId>org.apache.ant</groupId>
						<artifactId>ant</artifactId>
						<version>1.7.1</version>
					</dependency>
					<dependency>
						<groupId>org.apache.ant</groupId>
						<artifactId>ant-launcher</artifactId>
						<version>1.7.1</version>
					</dependency>
				</dependencies>
			</plugin>
		</plugins>
	</build>
	...
</project>
```

Q: 如果插件A不依赖插件B，但是A中强行写了对B的依赖会怎么办？

plugin inheritance
======================
plugin默认是继承的，使用`<inherited>`可以使子项目不继承该plugin：
```
<project>
	...
	<build>
		<plugins>
			<plugin>
				<groupId>org.apache.maven.plugins</groupId>
				<artifactId>maven-antrun-plugin</artifactId>
				<version>1.2</version>
				<inherited>false</inherited>
				...
			</plugin>
		</plugins>
	</build>
	...
</project>
```

pluginMamagement
=======================
pluginManagement提供了对在本项目及子项目中可能出现的plugin的约束，和dependencyManagement一样，这里的逻辑是"If what I specify here is encountered in the future, use the configuration here"，即本身并不声明使用任何插件，只是对可能出现的插件的约束。

子项目有权覆盖继承来的pluginManagement


3 built-in lifecycle & their phases
=================
default
clean
site

每个lifecycle的phases及其顺序是固定的，参考：Apache Maven Doc - Lifecycle Reference

在CLI上作为参数调用的可以是一个phase，也可以直接是一个plugin提供的goal，该plugin并不一定需要在pom.xml里声明

CLI上的plugin有两种调用形式：
1. `mvn plugin-prefix:goal`
2. `mvn <plugin-triplet>:goal` - 其中<plugin-triplet>就是`plugin-groupId:plugin-artifactId:plugin-version`

对于第1种使用plugin短名称的调用，需要一种plugin prefix resolution的短名称决议方式来决定到底使用哪个插件的哪个版本：https://maven.apache.org/guides/introduction/introduction-to-plugin-prefix-mapping.html

通常名字带hyphen (-)的phase都**不会**直接在CLI上被调用，这些中间pahse往往代表一些pending / hanging的state，有可能会导致诸如容器（Tomcat、Docker）未被回收之类的不一致性问题。

pom.xml的`<packaging>`决定了哪些官方发布的插件的通用goals要绑定到哪些phase上，这很好理解：打包jar的package phase所要进行的操作肯定不同于打包war所要进行的操作。

由`<packaging>`值所决定的一系列goals的bindings优先级是最高的，会在phase中首先执行，其次才是该phase中由executions绑定的goals，依照其execution在pom.xml出现的顺序执行

同一个plugin的多个instance是不支持的，也就是说一个plugin的全局配置只能有一个，同一个plugin的多次声明会在执行时被合并（after Maven 2.0.11）。

Mojo
==============
Maven old Java Object

一个Mojo对应一个goal，一个plugin由1个或多个Mojo组成

一个Mojo对应的goal名在Mojo类的上面用annotation `@goal goal_name`来声明

一个goal可以有默认绑定的phase，在其Mojo类上面用annotation `@phase default_phase`来声明

Mojo提供setters，Maven通过传统套路（删掉setXxxx的set）来从pom.xml里映射<configuration>中的配置给Mojo

对于数组String[] options，pom.xml里可以写：
```
	<options>
		<option>one</option>
		<option>two</option>
		<option>three</option>
	</options>
```
Maven会找到合适的方式来处理数组映射。

有些goal设计之初就是为了直接从CLI上invoke，此时goal更希望直接从被称为system properties的参数传递方式中获得参数，在Mojo中相应的field上用`@parameter expression="${name_used_in_CLI_for_this_field}"`来声明这种可直接接受system properties的性质。感觉就是个fancy word，跟OS的环境变量也毫无关系，就是通过CLI `-D`参数指定的key-value pair，参考`mvn -help`

可以注意到CLI上使用的名字并不一定和Mojo对应的field名字一样，但是pom.xml里却一定要一致，这导致了一些不一致性 - 出于历史原因，一些插件期待的system properties的名字和其Mojo field名完全无关，所以总是检查插件文档是一个好的习惯。

system properties是一个统一的namespace，在命令行上总是统一在goals和phases之前指定：
```
mvn [options] [<goal(s)>] [<phase(s)>]
```
所以为了避免各个goals使用的system properties冲突，goals会使用`foo:bar`这样的namespace机制，调用的时候可能是：
```
mvn -DgoalA.sp0=value0 -DgoalB.sp0=value1 pluginA:goalA pluginB:goalB some_phase ...
```

大多数plugin有一个help goal：
```
mvn dependency:help
	-Ddetail to be verbose
	-Dgoal=xxx to only display help about a specific goal
```

profile
===============
Maven profile指的是：
- pom.xlm
- user-specific settings.xml
- installation-specific settings.xml
- profile.xml in project basedir (obsoleted and unsupported in Maven 3.0)

execution
===============
`<executions>`外面的configuration是全局的，会对该plugin的所有goals的每次invocation生效。

`<execution>`用来把一个plugin的一个或多个goal(s)绑定到一个phase上去，会覆盖默认绑定的phase，可以有自己的配置（会覆盖全局吧）

曾经execution里的

如果一个plugin有execution：
	如果该execution有phase：把该execution的goals里的所有goal都绑定到该phase
	如果该execution没有phase：把该execution的goals里的所有goal都绑定到默认phase
如果该plugin没有execution：
	该plugin的每个goal绑定到各自的default phase

Q：是否单纯的声明一个plugin的存在就会把它的所有拥有默认phase的goals进行默认绑定？然后声明一个execution是额外再进行绑定？
A: 如果一个plugin没有execution是根本不会执行的，如果当前pom没有看到execution，多半是继承了父项目的plugin配置（plugin / pluginManagement）

在单个execution可以直接从CLI上调用这个意义上，execution更像是单独的一套配置，这套配置可以绑定至某个phase执行，也可以从命令行上以这套配置运行（而不是plugin全局配置）

plugin dev
==================
/* @goal name */ 和 `@Mojo( name = "name" )`似乎一样，都是指定了goal的名字

`mvn install`同一个triplet会覆盖本地repo的文件

pom.xml里没有声明某插件，仍然可以直接在CLI上调用某插件的某个goal

缩短CLI typing的方式：
- 省略version，自动使用plugin在本地仓库的最新版本
- 如果plugin符合命名规范（https://maven.apache.org/guides/introduction/introduction-to-plugin-prefix-mapping.html），则可以用plugin-prefix
- 如果想省略groupId，需要把插件的groupId加到groupId search范围里，${user.home}/.m2/settings.xml：
```
	<pluginGroups>
		<pluginGroup>sample.plugin</pluginGroup>
	</pluginGroups>
```

此时可以简单地用`mvn hello:sayhi`来调用goal

triplet
==================
groupId只是一个标识，不一定要符合任何域名反写的规约，比如junit项目在Maven repo的groupId就是`junit`

groupId的dot notation不一定对应于项目的package结构，but it is a good practice to follow

假设groupId由`domain0.domain1.domain2`组成，在repo存储的时候，会按${repoBase}/domain0/domain1/domain2/artifactId/version/.jar的方式存储

有时packaging也作为project coordinate的一个字段：
You will sometimes see Maven print out a project coordinate as
`groupId:artifactId:packaging:version`

还有一个element叫classifier，有时也作为project coordinate的一个字段：
`groupId:artifactId:packaging:classifier:version`


Dependency
================
项目应该只描述自己的依赖，依赖的依赖（transitive dependencies）应该交给maven来处理

shaded dependencies应该从依赖中除名？因为它已经成为该项目的built-in (private) bit?

当依赖不存在于Maven central repo的时候（比如第三方闭源jar），有三种方式处理：

1. 手动安装jar至local repo，使其成为Maven可管理的依赖：
```
mvn install:install-file
	-Dfile=non-maven-proj.jar
	-DgroupId=some.group
	-DartifactId=non-maven-proj
	-Dversion=1
	-Dpackaging=jar
```
install plugin会自动创建POM

2. 在公司内网，往往采用deploy到公司的repo服务器的方式
3. Deprecated: Set the dependency scope to system and define a systemPath. 

classfier: 用来区分同一个POM构建的，但却内容不同的artifacts，是一个可选且任意的字符串，一般（在坐标和文件名中？）放在version number后面（如果存在）。

type: 常对应依赖artifact的packaging值，默认为jar。（使用待研究）

scope: 决定了该依赖加入哪些（phase的）classpath（每个用到classpath的pahse都会有自己的classpass，e.g. compile classpath, test classpath），以及依赖的传递性。有5个可用的scopes:
http://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#Dependency_Scope
	- compile: 默认值。依赖在所有classpath都可用。会传递到依赖本项目的项目。
	- provided: 与provided基本相似，但是表示期待该依赖会在运行时由JDK或容器在运行时提供。只在编译和test时加入classpath。
	- runtime: 编译时不需要，执行时需要。加入runtime和test classpath，不加入compile classpath（会写到jar包manifest的classpath里？）
	- test: 表示并非应用通常运行时需要的依赖。只加入test-compile和execution phase。non-transitive.
	- system: 与provided相似，只是你需要explicitly提供该依赖的jar。总是可用（在所有classpath上），并且不会在repo里查找（不受Maven管理）。
	- import: (supported after Maven 2.0.9) 该依赖的在`<dependencyManagement>`里的type必须是`pom`，会把该依赖的dependencyManagement的值import到当前项目（即将当前依赖规定替换成该依赖的依赖规定），因为是替换，所以import这个scope本身不会影响到传递性。

systemPath:
	指定scope为system的依赖的搜索路径，必须为绝对值。用户需要手动确保需要的依赖的jar包存在于路径上，否则构建会失败。

optional:
	构建项目A依赖于项目B，但是当A本身只是项目X的依赖的时候，A中依赖于B的那部分代码可能不会被用到，此时在A中将B标记为一个optional dependency。

Excluded dependencies
--------------
If project X depends on project Y, and project Y depends on project Z, the owner of project X can explicitly exclude project Z as a dependency, using the "exclusion" element.

Optional dependencies
---------------
If project Y depends on project Z, the owner of project Y can mark project Z as an optional dependency, using the "optional" element. When project X depends on project Y, X will depend only on Y and not on Y's optional dependency Z. The owner of project X may then explicitly add a dependency on Z, at her option. (It may be helpful to think of optional dependencies as "excluded by default.")

Dependency Version Requirement Specification
=====================
- 1.0: "Soft" requirement on 1.0 (just a recommendation, if it matches all other ranges for the dependency)
- [1.0]: "Hard" requirement on 1.0
- (,1.0]: x <= 1.0
- [1.2,1.3]: 1.2 <= x <= 1.3
- [1.0,2.0): 1.0 <= x < 2.0
- [1.5,): x >= 1.5
- (,1.0],[1.2,): x <= 1.0 or x >= 1.2; multiple sets are comma-separated
- (,1.1),(1.1,): this excludes 1.1 (for example if it is known not to work in combination with this library)


继承
===============
**parent和aggregation项目的packaging必须为`pom`**

parent artifact必须是纯粹的metainfo


https://stackoverflow.com/questions/9120294/how-do-i-show-the-maven-pom-hierarchy

不会被继承的element:
	artifactId
	name
	prerequisites

```
	<parent>
		<groupId>org.codehaus.mojo</groupId>
		<artifactId>my-parent</artifactId>
		<version>2.0</version>
		<relativePath>../my-parent</relativePath>
	</parent>
```
`<relativePath>` element告诉Maven首先搜索此处指定的path来找parent，其次才是local repo，其次才是remote repo

Q: 如何强制Maven使用remote repo？
A:

`mvn help:effective-pom`可以显示继承之后最终的`pom.xml`

`<dependencyManagent>`用来管理本pom的所有子pom的依赖属性。如果parent的`<dependencyManagent>`指定了`junit:junit:4.0`，其子pom使用junit时可以只声明groupId=junit和artifactId=junit，Maven会自动设置version为4.0。该特性意义在于统一管理继承树上的依赖。

archetype:generate through proxy
=================
1. PowerShell:
```
Invoke-WebRequest https://repo.maven.apache.org/maven2/archetype-catalog.xml -OutFile archetype-catalog.xml
```
with global mode of shadowsocks-windows, or any other way you can to download this file manually.

2. copy the file you've just downloaded to ~/.m2/repository/

3. `mvn archetype:generate -DarchetypeCatalog=local`

Ref: https://issues.apache.org/jira/browse/ARCHETYPE-202

same dependency, different version
=================
如果A（直接或间接地）依赖了B 1.0和B 2.0，对于B而言的一个问题是，classpath上不能存在qualified name完全相同的两个类。

nearest definition原则：
如果A有依赖
A -> B -> C -> D 2.0
和
A -> E -> D 1.0
由于D 1.0在依赖树上离A最近，D 1.0会被使用
如果想强制使用D 2.0，需要给A显式地添加对D 2.0的依赖（尽管A本身并不直接依赖D），显然不够好

Q: API接口的一致性？兼容性？

`<dependencyManagement>`可以解决这个问题：
指定：如果遇到该依赖，则使用特定的版本（本身并不会引入任何依赖，只是对可能出现的依赖的规定）

variables
==============
${variableName}
任何pom.xml模型中单一值的element（没有子element）都可以作为一个变量被引用

`<properties>`中可以自定义变量

有3个特殊变量，总是可用，由Maven直接提供：
- project.basedir	pom.xml所在的目录
- project.baseUri	URI表示的project.basedir (since Maven 2.1.0)
- maven.build.timestamp	开始构建的时间 (since Maven 2.1.0-M1)

spring boot maven
====================
spring-boot-dependencies
	继承树最顶层，2636行
	没有引入任何依赖，只有dependencyManagement（parent项目是metainfo，不可能引入任何依赖）
	大部分是dependencyManagement（2000多行）
	properties里统一定义了各种依赖的版本要求
	插件方面大部分是pluginManagement
	只引入了3个插件：
		maven-help-plugin				不继承
		org.codehaus.mojo:xml-maven-plugin		不继承
		org.codehaus.mojo:build-helper-maven-plugin	不继承

spring-boot-starter-parent:spring-boot-dependencies
	继承树第二层，200多行
	没有引入任何依赖，只有depManagement
	本身没有引入任何插件，只有pluginManagement

// parent项目的plugin也只是对纯pom本身进行检查？// 因为并不存在实际的代码
// parent是否总是不引入任何依赖，只是对可能出现的依赖进行约束？
// 以达成子项目的统一依赖标准化，构成一个依赖 / 插件版本的统一范式？

Q: plugin的继承有一个问题，继承中的父项目一定是个纯pom，那一个纯pom需要什么plugin呢？（XML核验？）

由于父项目是个纯pom，关于代码或者编译、构建的插件加在父项目上并没有任何意义，然而具体拥有代码的子项目往往拥有一些共同的任务，如果将这些共同的插件的共同的配置（执行、版本要求等）在每个子项目里都写一遍显然不优雅，packageManagement解决了这个问题，在父项目里声明的只是对依赖的约束和执行配置，这会被子项目继承， 达成了统一性。

统一了依赖范式之后，子项目里引入依赖的时候只需要声明groupId和artifactId，而无需关心version以及是否兼容这种细节：parent项目的depManagement保证了整个项目中依赖的兼容性。

对于开发者而言，他可以只关心“我使用了这个依赖”，而不必关心兼容性之类的一系列琐碎的问题。

https://maven.apache.org/pom.html#Plugin_Management

Maven用{groupId, artifactId, type, classifier}四元组来唯一确定子项目中的一个依赖应该对应父项目depManagement中对其的描述。如果子项目需要的是type=jar, classifier=null的话，只要声明groupId和artifactId就能使配置对应生效，因为这就是这两项的默认值。但是如果这两项不是默认值，那就仍然需要在子项目中指定type和classifier，才能绑定父项目中dependenceManagement的值。
http://maven.apache.org/guides/introduction/introduction-to-dependency-mechanism.html#Importing_Dependencies
NOTE: In two of these dependency references, we had to specify the <type/> element. This is because the minimal set of information for matching a dependency reference against a dependencyManagement section is actually {groupId, artifactId, type, classifier}. In many cases, these dependencies will refer to jar artifacts with no classifier. This allows us to shorthand the identity set to {groupId, artifactId}, since the default for the type field is jar, and the default classifier is null.

project.dependencies的声明优先级高于（继承来的）project.dependencyManagement
当前项目的dependencyManagement的优先级高于父项目的dependencyManagement
用当前项目的project.dependencies覆盖当前项目的project.dependencyManagement是一种矛盾的行为（如果Maven把继承来的depManagement和当前项目的depManagement进行叠加那就无法对“继承来的”和“当前项目的”加以区分了）

depManagement import
==============
pom只能有一个parent，但是项目B继承自项目A，但是项目B也想使用项目X的depManagement，此时可以使用import

如果项目A import 了项目B和项目C，项目B和项目C的depManagement里包含了对同一个依赖的不同版本的指定，那么先出现在A的pom中的那一个import胜出。

import是递归的，A import 了B，B中又import了C，那么从A的角度来看，就好像C中的depManagement早就在B中一样。

Q: 如果继承来的depManagement和import来的depManagement发生冲突，谁会胜出？

Dingus
============
plugin和dependency的本质是一样的，都由maven统一管理，前者作用于构建过程本身，后者作用于代码本身，在逻辑上都是库，提供了即插即用的便利的功能。
