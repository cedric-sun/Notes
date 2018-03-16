Asterisk紧贴变量名 & 指针/非指针分开写
====================
#### Right
```
int *ptr_a, *ptr_b;
int c;
```

#### Wrong

```
int* ptr_a, b;
```

const
==============
常指针的Asterisk紧贴const
```
int const *ptr_a;	// 指向常量的指针
int *const ptr_b;	// 常指针
```
