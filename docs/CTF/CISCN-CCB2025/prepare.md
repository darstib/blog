## CISCN2024

### rasnd

```python title="task.py"
from Crypto.Util.number import getPrime, bytes_to_long
from random import randint
import os

FLAG = os.getenv("FLAG").encode()
flag1 = FLAG[:15]
flag2 = FLAG[15:]

def crypto1():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 0x10001
    x1=randint(0,2**11)
    y1=randint(0,2**114)
    x2=randint(0,2**11)
    y2=randint(0,2**514)
    hint1=x1*p+y1*q-0x114
    hint2=x2*p+y2*q-0x514
    c = pow(bytes_to_long(flag1), e, n)
    print(n)
    print(c)
    print(hint1)
    print(hint2)


def crypto2():
    p = getPrime(1024)
    q = getPrime(1024)
    n = p * q
    e = 0x10001
    hint = pow(514*p - 114*q, n - p - q, n)
    c = pow(bytes_to_long(flag2),e,n)
    print(n)
    print(c)
    print(hint)
print("==================================================================")
crypto1()
print("==================================================================")
crypto2()
print("==================================================================")

```

#### part1

数学推导如下：

```python
h1 = hint0 + 0x114
h2 = hint1 + 0x514
# h1x2 - h2x1 = (xxxx) * q
# n == p * q
xxxq = h1*x2 - h2*x1
q = gcd(xxxq, n)
```

exp:

```python title="exp1.py"
h1 = hint0 + 0x114
h2 = hint1 + 0x514
# h1x2 - h2x1 = (xxxx) * q
bre_flag = 0
for x1 in range(1, 2**11):
    if bre_flag == 1:
        break
    for x2 in range(1, 2**11):
        xxxq = (h1*x2 - h2*x1)
        q1 = gcd(n1, xxxq)
        if q1 != 1:
            print(q1) #             176718842918934403373560735237267783646560110375877372435516397884541555216499772644767143216833396058696600750601156650487749554052769488220609295149169894128224967370254001256208386281086004900940249917106345608038996889456200505150003465726090464499880867387632371065250812358424130719972586001655587931293
            bre_flag = 1
            break
p1 = n1 // q1
assert n1 == p1 * q1
phi1 = (p1-1)*(q1-1)
d1 = inverse_mod(0x10001, phi1)
m1 = pow(c1,d1,n1)
bytes.fromhex(hex(m1)[2:]) # b'flag{f9599e4a-61c5-'
```

#### part2

```python title="exp2"
"""
p = var('p')
hint2_ = inverse_mod(hint2, n2)
f = (114*n2 - p * (514*p - hint2_))
# print(f)
for root in f.roots():
    if int(n2) % int(abs(root[0])) == 0:
        print(root)
"""

p2 = 176882095226432306034448650965445366491715088358617642237883735556959553875011707530467882588661269807611852240357473621012337185916620965398885616805056733138984533627355664213597543853939291550947519740076465163143147599877105409063109532832084220155702706914715809698106501189492449517168532756045900245323

q2 = n2 // p2
assert n2 == p2 * q2
phi2 = (p2 - 1) * (q2 - 1)
d2 = int(pow(e, -1, phi2))
m = pow(c2, d2, int(n2))
print(long_to_bytes(int(m)))
# b'48c5-ada6-558ae883ace2}'
```

> [!FLAG]
>
> flag{f9599e4a-61c5-48c5-ada6-558ae883ace2}

### fffffhash

> [!quote] 
>
> - https://ctf-wiki.org/crypto/hash/fnv/ 
> - https://blog.maple3142.net/2023/09/03/downunderctf-2023-writeups/#fnv
> - https://viol1t.com/2024/12/15/2024%E5%B9%B4CISCN-%E9%95%BF%E5%9F%8E%E6%9D%AF%E5%88%9D%E8%B5%9Bwp/#fffffhash
> - https://github.com/DownUnderCTF/Challenges_2023_Public/blob/main/crypto/fnv/solve/solution_joseph_LLL.sage

```python title="fffffhash.py"
import os
from Crypto.Util.number import *
def giaogiao(hex_string):
    base_num = 0x6c62272e07bb014262b821756295c58d
    x = 0x0000000001000000000000000000013b
    MOD = 2**128
    for i in hex_string:
        base_num = (base_num * x) & (MOD - 1) 
        base_num ^= i
    return base_num


giao=201431453607244229943761366749810895688

print("1geiwoligiaogiao")
hex_string = int(input(),16)
s = long_to_bytes(hex_string)

if giaogiao(s) == giao:
    print("flag{fNV_1_h4sh_c0llision_succ3ss}")
    # print(os.getenv('FLAG'))
else:
    print("error")
```



> [maple 师傅](https://blog.maple3142.net/2023/09/03/downunderctf-2023-writeups/#fnv) 给出了一个更加原始的解题思路：

由于异或的可逆性，从 base_num 到 giao 和从 giao 爆破到 base_num 的难度是一样的，如果是直接爆破非常困难；但是如果能够获得正中的值，时间复杂度将大大降低；大胆假设 hex_string 是偶数字节，逐渐尝试得到：

```c++ title="exp1"
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <algorithm>

__attribute__((always_inline)) inline void fnv_forward(uint64_t *s, uint8_t c) {
    *s *= 0x00000100000001b3;
    *s ^= c;
}
__attribute__((always_inline)) inline void fnv_backward(uint64_t *s,
                                                        uint8_t c) {
    *s ^= c;
    *s *= 0xce965057aff6957b;
}
int main() {
    const size_t tbl_size = (1L << 32) * sizeof(uint64_t);

    uint64_t *tbl = (uint64_t *)malloc(tbl_size);
    uint64_t *tblend = tbl + (1L << 32);

    uint64_t start = 0xcbf29ce484222325;
    uint64_t end = 0x1337133713371337;
    uint64_t *tblptr = tbl;
    for (uint8_t a = 0; a < 256; a++) {
        printf("a: %d\n", a);
        for (uint8_t b = 0; b < 256; b++) {
            for (uint8_t c = 0; c < 256; c++) {
                for (uint8_t d = 0; d < 256; d++) {
                    uint64_t s = start;
                    fnv_forward(&s, a);
                    fnv_forward(&s, b);
                    fnv_forward(&s, c);
                    fnv_forward(&s, d);
                    *tblptr = s;
                    tblptr++;
                    if (d == 255)
                        break;
                }
                if (c == 255)
                    break;
            }
            if (b == 255)
                break;
        }
        if (a == 255)
            break;
    }
    printf("done part 1\n");

    std::sort(tbl, tblend);
    printf("done sort\n");

    for (uint8_t a = 0; a < 256; a++) {
        printf("a: %d\n", a);
        for (uint8_t b = 0; b < 256; b++) {
            for (uint8_t c = 0; c < 256; c++) {
                for (uint8_t d = 0; d < 256; d++) {
                    uint64_t s = end;
                    fnv_backward(&s, a);
                    fnv_backward(&s, b);
                    fnv_backward(&s, c);
                    fnv_backward(&s, d);
                    uint64_t *f = std::lower_bound(tbl, tblend, s);
                    if (f != tblend && *f == s) {
                        printf("found %lx\n", s);
                        printf("a: %d, b: %d, c: %d, d: %d\n", a, b, c, d);
                    }
                    if (d == 255)
                        break;
                }
                if (c == 255)
                    break;
            }
            if (b == 255)
                break;
        }
        if (a == 255)
            break;
    }
    return 0;
}
```

获得中间 hex_string 即前半段 hex_string 为: `190611621811271486914581235098607354759`

接着从两遍往中间爆破即可：

```cpp title="exp2"
#include <fcntl.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <algorithm>

__attribute__((always_inline)) inline void fnv_forward(uint64_t *s, uint8_t c) {
    *s *= 0x00000100000001b3;
    *s ^= c;
}
__attribute__((always_inline)) inline void fnv_backward(uint64_t *s,
                                                        uint8_t c) {
    *s ^= c;
    *s *= 0xce965057aff6957b;
}
int main() {
    uint64_t start = 0x6C62272E07BB014262B821756295C58D;
    uint64_t end = 0x978a496d524f0ee5b806e89cf4c1ab48;
    uint64_t target = 0x8f6676887165995bdbefd1ca0d430387;
    for (uint8_t a = 0; a < 256; a++) {
        printf("a: %d\n", a);
        for (uint8_t b = 0; b < 256; b++) {
            for (uint8_t c = 0; c < 256; c++) {
                for (uint8_t d = 0; d < 256; d++) {
                    uint64_t s = start;
                    fnv_forward(&s, a);
                    fnv_forward(&s, b);
                    fnv_forward(&s, c);
                    fnv_forward(&s, d);
                    if (s == target) {
                        printf("found %lx\n", s);     
                    }
                    if (d == 255)
                        break;
                }
                if (c == 255)
                    break;
            }
            if (b == 255)
                break;
        }
        if (a == 255)
            break;
    }
    printf("done\n");
    return 0;
}
```

最后获得 hex_string :

`0x020101081b04390001051a020a3d0f0f`

> [!FLAG]
>
> flag{62bdc683-9476-4740-b7a1-e9d652b8efc4}

### LWEWL

> - https://github.com/CTF-Archives/2024-CISCN-Quals/releases/tag/Latest
> - https://suhanhan-cpu.github.io/2024/12/21/2024%20CISCN%20x%20%E9%95%BF%E5%9F%8E%E6%9D%AF%E9%93%81%E4%BA%BA%E4%B8%89%E9%A1%B9%20%E5%88%9D%E8%B5%9B%20WriteUp/#lwewl


### hash

```python title="hash.py"
#!/usr/bin/python2
# Python 2.7 (64-bit version)
from secret import flag
import os, binascii, hashlib
key = os.urandom(7)
print hash(key)
print int(hashlib.sha384(binascii.hexlify(key)).hexdigest(), 16) ^ int(binascii.hexlify(flag), 16)

"""
7457312583301101235
13903983817893117249931704406959869971132956255130487015289848690577655239262013033618370827749581909492660806312017
"""
```

显然恢复 key 就可以恢复 flag 了，提示了版本，自然去找：

```python title="py27-hash.py"
# https://github.com/neuml/py27hash/blob/4d814de4ab616f33bb2d74c687e74fa57c399a56/src/python/py27hash/hash.py#L129

class Hash(object):
    @staticmethod
    def shash(value):
        """
        Returns a Python 2.7 hash for a string.
        Logic ported from the 2.7 Python branch: cpython/Objects/stringobject.c
        Method: static long string_hash(PyStringObject *a)
        Args:
            value: input string
        Returns:
            Python 2.7 hash
        """
        length = len(value)
        if length == 0:
            return 0
        mask = 0xffffffffffffffff
        x = (Hash.ordinal(value[0]) << 7) & mask
        for c in value:
            x = (1000003 * x) & mask ^ Hash.ordinal(c)
        x ^= length & mask
        # Convert to C long type
        x = ctypes.c_long(x).value
        if x == -1:
            x = -2
        return x
    @staticmethod
    def ordinal(value):
        return value if isinstance(value, int) else ord(value)
```

从 py27-hash.py 可以得知：

1. 最终返回的哈希值 x 被转变为了 C 语言的 long 类型，且计算过程中经常 `&mask`，所以一定为 64 位；
2. 哈希过程非常简单

	```
	for c in value:
	    x = (1000003 * x) & mask ^ Hash.ordinal(c)
	```

 在 [xia0ji233](https://xia0ji233.pro/2024/05/19/CISCN2024/index.html) 的题解中给出了中间相遇攻击的思路：先穷举前三个字节并保存在字典中，再穷举后四个字节，从结果哈希值出发反向计算，并在字典中查找是否存在。

遗憾的是，我用给出的脚本直接运行得到的 key 是 `b']\x8c\xf0?Z\x08U'` ，发现 xia0 师傅在写 wp 的时候漏了一个细节：

3. 返回哈希值前进行了 `x ^= length & mask` 操作

所以对 r 异或一个 7 再开始爆破就可以了（大概是十几分钟，让 AI 写了个多进程版本，能够在 1 分钟左右得出结果）：

```python title="exp1.py"
# modified from https://xia0ji233.pro/2024/05/19/CISCN2024/index.html
from Crypto.Util.number import *
import hashlib,binascii

l=64
mask=(1<<l)-1
def pre_dic():
    dic={}
    for a in range(256):
        x = 0
        x=(x^(a<<7))&mask
        x = ((x * 1000003) ^ a) & mask
        for b in range(256):
            x2=((x*1000003)^b) & mask
            for c in range(256):
                x3=((x2*1000003)^c) & mask
                dic[x3]=bytes([a,b,c])
    return dic
dic = pre_dic()
print("dic done")
ni=inverse(1000003,1<<l)
r=7457312583301101235 ^ 7
def burst_key(dic):
    # for a in range(256):
    for a in range(82, 88):
        print(a) # 知道结果是 82 了，为了快一点直接从这开始
        r1=((r^a)*ni)&mask
        for b in range(256):
            r2=((r1^b)*ni)&mask
            for c in range(256):
                r3 = ((r2 ^ c) * ni) & mask
                for d in range(256):
                    r4 = ((r3 ^ d) * ni) & mask
                    if r4 in dic.keys():
                        print(dic[r4]+bytes([d,c,b,a])) # b']\x8c\xf0?Z\x08R'
                        key = dic[r4]+bytes([d,c,b,a])
                        return key
    return None

key = burst_key(dic)
if key:
    enc_flag_int = 13903983817893117249931704406959869971132956255130487015289848690577655239262013033618370827749581909492660806312017

    sha384_val = int(hashlib.sha384(binascii.hexlify(key)).hexdigest(), 16)
    flag_int = enc_flag_int ^ sha384_val
    print(binascii.unhexlify(hex(flag_int)[2:].strip('L')))
    # flag{bdb537aa-87ef-4e95-bea4-2f79259bdd07}
else:
    print("No key found")
print("Done")
```

再看主要求哈希的过程，一股 [fnv](https://github.com/DownUnderCTF/Challenges_2023_Public/blob/main/crypto/fnv/src/fnv.py) 的味道，后面尝试仿照[经典脚本](https://github.com/DownUnderCTF/Challenges_2023_Public/blob/main/crypto/fnv/solve/solution_joseph_LLL.sage)用格求解（需要枚举初始状态，几秒内就可以求解）：

```python title="exp2.sage"
# sage
import hashlib
import binascii

TARGET_HASH = 7457312583301101235
ENC_FLAG = 13903983817893117249931704406959869971132956255130487015289848690577655239262013033618370827749581909492660806312017

p = 1000003
MOD = 2**64
TARGET = TARGET_HASH ^^ 7

recovered_key_hex = ""

for k0 in range(256):
    h0 = ((k0 << 7) * p) ^^ k0
    h0 &= (MOD - 1)
    
    n = 6
    col_elements = [p^(n - i - 1) for i in range(n)] + [-(TARGET - h0*p^n), MOD]
    M = matrix(ZZ, col_elements).transpose()
    M = M.augment(identity_matrix(n+1).stack(vector([0] * (n+1))))
    
    Q = diagonal_matrix([2^64] + [2^4] * n + [2^8])
    M *= Q
    M = M.BKZ()
    M /= Q
    
    good = None
    for r in M:
        if r[0] == 0 and abs(r[-1]) == 1:
            r *= r[-1]
            good = r[1:-1]
            break
            
    if good is not None:
        inp = [k0]
        y = int(h0 * p)
        t = (h0*p^n + good[0] * p^(n-1)) % MOD
        valid = True
        for i in range(n):
            found = False
            for x in range(256):
                y_ = (int(y) ^^ int(x)) * p^(n-i-1) % MOD
                if y_ == t:
                    inp.append(x)
                    found = True
                    if i < n-1:
                        t = (t + good[i+1] * p^(n-i-2)) % MOD
                        y = ((int(y) ^^ int(x)) * p) % MOD
                    break
            if not found:
                valid = False
                break
        
        if valid:
            recovered_key_hex = bytes(inp).hex()
            break

if recovered_key_hex:
    print(f"Recovered Key: {recovered_key_hex}")
    
    # Decrypt Flag
    # Logic: int(hashlib.sha384(binascii.hexlify(key)).hexdigest(), 16) ^ enc_flag
    sha384_val = int(hashlib.sha384(recovered_key_hex.encode()).hexdigest(), 16)
    flag_int = ENC_FLAG ^^ sha384_val
    
    flag_hex = hex(flag_int)[2:]
    if flag_hex.endswith('L'): flag_hex = flag_hex[:-1]
    if len(flag_hex) % 2 != 0: flag_hex = '0' + flag_hex
    
    try:
        print(f"Flag: {binascii.unhexlify(flag_hex).decode()}")
        # Recovered Key: 5d8cf03f5a0852
        # Flag: flag{bdb537aa-87ef-4e95-bea4-2f79259bdd07}
    except Exception as e:
        print(f"Decryption error: {e}")
else:
    print("Failed to recover key.")
```

### OvO

```python title="task.py"
from Crypto.Util.number import *
from secret import flag

nbits = 512
p = getPrime(nbits)
q = getPrime(nbits)
n = p * q
phi = (p-1) * (q-1)
while True:
    kk = getPrime(128)
    rr = kk + 2
    e = 65537 + kk * p + rr * ((p+1) * (q+1)) + 1
    if gcd(e, phi) == 1:
        break
m = bytes_to_long(flag)
c = pow(m, e, n)

e = e >> 200 << 200
print(f'n = {n}')
print(f'e = {e}')
print(f'c = {c}')

"""
n = 111922722351752356094117957341697336848130397712588425954225300832977768690114834703654895285440684751636198779555891692340301590396539921700125219784729325979197290342352480495970455903120265334661588516182848933843212275742914269686197484648288073599387074325226321407600351615258973610780463417788580083967
e = 37059679294843322451875129178470872595128216054082068877693632035071251762179299783152435312052608685562859680569924924133175684413544051218945466380415013172416093939670064185752780945383069447693745538721548393982857225386614608359109463927663728739248286686902750649766277564516226052064304547032760477638585302695605907950461140971727150383104
c = 14999622534973796113769052025256345914577762432817016713135991450161695032250733213228587506601968633155119211807176051329626895125610484405486794783282214597165875393081405999090879096563311452831794796859427268724737377560053552626220191435015101496941337770496898383092414492348672126813183368337602023823
"""
```

将 e 的表达式展开可以注意到，e 的量级几乎全由 `r*n` 提供，那么可以得到 $r \approx \frac{e'}{n}$ （这里 e' 表示我们已知的高位部分）；当然稳妥起见，我们可以在周围一定范围内枚举并通过是否为质数筛选（当然也可以多试试几次随机生成数据，发现直接求解得到的就是 r）。这样我们可以认为 k, r 都是已知数，加上一个在 RSA 中常用的技巧：通过 $n=pq$ 将表达式变为只包含 p/q 的方程：

$$
f = 2(k+1)*p^2 + (rn-e)*p+rn+65540 = 0
$$

当然我们实际已知的是 $e'$，所以求解得到得 p 只是一个近似数，从而转变为已知 p 高位问题，进而求解：

```python title="exp.py"
n = 
e = 
c = 

def solve_p(p_high, shift = 200):
    """
    已知 p 高位问题
    """
    from sage.all import Zmod
    x = Zmod(n)['x'].gen()
    print(p_high)
    # x1 = p-p_high => x1+p_higt % p == 0
    f1 = x + p_high
    root1 = f1.small_roots(X=2**shift, beta=0.4)
    for root in root1:
        root = int(root)
        if n % (root + p_high) == 0:
            p = root + p_high
            q = n // p
            return p, q
    return None, None

from sympy import isprime, symbols, solve

approx_rr = e // n
approx_kk = approx_rr - 2
kks = []
radius = 10
for i in range(-radius, radius):
    cand_k = approx_kk + i
    if isprime(cand_k):
        kks.append(cand_k)

print(kks, len(kks))

for kk in kks:
    rr = kk + 2
    p = symbols('p')
    f = (kk+rr)*p**2 +(rr*n-e)*p + rr*n+65540
    ps = solve(f, 'p')
    for approx_p in ps:
        p_high = int(approx_p)
        p, q = solve_p(p_high)
        if all([p, q]):
            print(p, q)
            e_true = 65537 + kk * p + rr * ((p+1) * (q+1)) + 1
            d = pow(e_true, -1, (p-1)*(q-1))
            print(bytes.fromhex(hex(pow(c, d, n))[2:])) # b'flag{b5f771c6-18df-49a9-9d6d-ee7804f5416c}'
        else:
            print('no solution for', p_high)
            continue
```

### ezRSA

```python title="ezrsa.py"
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
import random
from secret import flag

m = bytes_to_long(flag)
key = RSA.generate(1024)
passphrase = str(random.randint(0,999999)).zfill(6).encode()
output = key.export_key(passphrase=passphrase).split(b'\n')
for i in range(7, 15):
    output[i] = b'*' * 64
with open("priv.pem", 'wb') as f:
    for line in output:
        f.write(line + b'\n')
with open("enc.txt", 'w') as f:
    f.write(str(key._encrypt(m)))
    
"""
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: DES-EDE3-CBC,435BF84C562FE793

9phAgeyjnJYZ6lgLYflgduBQjdX+V/Ph/fO8QB2ZubhBVOFJMHbwHbtgBaN3eGlh
WiEFEdQWoOFvpip0whr4r7aGOhavWhIfRjiqfQVcKZx4/f02W4pcWVYo9/p3otdD
ig+kofIR9Ky8o9vQk7H1eESNMdq3PPmvd7KTE98ZPqtIIrjbSsJ9XRL+gr5a91gH
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
****************************************************************
hQds7ZdA9yv+yKUYv2e4de8RxX356wYq7r8paBHPXisOkGIVEBYNviMSIbgelkSI
jLQka+ZmC2YOgY/DgGJ82JmFG8mmYCcSooGL4ytVUY9dZa1khfhceg==
-----END RSA PRIVATE KEY-----

55149764057291700808946379593274733093556529902852874590948688362865310469901900909075397929997623185589518643636792828743516623112272635512151466304164301360740002369759704802706396320622342771513106879732891498365431042081036698760861996177532930798842690295051476263556258192509634233232717503575429327989
"""
```

- [RSA 密钥格式解析](https://www.jianshu.com/p/c93a993f8997)
- [20220709-蓝帽杯-CryptoSecWriteUp](https://4xwi11.github.io/posts/9864757a/)
    
- [ezrsa-复现](https://dexterjie.github.io/2024/05/18/%E8%B5%9B%E9%A2%98%E5%A4%8D%E7%8E%B0/2024CISCN/#ezrsa%E2%80%94%E2%80%94%E5%A4%8D%E7%8E%B0) `flag{df4a4054-23eb-4ba4-be5e-15b247d7b819}`

## CISCN2023 初赛

### Sign_in_passwd

```
j2rXjx8yjd=YRZWyTIuwRdbyQdbqR3R9iZmsScutj2iqj3/tidj1jd=D
GHI3KLMNJOPQRSTUb%3DcdefghijklmnopWXYZ%2F12%2B406789VaqrstuvwxyzABCDEF5
```

第二行像是 url 编码，解码后猜测是自定义 base64：

> [!FLAG]
>
> flag{8e4b2888-6148-4003-b725-3ff0d93a6ee4}

### badkey

```python title="badkey1.py"
from Crypto.Util.number import *
from Crypto.PublicKey import RSA
from hashlib import sha256
import random, os, signal, string
 
def proof_of_work():
    random.seed(os.urandom(8))
    proof = ''.join([random.choice(string.ascii_letters+string.digits) for _ in range(20)])
    _hexdigest = sha256(proof.encode()).hexdigest()
    print(f"sha256(XXXX+{proof[4:]}) == {_hexdigest}")
    print('Give me XXXX: ')
    x = input()
    if len(x) != 4 or sha256(x.encode()+proof[4:].encode()).hexdigest() != _hexdigest:
        print('Wrong PoW')
        return False
    return True
 
if not proof_of_work():
    exit(1)
    
signal.alarm(10)
print("Give me a bad RSA keypair.")
 
try:
    p = int(input('p = '))
    q = int(input('q = '))
    assert p > 0
    assert q > 0
    assert p != q
    assert p.bit_length() == 512
    assert q.bit_length() == 512
    assert isPrime(p)
    assert isPrime(q)
    n = p * q
    e = 65537
    assert p % e != 1
    assert q % e != 1
    d = inverse(e, (p-1)*(q-1))
except:
    print("Invalid params")
    exit(2)
 
try:
    key = RSA.construct([n,e,d,p,q])
    print("This is not a bad RSA keypair.")
    exit(3)
except KeyboardInterrupt:
    print("Hacker detected.")
    exit(4)
except ValueError:
    print("How could this happen?")
    from secret import flag
    print(flag)
```

显然就是要触发 ValueError，源码审计……

```python title="badkey_solver.py"
def pf(rmt):
    def PoW(rec: str) -> str:
        import re
        import string
        from hashlib import sha256
        import itertools
        
        # Extract suffix and target hash using regex
        pattern = r"sha256\(XXXX\+(.*?)\) == ([a-f0-9]{64})"
        match = re.search(pattern, rec)
        
        if not match:
            return None
        
        suffix = match.group(1)
        target_hash = match.group(2)
        
        # Solve the PoW challenge
        chars = string.ascii_letters + string.digits
        for attempt in itertools.product(chars, repeat=4):
            prefix = "".join(attempt)
            test_str = prefix + suffix
            if sha256(test_str.encode()).hexdigest() == target_hash:
                return prefix
        
        return None
        
    rec = rmt.recv(1024)
    rmt.sendline(PoW(rec.decode()).encode())
    rmt.recvuntil(b"p = ")


from pwn import *

rmt = remote("node4.anna.nssctf.cn", 28528, level="debug")
pf(rmt)

# https://www.nssctf.cn/note/set/3134
def get_pq(l=512, e=0x10001):
    from Crypto.Util.number import isPrime, inverse, getPrime

    while True:
        p = getPrime(l)
        m = inverse(e, p - 1)
        temp = (e * m * p - 1) // (p - 1)
        for k in range(1, e + 1):
            if temp % k == 0:
                q = temp // k + 1
                if isPrime(q) and q.bit_length() == l:
                    return p, q


# p, q = get_pq()

p = 8421653256813693467327420543663576095525957858499069795905275775105913628777973154663037299646187656120434361709768773180360369189504761968356610803846019
q = 8268931175064080437894709841703693765995327463048305152043396908528782858938453271740660539203864353919527661268006747865039212242353910906779185878512409
rmt.sendline(str(p).encode())
rmt.sendline(str(q).encode())
rmt.recvall(timeout=1)
```

> [!FLAG]
>
> NSSCTF{28dede1c-98bb-4443-a94f-6f1976ddcf0c}

### badkey2

> 写到这里感觉自己对 RSA 密钥的构造并不熟悉；忙别的去了，先放着。
> 
> https://blog.csdn.net/qq_41626232/article/details/130928246

## CISCN2022

### math

```python title="task.py"
import gmpy2
from Crypto.Util.number import *
from flag import flag
assert flag.startswith(b"flag{")
assert flag.endswith(b"}")
message=bytes_to_long(flag)
def keygen(nbit, dbit):
    if 2*dbit < nbit:
        while True:
            a1 = getRandomNBitInteger(dbit)
            b1 = getRandomNBitInteger(nbit//2-dbit)

            n1 = a1*b1+1

            if isPrime(n1):
                break
        while True:
            a2 = getRandomNBitInteger(dbit)
            b2 = getRandomNBitInteger(nbit//2-dbit)

            n2=a2*b2+1

            n3=a1*b2+1
            if isPrime(n2) and isPrime(n3):
                break
        while True:
            a3=getRandomNBitInteger(dbit)
            if gmpy2.gcd(a3,a1*b1*a2*b2)==1:
                v1=(n1-1)*(n2-1) # phi1
                k=(a3*inverse(a3,v1)-1)//v1  # k * phi1=k * v1 = ed-1
                v2=k*b1+1
                if isPrime(v2):
                    return a3,n1*n2,n3*v2
def encrypt(msg, pubkey):
    return pow(msg, pubkey[0], pubkey[1])

nbit = 1024
dbit = 256
e, n1, n2=keygen(nbit, dbit)
print('e =', e)
print('n1 =', n1)
print('n2 =', n2)
c1 = encrypt(message, [e, n1])
c2 = encrypt(message, [e, n2])
print('enc1 =', c1)
print('enc2 =', c2)
# e = 86905291018330218127760596324522274547253465551209634052618098249596388694529
# n1 = 112187114035595515717020336420063560192608507634951355884730277020103272516595827630685773552014888608894587055283796519554267693654102295681730016199369580577243573496236556117934113361938190726830349853086562389955289707685145472794173966128519654167325961312446648312096211985486925702789773780669802574893
# n2 = 95727255683184071257205119413595957528984743590073248708202176413951084648626277198841459757379712896901385049813671642628441940941434989886894512089336243796745883128585743868974053010151180059532129088434348142499209024860189145032192068409977856355513219728891104598071910465809354419035148873624856313067
# enc1 = 71281698683006229705169274763783817580572445422844810406739630520060179171191882439102256990860101502686218994669784245358102850927955191225903171777969259480990566718683951421349181856119965365618782630111357309280954558872160237158905739584091706635219142133906953305905313538806862536551652537126291478865
# enc2 = 7333744583943012697651917897083326988621572932105018877567461023651527927346658805965099102481100945100738540533077677296823678241143375320240933128613487693799458418017975152399878829426141218077564669468040331339428477336144493624090728897185260894290517440392720900787100373142671471448913212103518035775
```

最多做到用连分数求解 $a_{2} 和 k$ 了，后面属实是没想到，参考 [nssctf 上的题解](https://www.nssctf.cn/note/set/3949)

```python title="solver.py"
from Crypto.Util.number import *
from sage.all import *

e = 86905291018330218127760596324522274547253465551209634052618098249596388694529
n1 = 112187114035595515717020336420063560192608507634951355884730277020103272516595827630685773552014888608894587055283796519554267693654102295681730016199369580577243573496236556117934113361938190726830349853086562389955289707685145472794173966128519654167325961312446648312096211985486925702789773780669802574893
n2 = 95727255683184071257205119413595957528984743590073248708202176413951084648626277198841459757379712896901385049813671642628441940941434989886894512089336243796745883128585743868974053010151180059532129088434348142499209024860189145032192068409977856355513219728891104598071910465809354419035148873624856313067
enc1 = 71281698683006229705169274763783817580572445422844810406739630520060179171191882439102256990860101502686218994669784245358102850927955191225903171777969259480990566718683951421349181856119965365618782630111357309280954558872160237158905739584091706635219142133906953305905313538806862536551652537126291478865
enc2 = 7333744583943012697651917897083326988621572932105018877567461023651527927346658805965099102481100945100738540533077677296823678241143375320240933128613487693799458418017975152399878829426141218077564669468040331339428477336144493624090728897185260894290517440392720900787100373142671471448913212103518035775

convergents = continued_fraction(ZZ(n1)/ZZ(n2)).convergents()
for conv in convergents:
    a2 = conv.numerator()
    k = conv.denominator()
    if(a2.bit_length() == 256):
        print(a2, k)
        phi_ = crt([-inverse(k,e),0], [e,a2]) # < 512 bit
        mod = e*a2 // gcd(e,a2)
        # phi = phi_ + t*mod = N1 -(n1+n2) +1, where N1 = n1*n2
        # phi 接近于 N1 且 phi = phi_%mod
        phi = phi_ + n1//mod *mod
        for i in range(4):
            phi -= i*mod
            try:
                d1 = inverse_mod(e,phi)
                m = pow(enc1,d1,n1)
                flag = bytes.fromhex(hex(m)[2:])
                if b'flag' in flag:
                    print(flag)
                    break
            except:
                pass
```

> [!FLAG]
>
> flag{b5073f3d774c460ae2b714010cc69435}

## CISCN2021 初赛

### rsa

```python title="part1"
from Crypto.Util.number import long_to_bytes, bytes_to_long
c1 = 19105765285510667553313898813498220212421177527647187802549913914263968945493144633390670605116251064550364704789358830072133349108808799075021540479815182657667763617178044110939458834654922540704196330451979349353031578518479199454480458137984734402248011464467312753683234543319955893
e1 = 3
N1 = 123814470394550598363280518848914546938137731026777975885846733672494493975703069760053867471836249473290828799962586855892685902902050630018312939010564945676699712246249820341712155938398068732866646422826619477180434858148938235662092482058999079105450136181685141895955574548671667320167741641072330259009
from gmpy2 import iroot
print(long_to_bytes(iroot(c1,e1)[0]))
```

```python title="part2"
c2 = 54995751387258798791895413216172284653407054079765769704170763023830130981480272943338445245689293729308200574217959018462512790523622252479258419498858307898118907076773470253533344877959508766285730509067829684427375759345623701605997067135659404296663877453758701010726561824951602615501078818914410959610
c3 = 91290935267458356541959327381220067466104890455391103989639822855753797805354139741959957951983943146108552762756444475545250343766798220348240377590112854890482375744876016191773471853704014735936608436210153669829454288199838827646402742554134017280213707222338496271289894681312606239512924842845268366950
e2 = 17
e3 = 65537
N2 = 111381961169589927896512557754289420474877632607334685306667977794938824018345795836303161492076539375959731633270626091498843936401996648820451019811592594528673182109109991384472979198906744569181673282663323892346854520052840694924830064546269187849702880332522636682366270177489467478933966884097824069977

from sage.all import *
s,s1,s2 = xgcd(e2,e3)
m2 = mod(power_mod(c2,s1,N2)*power_mod(c3,s2,N2), N2)
print(long_to_bytes(int(m2)))
```

```python title="part3"
c3 = 59213696442373765895948702611659756779813897653022080905635545636905434038306468935283962686059037461940227618715695875589055593696352594630107082714757036815875497138523738695066811985036315624927897081153190329636864005133757096991035607918106529151451834369442313673849563635248465014289409374291381429646
e3 = 65537
N3 = 113432930155033263769270712825121761080813952100666693606866355917116416984149165507231925180593860836255402950358327422447359200689537217528547623691586008952619063846801829802637448874451228957635707553980210685985215887107300416969549087293746310593988908287181025770739538992559714587375763131132963783147
p3_high = 7117286695925472918001071846973900342640107770214858928188419765628151478620236042882657992902
x = Zmod(N3)['x'].gen()
# x1 = p-p_high => x1+p_higt % p == 0
shift1 = 200
p3_high = p3_high<<shift1
f1 = x + (p3_high)
root1 = f1.small_roots(X=2**shift1, beta=0.4)
print(root1)
for root in root1:
    root = int(root)
    if N3 % (root + p3_high) == 0:
        p = root + p3_high
        q = N3 // p
        print("ok")
        break
d3 = pow(e3, -1, (p-1)*(q-1))
print(bytes.fromhex(hex(pow(c3, d3, N3))[2:]))
```

```python title="final"
from hashlib import md5
text = b" \nO wild West Wind, thou breath of Autumn's being,\nThou, from whose unseen presence the leaves dead\nAre driven, like ghosts from an enchanter fleeing,\nYellow, and black, and pale, and hectic red,\nPestilence-stricken multitudes: O thou,\nWho chariotest to their dark wintry bed\n"
md5(text).hexdigest()
```

> [!FLAG]
>
> CISCN{3943e8843a19149497956901e5d98639}

### small

```python title="task.py"
import random, hashlib
from Crypto.Util.number import getPrime
from secret import x, y, flag

BITS = 70

assert(2**BITS < x < 2**(BITS+1))
assert(2**BITS < y < 2**(BITS+1))

m = str(x) + str(y)
h = hashlib.sha256()
h.update(m.encode())
assert(flag == "flag{" + h.hexdigest() + "}")


p = getPrime(512)
a = getPrime(510)
b = getPrime(510)
c = (1 + a * x * y ** 2 + b * x ** 2 * y) % p
print("p = " + str(p))
print("a = " + str(a))
print("b = " + str(b))
print("c = " + str(c))

'''
p = 8813834626918693034209829623386418111935369643440896703895290043343199520112218432639643684400534953548489779045914955504743423765099014797611981422650409
a = 2817275225516767613658440250260394873529274896419346861054126128919212362519165468003171950475070788320195398302803745633617864408366174315471102773073469
b = 1763620527779958060718182646420541623477856799630691559360944374374235694750950917040727594731391703184965719358552775151767735359739899063298735788999711
c = 2298790980294663527827702586525963981886518365072523836572440106026473419042192180086308154346777239817235315513418426401278994450805667292449334757693881
'''
```

不难知道： 
$$\begin{align}
& c = (1+axy^2+bx^2y)\pmod{p} \\
&\implies (c-1)a^{-1} -ba^{-1}x^2y=xy^2\pmod{p}\\
&\implies xy^2 = (c-1)a^{-1} -ba^{-1}x^2y -kp \\
&\implies (1,x^2y,k)
\begin{pmatrix}
2^{(3*BITS)} & 0 &(c-1)a^{-1} \\
0 & 1 & -ba^{-1} \\
0 & 0 & p
\end{pmatrix} = (2^{(3*BITS)}, x^2y, xy^2)
\end{align}
$$

其中 $2^{(3*BITS)}$ 的目的是使得我们最后得到的向量是相近的小向量。

```python title="small_solve.py"
# https://www.nssctf.cn/note/set/4323
from sage.all import *
import hashlib
import gmpy2
from Crypto.Util.number import *

p = 8813834626918693034209829623386418111935369643440896703895290043343199520112218432639643684400534953548489779045914955504743423765099014797611981422650409
a = 2817275225516767613658440250260394873529274896419346861054126128919212362519165468003171950475070788320195398302803745633617864408366174315471102773073469
b = 1763620527779958060718182646420541623477856799630691559360944374374235694750950917040727594731391703184965719358552775151767735359739899063298735788999711
c = 2298790980294663527827702586525963981886518365072523836572440106026473419042192180086308154346777239817235315513418426401278994450805667292449334757693881
c = c-1
inv=inverse(a,p)
c=(inv*c)%p
b=((-b)*inv)%p

M = matrix(ZZ, [[1<<210,0,c],[0,1,b],[0,0,p]])
ML=M.LLL()
print(ML[0])
a=int(ML[0][0])
xy2=-int(ML[0][2])
x2y=-int(ML[0][1])
xy=gmpy2.gcd(x2y,xy2)
y=xy2//xy
x=x2y//xy

m = str(x) + str(y)
h = hashlib.sha256()
h.update(m.encode())
flag = "flag{" + h.hexdigest() + "}"
print(flag)
```

> [!FLAG]
>
> flag{e94e1ea0b945c6573b64ae79f0ebf33d5a585398c183a6752c74c3826bceb74c}

### imageencrypt

基于异或的特点，且 key 的值均小于 0xff，我们将 testimage 与 testresult （encrypt(testimage) 的结果）逐项异或，得到所有可能的 key 的值；接着枚举所有可能的 keys 对，获取对应的 binss；由于 `len(str(r)==3)` `x0 = round(random.random(),6)` 枚举所有可能的 r,x0 去利用 testimage testresult 构造 bins，如果 bins 在 binss 中，则对应的 keys 对可能有效，存入 xrb 列表中；最后遍历 xrb 列表中的内容，尝试解 flag。 

注意，python 编译器应该使用 python2，由 `import md5` 以及 `print testimage` 等可以看出来；否则 md5 的结果可能不同。
 
```python title="image_solve.py"
#!/usr/bin/env python2
def getFlag(flagimage):
    import md5
    data = ''.join(map(chr,flagimage))
    return "CISCN{"+md5.new(data).hexdigest()+"}"
    # return "NSSCTF{"+md5.new(data).hexdigest()+"}"

def xor(a, b):
    return (a^b)&0xff

def getKeys(testimage,  testresult):

    keys = []
    for pix, cipher in zip(testimage, testresult):
        tmp1 = xor(pix, cipher)
        tmp2 = xor(~pix, cipher)
        if tmp1 not in keys:
            keys.append(tmp1)
        if tmp2 not in keys:
            keys.append(tmp2)
    return keys

with open('out', 'r') as out:
    testimage = eval(out.readline())
    testresult = eval(out.readline())
    flagresult = eval(out.readline())

# keys = getKeys(testimage, testresult); keys
from itertools import permutations
keys = [78, 177, 169, 86]
keyss = [keys for keys in permutations(keys, 2)]
# print(keyss)

def getBins(keys, testimage, testresult):
    binss = []
    for key1, key2 in keyss:
        bins = ''
        for pix, cipher in zip(testimage, testresult):
            if xor(pix,key1) == cipher:
                bins += '00'
            elif xor(~pix,key1) == cipher:
                bins += '01'
            elif xor(pix,key2) == cipher:
                bins += '10'
            elif xor(~pix,key2) == cipher:
                bins += '11'
        binss.append(bins)
    return binss
# binss = getBins(keys, testimage, testresult); binss
# 将结果复制进入 bins
binss = eval(open('bins', 'r').readline())

def getBin(m, n, x, r):
    def generate(x):
        return round(r*x*(3-x), 6)
    num = int(m*n/8)    
    seqs = []
    bins = ''
    tmp = []
    for i in range(num):
        x = generate(x)
        if x < 1e-6:  # Ensure x is within a valid range
            return None  # Return None if x is too small
        print(x)
        tmp.append(x)
        seqs.append(int(x*22000))
    for x in seqs:
        bin_x  = bin(x)[2:]
        if len(bin_x) < 16:
            bin_x = '0'*(16-len(bin_x))+bin_x
        bins += bin_x
    return bins


def getXrb(m, n):
    def getRs(l):
        rs = []
        for i in range(10**(l-1)):
            d = i // (10**(l-2))
            f = i % (10**(l-2))
            rs.append(eval(str(d)+'.'+str(f)))
        for i in range(10**l):
            rs.append(i)
        return rs
    # print(getRs(3))
    rs = getRs(3)
    xrb = []
    for x1 in range(1, 1000000):
        x0 = round(x1/1e6, 6)
        for r in rs:
            if x0 == 900000:
                print(x0, r, b)
            Bin = getBin(m, n, x0, r)
            if Bin in binss:
                xrb.append((x0, r, binss.index(Bin)))
                return xrb # save time
    # return xrb

# print(getXrb(16, 16))
xrb = [(0.840264, 1.2, 6)]

def encrypt(pixel,key1,key2,x0,m,n, r):
    def generate(x):
        return round(r*x*(3-x),6)
    num = int(m*n/8)    
    seqs = []
    x = x0
    bins = ''
    tmp = []
    for i in range(num):
        x = generate(x)
        tmp.append(x)
        seqs.append(int(x*22000))
    for x in seqs:
        bin_x  = bin(x)[2:]
        if len(bin_x) < 16:
            bin_x = '0'*(16-len(bin_x))+bin_x
        bins += bin_x
    assert(len(pixel) == m*n)
    cipher = [ 0 for i in range(m) for j in range(n)]
    for i in range(m):
        for j in range(n):
            index = n*i+j
            ch = int(bins[2*index:2*index+2],2)
            pix = pixel[index]
            if ch == 0:
                pix = (pix^key1)&0xff
            if ch == 1:
                pix = (~pix^key1)&0xff
            if ch == 2:
                pix = (pix^key2)&0xff
            if ch == 3:
                pix = (~pix^key2)&0xff
            cipher[index] = pix 
    return cipher

for x, r, b in xrb:
    key1, key2 = keyss[b]
    flagimage = encrypt(flagresult, key1, key2, x, 24, 16, r)
    print(getFlag(flagimage)) 
```

> [!FLAG]
>
> CISCN{7fa176002ced947e49f1752c1eb9dd62}

### oddaes

> 参考：https://tr0jan.top/archives/107/

附件实现了一个正常的 AES，并给了我们同一个 key 在加密一个 plain 以及随机扰动的 plain 情况下的密文；利用 **[dfa-aes](https://github.com/Daeinar/dfa-aes)** [^1]这个工具进行差分密码爆破：

[^1]: 在 make 的时候，如果只能够安装 g++-4.8 ，可以自行修改 makefile 文件。

```shell title="get_key"
$ ./dfa 32 -1 oddaes.csv 
(0) Analysing ciphertext pair:

b784d7dda768571f38562cf19218ab75 a3f7ea6521a0c7a480653339edc261b4

Number of core(s): 32 
----------------------------------------------------
Fault location: 0
Applying standard filter. Done.
Size of keyspace: 7770931200 = 2^32.855440 
Applying improved filter. Done.
Size of keyspace: 474 = 2^8.888743 
----------------------------------------------------
Fault location: 1
Applying standard filter. Done.
Size of keyspace: 3538944000 = 2^31.720672 
Applying improved filter. Done.
Size of keyspace: 210 = 2^7.714246 
----------------------------------------------------
Fault location: 2
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 189 = 2^7.562242 
----------------------------------------------------
Fault location: 3
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 204 = 2^7.672425 
----------------------------------------------------
Fault location: 4
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 207 = 2^7.693487 
----------------------------------------------------
Fault location: 5
Applying standard filter. Done.
Size of keyspace: 7770931200 = 2^32.855440 
Applying improved filter. Done.
Size of keyspace: 503 = 2^8.974415 
----------------------------------------------------
Fault location: 6
Applying standard filter. Done.
Size of keyspace: 3538944000 = 2^31.720672 
Applying improved filter. Done.
Size of keyspace: 190 = 2^7.569856 
----------------------------------------------------
Fault location: 7
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 196 = 2^7.614710 
----------------------------------------------------
Fault location: 8
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 197 = 2^7.622052 
----------------------------------------------------
Fault location: 9
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 202 = 2^7.658211 
----------------------------------------------------
Fault location: 10
Applying standard filter. Done.
Size of keyspace: 7770931200 = 2^32.855440 
Applying improved filter. Done.
Size of keyspace: 408 = 2^8.672425 
----------------------------------------------------
Fault location: 11
Applying standard filter. Done.
Size of keyspace: 3538944000 = 2^31.720672 
Applying improved filter. Done.
Size of keyspace: 190 = 2^7.569856 
----------------------------------------------------
Fault location: 12
Applying standard filter. Done.
Size of keyspace: 3538944000 = 2^31.720672 
Applying improved filter. Done.
Size of keyspace: 233 = 2^7.864186 
----------------------------------------------------
Fault location: 13
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 177 = 2^7.467606 
----------------------------------------------------
Fault location: 14
Applying standard filter. Done.
Size of keyspace: 3317760000 = 2^31.627562 
Applying improved filter. Done.
Size of keyspace: 215 = 2^7.748193 
----------------------------------------------------
Fault location: 15
Applying standard filter. Done.
Size of keyspace: 7770931200 = 2^32.855440 
Applying improved filter. Done.
Size of keyspace: 471 = 2^8.879583 

4266 masterkeys written to keys-0.csv
```

```python title="solve.py"
from aes import AES
import hashlib
import os
f = open('keys-0.csv', 'r')
cipher1 = '973f5ae78bc933a8fc7f7ab98d53d16f'
cipher2 = '628aab012199cdab83cc1aa72204ea98'
plain = os.urandom(16)
for key in f.readlines():
    cipher, k = AES(bytes.fromhex(key)).encrypt_block_(plain, 123)
    piece1 = [k[0], k[1], k[4], k[7], k[10], k[11], k[13], k[14]]
    piece2 = [k[2], k[3], k[5], k[6], k[8], k[9], k[12], k[15]]
    if hashlib.md5(bytes(piece1)).hexdigest() == cipher1 and hashlib.md5(bytes(piece2)).hexdigest().replace('0x', '') == cipher2:
        print('key :' + key)
        print('flag:' + hashlib.md5(bytes.fromhex(key)).hexdigest())
        exit(0)
```

![](attachments/ciscn_crypto-1.png)

> [!FLAG]
>
> CISCN{8e786b3efe3fa5c0984894a7b75e8324}

### classic

ADFGX(phqgmeaynofdxkrcvszwbutil) + caeser (box)

最后得到了

> CISCNBRACETHREECONEFOURDEONEAFOURCEFFFSEVENSEVENONEYERONINEDCFOURYEROASIXYEROSIXAFIVEADYEROBRACE

属实是有点恶心的……

> [!FLAG]
>
> CISCN{3c14de1a4cefff77109dc40a606a5ad0}

### move

```python
from Crypto.Util.number import *
from math import sqrt, gcd
import random

BITS = 512
f = open("flag.txt", "rb")
flag = f.read()
f.close()

def get_prime(nbit):
    while True:
        p = getPrime(nbit)
        if p % 3 == 2:
            return p


def gen(nbit):
    p = get_prime(nbit)
    q = get_prime(nbit)
    if q > p:
        p, q = q, p
    n = p * q
    bound = int(sqrt(2 * n)) // 12
    while True:
        x = random.randint(1, round(sqrt(bound)))
        y = random.randint(1, bound) // x
        zbound = int(((p - q) * round(n ** 0.25) * y) // (3 * (p + q)))
        z = zbound - ((p + 1) * (q + 1) * y + zbound) % x
        e = ((p + 1) * (q + 1) * y + z) // x
        if gcd(e, (p + 1) * (q + 1)) == 1:
            break
    gifts = [int(bin(p)[2:][:22], 2), int(bin(p)[2:][256:276], 2)]
    return n, e, gifts


def add(p1, p2):
    if p1 == (0, 0):
        return p2
    if p2 == (0, 0):
        return p1
    if p1[0] == p2[0] and (p1[1] != p2[1] or p1[1] == 0):
        return (0, 0)
    if p1[0] == p2[0]:
        tmp = (3 * p1[0] * p1[0]) * inverse(2 * p1[1], n) % n
    else:
        tmp = (p2[1] - p1[1]) * inverse(p2[0] - p1[0], n) % n
    x = (tmp * tmp - p1[0] - p2[0]) % n
    y = (tmp * (p1[0] - x) - p1[1]) % n
    return (int(x), int(y))


def mul(n, p):
    r = (0, 0)
    tmp = p
    while 0 < n:
        if n & 1 == 1:
            r = add(r, tmp)
        n, tmp = n >> 1, add(tmp, tmp)
    return r


n, e, hint = gen(BITS)
pt = (bytes_to_long(flag[:len(flag) // 2]), bytes_to_long(flag[len(flag) // 2:]))
c = mul(e, pt)
f = open("output.txt", "w")
f.write(f"n = {n}\n")
f.write(f"e = {e}\n")
f.write(f"h1 = {hint[0]}\n")
f.write(f"h2 = {hint[1]}\n")
f.write(f"c = {c}\n")
f.close()
# output.txt 内容在第一个代码格中
```

基本上就是参考 [writeup for 2021虎符 - simultaneous](https://tearsjin.github.io/2021/04/06/writeup-for-2021%E8%99%8E%E7%AC%A6/#0x01-simultaneous) 进行了一个复现（本来写在 ipynb 中，所以有点怪）：

```python title="exp.sage"
# sage
n = 80263253261445006152401958351371889864136455346002795891511487600252909606767728751977033280031100015044527491214958035106007038983560835618126173948587479951247946411421106848023637323702085026892674032294882180449860010755423988302942811352582243198025232225481839705626921264432951916313817802968185697281
e = 67595664083683668964629173652731210158790440033379175857028564313854014366016864587830963691802591775486321717360190604997584315420339351524880699113147436604350832401671422613906522464334532396034178284918058690365507263856479304019153987101884697932619200538492228093521576834081916538860988787322736613809
h1 = 3518005
h2 = 641975
c = (6785035174838834841914183175930647480879288136014127270387869708755060512201304812721289604897359441373759673837533885681257952731178067761309151636485456082277426056629351492198510336245951408977207910307892423796711701271285060489337800033465030600312615976587155922834617686938658973507383512257481837605, 38233052047321946362283579951524857528047793820071079629483638995357740390030253046483152584725740787856777849310333417930989050087087487329435299064039690255526263003473139694460808679743076963542716855777569123353687450350073011620347635639646034793626760244748027610309830233139635078417444771674354527028)

# M = Matrix(ZZ, [[int(n.sqrt()), e], [0, -n]])

M = Matrix(ZZ, [[1<<512, e], [0, -n]])
L = M.LLL(); L

_512_x, s = L[0]
x = _512_x >> 512
y = (e*x - s) // n
x, y

def add(p1, p2):
    from Crypto.Util.number import inverse
    if p1 == (0, 0):
        return p2
    if p2 == (0, 0):
        return p1
    if p1[0] == p2[0] and (p1[1] != p2[1] or p1[1] == 0):
        return (0, 0)
    if p1[0] == p2[0]:
        tmp = (3 * p1[0] * p1[0]) * inverse(2 * p1[1], n) % n
    else:
        tmp = (p2[1] - p1[1]) * inverse(p2[0] - p1[0], n) % n
    x = (tmp * tmp - p1[0] - p2[0]) % n
    y = (tmp * (p1[0] - x) - p1[1]) % n
    return (int(x), int(y))


def mul(n, p):
    r = (0, 0)
    tmp = p
    while 0 < n:
        if n & 1 == 1:
            r = add(r, tmp)
        n, tmp = n >> 1, add(tmp, tmp)
    return r
    
def find_p_add_q(f, k):
    l = 0
    r = k
    for i in range(k.bit_length()): # 二分法的理论界限
        m = (l + r) // 2
        if f.subs(x==m) > 0:
            l = m
        else:
            r = m
    return m

k = s//y
x = var('x')
f = (3*x*(k-1-x))**2 - round(n**0.25)**2 * (x**2 - 4*n)
pmq = find_p_add_q(f, k); pmq

for error in range(-3, 4): # 可能有误差
    try:
        d = inverse_mod(e, n + pmq + 1 + error); d # (p+1)*(q+1) = x+p+q+1
        pt = mul(d, c)
        print([bytes.fromhex(hex(p)[2:]) for p in pt])
    except:
        continue

"""
[b'g\x9d@\x8b\x1fJ\xe1\xec\xd2\xb7@N\xf4\xcc\xed\xca9S~k\x89\x0fFc\xc6\xfb\xd8\xbd\x08m\xf8\x1a;\xf4\x16\x16\xe5q\x00{!q\x14\xc4\xfe_\x9b\xc2\xa8\x16/\xfc\x1b\x92\x91}\xe5\xbb\xf4\x7f\xc7]!"\x18L\x9c*tW\x0fEu\x0e\x9f-DKm\xbdAi9\xfb\xd0\x82>|\x87\xf3v\x90\xc3\xce\xd2\xf9u\x8fh\xa5w\xa2\x83\x0cJ\xb6\xef\xcd\xf6G.k\xd08N\xe8n\xf9\xe5\x80ZD\xad\xf1D\xca\xcf\xb6', b'T\xdb\x8d\x96\xeb3\x01\x91\xe5\x1d\xb1\n\xdb:U1\xa3_Je\xc3\x89\x8ds}\xc2\xf1\x88\x832T\xc2Lp\x1a\xb5J-!e\xf0q\xbf\x13b\xc7O}\x05\xef\x1c\x02\x9c,\x8b\xc9\xb7s\x98\xdda\x91JL\xca\x83I\xc1\x19H\xda\xf8g9\xe2\x9a\xeb\x00\xa6\xf0\xbc\xa3?I\x03\xbe\x12a\x96\xad\xf7\x7f:\x7f\xb3+,\xf5E\x0c\xc8^\x0f\xbc\xbf\r\xd8\xee\xcd\t\xec\xe4\x89\xf0\x12\xdd_T\x89e?\x86OX\x17\x06\xc0\x8d']
[b'\xd4[wX\xfftF\x82y\xdd\xfd{\xdb\xb3\x90\x15\xde\x82\xe0\x18}\xe59\x93 3&M|\x8c\x9f\x06\xb8\xa6\x96\x98\x99\xf3\x13\xc6\xc0\xac7f\x9ew\xa8\xbdV\xa6\xb1\x18\xb0\xd9/\xec9\xfc\xf6U^\x8d5\xb3>\xad\x8c\xd9\xaa\xc4\xf5=}[\x1d={F\xeaW\x1bs\xf08k\x05\xf6syY\xa3C\xb3ySC\x946%-\xd6Z\xa0\x13\xf0YG\x89\x95\x8fw\xfe\x80\x88d\xc8n}\xcel\x88\xad\xa6K\xa4\x06H', b'j\xf7\x81\x1f\xf9}\x92k\x83V\xd9y\x8aA\xf5\teA\xca\xb9\xd8R\xcfg\xc5h3\xc5\xdd3aw\xf2\xcc8\xbeW\x98\xc0:4g0#\xc1\x0cc\xce_\x86\xd9\xe1 U=\xdc{]\xe3\xc5\xac#\xdb\xd6\xe74\x04\xcc\xd6\xf1\x1b\x9a\x89 \x84v\x97\xe5\xac\x06^\x823\xbc\xa5\x16\x87Q$\xd1\xca\xcc5\td6 6\xc7\xc7\xcc\xb8T%\xf2C\xe9\x89[9\t\x00Rc\xf6J\xe9\xceht\xbe\x93\xb3\x17\xd1?X\n']
[b'CISCN{e91fef4ead746', b'3b13d00bda65f540477}']
[b'hn\xa0Y\xe2Kf\x8f\x92yr\x11\xd5\x05\xcf\xee\x9cT\x94\x87c9\x13\xa1\x1254\x86\xd4p\xf8:\xdd^\x99\xb2\x01\x04\xd0\xd0\xbdR\xe7\xe8=5\x0c\x9f\xecL*\xbe\xed\x80R\x0b\xb8d\xf7N\xa1\x88\xa6t\x860\x90\x19\x9ej\xa8w\x8b\x82Hrn\x8e\xf9\x01\xa4\xa2F\xed\x85u\x0b\x86\xe22\xce\x13/\x1c\x88\x95<\xd6\xdbe\x00.\x892\xde\xd8\xb2<\x03\x0b\xda\x99@q\xaej\xd8w;\xb6\xf0Q\xf9c5.\xbd\x1b', b'!Fi/\xff03\xf6%\xff\x00\x10\xbf\x14zL\x11\x8f\xb5\xf2\x0fE-\x92q&\x80d8ykUc\xff\x15\x9ci\xa6&1AI\xd7A\xbd\xafmH\xe57\x11\xcd\xb3\x85\x89\xb9\x7f2\tqj\xccSB\x8c,\xb7\xb6\xd8\xec\xc5\xc5B\xd7v\x8c66q\xac\xdeK[\x18+\x9e\xf9\xfc\x03\xc9\x0e\xc9y\x0f\x9a\x89\x98\xd0\xc1\x02\x881\xb5\xe6\xe9\xff\xd0\xeb\xd6o\xff\x9e}\xd0|\xab\xa2\xe6\xa1\xfd\xe5\x82\xebUg\x1c\xfc^']
"""
```

> [!FLAG]
>
> CISCN{e91fef4ead7463b13d00bda65f540477}

但是有一个点没能很理解：最后我们对明文的求解为

```python
d = inverse_mod(e, (p + 1) * (q + 1))
pt = mul(d, c)
```

姑且看着答案写过程，谈谈我的理解。我们知道 c = mul(e, pt)，又在构造过程中有：`gcd(e, (p + 1) * (q + 1)) == 1` ，`add()` `mul()` 的操作，很难不想到椭圆曲线加密。

接着我们来看如果我们手算 ECC 中两个点相“加”的过程：

$$
\begin{aligned}&\text{ALgorithm for the addition of two points: }P+Q\\&\text{(a) If }P=O,\text{ then }P+Q=Q.\\&\text{(b) Othenwise, if }Q=O,\text{ then }P+Q=P.\\&\text{(c) Othenwise, write }P=(x_1,y_1)\mathrm{~and~}Q=(x_2,y_2).\\&\text{(d) If }x_1=x_2\mathrm{~and~}y_1=-y_2,\text{ then }P+Q=O.\\&\text{(e) Othenwise:}\\&\text{  (e1) if }P\neq Q;\lambda=(y_2-y_1)/(x_2-x_1)\\&\text{   (e2) if }P=Q;\lambda=(3x_1^2+a)/2y_1\\&\text{(f) }x_3=\lambda^2-x_1-x_2\\&\text{(h) }y_3=\lambda(x_1-x_3)-y_1\\&\text{(i) }P+Q=(x_3,y_3)\end{aligned}
$$

可以看到确实 ~~基本上~~ 完全一致，那么一切都解释的通了。

## CISCN2018

### sm

```python title="sm.py"
from Crypto.Util.number import getPrime, long_to_bytes, bytes_to_long
from Crypto.Cipher import AES
import hashlib
from random import randint


def gen512num():
    order = []
    while len(order) != 512:
        tmp = randint(1, 512)
        if tmp not in order:
            order.append(tmp)
    ps = []
    for i in range(512):
        p = getPrime(512 - order[i] + 10)
        pre = bin(p)[2:][0 : (512 - order[i])] + "1"
        ps.append(int(pre + "0" * (512 - len(pre)), 2))
    return ps


def run():
    choose = getPrime(512)
    ps = gen512num()
    print("gen over")
    bchoose = bin(choose)[2:]
    r = 0
    bchoose = "0" * (512 - len(bchoose)) + bchoose
    for i in range(512):
        if bchoose[i] == "1":
            r = r ^ ps[i]
    flag = open("flag", "r").read()

    key = long_to_bytes(int(hashlib.md5(long_to_bytes(choose)).hexdigest(), 16))
    aes_obj = AES.new(key, AES.MODE_ECB)
    ef = aes_obj.encrypt(flag).encode("base64")

    open("r", "w").write(str(r))
    open("ef", "w").write(ef)
    gg = ""
    for p in ps:
        gg += str(p) + "\n"
    open("ps", "w").write(gg)

run()
```

> 以下讨论均将数字看作 GF(2) 上的向量。

在 GF(2) 上，加法可以看作是异或；或者在这里，我们将 {0,1} 上的异或看作是加法。那么对于加密的核心过程（下面这段），

```python
for i in range(512):
    if bchoose[i] == "1":
        r = r ^ ps[i]
```

我们大可看作（下面的公式中 pi 为比特向量，bi 和 ri 为比特）：

$$
(b_{1},b_{2}\dots b_{510},b_{511}) * 
\begin{pmatrix}
 p_0\\
 p_1\\
 ...\\
 p_{510}\\
p_{511}
\end{pmatrix} = (r_{1},r_{2}\dots r_{510},r_{511})
\implies B*P = R
$$

显然我们能够获得 P,R，解出 B 就获得了密钥：

```python title="sm_solver.py"
# sagemath 10.4
from Crypto.Util.number import long_to_bytes
from Crypto.Cipher import AES
import hashlib
from base64 import b64decode
with open("r", "r") as f:
    r = int(f.read().strip())

with open("ef", "r") as f:
    ef = f.read().strip()
ct = b64decode(ef)

with open("ps", "r") as f:
    ps = [int(line.strip()) for line in f.readlines()]

Ps = [[int(x) for x in bin(p)[2:].zfill(512)] for p in ps]
Rs = [int(x) for x in bin(r)[2:].zfill(512)]
P = Matrix(GF(2), Ps)
R = Matrix(GF(2), Rs)
# C = R * P.inverse()
C = P.solve_left(R)
choose = int("".join([str(x) for x in C.list()]), 2)
key = long_to_bytes(int(hashlib.md5(long_to_bytes(choose)).hexdigest(), 16))
aes_obj = AES.new(key, AES.MODE_ECB)
pt = aes_obj.decrypt(ct)
print(pt) # b'flag{shemir_alotof_in_wctf_fun!}'
```

## 参考

- [2024-CISCN-Quals - CTF-Archive](https://github.com/CTF-Archives/2024-CISCN-Quals)
- [x] https://dawn1ight.github.io/post/43135/index.html
- [x] https://blog.csdn.net/XiongSiqi_blog/article/details/139064568
- [x] https://dexterjie.github.io/2024/05/18/%E8%B5%9B%E9%A2%98%E5%A4%8D%E7%8E%B0/2024CISCN/
- [x] https://ghostfrankwu.github.io/2023/05/29/2023ciscn/
	- 国密 SM2
- [x] https://blog.csdn.net/XiongSiqi_blog/article/details/139064568
	- [x] checkin
- [x] https://xia0ji233.pro/2024/05/19/CISCN2024/index.html
	- [x] hash
- [x] [第二届“长城杯”铁人三项赛 (防护赛)初赛WriteUP](https://cloud.tencent.com/developer/article/2477739) or https://lrhtony.cn/2024/12/17/ccbciscn/#wei-xie-jian-ce-yu-wang-luo-liu-liang-fen-xi
	- 威胁检测/网络流量分析
- [x] [[可信计算] 刷题记录](https://blog.hxzzz.asia/archives/180/)
	- `grep -r "flag{" /`
	- `grep -ra flag{`
	- `find / -name flag\* 2>/dev/null`
	- `cat /root/cube-shell/instance/flag_server/flag.list`
