---
tags:
- notes
- ctf
comments: true
---

### baby_equation

由因式分解： `((a**2 + 1) * (b**2 + 1) - 2 * (a - b) * (a * b - 1)) == 4 * (k + a * b) => ((a+1)*(b-1))**2 == 4*k` ，显然我们可以将 `(a+1)(b-1)` 计算出来，再用 [factordb](https://factordb.com/) 将其分解，获得 a/b 的可能值并求解。

```python title="baby_equation.py"
from Crypto.Util.number import *

# from secret import flag


# l = len(flag)
# m1, m2 = flag[: l // 2], flag[l // 2 :]
# a = bytes_to_long(m1)
# b = bytes_to_long(m2)
k = 0x2227E398FC6FFCF5159863A345DF85BA50D6845F8C06747769FEE78F598E7CB1BCF875FB9E5A69DDD39DA950F21CB49581C3487C29B7C61DA0F584C32EA21CE1EDDA7F09A6E4C3AE3B4C8C12002BB2DFD0951037D3773A216E209900E51C7D78A0066AA9A387B068ACBD4FB3168E915F306BA40
# assert ((a**2 + 1) * (b**2 + 1) - 2 * (a - b) * (a * b - 1)) == 4 * (k + a * b)
# => ((a+1)*(b-1))**2 == 4*k

import math

t = 2 * int(math.isqrt(k))
assert t**2 == 4 * k  # AssertionError

# print(t)
# t== (2**4) * (3**2) * 31 * 61 * 223 * 4013 * 281317 * 4151351 * 339386329 * 370523737 * 5404604441993 * 26798471753993 * 25866088332911027256931479223 * 64889106213996537255229963986303510188999911

factors = (
    [2] * 4
    + [3] * 2
    + [
        31,
        61,
        223,
        4013,
        281317,
        4151351,
        339386329,
        370523737,
        5404604441993,
        26798471753993,
        25866088332911027256931479223,
        64889106213996537255229963986303510188999911,
    ]
)

from itertools import chain, combinations


def powerset(iterable):
    "生成可迭代对象的所有子集"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


xs = set()  # 使用集合来存储结果，避免重复

for subset in powerset(factors):
    product = 1
    for num in subset:
        product *= num
    xs.add(product)

xs = list(xs)  # 将集合转换为列表
xs.sort()  # 对结果进行排序

with open("tmp.txt", "w") as f:
    for x in xs:
        a = x - 1
        b = t // x + 1
        m1 = long_to_bytes(a)
        m2 = long_to_bytes(b)
        flag = "".join(chr(c) for c in (m1 + m2) if 32 <= c < 127)
        if flag.startswith("moectf{"):
            print(flag)
```
### ez_hash

直接爆破即可；提前生成速度更快？

```python title="ez_hash.py"
import hashlib
import itertools
from string import digits, ascii_letters, punctuation

alpha_bet = digits + ascii_letters + punctuation
strlist = itertools.product(digits, repeat=6)

for strl in strlist:
    strl = "2100" + "".join(strl)
    if (
        hashlib.sha256(strl.encode()).hexdigest()
        == "3a5137149f705e4da1bf6742e62c018e3f7a1784ceebcb0030656a2b42f50b6a"
    ):
        print(strl)
        break
```

> [!FLAG]
>
> moectf{2100360168}

