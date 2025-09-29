---
comments: true
dg-publish: true
tags:
- DMPT
- notes
---

> In this note, we discuss a very nice and important application of modular arithmetic: the _RSA public-key cryptosystem_ , named after its inventors Ronald Rivest, Adi Shamir and Leonard Adleman.

嗯……这个 RSA 我在尝试 CTF 解题时看过 [cyrus 的讲解](https://cyrus28214.top/post/b161510a6684/?highlight=rsa) ，有兴趣自行观看；同时可以学习一下其 python 实现。

下面是 RSA 的基本过程

1. **密钥生成**：
    - **选择两个大质数** p 和 q。
    - **计算模数** n：n=p×q，这将是公钥和私钥的一部分。
    - **计算欧拉函数** ϕ(n)：ϕ(n)=(p−1)(q−1)。
    - **选择加密指数** e：选择一个与 ϕ(n) 互质的整数 e，通常选择一个较小的质数。
    - **计算解密指数** d：找到一个整数 d，使得 e×d≡1modϕ(n)。这里 d 是 e 关于模 ϕ(n) 的乘法逆元，即 $de \equiv 1 (mod\quad \phi (n))$ 
    - **公钥** 为(e,n)，**私钥** 为 (d,n)。
2. **加密过程**：
    - 对于要加密的消息 m（一个小于 n 的整数），计算密文 c：$c=m^{e}\quad mod\quad n$。
3. **解密过程**：
    - 使用私钥 (d,n) 来解密密文 c，计算原始消息 m：$m=c^{d}\quad mod\quad n$。

