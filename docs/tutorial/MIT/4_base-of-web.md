---
comments: true
date: 2024-06-29
tags:
- MIT
- blog
- note
---
***

> [!SUMMARY]-
>
> 本文介绍了网络基础知识，包括 IP 协议、传输层协议、域名系统、HTTP 协议和现代网络安全。
>
> - **IP 协议：** IPv4 和 IPv6 协议，用于在网络中标识设备。
> - **传输层协议：** TCP 和 UDP 协议，用于在网络中传输数据。
> - **域名系统：** DNS，用于将域名转换为 IP 地址。
> - **HTTP 协议：** 用于在客户端和服务器之间传输网页。
> - **现代网络安全：** HTTPS 协议，用于保护 HTTP 通信；TLS 协议，用于加密和认证通信；CA 证书，用于验证服务器身份。

## IP (Internet Protocol)

> [!WIKI]
>
> The **Internet Protocol** (**IP**) is the [network layer](https://en.wikipedia.org/wiki/Network_layer "Network layer") [communications protocol](https://en.wikipedia.org/wiki/Communications_protocol "Communications protocol") in the [Internet protocol suite](https://en.wikipedia.org/wiki/Internet_protocol_suite "Internet protocol suite") for relaying [datagrams](https://en.wikipedia.org/wiki/Datagram "Datagram") across network boundaries. Its [routing](https://en.wikipedia.org/wiki/Routing "Routing") function enables [internetworking](https://en.wikipedia.org/wiki/Internetworking "Internetworking"), and essentially establishes the [Internet](https://en.wikipedia.org/wiki/Internet "Internet").

### IPv4 (Internet Protocol version 4)

- 由 4 个**段** (octet)组成，每个段 8 位，可以用任何表示 32 位整数的方式表示 IPv4 地址
    - [10.78.18.216](http://10.78.18.216/) = [0xA4E12D8](http://10.78.18.216/) = [172888792](http://10.78.18.216/)
    - 理论上有 232232 个不同的地址，但并非所有都可以使用，有复杂的地址分配机制
    - 2019 年 11 月 25 日，RIPE NCC 宣布 IPv4 地址耗尽

![](attachments/1-4-base%20of%20web.png)

### IPv6 (Internet Protocol version 6)

- 由 8 个段hextet组成，每个段 16 位
    - [2001:da8:e000:731a:ff00:0:0:642d](http://[2001:da8:e000:731a:ff00::642d]/)
    - 理论上有 $2^{128}$ ≈ $3.4×10^{38}$ 个不同的地址
    - 极大地简化了 IPv4 存在的地址分配问题
    - 连续的全 0 段可以省略：[2001:da8:e000:731a:ff00::642d](http://[2001:da8:e000:731a:ff00::642d]/)
    - 也有 IPv4-mapped IPv6 地址：[::ffff:10.78.18.216](http://[::ffff:a4e:12d8]/)
    - [https://test-ipv6.com](https://test-ipv6.com/) 测试你的 IPv6 连接
    - Linux 下有 ping6 命令

### 广域网与局域网

- 广域网Wide Area Network：跨越大范围的网络，如互联网

- 局域网Local Area Network：小范围的网络，如家庭、学校、公司内部的网络

- 一般来说，局域网之间的主机可以互相访问，但其不能直接访问互联网
    - 需要一个**路由器**连接不同层级的网络
- 一台主机可以有多个 IP 地址

    - 例如一个局域网内的主机可能有多个局域网 IP 和公网 IP
    - 一个主机可以有多个网卡，每个网卡可以有多个 IP 地址

### 回环地址

- 回环地址Loopback address：127.0.0.1IPv4 / ::1IPv6 / localhost主机名
    - 用于主机自身的通信，不会发送到网络上

### 网关与子网掩码

- 网关Gateway：将不同网络连接起来的设备
    - 例如连接局域网和互联网的路由器
    - 一般来说，局域网内的主机的网关是路由器的 IP 地址
- 子网Subnet：将一个大的 IP 地址段划分为多个小的 IP 地址段
    - 例如，对于IP地址192.168.1.1，如果子网掩码是255.255.255.0（或者用CIDR表示法写作192.168.1.1/24），这意味着前24位（即192.168.1）是网络地址，剩下的8位（即最后一个1）是主机地址。
    - 子网掩码用于判断两个 IP 地址是否在同一个子网内
- NAT：网络地址转换
    - 用于将局域网内的多个主机共享一个公网 IP 地址
    - 通过修改 IP 数据包的源地址和目的地址来实现

## 传输层协议 TCP 与 UDP

### OSI 七层模型

- 应用层Application layer：浏览器
- 表示层Presentation layer
- 会话层Session layer
- 传输层Transport layer：TCP 和 UDP
- 网络层Network layer：IP
- 数据链路层Data link layer：以太网 / Wi-Fi
- 物理层Physical layer：网卡 / 路由器

![cyrus对OSI总结图片](https://cyrus28214.top/img/TransportLayer.drawio.png)

> 详细可见 [Cyrus' Blog](https://cyrus28214.top/post/303a9aabf405/)，上面的图片就来自于此。

### TCP 与 UDP

- TCP：传输控制协议Transmission Control Protocol：面向连接的协议
    - 通过复杂的握手、确认、重传等机制保证数据的顺序和可靠性
- UDP：用户数据报协议User Datagram Protocol：无连接；"send and forget"
    - 更简单且快速；单向传输，不保证顺序，不保证可靠性

### 端口

- 软件层面的通信端点，与 IP 地址一起构成网络通信的基础
    - IP 地址识别机器，端口号识别软件（服务）
    - TCP 与 UDP 的端口号是分开的，即同一个端口号可以同时用于 TCP 和 UDP
    - 可以设置只监听（**bind**）某个 IP 地址的某个端口号
- 端口号的范围是 0~65535
    - 其中 0~1023 为系统保留端口，一般不用于通用服务
- 一般情况下，不同的软件使用不同的端口号
    - 通过端口号可以区分不同的服务，例如 HTTP 的分配端口是 TCP 80
        - 即 [http://10.78.18.216](http://10.78.18.216/) 就是 [http://10.78.18.216:80](http://10.78.18.216/)
        - 否则需要写明端口号，如 [http://10.78.18.216:39200](http://10.78.18.216:39200/)

## 域名系统与 DNS

### 域名

- 域名Domain Name用于标识互联网上的计算机
    - 由一串用 . 分隔的字符串组成，例如 [example.com](https://example.com/)
    - 最右侧的部分称为**顶级域名**Top-Level Domain：.com .net .org .cn 等
    - 从右至左依次为二级、三级域名等：[www.example.com](https://www.example.com/)
- 如何拥有一个域名？
    - 在**域名注册商**处购买，如阿里云、腾讯云、Cloudflare 等
    - 根据域名的 TLD、长度等因素，价格从几元到几千元不等（每年）
- 拥有一个域名意味着拥有在互联网上的一个身份
    - 域名并不是只能用于网站，还可以用于很多其他用途，如邮箱
    - 可以设置任意多的子域名，如 blog.example.com 等
- 只拥有一个域名是不够的！
    - 还需要有东西可以访问（一个服务器）

> [!DEFINITION ]
>
> DNS（Domain Name System，域名系统）是一个分布式的命名系统，**主要**用于将人类可读的域名（如 www.example.com ）转换为机器可读的IP地址。DNS是互联网的一个关键组件，因为它使得用户可以通过域名而不是IP地址来访问网络资源。

### DNS的工作原理：

1. **域名解析请求**：

    - 当你在浏览器中输入一个网址（例如 www.example.com）时，你的计算机会首先检查本地缓存中是否有该域名的IP地址记录。
    - 如果没有找到，计算机会向你的网络配置中指定的DNS服务器发送一个DNS查询请求。

2. **递归查询**：
    - 你的DNS服务器（通常是你的互联网服务提供商提供的）会尝试从其缓存中找到答案。如果它没有找到，它将代表你的计算机进行递归查询。
    - 这意味着它会与其他DNS服务器通信，直到找到包含所需信息的DNS服务器。

3. **DNS记录**：
    - DNS服务器之间通过查询不同的DNS记录来找到答案。最常见的记录类型包括：
        - A记录：将域名映射到IPv4地址。
        - AAAA记录：将域名映射到IPv6地址。
        - CNAME记录：将一个域名映射到另一个域名（常用于子域名）。
        - MX记录：指定接收电子邮件的邮件服务器。
        - NS记录：指定负责一个域的DNS服务器。
        - TXT记录：用于各种验证和配置，如SPF记录。

4. **响应查询**：
    - 一旦找到答案，DNS服务器会将IP地址返回给你的计算机。
    - 你的计算机将这个IP地址存储在本地缓存中，以便在将来的查询中使用。

5. **浏览器连接**：
    - 得到IP地址后，你的浏览器可以使用这个地址来建立与目标网站的连接。

## 应用层协议 HTTP

### HTTP 协议

- 超文本传输协议HyperText Transfer Protocol
- 是基于文本的协议，用于在客户端和服务器之间传输网页

### 客户端 - 服务器（C/S）架构

- 任何一台计算机都可以作为服务器
- 发起连接的节点是客户端，接受连接的节点是服务器
    - 在这个过程中，客户端和服务器是对等的
    - 服务器不能主动发起连接，只能等待客户端的连接
- 服务器不一定只能处理 HTTP 请求
    - 如 DNS 服务器
- 服务器可以同时处理多个客户端的连接
    - 客户端在本地选取一个空闲的高端口号，连接到服务器的 80 端口
    - client:49152 <-> server:80
- DoS 攻击：通过大量的无效请求占用服务器资源，使得合法请求无法被处理
    - DDoS 攻击：分布式拒绝服务攻击

### URL：统一资源定位符

[![](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-fall-ckc/lec6/lec6/URI_syntax_diagram.svg.avif)](https://commons.wikimedia.org/wiki/File:URI_syntax_diagram.svg)

- URI（统一资源标识符）的一种，用于定位互联网上的资源
    - 格式如上图，重要性由左至右递减

```url
https://www.example.com:443/path/to/resource?query=1#frag
```

- 协议：https
- 主机：[www.example.com](http://www.example.com/)
- 端口：443
- 路径：/path/to/resource
- 查询：query=1
- 片段：frag
- URL 中只能包含 ASCII 字符，由**百分号编码**定义的字符集
    - 例如空格编码为 %20，或有些情况下编码为 +
    - [https://www.google.com/search?q=what+is+a+url%3F](https://www.google.com/search?q=what+is+a+url%3F)
    - [Percent-encoding - MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Glossary/Percent-encoding)

### 请求方法

- [HTTP 请求方法 - MDN Web Docs](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods)

## TLS 与现代网络安全

### HTTP 与 HTTPS

- HTTP 的**一切**都是明文传输
    - 两个节点间的任何一个中间节点都可以窃听并干预/修改通信内容
- HTTPS：HTTP over TLS
    - 传输层安全协议Transport Layer Security，旧称安全套接层Secure Sockets Layer
    - 不只是 HTTP，任何应用层协议都可以透明地使用 TLS
    - 通过加密、认证和完整性保护来保护通信内容
    - [The Illustrated TLS Connection: Every Byte Explained](https://tls12.xargs.org/)

### 通信安全

#### 对称加密

- 对称加密算法：如 AES、ChaCha20 等
    - Alice 和 Bob 如何确保他们的消息是安全的？
    - Alice 用密钥 K 加密消息 M，得到 C，发送给 Bob
    - Bob 用密钥 K 解密 C，得到 M
    - 但两人如何协商密钥 K？
        - 通过线下见面交换 K？
        - 随 C 一起发送 K？
            - 任何拿到 K 的人都可以用其解密 C

#### 非对称加密

##### 现代密码学：Diffie-Hellman 密钥交换

- 1976 年发明，公钥密码学的基础
- 基于数学假设：离散对数问题（DLP）是困难的
- Alice 和 Bob 如何确保他们的通信能够保密？
    - 设 Alice 的秘密值 𝑎a，Bob 的秘密值 𝑏b
    - 两人事前约定两个公开参数 𝑝p 和 𝑔g，所有运算都在模 𝑝p 群上进行
    - Alice 计算 𝑔𝑎ga，Bob 计算 𝑔𝑏gb
    - 两人通过公开信道交换 𝑔𝑎ga 和 𝑔𝑏gb，在这之间可能存在窃听者 Eve
    - Alice 计算 (𝑔𝑏)𝑎(gb)a，Bob 计算 (𝑔𝑎)𝑏(ga)b
    - Eve 可能窃听到 𝑔𝑎ga 和 𝑔𝑏gb，她也知道 𝑝p 和 𝑔g，如何求解 𝑔𝑎𝑏gab？
        - 如果 𝑝p 和 𝑔g 很大？

##### RSA 与 ECC

- RSA 公钥密码学
    - 基于数学假设：大整数的因数分解是困难的
    - 有两个很大的质数 𝑝p 和 𝑞q，计算 𝑝𝑞pq 是非常容易的
    - 但给定 𝑝𝑞pq，要分解出 𝑝p 和 𝑞q 是困难的
- ECC 椭圆曲线密码学
    - 基于椭圆曲线上的离散对数问题（ECDLP），类似 Diffie-Hellman 密钥交换
    - 𝑔g 是椭圆曲线上的一个公开点，𝑎a 是秘密值，计算 𝑎⋅𝑔a⋅g 是容易的
    - 但给定 g 和 a⋅g，要找到 𝑎a 是困难的
    - 相比 RSA，ECC 能够在更短的密钥长度下提供相同的安全性
- 后量子密码学：基于格、哈希函数、代码等构建的密码学
    - [https://eprint.iacr.org/2024/555](https://eprint.iacr.org/2024/555)
    - AES 等对称加密算法不受量子计算机的影响

#### 中间人攻击

- Diffie-Hellman 密钥交换仍然不能解决中间人攻击

### TLS 证书与 CA

- 证书：数字签名的公钥
    - 由一个双方都相信的第三者 Charlie 签发，Charlie 就是 CA
    - Charlie 通过其他安全手段验证 Bob 的身份，签发 Bob 的证书
        - 相当于 Charlie 为 Bob 的身份背书
    - Bob 在交换密钥的同时发送自己的证书，以证明自己是真的 Bob
    - 如果 Alice 信任 Charlie，那么她也会信任 Bob 的证书进而信任 Bob
    - Eve 无法伪造 Bob 的证书，因为她无法向 Charlie 证明自己是 Bob
- 如何确保 CA 是可信的？
    - 由操作系统或浏览器内置的 CA 列表：**根证书**，[约 150 个](https://ccadb.my.salesforce-sites.com/mozilla/IncludedCACertificateReport)
    - 根证书是自签名的且被信任，其签发一系列中间证书，中间证书签发终端证书
    - 不守规矩的 CA 会被吊销证书，不再被信任（WoSign 违规事件，2016）
    - [证书透明度](https://developer.mozilla.org/zh-CN/docs/Web/Security/Certificate_Transparency)：公开 CA 签发的证书，防止 CA 恶意签发证书

### mTLS

- 一般来说，服务器需要向客户端证明自己
- 在有些情况下，客户端也需要向服务器证明自己
    - 例如服务器需要验证客户端是否有权限访问某些资源
- mTLS：Mutual TLS
    - 客户端和服务器都需要向对方提供证书
    - 相互验证对方的证书
    - 相比于传统的帐密验证，mTLS 更加安全，但设置也更复杂

## 参考资料

- [「实用技能拾遗」网络/网站基础知识概述](https://slides.tonycrane.cc/PracticalSkillsTutorial/2023-fall-ckc/lec6/#/)
- [Web机制](https://developer.mozilla.org/zh-CN/docs/Learn/Common_questions/Web_mechanics)
- [互联网是如何工作的](https://developer.mozilla.org/zh-CN/docs/Learn/Common_questions/Web_mechanics/How_does_the_Internet_work)