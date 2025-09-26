---
tags:
- notes
- ctf
comments: true
---

## Mycode

### 附件

```python
import numpy as np

def substitute(state, sub_box):
    return [sub_box[b & 0xF] | (sub_box[(b >> 4) & 0xF] << 4) for b in state]

def generate_round_keys(base_key, rounds):
    round_keys = []
    temp_key = base_key
    for _ in range(rounds):
        round_keys.append(temp_key & 0xFFFFFFFF)
        temp_key ^= ((temp_key << 1) & 0xFFFFFFFF) | ((temp_key >> 31) & 0x1)
    return round_keys

def process_state(base_key, state, rounds, encrypt):
    sub_box = [0x9, 0x4, 0xA, 0xB, 0xD, 0x1, 0x8, 0x5, 0x6, 0x2, 0x0, 0x3, 0xC, 0xE, 0xF, 0x7]
    inv_sub_box = [0xA, 0x5, 0x9, 0xB, 0x1, 0x7, 0x8, 0xF, 0x6, 0x0, 0x2, 0x3, 0xC, 0x4, 0xD, 0xE]

    round_keys = generate_round_keys(base_key, rounds)

    if encrypt:
        for round in range(rounds):
            state = substitute(state, sub_box)
            state = [s ^ ((round_keys[round] >> (i * 8)) & 0xFF) for i, s in enumerate(state)]
    else:
        for round in range(rounds - 1, -1, -1):
            state = [s ^ ((round_keys[round] >> (i * 8)) & 0xFF) for i, s in enumerate(state)]
            state = substitute(state, inv_sub_box)

    return state

def encrypt(plaintext, key, rounds=10):
    length = len(plaintext)
    padded_length = length if length % 4 == 0 else length + (4 - (length % 4))
    plaintext += b'\x00' * (padded_length - length)

    ciphertext = bytearray(padded_length)
    for i in range(0, padded_length, 4):
        state = list(plaintext[i:i+4])
        state = process_state(key, state, rounds, True)
        ciphertext[i:i+4] = state

    return ciphertext

def decrypt(ciphertext, key, rounds=10):
    length = len(ciphertext)
    plaintext = bytearray(length)
    for i in range(0, length, 4):
        state = list(ciphertext[i:i+4])
        state = process_state(key, state, rounds, False)
        plaintext[i:i+4] = state

    return plaintext.rstrip(b'\x00')

def main():
    plaintext = b"DASCTF{******}"
    # key = 0xECB... # 4 bytes
    ciphertext = encrypt(plaintext, key)
    print("Ciphertext:", "".join(f"{b:02X}" for b in ciphertext))


if __name__ == "__main__":
    main()
# Ciphertext: A6B343D2C6BE1B268C3EA4744E3AA9914E29A0789F299022820299248C23D678442A902B4C24A8784A3EA401
```

### 题解

显然，密钥一部分都告诉我们了，穷举 Key 爆破：

```python
ciphertext = "A6B343D2C6BE1B268C3EA4744E3AA9914E29A0789F299022820299248C23D678442A902B4C24A8784A3EA401"
known_key = "ECB"
for c1 in "0123456789ABCDEF":
    for c2 in "0123456789ABCDEF":
        for c3 in "0123456789ABCDEF":
            for c4 in "0123456789ABCDEF":
                for c5 in "0123456789ABCDEF":
                    key = int(
                        (known_key + c1 + c2 + c3 + c4 + c5).encode().hex(), base=16
                    )
                    print(
                        "key:",
                        key,
                        type(key),
                    )
                    pt = decrypt(ciphertext.encode(), key, rounds=10)
                    try:
                        print(pt)
                        if b"DAS" in pt:
                            exit()
                    except error as e:
                        print(e)
```

当然，上面那样写比较丑陋，我们可以：

```python
from itertools import product
ciphertext = "A6B343D2C6BE1B268C3EA4744E3AA9914E29A0789F299022820299248C23D678442A902B4C24A8784A3EA401"
known_key = "ECB"
hex_chars = "0123456789ABCDEF"
for c1, c2, c3, c4, c5 in product(hex_chars, repeat=5):
    key = int((known_key + c1 + c2 + c3 + c4 + c5).encode().hex(), base=16)
    pt = decrypt(ciphertext.encode(), key, rounds=10)
    print(pt)
    if b"DAS" in pt:
        exit()
```

爆破时间有点久，`Key = 0xecb4f678`

> [!FLAG]
>
> DASCTF{6ef4d8e1-845a-4e3c-a4e1-a15e5530a0f4}

## DlcgH_r

### 附件

```python
from Crypto.Util.number import *
from gmpy2 import *

flag = b"DASCTF{******}"


def iterate_function(seed, coeff_a, coeff_b, prime_modulus):
    return (coeff_a * seed + coeff_b) % prime_modulus


def iterate_multiple_times(seed, num_iterations, coeff_a, coeff_b, prime_modulus):
    for _ in range(num_iterations):
        seed = iterate_function(seed, coeff_a, coeff_b, prime_modulus)
    return seed


p = getPrime(600)
a = getPrime(512)
b = getPrime(512)
s = getPrime(512)
k = getPrime(512)
t = getPrime(512)

A = iterate_multiple_times(s, k, a, b, p)
B = iterate_multiple_times(s, t, a, b, p)
# A B seed 相同，不同的只是轮数
print("p =", p)
print("a =", a)
print("b =", b)
print("s =", s)
print("A =", A)
print("B =", B)
# 只有 k t 没告诉我们
secret1 = iterate_multiple_times(A, k, a, b, p)
secret2 = iterate_multiple_times(B, t, a, b, p)

assert secret1 == secret2
"""
p = 2565258348684709722726260231955260453241716968378483821594041597297293609376806025180965681289016169408781752953380586044352169083397987333072306444539318806255242559916564022662479
a = 7703427441632069990122897903141278700284019287330080801753208940444135129072547305259960648105321270085533531118395452229965873504176368162947864923497711
b = 8477265953761650860710068507342719089504862957398782381045770264963932696457722724393775545810962476516315838411812248360284564925846788951219272632661157
s = 9228773209718156231041982890745928246648483643042884535935071957475932603607283209094294685862893340598940862096657878372229519375655468524041406914666867
A = 434251860827782638796736001849473241231781620594954088572922898040098881748337513244415553659525671751903798527967205418513869125476445927127124010452649344318178999731385274553080
B = 434251860827782638796736001849473241231781620594954088572922898040098881748337513244415553659525671751903798527967205418513869125476445927127124010452649344318178999731385274553080
"""

p2 = next_prime(secret1)
q2 = getPrime(600)
n2 = p2 * q2
e = 4
m = bytes_to_long(flag)
c = pow(m, e, n2)
print("n2 =", n2)
print("c =", c)

"""
n2 = 3241139665583501598296135149075754735041636843305130049654913708275571916563715101898946962033698805416493133339619007016676895968314902474922279948997540924678346952667095320094789476561995339618782687993966133770687551933070478999383821269223854568552819152909266096733330218505088222661907600152055916956562332379930822529724151378274932991887183193175206749
c = 1131281812215293796960536920068009435705926803182047772347743960804329656316689664084120353862091370978145286943689311985878028828902275260824388998300548644880722651153603738691769179255824425771260974588160589473958033612303767050773921373389315920529311000160530833707622310013322631917184737227893101365726934901652170763292132835433158093074003616578836411
"""
```

### 题解

题目提示说密钥交换，除了最后 secret 是一样的，没看出来交换了什么。

比赛时应该是非预期解？发现 `A==B` `secret1==secret2` ，猜测 k t 在 lcg 中模其周期后相同，尝试爆破：

```python title="find_k"
p = 2565258348684709722726260231955260453241716968378483821594041597297293609376806025180965681289016169408781752953380586044352169083397987333072306444539318806255242559916564022662479
a = 7703427441632069990122897903141278700284019287330080801753208940444135129072547305259960648105321270085533531118395452229965873504176368162947864923497711
b = 8477265953761650860710068507342719089504862957398782381045770264963932696457722724393775545810962476516315838411812248360284564925846788951219272632661157
s = 9228773209718156231041982890745928246648483643042884535935071957475932603607283209094294685862893340598940862096657878372229519375655468524041406914666867
A = 434251860827782638796736001849473241231781620594954088572922898040098881748337513244415553659525671751903798527967205418513869125476445927127124010452649344318178999731385274553080
B = 434251860827782638796736001849473241231781620594954088572922898040098881748337513244415553659525671751903798527967205418513869125476445927127124010452649344318178999731385274553080


def iterate_function(seed, coeff_a, coeff_b, prime_modulus):
    return (coeff_a * seed + coeff_b) % prime_modulus


def iterate_multiple_times(seed, num_iterations, coeff_a, coeff_b, prime_modulus):
    for _ in range(num_iterations):
        seed = iterate_function(seed, coeff_a, coeff_b, prime_modulus)
    return seed


si = s
with open("i.out", "a") as i_out:
    for i in range(p):
        si = iterate_function(si, a, b, p)
        if si == A:
            print(si)
            print(f"{i+1} is right")
            break
        if i % 1000000 == 0:
            print(f"testing {i} times")
# 12345
```

果真发现了 `k = 12345`，进而分解了 n；

```python
secret2 = iterate_multiple_times(A, 12345, a, b, p)
```

但是当时卡在 e = 4 ，不会求解；忘记了 sage 中内置了分解方法，rabin 算法也不记得了手动实现，遗憾未解；甚至忘记了可以用多项式求解根……

当然，如果不猜 k ，咋办？

由于 lcg 的生成固定性，在第一次有：

$a(\dots a(a*s_{0}+b)+\dots)+b = A = s_{0}*a^k + b(a^{k-1}+\dots+a+1) = s_{0}* a^k + \frac{b}{a-1}(a^k-1)$，不难发现 k=0 时依旧成立，故有 $s_{k}=\left( s_{0}+ \frac{b}{a-1} \right)*a^k- \frac{b}{a-1}$ 。

未知量只有 $a^k$ 了，解方程有 $k = \frac{A(a-1)+b}{(a-1)s_{0}+b} \pmod{p}$

```python
k = (A*(a-1)+b)/((a-1)*s+b)%p
assert (s*k+(k-1)/(a-1)*b)%p == A
secret1 = (A*k+(k-1)/(a-1)*b)%p
```

输出后可以发现，这里的 k 并不等于 12345，但是它们产生的 secret 是一致的。

```python
from sage.all import *
from Crypto.Util.number import long_to_bytes
from gmpy2 import *
e = 4
n2 = 3241139665583501598296135149075754735041636843305130049654913708275571916563715101898946962033698805416493133339619007016676895968314902474922279948997540924678346952667095320094789476561995339618782687993966133770687551933070478999383821269223854568552819152909266096733330218505088222661907600152055916956562332379930822529724151378274932991887183193175206749
c = 1131281812215293796960536920068009435705926803182047772347743960804329656316689664084120353862091370978145286943689311985878028828902275260824388998300548644880722651153603738691769179255824425771260974588160589473958033612303767050773921373389315920529311000160530833707622310013322631917184737227893101365726934901652170763292132835433158093074003616578836411
secret = 1472490340321845700492870656866629756386520746748019952980831685935628618084832981576756885932019702470337632472478610542460495595381421112792242654382213433012352298291319463142353
p = next_prime(secret)
assert n2 % p == 0
q = n2//p
assert q * p == n2

x_s = Mod(c, p).nth_root(e, all=True)
y_s = Mod(c, q).nth_root(e, all=True)
for x in x_s:
    for y in y_s:
        m = crt([int(x), int(y)], [p, q])
        print(long_to_bytes(m)) 
        # b'DASCTF{450a759e-1c7d-4b97-a9de-78b31eff42a9}'
```

> [!FLAG]
>
> DASCTF{450a759e-1c7d-4b97-a9de-78b31eff42a9}

## APT

[第七届浙江省大学生网络与信息安全竞赛决赛 Wirteup By 0RAYS](https://mp.weixin.qq.com/s/eQlZeeUigFIF-xQCTrs88Q#:~:text=4b97%2Da9de%2D78b31eff42a9%7D-,APT,-%F0%9F%92%A9)