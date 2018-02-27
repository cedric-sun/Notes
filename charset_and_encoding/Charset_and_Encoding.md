Charset & Encoding
===========================
Diff charset encoding: http://www.grauw.nl/blog/entry/254

Unicode
------------------
Unicode是一种Charset，具体怎么存储/传输要看用什么encoding实现Unicode

Unicode中每一个字符被称为一个code point

Unicode中每0x10000个code points被称为一个Plane
e.g. Plane0 = 0x0000 - 0xFFFF, Plane 1 = 0x10000 - 0x1FFFF

Plane 0 (0x00000 - 0x0FFFF)	被称为Basic Multilingual Plane (a.k.a BMP)
Plane 1 (0x10000 - 0x1FFFF)	被称为Supplementary Multilingual Plane (SMP)
Plane 2 (0x20000 - 0x2FFFF)	被称为Supplementary Ideographic Plane (SIP)
Plane 3 - 13	未使用
Plane 14 (0xE0000 - 0xEFFFF)	被称为Supplementary Special-purpose Plane (SSP)
Plane 15 - 16 (0xF0000 - 0xFFFFF + 0x100000 - 0x10FFFF)	被称为Supplementary Private Use Area planes (SPUA)，其中：
	Plane 15被称为SPUA-A: 0xF0000 - 0xFFFFF
	Plane 16被称为SPUA-B: 0x100000 - 0x10FFFF

### History & Legacy
人们意识到世界需要一种统一的字符集和编码之后，有2个组织同时开始了这一工作：
	ISO & IEC制定了ISO/IEC 10646
	Unicode Consortium制定了Unicode 1.0

后者是软件制造商组成的协会。这种事情在CS历史上其实很常有不是吗，两套标准，最后以制造商们制定的、或者既成业界的de facto标准的那个取胜了，而专门精心制定的标准却失败了（参见OSI vs. TCP/IP）

其中
	ISO把自己的项目叫做Universal Coded Character Set (UCS)

### Encoding of Unicode
#### UCS-2
UCS-2是一种早期的Unicode的encoding，使用定长的2字节来编码，显然这只能表示BMP中的code points。现已基本被淘汰。

#### UTF-16	16-bit Unicode Transformation Format
UTF-16改进了UCS-2。UTF-16并不意味着总是用16 bits来编码Unicode，而只是一个名称。

对于(U+0000 - U+D7FF) + (U+E000 - U+FFFF)的code points:
	UTF-16和UCS-2都采用直接的code points作为encoding，16 bits。

对于(U+10000 - U+10FFFF)的code points:
	先减去0x10000，范围变为0x00000 - 0xFFFFF (20 bits)，这20 bits中：
	前10个(0x0000 - 0x03FF)加上0xD800组成16 bits的high surrogate (0xD800 - 0xDBFF)
	后10个(0x0000 - 0x3FFF)加上0xDC00组成16 bits的low surrogate (0xDC00 - 0xDFFF)

这样对于非BMP的code points，UTF-16采用32 bits来编码。并且由于需要用D8 - DF这几个前缀字节来表示“此处是一个32bits”的非BMP code points，在BMP中D8-DF这一部分就留空了出来。可以看到Unicode Charset制定的时候也是考虑到了Encoding实现时的问题的。

任何超出1字节的信息单元要以字节形式存放，都要考虑Endianness的问题。在UTF-16中这一问题的体现是：一个code point要编码成2字节甚至4字节，该如何表明字节序？

UTF-16 (以及UTF-32)有3种flavor，BE，LE和unmarked，BE = big-endian，LE = little-endian，unmarked默认使用BE进行序列化，但是接受BOM进行指示。

Byte Order Mark (BOM)，BOM是code point为U+FEFF的那个字符，Encoder在文件头以它所在平台的Endianness写入U+FEFF，Decoder收到时就能根据到底是0xFEFF还是0xFFFE来决定接下来的流是BE还是LE。

2018-02-10
但是我还是没有彻底搞懂：
	1. Endianness到底如何影响了UTF-16的处理？
	2. 为什么UTF-8就不存在这个问题？什么叫byte oriented？



* U+FEFF是一个不可见的zero-width non-breaking space/ZWNBSP，其原本用途是用来指示单词分割不应该在此处发生，原本用途现已被U+2060 Word Joiner取代，在正文中使用U+FEFF已经是deprecated

### UTF-32
直接使用code points来编码Unicode，定长32 bits。

### UTF-8
UTF-16的问题是，即使是BMP也需要定长16 bits来表示。在这个英语为主流语言的世界，当大多数书写、传输的字符是英文字母的时候，使用UTF-16甚至比使用古代的ASCII还多占用一倍的空间（磁盘，内存，网络流量 —— 过长的encoding方案带来的问题是全面的）

UTF-8的编码方案
Number		Bits for	First 		Last 
of bytes	code point	code point	code point	Byte 1		Byte 2		Byte 3		Byte 4
1		7		U+0000		U+007F		0xxxxxxx			
2		11		U+0080		U+07FF		110xxxxx	10xxxxxx		
3		16		U+0800		U+FFFF		1110xxxx	10xxxxxx	10xxxxxx	
4		21		U+10000		U+10FFFF	11110xxx	10xxxxxx	10xxxxxx	10xxxxxx


Reference
----------------
https://en.wikipedia.org/wiki/Universal_Coded_Character_Set
https://en.wikipedia.org/wiki/Unicode
