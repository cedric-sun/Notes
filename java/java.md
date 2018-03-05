Does `java` call `javac` or not?
===============
`packageA.ClassA`依赖`packageB.ClassB`，然而执行`ClassA.class`的时候ClassB仍然处于源代码`ClassB.java`的状态，`java`会如何处理？

Interface
==============
接口中
1. 方法必须是public abstract
2. 变量必须是public static final
如果不指定，则视为隐式指定
