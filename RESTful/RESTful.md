RESTful
===================
1. URI标识一个资源，动词决定操作
2. 充分利用HTTP协议的各个字段，如Accept和content-type来
3. http协议的URI部分应该只用来标识一个资源，至于做什么，交给HTTP协议剩下的信息来描述（动词、header field等）

https://en.wikipedia.org/wiki/List_of_HTTP_header_fields


用URI标识资源，用operation操作资源，用representation指定表现形式。

资源位置、操作、和期待的表现层结果分离，REST不限于HTTP，只是因为HTTP恰好能够实现REST（对动词的支持，对表现层约束的支持(request header field: Accept)），并且也是当下最流行的协议。

资源和其representation是两个独立的概念：一个resource，用户可以索取其json表现形式，也可以索取其xml表现形式 - 尽管这也只是http支持的实现。


在REST in Practice (豆瓣)书中介绍了一种叫做Richardson Maturity Model的Web服务成熟度模型。而上面的这种API属于其第二层HTTP Verbs，RESTful的API属于第三层Hypermedia Controls。相比第二层，第三层的Web服务具有一个很明显的优势，客户端与服务端交互解耦。服务端可以仅仅提供单一的入口，客户端只要依次“遍历”超链接，就可以完成对应的合法业务逻辑。当资源的转换规则发送变化时（如某一页由于历史文章被删除了而没有下一页，又或者某篇文章转储在了其他网站上），客户端不需要作额外的更新升级，只需要升级服务端返回的超链接即可。

作者：季文昊
链接：https://www.zhihu.com/question/28557115/answer/48120528
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。


REST接口要有能力描述它自己，以及接下来可以transfer到哪些状态：what to call, and when
