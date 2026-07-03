---
comments: true
date: 2024-06-28
tags:
- begin
---

***

了解 URL，可以帮助我们包括但不限于：便于访问资源；更好地获取资源；不容易被链接欺骗……尤其是对于[语义URL](https://developer.mozilla.org/zh-CN/docs/Learn/Common_questions/Web_mechanics/What_is_a_URL#%E8%AF%AD%E4%B9%89_url) 。

<!-- more -->

> [!attention]+
>
> - 文章提到的演示界面/链接均可访问，如有不当，请[联系我](../../connect_me.md)删除；
> - 本文面向完全不懂计算机知识的人群，专业严谨的介绍可见 [MDN web docs](https://developer.mozilla.org/zh-CN/docs/Learn_web_development/Howto/Web_mechanics/What_is_a_URL)；同时很推荐在其中了解更多的网络的基础知识。

## 基本介绍

> [!tip]- 什么是 URL？
>
> 我认为这种概念性内容通过搜索、询问 LLM 比询问任何一个人都更加直接且效果好。

URL（Uniform Resource Locator，统一资源定位符）是一个用于定位互联网上资源的地址。它是Web浏览器需要访问网站或文件时使用的地址。URL可以指向网页、图片、视频、文档等各种类型的资源。

一个典型的URL包括以下几个部分：

- **协议**：定义了客户端应该使用哪种协议来访问资源，如HTTP（Hypertext Transfer Protocol，超文本传输协议）、HTTPS（HTTP Secure，安全的超文本传输协议）、FTP（File Transfer Protocol，文件传输协议）等。
- **域名**：标识了资源所在的网站或服务器，例如 `www.example.com`。
- **路径**：指明了资源在服务器上的具体位置，例如 `/pages/home.html`。
- **查询参数**：提供了额外的信息，通常用于数据库查询或对网页内容的动态请求，例如 `?user=name&pass=password`。
- **片段标识符**：用于直接定位网页中的某个位置，通常用于锚点链接，例如 `#section2`。

例如，一个完整的URL可能看起来像这样：

```url
https://www.example.com/pages/home.html?user=name&pass=password#section2
```

- `https` 是协议，表示这是一个安全的超文本传输协议。
- `www.example.com` 是域名，指向特定服务器。
- `/pages/home.html` 是路径，指向服务器上特定文件。
- `?user=name&pass=password` 是查询参数，可能用于身份验证。
- `#section2` 是片段标识符，用于直接跳转到网页内的特定部分。

## 了解它有什么用？

### 访问资源减少限制

在别人的电脑上，我想要看我自己[博客](https://darstib.github.io/blog/)上的一些资源（或者一些小众但常用的网页，~~比如你的之后可能经常需要看的实验指导等等~~；又或者是想要切换一个搜索引擎）怎么办？别人电脑上肯定不会存访问我博客的链接，使用搜索引擎也不见得搜得到[^1]；但是其实短链接是很好记住的：

[^1]: 基于 github page 部署的网页并没有备案，百度等搜索引擎是不会收录的；流量低、访问数少也会导致不会被搜索引擎爬取。

```url
https://darstib.github.io/blog/
```

浏览器会一般自动补充个开头的协议（默认使用 `https`），一个域名 darstib.github.io，访问其中的 blog，也很快的。

### 更好地获取资源

#### 域名

假设我们（通过搜索/别人推荐）发现了一个网页，他展示的功能很强大（下面是一个计算行列式特征值和特征向量的一个演示）：

```url
https://www.wolframalpha.com/input?i=eigenvalues+%7B%7B0%2C2%2C1%7D%2C%7B-2%2C0%2C3%7D%2C%7B-1%2C-3%2C0%7D%7D
```

![](attachments/What%20Url%20can%20do.png)

我想看看这个网站有没有更好的功能：比如计算行列式的值、幂；甚至能不能计算微积分来**检验我平时作业的正确性**（无不良引导，请正确使用）。

那我们直接把后面的直接删掉（其实看看删除部分和黄色框内的是一样的，对应了 url 编码罢了）只留必要部分：

```url
https://www.wolframalpha.com/
```

#### 子域名

```url
https://note.tonycrane.cc/
```

熟悉 url 的话就能够看到前面的子域名 `note` ，这也对应了 **笔记** 这一字样；那么很可能原域名

```url
https://tonycrane.cc/
```

也是可访问的，而且可以看到大佬公开的更多资源。

> [!WARNING]
>
> 但是切记，掌握了能力不可以用于非法行为，请控制程度，不要到窃取信息、侵犯隐私的地步。

### 不容易被链接欺骗

#### 例 1

一个很愚蠢但是很经典的例子，你看到了一段文字，写的是：

```txt
其实高考出分前还可以做下面这些措施减少失分！
https://zhidao.baidu.com/question/150256286.html
```

先不说这句话假不假吧，你看这个 `zhidao.baidu.com` ，猜也是“百度知道”，真能这么公开能放百度上去？`question` 猜测是别人提问做出的回答，能在这里回答这种问题真是见鬼了。~~愿意相信的点开看看也无妨~~

#### 例 2

再举一个例子：

<div style="text-align: center;"><img src="https://raw.githubusercontent.com/darstib/public_imgs/utool/tuchuang/1739758366531What Url can do-2.png" alt="img" style="width: 30%;"><p></p></div>

`.edu.cn` 是中国教育相关网站的通用顶级域名。这个域名通常用于中国的教育机构、大学、以及其他与教育相关的组织。你说官方查成绩，可能可信吧；但是 **whu** ，大家自己搜搜是哪个吧😁；“虚假成绩查询网站” 是 **hust** 🤣。
