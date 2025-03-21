---
tags:
- notes
- ctf
comments: true
---

## 引入

> 首先允许我使用明文和密文来对应编码前后的信息；姑且将其看作密钥公开的对称加密吧。

一直以来，都把 base 编码/解码当作理所应当的事情；充其量也就是了解到：

- base 编码是将明文以 ASCII 的形式转变为二进制流；
- base 16/32/64 等以 4/5/6 位二进制数去进行截断，之后映射到对应的字符即可。

但是问题来了，base36/52 等等呢？它们是如何工作的？

## 实战

引发这个思考来自于 zjuctf2024 的 “锅里捞面” 题。这道题前面获取密文和提示都较为复杂，具体见 `ZJUCTF2024 #MISC` 题解。

我们得到两部分信息：

- `AYICIKQXHR320E7CHW4Y84ZGM954UG061H9QV9X2360TJJ37H9ABL42ABJH5BB`
- `BASE36ENCODETABLE:ZJUCTF24ABDEGHIKLMNOPQRSVWXY01356789`

也就说我们要使用自定义的 base36 来解码上面的内容。

显然，明文空间：`ZJUCTF24ABDEGHIKLMNOPQRSVWXY01356789` 。

起初，我的想法是：$log_2 36 < 6$ 所以转 6 位二进制，随后每 8 位截断；但是自然是错了。

## 学习

base 是进制，base36 代表的应该是 36 进制，只不过用对应字符来表示；就像 16 进制一样，字母表示的也是数字。

那么就很简单了，所谓的 base 编码不过是进制转换，我们做的，不过是 36 进制转 256 进制（ASCII）；又 long_to_bytes 其实做的就是 10 进制转 256 进制，所以有：

```python title="self_base.py"
base = 36
custom_base = "ZJUCTF24ABDEGHIKLMNOPQRSVWXY01356789"

cipher_str = "AYICIKQXHR320E7CHW4Y84ZGM954UG061H9QV9X2360TJJ37H9ABL42ABJH5BB"

assert len(custom_base) == base

# print("len(cipher) =", len(cipher))
cipher_int = 0
for c in cipher_str:
    cipher_int = cipher_int * base + custom_base.index(c)

print("cipher_int =", hex(cipher_int))

from Crypto.Util.number import long_to_bytes

print(long_to_bytes(cipher_int))
```

> [!FLAG]
>
> ZJUCTF{A_13G3nd4Ry_4h0uR-T3l36r4Phls7XD}