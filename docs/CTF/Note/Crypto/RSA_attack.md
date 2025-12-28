---
tags:
- notes
- ctf
comments: true
---

## 基本原理

### 加密原理

1. 寻找两个大质数 p, q（p/q 之间的关系暂且不谈，不当的选取就会导致攻击漏洞）；
2. n = pq; $phi = \phi(n) = (p-1)(q-1)$ （欧拉函数）
3. 寻找一个 e，使得：$1<e<phi$ 且 gcd(e, phi) = 1
4. m 为明文映射为的大数，则密文 $c\equiv m^e\pmod{n}$
5. (e, n) 作为公钥公开。

### 解密原理

1. 私钥为 $d=e^{-1}\pmod{\phi(n)}$
2. $c^d = m^{ed}\pmod{n} = m^{ed\pmod{\phi(n)}} =m$

### 安全性保证

**合理**的 RSA 的安全性完全来自 n 的质数分解难度；不合理的是什么？看下面就知道了。

## Exponential attack

### Low public exponent attack

低加密指数攻击，攻击条件：e 很小

> [!tip] 优先尝试 sagemath 的 `m = Integer(c).nth_root(e)`

> [!note]+ solution of m^e （解的数量）
> 
> > [!THEOREM]
> >
> > If $gcd(e, p-1)=1$ and p is prime, the $m^e \equiv c\pmod{p}$ has exactly one solution for m.
> 
> [math.stackexchange 上的问答](https://math.stackexchange.com/questions/2842399/solutions-to-xn-equiv-a-pmodp)中较为靠下的一个回答给出更广泛的结论：
> 
> > [!THEOREM]
> >
> > If p is prime, $p \nmid c$, then $m^e \equiv c \pmod{p}$ has **0 or d = gcd(e, p-1)** solutions, being the latter if $c^{\frac{p-1}{d}}\equiv 1 \pmod{p}$.
> 
> 证明略，其中最后一两步如果看不懂可以参考 [group theory - Solution to $x^n=a \pmod p$ where $p$ is a prime](https://math.stackexchange.com/questions/1491103/solution-to-xn-a-pmod-p-where-p-is-a-prime) .
> 
> 依据费马小定理，在 p 是素数时，随机在 $\mathbb{Z}_{p}$ 中生成一个非零元素 x 将会满足 $x^{(p-1 /n)*n} = x^{p-1}\equiv 1 \pmod{p}$，此时 $x^{(p-1 / n)}$ 称为素数 p 有限域 $F_{p}$ 上的一个 n 次单位根；
> 
> 更基础的结论是：在素数 p 有限域 $F_{p}$ 中，乘法子群的阶为 p-1；对于 n，如果满足 $n|p-1$，则有 n 个单位根；否则只有 1 本身。对于 e 而言，即如果 $e|p-1$，则有 e 个根 m 满足 $m^e \equiv c \pmod{p}$

#### e = 1

> [!QUESTION]
>
> [cryptohack - Salty](https://cryptohack.org/challenges/rsa/)

cryptohack 上刚好有这么一个题：

```python
n = 110581795715958566206600392161360212579669637391437097703685154237017351570464767725324182051199901920318211290404777259728923614917211291562555864753005179326101890427669819834642007924406862482343614488768256951616086287044725034412802176312273081322195866046098595306261781788276570920467840172004530873767                                                                  
e = 1
ct = 44981230718212183604274785925793145442655465025264554046028251311164494127485
for i in range(123456789):
    pt = ct + i * n
    plaintext = bytes.fromhex(hex(pt)[2:])
    if b'crypto' in plaintext:
        print("i =", i, plaintext) # i = 0 b'crypto{saltstack_fell_for_this!}'
        break
    if i % 10000 == 0:
        print(i)
```

> [!FLAG]-
>
> crypto{saltstack_fell_for_this!}

#### e = 2 (Rabin)

$\phi=(p-1)(q-1)$ 且由于 p/q 为素数，所以 $gcd(e, \phi)\neq 1$ ，那么怎么做？

回顾 $c=m^e\pmod{n}$ ，现在就是 $m^2=c\pmod{n}$ 。

如果 $m^e < n$ ，那么甚至不用取模了，直接开根：

```python title="m^e < n"
c = 42482525051044
e = 2
long_to_bytes(gmpy2.iroot(c, e)[0]) # b'ctf'
```

如果要取模呢？可以使用 **Rabin 算法** 转变为二次剩余问题。但是注意，这一切的前提是模数为素数；n 又不是素数，怎么做？

```python title="e = 2"
n = 87924348264132406875276140514499937145050893665602592992418171647042491658461
e = 2
pt = "darctf{xxx}"
m = int(pt.encode().hex(), 16)
c = pow(m, e, n)
print(c) 
# 55804540899466191494822903355151119222813727476411593093741269550876471676261
```

作为练习，我使用了一个较小的 n ，可以很容易分解：

```
n = 275127860351348928173285174381581152299 * 319576316814478949870590164193048041239
```

$$
m^2 \equiv c\pmod{n} \iff \begin{cases}m^2\equiv c\pmod{p}\\m^2\equiv c\pmod{q}\end{cases}
$$

在 [m 的解个数](RSA_attack.md#m%20的解个数) 中的结论，我们可以知道对于上方右侧的每个方程，都有 gcd(e, p-1) = 2 个解，分别记作 `[x1, x2] [y1, y2]` [^1]。

[^1]: 这个求解请自行学习二次剩余求解，当然下面代码也会反映出一些想法。
$$
\begin{cases}
m \equiv x \pmod{p} \\ m \equiv y \pmod{q}
\end{cases}
$$
这下看懂了，对四种情况分别中国剩余定理求解即可。

```python title="rabin"
n = 275127860351348928173285174381581152299 * 319576316814478949870590164193048041239
p, q = 275127860351348928173285174381581152299, 319576316814478949870590164193048041239

import gmpy2

def squareMod(c, mod):          # 模意义下开根，找到 x, 使得 x^2 % mod = c
    assert(mod % 4 == 3)
    res = gmpy2.powmod(c, (mod+1)//4, mod)
    return res, mod - res

def getPlaintext(x, y, p, q):   # 假设 m%p=x, m%q=y, 求明文
    res = x*q*gmpy2.invert(q, p) + y*p*gmpy2.invert(p, q)
    return res % (p*q)

def solve(c, p, q):             # 已知 p,q, 解密 c
    px = squareMod(c, p)
    py = squareMod(c, q)

    for x in px:
        for y in py:
            yield getPlaintext(x, y, p, q)

c = 55804540899466191494822903355151119222813727476411593093741269550876471676261
p = 275127860351348928173285174381581152299
q = 319576316814478949870590164193048041239

for msg in solve(c, p, q):
    res = hex(msg)[2:]
    if len(res) % 2 == 1:
        res = '0' + res
    print(bytes.fromhex(res))

# b'r\xd8lq+g\xc8r\x84\x04\xe2\xc6i\xb4\\?\xb13\xa9_[\xa3\x8b\xcb\xbd\xbf\xe6\x95K)h\xe1'
# b'darctf{r@bln_a77@ck_e_2}'
# b'\xc2cj\xe5\xc3\xd8\xe4?\x9768\xa5\x8e(\x9f:+\xa9\x8a^\xde\x0f\xb4\x92\xe7\xb8\x94\x8a\x1a^\xfe`'
# b'O\x8a\xfet\x98q\x1b\xcdw\x92\xc8B\x98\xda\xbel\xba\xd8Mm\xe1\xcd_\xfej\\\x19T4\x94\xc7\xfc'
```

当然，sage 中应当是帮我们内置了这么一个算法，所以：

```python title="mod(c, p).sqrt(all=True)"
from sage.all import *
c = 55804540899466191494822903355151119222813727476411593093741269550876471676261
p = 275127860351348928173285174381581152299
q = 319576316814478949870590164193048041239
sqrt_c_p = Mod(c, p).sqrt(all=True)
sqrt_c_q = Mod(c, q).sqrt(all=True)
for i in sqrt_c_p:
    for j in sqrt_c_q:
        m = crt([int(i), int(j)], [p, q])
        from Crypto.Util.number import long_to_bytes
        print(long_to_bytes(m))
```

#### e = 3

如果 $m^e < n$ ，仍然可以直接开根；不然，可以由 $m^e = kn+c$ ，尝试爆破 k 并尝试开 3 次根，能分解多半是可行解；但是一般来说花费时间有点久。

当然，sage 帮我们方便的实现了这个功能（下面的分解用时约 3min ，可见效率还是很低的，毕竟这里的 n 非常小了）：

```python title="e = 3"
from sage.all import *
n = 87924348264132406875276140514499937145050893665602592992418171647042491658461
e = 3
pt = "darctf{r@bln_a77@ck_e_2}"
m = int(pt.encode().hex(), 16)
c = pow(m, e, n)
print(c) # 82453779934743057049976069612841272595880705095622841974484769483483076860419

from Crypto.Util.number import *
import gmpy2

c = 82453779934743057049976069612841272595880705095622841974484769483483076860419
m = Mod(c, n).nth_root(e)
print(long_to_bytes(m)) # b'darctf{r@bln_a77@ck_e_2}'
```

### gcd(e, phi) != 1

> 参考[针对 CTFer 的 e 与 phi 不互素的问题](https://tttang.com/archive/1504/)

一般来说 $gcd(e, \phi)=1$ 的，但要是 $gcd(e, \phi)\neq 1$ ，那么怎么做？e=2/3/4 …… 等十分小的数时前面已经说明了，这里考虑比较一般的情况。

由于 $gcd(e, \phi)\neq 1$，正常意义下的私钥 d 是不存在的，但是考虑到欧拉扩展定理：

若 $gcd(e, \phi) = b \neq 1$ ，则有 $c = m^e = m^{ab}\pmod{n} = m^{ab \pmod{\phi}}$；

#### gcd(a, phi)=1

1. 当 b 比较小的时候

取 $d = a^{-1}\pmod{\phi}$，则有 $c^d = m^{abd\pmod{\phi}} =  m^b\pmod{n}$；所以只需要对 $c^d\pmod{\phi}$ 开 b 次根就好。

当然，不难发现，哪怕 $gcd(e, \phi)=1$ ，上述过程依然适用。

```python
from sage.all import *

p= 127577058764408216374028752283743628765651360507566484643526093715329608267323381565274095814069864692746147152580906850350743742856555229701448239882612922698102985146366639955081466129923966803267071097174222576416224094182123529282235807472362341680183683025490897702891081336913842652559163341223338641607
q= 156492273708587234539506501480609692085997989594717058472605523051244522493701609615085173280972894139427194976925940854142835807192417391269823151398439665817176522629246535810290194301862945052149450578938260979300632842291287807430486629994530805358742405299538986591596966945727494262182814875780600646003
e= 750
c= 7029383721249299532521086933490698266831518266762255492452526410777276825803657150303837084263410309063739203644435184397762022380085273363900423091223180151147964276354189658062571415744140073426572149093499560918765793389358300893454490774387180728097370701432534877005948330689495694820361726719418371072834639369078180094444137972424909816959445043108154884587947573054460257114169961823509538355580857411319157089278918107229480661280354242839678709689654304688727345294473487201644985815128413154870914132135222144633969959773621933444285994038028721862094040876152694240238708737727034258171506516394913692187

def get_ms(n, e, c, phi=None) -> list:
    """
    Returns the private exponent for the given public exponent and modulus.
    """
    from sage.all import is_prime, euler_phi, GCD, inverse_mod, power_mod, Integer, ZZ, Zmod
    if not phi:
        if is_prime(n):
            phi = n - 1
        elif phi is None:
            phi = euler_phi(n)
    b = GCD(e, phi)
    ms = None
    if b == 1:
        d = inverse_mod(e, phi)
        ms = [power_mod(c, d, n)]
    else:
        a = e // b
        assert a*b == e
        assert gcd(a, phi) == 1
        d = inverse_mod(a, phi)
        mb = power_mod(c, d, n) # mb = m^b % n
        ##### if m^b < n
        ## Method 1
        # ms = [Integer(mb).nth_root(b)]
        ## Method 2
        # x = ZZ['x'].gen(); f = x**b - mb
        # ms = f.roots(multiplicities=False)
        ##### if m^b >= n
        ## Method 3
        # ms = Zmod(n)(mb).nth_root(b, all=True)
        ## Method 4
        ms = Mod(mb, n).nth_root(b, all=True)
        ## Method 5
        # x = Zmod(n)['x'].gen(); f = x**b - mb
        # ms = f.roots(multiplicities=False)
    return ms

n = p*q
phi = (p-1)*(q-1)
ms = get_m(n, e, c, phi)
for m in ms:
    print(bytes.fromhex(hex(abs(m))[2:]))
# b'flag{0e2f9add-31fd-4733-8f25-39297516f4e2}'
```

2. 当 b = e 时，考虑 AMM 算法 ([Adleman-Manders-Miller rth Root Extraction Method](https://arxiv.org/pdf/1111.4877))，示例来自 [NCTF2019 - easyRSA](https://blog.soreatu.com/posts/intended-solution-to-crypto-problems-in-nctf-2019/)

```python title="NCTF2019 - easyRSA"
# https://tttang.com/archive/1504/#toc_0x00
from flag import flag

e = 0x1337
p = 199138677823743837339927520157607820029746574557746549094921488292877226509198315016018919385259781238148402833316033634968163276198999279327827901879426429664674358844084491830543271625147280950273934405879341438429171453002453838897458102128836690385604150324972907981960626767679153125735677417397078196059
q = 112213695905472142415221444515326532320352429478341683352811183503269676555434601229013679319423878238944956830244386653674413411658696751173844443394608246716053086226910581400528167848306119179879115809778793093611381764939789057524575349501163689452810148280625226541609383166347879832134495444706697124741
n = p * q

assert(flag.startswith('NCTF'))
m = int.from_bytes(flag.encode(), 'big')
assert(m.bit_length() > 1337)

c = pow(m, e, n)
print(c)
# 10562302690541901187975815594605242014385201583329309191736952454310803387032252007244962585846519762051885640856082157060593829013572592812958261432327975138581784360302599265408134332094134880789013207382277849503344042487389850373487656200657856862096900860792273206447552132458430989534820256156021128891296387414689693952047302604774923411425863612316726417214819110981605912408620996068520823370069362751149060142640529571400977787330956486849449005402750224992048562898004309319577192693315658275912449198365737965570035264841782399978307388920681068646219895287752359564029778568376881425070363592696751183359
```

帮我们分解好了 n，但是求 $\phi$ 后可以发现 $gcd(e, \phi)=e$，即 $e|\phi$；由于 e 是素数，所以肯定存在 $e|p-1 \lor e|q-1$ ；测试发现这里：$e|p-1, e|q-1$ 均成立；考虑分治为：$m^e \equiv c \pmod{p}, m^e \equiv c \pmod{q}$ 再通过 CRT 进行组合。

以 p 为例，问题转向：$m^e \equiv c \pmod{p}$；首先考虑如何求解，AMM 算法能够做到这件事（注意 p 为素数）：

```python title="AMM"
def AMM(o, r, q) -> int:
    """
    使用 Adleman-Manders-Miller 算法在模 q 的有限域中求 r 次根的一组解中的一个。
    参数:
        o (int): 要开 r 次根的元素（明文在模 q 下的值）。
        r (int): 根的阶（例如 e = 0x1337）。
        q (int): 素数模数，定义有限域 GF(q)。
    返回:
        int: o 在 GF(q) 上的一个 r 次根。
    """
    pass
```

考虑前面提到的“解的数量”，我们验证 $c^{\frac{p-1}{d}} \equiv 1 \pmod{p}$ 通过，表明 $m^e \equiv c \pmod{p}$ 可以得到 $gcd(e, \phi)=e=0x1337$ 个解；考虑两个公式，我们一共有 $e^2 = 24196561$ 种可能；同时我们也提到了有 e 个根的原因是对应于有 e 个 e 次单位根，而 [Finding the n-th root of unity in a finite field](https://crypto.stackexchange.com/questions/63614/finding-the-n-th-root-of-unity-in-a-finite-field) 向我们介绍了如何找到一个单位根（代码来自 [Van1sh](https://jayxv.github.io/2019/12/04/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%E4%B9%8B%E6%B5%85%E6%9E%90On%20r-th%20Root%20Extraction%20Algorithm%20in%20Fq/)）：

```python title="onemod"
def onemod(p, r):
    """
    在模素数 p 的乘法群中找到一个阶为 r 的元素 g，使得 g^r ≡ 1 (mod p)。
    参数:
        p (int): 素数模数。
        r (int): 期望的阶。
    返回:
        int: 一个满足 g^r ≡ 1 (mod p) 且阶整除 r 的元素 g。
    """
    t = p - 2
    while pow(t, (p-1) // r, p) == 1:
        t -= 1
    return pow(t, (p-1) // r, p)
```

以及扩展扩展找到其他单位根：

```python title="solution"
def solution(p, root, e):
    """
    根据一个 e 次根 root，枚举模 p 下所有可能的 e 次根解集合。
    给定某个根 root，使得 root^e ≡ c (mod p)，通过乘以所有阶为 e 的生成元幂得到
    所有等价的解。
    参数:
        p (int): 素数模数。
        root (int): 已知的一个 e 次根。
        e (int): 指数 e。
    返回:
        set[int]: 所有可能的 e 次根集合。
    """
    g = onemod(p, e)
    may = set()
    for i in range(e):
        may.add(root * pow(g, i, p) % p)
    return may
```

总结一下，我们的思路就是：

1. 通过 AMM 找到一个根
2. 通过 onemod 找到一个 e 次单位根
3. 通过 solution 扩展到所有根
4. 通过 CRT 合并答案

```python title="exp.py"
cp = c % p
cq = c % q
mp = AMM(cp,e,p)
mq = AMM(cq,e,q)
mps = solution(p,mp,e)
mqs = solution(q,mq,e)
for mpp in tqdm(mps):
    for mqq in mqs:
        ai = [int(mpp),int(mqq)]
        mi = [p,q]
        m = CRT_list(ai,mi)
        flag = long_to_bytes(m)
        if b'NCTF' in flag:
            print(flag)
            exit(0)
            
"""
 46%|████████████████████████████████▍                                     | 2280/4919 [06:02<06:59,  6.30it/s]
 b'NCTF{T4k31ng_Ox1337_r00t_1s_n0t_th4t_34sy}e$71N{D]0su{ZDEKfEnY>TTQ(=qR?GBpN\\U{3@O\\/I8ZsxW.Uw)3&&s&xD-<Uf*pKXOkV0~oiWubv<VAD9roRJU9:9S?>MyZ<wMN~T||%PC*j]inkgus4f9t:g:O9!FsIas^?M*q:BU{_J*r"*6Fi94hdRUW#s0=N+][l}Js7j,c5kiLB+/f<_1*N=V3Eq%~s^!5Gh8*'
 46%|████████████████████████████████▍                                     | 2280/4919 [06:02<06:59,  6.29it/s]
python 运行 6 m 7s，sagemath 运行 5m 26s
"""
```

> [!extra]- [HackGame2019 - 十次方根](https://github.com/ustclug/hackergame2019-writeups/blob/master/official/%E5%8D%81%E6%AC%A1%E6%96%B9%E6%A0%B9/src/easy_math.py)
> 
> 这是一个 e=10 的 RSA 问题（且 $gcd(e,\phi)=e$）；但对于我们前面提到的算法重点在于 $n =x*y^3$，且 $e|x-1$ 不成立，直接套 AMM 似乎存在问题；
> 
> - [7feilee r认为](https://github.com/ustclug/hackergame2019-writeups/blob/master/players/7feilee/writeup-%E5%8D%81%E6%AC%A1%E6%96%B9%E6%A0%B9.md) e=10 比较小，可以针对 x,y 分别开根，使用 Hensel’s lifting 提升到 $y_{3}$
> - [官方题解](https://github.com/ustclug/hackergame2019-writeups/tree/master/official/%E5%8D%81%E6%AC%A1%E6%96%B9%E6%A0%B9)给出了一个使用 wolfram math 的方法，[在线存档](https://www.wolframcloud.com/obj/darstibreed/Published/HackGame-10TimesRoot.nb)。

#### gcd(a, phi)!=1

如果 $gcd(a, \phi) \neq 1$，也就同样无法找到 a 的逆元 d；此时考虑递归求解：

```python
def get_mb(n, e, c, phi=None):
    """
    Returns the private exponent for the given public exponent and modulus.
    """
    from sage.all import GCD, euler_phi, inverse_mod, power_mod, is_prime
    if is_prime(n):
        phi = n - 1
    elif phi is None:
        phi = euler_phi(n)
    b = GCD(e, phi)
    if b == 1:
        d = inverse_mod(e, phi)
    else:
        a = e // b
        assert a*b == e
        # print(a, b)
        if GCD(a, phi) == 1:
            d = inverse_mod(a, phi)
            mb = power_mod(c, d, n)
        else:
            print("gcd(a, phi) != 1, a =", a)
            mb, b_ = get_mb(n, a, c, phi=phi)
            b *= b_
    return mb, b
    
from sage.all import Integer
mb, b = get_mb(n, e, c)
m = Integer(mb).nth_root(b)
```

如果最后一个 get_mb 中得到的 a = 1，那么毫无疑问 b = e，且 mb = c，回到上一部分讨论的 AMM 算法。

- 大概率是 $e=2^{k}, k\in N$ 的情况；而这样我们可以一层一层开平方根（此时攻击条件与 e=2 相同）
	- 示例来自 [cryptohack - Broken RSA](https://cryptohack.org/challenges/maths/)：

```python title="broken rsa"
from sage.all import *
from Crypto.Util.number import long_to_bytes
from sympy import sqrt_mod, legendre_symbol
n = 27772857409875257529415990911214211975844307184430241451899407838750503024323367895540981606586709985980003435082116995888017731426634845808624796292507989171497629109450825818587383112280639037484593490692935998202437639626747133650990603333094513531505209954273004473567193235535061942991750932725808679249964667090723480397916715320876867803719301313440005075056481203859010490836599717523664197112053206745235908610484907715210436413015546671034478367679465233737115549451849810421017181842615880836253875862101545582922437858358265964489786463923280312860843031914516061327752183283528015684588796400861331354873
e = 16
ct = 11303174761894431146735697569489134747234975144162172162401674567273034831391936916397234068346115459134602443963604063679379285919302225719050193590179240191429612072131629779948379821039610415099784351073443218911356328815458050694493726951231241096695626477586428880220528001269746547018741237131741255022371957489462380305100634600499204435763201371188769446054925748151987175656677342779043435047048130599123081581036362712208692748034620245590448762406543804069935873123161582756799517226666835316588896306926659321054276507714414876684738121421124177324568084533020088172040422767194971217814466953837590498718

################# m^16 = m^2^2^2^2
assert is_prime(n)

def debug_info(*args, **kwargs):
    DEBUG = False
    if DEBUG:
        print(*args, **kwargs)
        
def sqrt_mods(cs:list, n, debug=False):
    ms = []
    for c in cs:
        if legendre_symbol(int(c), int(n)) != 1:
            # 不是二次剩余，不可开根
            continue

        m_ = Mod(c, n).sqrt(all=True)
        debug_info("dealing c:", c)
        for m in m_:
            debug_info(long_to_bytes(int(m)))
        ms += m_

        # sympy 的 sqrt_mod 只分解得到其中一个结果，最终会漏掉
        # 详见 https://darstib.github.io/blog/CTF/Note/Crypto/RSA_attack/#m-%E7%9A%84%E8%A7%A3%E4%B8%AA%E6%95%B0
        # m = sqrt_mod(c, n)
        # debug_info(long_to_bytes(m))
        # ms.append(m)
    return ms


m16s = [ct]
m8s = sqrt_mods(m16s, n)
debug_info("m8s:", m8s)
m4s = sqrt_mods(m8s, n)
debug_info("m4s:", m4s)
m2s = sqrt_mods(m4s, n)
debug_info("m2s:", m2s)
ms = sqrt_mods(m2s, n, debug=True)
debug_info("ms:", ms)
for m in ms:
    print(long_to_bytes(int(m)))

# b"Hey, if you are reading this maybe I didn't mess up my code too much. Phew. I really should play more CryptoHack before rushing to code stuff from scratch again. Here's the flag: crypto{m0dul4r_squ4r3_r00t}"
```

### Multi e&phi

低加密指数广播攻击，攻击条件：gcd(e, phi) != 1，gcd(n1, n2) != 1

类似于模不互素，我们令 p = gcd(n1, n2) ，则 q1 = n1//p, q2 = n2//p，则有：

$$
\begin{cases}
c_1^{d_1}=m^b\bmod q_1 \\ 
c_2^{d_2}=m^b\bmod q_2
\end{cases} \implies m^b = crt([c_{1}^{d_{1}}\%q_{1}, c_{2}^{d_{2}}\% q_{2}], [q_{1}, q_{2}])
$$

但是发现此时求得的 $m^b$ 并不能直接开 b 次根[^1]；但换个角度看，这不也是我们在解决的 rsa 问题吗？现在新的密文是[^2] $c <= m^b, n <= q_{1}*q_{2}, e <= b$ ，这不是就解决了吗？

[^1]: 可能是由于两次使用的 n 不同，m 所在的有限域不同导致的（猜测）。
[^2]: `<=` 表示的是赋值，并非 `≤` 。

#### new gcd(e,phi)=1

如果在经过上面转变后，新的 gcd(e, phi)=1 ，那么我们就是正常的 rsa 了，且 n 已经分解好：

```python title="many_e_phi_1.py"
"""
from Crypto.Util.number import *
import random
# from secret import flag
flag=''
table='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
pad=100-len(flag)
for i in range(pad):
    flag+=random.choice(table).encode()
e=343284449
m=bytes_to_long(flag)
assert m>(1<<512)
assert m<(1<<1024)
p=getPrime(512)
q=getPrime(512)
r=getPrime(512)
print('p=',p)
print('q=',q)
print('r=',r)
n1=p*q
n2=q*r
c1=pow(m,e,n1)
c2=pow(m,e,n2)
print('c1=',c1)
print('c2=',c2)
"""

from sage.all import *

e = 343284449
p = 11820891196647569262137841192985418014377132106496147254821784946481523526822939129065042819464351666077658751406165276121125571355594004514547517855730743
q = 10450390015864176713581330969519712299844487112687677452105216477861582967322473997670559995588440097951786576039009337782247912476227937589298529580432797
r = 9484954066160968219229920429258150817546418633451929876581842443665029377287119340232501682142185708534413073877473741393278935479791561681402673403009771

c1 = 69574855207460025252857869494766338442370688922127811393280455950372371842144946699073877876005649281006116543528211809466226185922844601714337317797534664683681334132261584497953105754257846471069875622054326463757746293958069752489458646460121725019594141157667480846709081917530190233900184428943585065316
c2 = 66183492015178047844987766781469734325646160179923242098082430373061510938987908656007752256556018402101435698352339429316390909525615464024332856855411414576031970267795270882896721069952171988506477519737923165566896609181813523905810373359029413963666924039857159685161563252396502381297700252749204993228

# 验证可行的必要条件
phi1 = (p - 1) * (q - 1)
phi2 = (q - 1) * (r - 1)
b1 = gcd(e, phi1)
b2 = gcd(e, phi2)
assert b1 == b2
a1 = e // b1
a2 = e // b2
b = b1 # 用 b 统一代替，b = 343284449 == e

# 求解
d1 = pow(a1, -1, phi1)
d2 = pow(a2, -1, phi2)
c = crt([pow(c1,d1,p), pow(c2,d2,r)], [p, r]) # == m^b
n = p * r # 新的 n

phi = (p - 1) * (r - 1)
d = pow(b, -1, phi)
m = pow(c, d, n)
print(bytes.fromhex(hex(m)[2:])) # b'moectf{Th1s_iS_Chinese_rEm41nDeR_The0rEm_CRT!}YWMZSTyfRvhjTCJuQCwALQBcWHFCgTDIZWJaxRUzBPCmFOnbDTRBau'
```

> [!Extra]
>
> 当使用的 e 相同时，其实不难得到：$\begin{cases}m^e =c_{1}\pmod{n_{1}}\\ m^e=c_{2}\pmod{n_{2}}\end{cases}$，使用 sagemath 中的 CRT_list() 方法可以很快的求解到 $m^e \pmod{p*q*r}$ ，可以验证这样获得值等于 $pow(m,e,p*q*r)$；但是模数太大了，难以分解；即使是很小的 e (e = 2) 我也没能分解出来。

#### new gcd(e, phi)!=1

要是新产生的 gcd(e,phi)!=1 ，就转变为了 **一组 e, phi** 的情况了：

```python title="many_e_phi_2.py"
from sage.all import *
e1 = 14606334023791426
n1 = 15848477716099753229061105911923143022389100496585807518993837576102534462043194116619385857927748061397249782381439885030297281760313655984354167005661008888718357134674249156614681638863679015479391847068348113489701337473262927808261967350366795633795543505703845606067045115243249537229108546272131429244457163342256387732236996418260843007569149387213329951406657469770618225877026401261848714538526688419134479943104911077402172330808220738139303070470120465456908824191640348115644774893040473576807682731982391129182748695821091864850237701682483798458814537415464726492081290583865419431028569430363239973387 

c1 = 11402389955595766056824801105373550411371729054679429421548608725777586555536302409478824585455648944737304660137306241012321255955693234304201530700362069004620531537922710568821152217381257446478619320278993539785699090234418603086426252498046106436360959622415398647198014716351359752734123844386459925553497427680448633869522591650121047156082228109421246662020164222925272078687550896012363926358633323439494967417041681357707006545728719651494384317497942177993032739778398001952201667284323691607312819796036779374423837576479275454953999865750584684592993292347483309178232523897058253412878901324740104919248

e2 = 13813369129257838
n2 = 11445377519264375060023079150962157833890568553640391338775989472330549038258150532468931626590818889296627067314268489584599131270267459828529179275532395041458525655212071679524344189181556827177841274953525505205469905975591164796436528919538933755927696086719287398795598052871568671842946947271918760899756232697968504961711410196730301840362369205729432748105709812801671538869541242955495144296736011715597473451149699457286420032252438757033057264819071583173255215409033569426653382271461349576578652124917074830516189769868866985581229557115992762278225013198895683154925091608336698625404745349624865012491
c2 = 7984888899827615209197324489527982755561403577403539988687419233579203660429542197972867526015619223510964699107198708420785278262082902359114040327940253582108364104049849773108799812000586446829979564395322118616382603675257162995702363051699403525169767736410365076696890117813211614468971386159587698853722658492385717150691206731593509168262529568464496911821756352254486299361607604338523750318977620039669792468240086472218586697386948479265417452517073901655900118259488507311321060895347770921790483894095085039802955700146474474606794444308825840221205073230671387989412399673375520605000270180367035526919

""" solve """

p = gcd(n1, n2)
q1, q2 = n1 // p, n2 // p
phi1, phi2 = (p-1)*(q1-1), (p-1)*(q2-1)
b1 = gcd(e1, phi1)
assert b1==gcd(e2, phi2)

a1, a2 = e1 // b1, e2 // b1
d1, d2 = inverse_mod(a1, phi1), inverse_mod(a2, phi2)
c1d1, c2d2 = power_mod(c1, d1, q1), power_mod(c2, d2, q2)
m_b1 = crt([c1d1, c2d2], [q1, q2])

# 按照只有一组 e phi 的方法继续做，n = q1*q2, e = b1
n = q1 * q2
phi = (q1-1) * (q2-1)
b2 = gcd(b1, phi)
a = b1 // b2
d = inverse_mod(a, phi)
m_b2 = power_mod(m_b1, d, n)
m = Integer(m_b2).nth_root(b2)
print(bytes.fromhex(hex(m)[2:])) # b"flag{gcd_e&\xcf\x86_isn't_1}"
```

## Modular attack

### N ezFactor

> [!QUESTION]
>
> [CryptoHack – RSA challenges](https://cryptohack.org/challenges/rsa/) Everything is Big

题目中给出了很大的 N，但是放到 factordb.com 中，分解一下就出来了；或者对于比较小的 N，[yafu](https://sourceforge.net/projects/yafu/) /sagemath 的 factor之类的都可以分解。

分解为 factors 如下：

```python
from Crypto.Util.number import *
e = 0x9ab58dbc8049b574c361573955f08ea69f97ecf37400f9626d8f5ac55ca087165ce5e1f459ef6fa5f158cc8e75cb400a7473e89dd38922ead221b33bc33d6d716fb0e4e127b0fc18a197daf856a7062b49fba7a86e3a138956af04f481b7a7d481994aeebc2672e500f3f6d8c581268c2cfad4845158f79c2ef28f242f4fa8f6e573b8723a752d96169c9d885ada59cdeb6dbe932de86a019a7e8fc8aeb07748cfb272bd36d94fe83351252187c2e0bc58bb7a0a0af154b63397e6c68af4314601e29b07caed301b6831cf34caa579eb42a8c8bf69898d04b495174b5d7de0f20cf2b8fc55ed35c6ad157d3e7009f16d6b61786ee40583850e67af13e9d25be3
c = 0x3f984ff5244f1836ed69361f29905ca1ae6b3dcf249133c398d7762f5e277919174694293989144c9d25e940d2f66058b2289c75d1b8d0729f9a7c4564404a5fd4313675f85f31b47156068878e236c5635156b0fa21e24346c2041ae42423078577a1413f41375a4d49296ab17910ae214b45155c4570f95ca874ccae9fa80433a1ab453cbb28d780c2f1f4dc7071c93aff3924d76c5b4068a0371dff82531313f281a8acadaa2bd5078d3ddcefcb981f37ff9b8b14c7d9bf1accffe7857160982a2c7d9ee01d3e82265eec9c7401ecc7f02581fd0d912684f42d1b71df87a1ca51515aab4e58fab4da96e154ea6cdfb573a71d81b2ea4a080a1066e1bc3474
factors = [134669927709128070756424801419548805501808076912262801434800605920827612464368906595661348393409080650056282638489243851059781971132159889896843018381187994628859917822755789986092763460463295405651440816348815008245093856412009397970192375577360567873185141159375280522236909060526334123001733587717969177157, 173121513995818161102245832683211062320154182361182024148671930683926870711405647497524667705258311163551127156955342410807842326402024536548989691926348678692995530897791794818646241971728281417961389048493180792474943296919266335463768525410560161755731138916915767148609523790355387780727531897114371948649]

phi = (factors[0] - 1) * (factors[1] - 1)
d = pow(e, -1, phi)
m = pow(c, d, N)
print(bytes.fromhex(hex(m)[2:]).decode()) # crypto{s0m3th1ng5_c4n_b3_t00_b1g}
```

### Roll enc

类似于分组加密，分别解密之后恢复即可。

```python
from sage.all import *
from Crypto.Util.number import *

n=920139713
e=19
c=[704796792,752211152,274704164,18414022,368270835,483295235,263072905,459788476,483295235,459788476,663551792,475206804,459788476,428313374,475206804,459788476,425392137,704796792,458265677,341524652,483295235,534149509,425392137,428313374,425392137,341524652,458265677,263072905,483295235,828509797,341524652,425392137,475206804,428313374,483295235,475206804,459788476,306220148]

phi = euler_phi(n)
d = inverse_mod(e,phi)
flag=""
for i in c:
  m=long_to_bytes(pow(i,d,n))
  flag=flag+m.decode()#decode返回字符串
print(flag)
```

### Modulars not coprime

模不互素是指：多次给出的 n 不互素，那么使用欧几里得算法求解公因数后两个都可以分解，从而被破解。

### n=multi primes

n 能够分解为多个素数，那么分解难度相对较低，分解后求解欧拉函数即可。

> [!QUESTION]
>
> [CryptoHack – RSA challenges](https://cryptohack.org/challenges/rsa/) Manyprime

可以使用下面的公式寻找 phi ：

```python title="manyPrime"
def manyPrime(n):
    from sage.all import *
    n = Integer(n)
    factors = factor(n)
    phi=1
    for i in factors:
        phi *= (i[0]-1)*(i[0]**(i[1]-1))
    return phi
```

当然 sagemath 中内置了 `euler_phi()` 方法直接寻找。

> [!TIP]
>
> 有时使用 factordb 分解大数，发现能够分解出一些小数，但是剩下最大的那个数依旧不是质数。如果已经分解出来的部分的乘积大于 m，那么也够用了。
>
> 例如，当前已经分解 $n = a*....*b * A$ 且 $is\_prime(A)==False$，那么我们记 $a*\dots*b = k, \phi(k)$ 是不难计算的。如果 m < k，则有 $m=c^{d_n}\pmod{n} = c^{d_{k}}\pmod{k}$ 其中 $d_x$ 表示在模 x 的情况下 e 的逆元。

### common modulars

共模攻击，攻击条件：使用相同的 n，不同的 e 对同一段密文进行了两次加密且 gcd(e1, e2)=1。

若 gcd(e1, e2)=1，由扩展欧几里得算法得 s1e1+s2e2 = 1 (mod n)，故有

$$
\begin{cases}
c_{1} = m^{e_{1}}\pmod{n} \\
c_{2} = m^{e_{2}}\pmod{n}
\end{cases} \implies c_{1}^{s_{1}}*c_{2}^{s_{2}} = m^{s_{1}e_{1}+s_{2}e_{2}} = m \pmod{n}
$$

```python title="same module problem"
from sage.all import *
from Crypto.Util.number import *
pt = "darctf{D0n't_uS@_s4me_m_wlth_s@m3_n}"
m = bytes_to_long(pt.encode())
p = getPrime(512)
q = getPrime(512)
n = p*q
e1 = 0x10001
e2 = 0x10003
c1 = pow(m,e1,n)
c2 = pow(m,e2,n)
print(n, c1, c2)
```

```python title="same module solver"
n, c1, c2 = 98579989110595409237121911373477535218782298101063142983736645609805239388519112976391020979766081600973756603466949088252537954226386662303812158399922085551030673235391122690690489614742213805086900032298294111577763523768897971988558981215342244298264282081994037439494627023764742694360182589392496394219, 72425280162325234030138440618893638248350200498036366062366806318799000892558826781676354721574015025260601419134051722219497286707335137576108567308732036645624100301827935632352883927544186998800800613763615685859542808865932240404766516153255982736474238236663712354416704416640104545540927957772848234809, 93315981548035764166225288143368979083298522822532493540407786336594222729430799616658596163211870306390452369608572159579771439267416866701746284141500177829084900908267884433644532039697396467417361020676970648165967089856122514452470159341424342038954503503377562938855963571013967607308287570236674707243
e1, e2 = 0x10001, 0x10003
s,s1,s2 = xgcd(e1,e2)
m = mod(power_mod(c1,s1,n)*power_mod(c2,s2,n), n)
print(long_to_bytes(int(m))) # b"darctf{D0n't_uS@_s4me_m_wlth_s@m3_n}"
```

### Get p q if we know phi

$$\begin{cases}p+q=n-\varphi(n)+1\\p-q=\sqrt{\left(n-\varphi(n)+1\right)^2-4n}\end{cases}$$

### Improper pq

#### small |p-q|

- [CTF Wiki (ctf-wiki.org)](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_module_attack/#p-q_1)
- [Wikipedia - Fermat's factorization](https://en.wikipedia.org/wiki/Fermat's_factorization_method)

常见的情况有 `q = next_prime(p)` 或者 `p, q = util.GeneratePrimePairByBitLength(bsize, gap)` 导致二者非常接近，可以使用费马因式分解法。

> [!QUESTION]
>
> [CryptoHack – RSA challenges](https://cryptohack.org/challenges/rsa/) Infinite Descent

```python title="small_p_min_q"
from sage.all import *
n = ...
e = 65537
c = ...

def fermat_factor(n):
    # from sage.all import ceil, is_square
    # def nth_root(n, e):
    #     return pow(n, 1 / e)

    from libnum import nroot
    from math import ceil
    from gmpy2 import is_square

    a = ceil(nroot(n, 2))
    b = a**2 - n
    while not is_square(b):
        a += 1
        b = a**2 - n

    c = nroot(b, 2)
    return a - c, a + c

p, q = fermat_factor(n)
# print(p, q)
phi = (p-1)*(q-1)
d = inverse_mod(e, phi)
m = power_mod(c, d, n)
from libnum import n2s
print(n2s(m)) # b'crypto{f3rm47_w45_4_g3n1u5}'
```

#### n&npnq

xxxBUS 上有这么一个题，给我 e, n, c 之外，还给我 npnq，其中 `n == p*q and npnq = next_prime(p)*next_prime(q)`

我们记 $npnq = np*nq$ ，则会发现：`p*nq - q*np` 很小！也就是说，我们可以利用上面讲的方法分解 `n*npnq` ，如果能够得到 $p1 = p*nq$ ，则有 $p = gcd(n, p_{1})$ ，这样 n 就分解出来了。

由于 $n*npnq = p*q * np * nq = p * nq * q * np$ ，所以被分解为哪种情况并不能确保，我们可以选择多保留几组；当然，考虑到 $|p*nq - q*np| < |np * nq - p*q|$，所以一般来说第一个解应该是我们想要的。

```python title="fematFactorization"
def fematFactorization(n, k=1) -> list:
    """n == p*q && |p-q| is small"""
    from gmpy2 import iroot, is_square
    from itertools import count

    factors_list = []
    a = iroot(n, 2)[0]
    b_2 = a**2 - n
    for a in count(a):
        b_2 = a**2 - n
        if b_2 < 0:
            continue
        b = iroot(b_2, 2)[0]
        if a ** 2 - b ** 2 == n:
            factors_list.append((a-b, a+b))
        if len(factors_list) == k:
            return factors_list

##### demo case #####
from sage.all import random_prime, next_prime, gcd, inverse_mod
m = int(b"darctf{_f3m4t_f4c70r1z4t10n_1s_s0_e4sy}".hex(), 16)
print(m)
p = random_prime(1 << 1024, lbound=1 << 1023)
q = random_prime(1 << 1024, lbound=1 << 1023)
n = p * q
npnq = next_prime(p) * next_prime(q)
e = 0x10001
c = pow(m, e, n)
print(c, n, npnq, sep='\n')
factors_list = fematFactorization(n * npnq, k=2) # 预防分解后对应结果为 n & npnq 而无效

for p1, q1 in factors_list:
    assert p1 * q1 == n * npnq
    p, q = gcd(p1, n), gcd(q1, n)
    assert p * q == n
    phi = (p - 1) * (q - 1)
    try:
        d = inverse_mod(e, phi)
        m = pow(c, d, n)
        print(bytes.fromhex(hex(m)[2:]))
    except Exception as error:
        print("Error:", error)
```

#### n&p.xor.q

> [!question]+ 在 [Math.stackexchange](https://math.stackexchange.com/questions/2087588/integer-factorization-with-additional-knowledge-of-p-oplus-q) 提出了一个问题：
> 
> Given two unknown large primes p and q, can we efficiently factor n=pq if we additionally know p⊕q (bitwise XOR of the primes)?

下面的回答给出了算法思路，大致思路是逐比特判断 $p[:k] \times q[:k] \equiv n[:k] \pmod{2^{k}}$ ，并从 0 开始逐步推导 p,q；但是显然每一步都有两种解，如此计算的复杂度依旧在 $O(2^{\log n})=O(n)$；而 $p \oplus q = t$ 作为一个约束，可以达到剪枝的效果，提高了算法思路的可行性。

提出问题的人也实现了这个算法，并放在了 [xor_factor](https://github.com/sliedes/xor_factor/blob/master/xor_factor.py) 。但是疑似存在一些 bug，来看 [zer0ptsCTF2022-AntiFermat](https://ctftime.org/writeup/32627)：

```python title="chall.py"
from Crypto.Util.number import isPrime, getStrongPrime
from gmpy import next_prime
from secret import flag

# Anti-Fermat Key Generation
p = getStrongPrime(1024)
q = next_prime(p ^ ((1<<1024)-1))
n = p * q
e = 65537

# Encryption
m = int.from_bytes(flag, 'big')
assert m < n
c = pow(m, e, n)

print('n = {}'.format(hex(n)))
print('c = {}'.format(hex(c)))
#n = 0x1ffc7dc6b9667b0dcd00d6ae92fb34ed0f3d84285364c73fbf6a572c9081931be0b0610464152de7e0468ca7452c738611656f1f9217a944e64ca2b3a89d889ffc06e6503cfec3ccb491e9b6176ec468687bf4763c6591f89e750bf1e4f9d6855752c19de4289d1a7cea33b077bdcda3c84f6f3762dc9d96d2853f94cc688b3c9d8e67386a147524a2b23b1092f0be1aa286f2aa13aafba62604435acbaa79f4e53dea93ae8a22655287f4d2fa95269877991c57da6fdeeb3d46270cd69b6bfa537bfd14c926cf39b94d0f06228313d21ec6be2311f526e6515069dbb1b06fe3cf1f62c0962da2bc98fa4808c201e4efe7a252f9f823e710d6ad2fb974949751
#c = 0x60160bfed79384048d0d46b807322e65c037fa90fac9fd08b512a3931b6dca2a745443a9b90de2fa47aaf8a250287e34563e6b1a6761dc0ccb99cb9d67ae1c9f49699651eafb71a74b097fc0def77cf287010f1e7bd614dccfb411cdccbb84c60830e515c05481769bd95e656d839337d430db66abcd3a869c6348616b78d06eb903f8abd121c851696bd4cb2a1a40a07eea17c4e33c6a1beafb79d881d595472ab6ce3c61d6d62c4ef6fa8903149435c844a3fab9286d212da72b2548f087e37105f4657d5a946afd12b1822ceb99c3b407bb40e21163c1466d116d67c16a2a3a79e5cc9d1f6a1054d6be6731e3cd19abbd9e9b23309f87bfe51a822410a62
```

只给出了 c, n，只能够从 p, q 的关系入手。依据素数分布定律，$next\_prime(k)-k$ 应该远小于 k，因而 

$$q = \text{next\_prime}(p \oplus((1\ll 1024) -1)) \approx p \oplus((1\ll 1024) -1) \implies p \oplus q \approx ((1\ll 1024) -1)$$

也即 $t = p\oplus q$ 的高位全为 1；关于低位，我们需要得知具体有多少位不可确认；依据有关[素数间隙](https://en.wikipedia.org/wiki/Prime_gap)的研究，我进行了简单的测试：

```python
def exp():
    """
    随机测试可以发现 p^q 的高 1004 位基本都是 1
    """
    for _ in range(10):
        p = getStrongPrime(1024)
        q = next_prime(p ^ ((1<<1024)-1))
        pxq = p^q
        print(pxq.bit_length(), bin(pxq))
```

观察多轮随机测试输出可以发现，pxq 的高位基本全为 1 符合猜想；第一个不为 0 的数为 **14** 位，因此只需要对低 14 位（或者保险一点使用 15 位）进行遍历填充，使用 [xor_factor](https://github.com/sliedes/xor_factor/blob/master/xor_factor.py) 算法即可。但是，在实际操作中发现没能成功分解；即便之后找答案拿到了 p, q，异或后依旧失败。检查信息后发现 bug：

```python
def factor(n, p_xor_q):
    ...
    PRIME_BITS = int(math.ceil(math.log(n, 2)/2))
    ...
    for k in range(2, PRIME_BITS+1):
    ...
```

在这里，$PRIME\_BITS =\lceil \frac{\log(n)}{2} \rceil$ 是 k 的上限，也即 p, q 的位数；但是作者没有考虑到 p, q 位数差别较大的情况（大概也就是题目的 anti fermat 的含义），这里就是如此：`p.bit_length() == 1022, q.bit_length() == 1024, n.bit_length() == 2045`，这导致 PRIME_BITS == 1023，故而始终无法求解。最简单的方法：

```python
PRIME_BITS = int(math.ceil(math.log(n, 2)/2)) + 1
```

就可以解题了。考虑如何修改的更加鲁棒，例如修改为 

```python
PRIME_BITS = p_xor_q.bit_length()
```

在本题中有效，但是如果 p, q 的高位都全为 1 显然会出问题，因而将他们结合起来好了：

```python
PRIME_BITS = max(p_xor_q.bit_length(), int(math.ceil(math.log(n, 2)/2)))
```

让 AI 封装了一下，预计之后加入 [pyPack](https://github.com/darstib/pyPack) 中去：

```python title="xor_factor.py"
"""Utilities for factoring RSA moduli when p ⊕ q is known.

The implementation follows the branching technique described in ``algo.md`` and
adds a robust bit-length heuristic so that the search is deep enough even when
p and q do not have identical bit lengths.  The core entry point is
``factor_from_xor`` which returns the two prime factors in ascending order.

modified from https://github.com/sliedes/xor_factor/blob/master/xor_factor.py
to xxx by @darstib
"""

import math
from typing import Iterable, Optional, Tuple

__all__ = ["factor_from_xor", "recover_plaintext"]


def _check_congruence(k: int, p: int, q: int, n: int, xored: Optional[int]) -> bool:
    """Check p·q ≡ n (mod 2ᵏ) and optionally p ⊕ q ≡ xored (mod 2ᵏ)."""
    kmask = (1 << k) - 1
    p &= kmask
    q &= kmask
    n &= kmask
    product = (p * q) & kmask
    if product != n:
        return False
    if xored is not None and (p ^ q) != (xored & kmask):
        return False
    return True


def _extend_candidates(k: int, prefix: int) -> Iterable[int]:
    """Yield prefix and prefix with the k-th bit set."""
    kbit = 1 << (k - 1)
    assert prefix < kbit
    yield prefix
    yield prefix | kbit


def _compute_prime_bits(n: int, p_xor_q: int) -> int:
    """Heuristic for the expected prime bit length.

    We combine the classical ceil(log₂(n)/2) estimate with the concrete bit
    length of the xor hint and take the maximum to avoid under-estimating the
    required depth in edge cases (e.g. p ≈ q).
    """
    estimate_from_n = int(math.ceil(math.log(n, 2) / 2)) + 1
    estimate_from_xor = p_xor_q.bit_length()
    return max(estimate_from_n, estimate_from_xor)


def factor_from_xor(n: int, p_xor_q: int) -> Tuple[int, int]:
    """Recover the prime factors (p, q) of n given the xor hint.

    Returns the two primes in ascending order.  Raises ``ValueError`` if the
    search exhausts all candidates without success, which usually indicates the
    xor hint is incorrect or inconsistent with ``n``.
    """
    tracked = {
        (p, q)
        for p in (0, 1)
        for q in (0, 1)
        if _check_congruence(1, p, q, n, p_xor_q)
    }

    max_prime_bits = _compute_prime_bits(n, p_xor_q)

    for k in range(2, max_prime_bits + 1):
        new_candidates = set()
        for prefix_p, prefix_q in tracked:
            for candidate_p in _extend_candidates(k, prefix_p):
                for candidate_q in _extend_candidates(k, prefix_q):
                    cand_p, cand_q = sorted((candidate_p, candidate_q))
                    if _check_congruence(k, cand_p, cand_q, n, p_xor_q):
                        new_candidates.add((cand_p, cand_q))
        tracked = new_candidates
        if not tracked:
            break

    for p, q in tracked:
        if p not in (0, 1) and p * q == n:
            return (p, q) if p <= q else (q, p)

    raise ValueError("Failed to recover RSA factors; check the xor hint.")


def crack_from_xor(n: int, e: int, c: int, p_xor_q: int) -> bytes:
    """Recover the RSA plaintext given n, e, ciphertext c, and p ⊕ q."""
    from Crypto.Util.number import inverse

    p, q = factor_from_xor(n, p_xor_q)
    phi = (p - 1) * (q - 1)
    d = inverse(e, phi)
    m = pow(c, d, n)
    hex_str = hex(m)[2:]
    if len(hex_str) % 2:
        hex_str = "0" + hex_str
    return bytes.fromhex(hex_str)

def _check():
    from Crypto.Util.number import getStrongPrime
    p = getStrongPrime(1024)
    q = getStrongPrime(1024)
    print("gold truth:", p, q)
    pq = p ^ q
    n = p * q
    p_, q_ = factor_from_xor(n, pq)
    assert p_ * q_ == n
    print("pass")
    return (p, q)

```

完整解题代码：

```python title="exp.py"
from Crypto.Util.number import inverse
from xor_factor import factor_from_xor

e = 65537
n = 0x1ffc7dc6b9667b0dcd00d6ae92fb34ed0f3d84285364c73fbf6a572c9081931be0b0610464152de7e0468ca7452c738611656f1f9217a944e64ca2b3a89d889ffc06e6503cfec3ccb491e9b6176ec468687bf4763c6591f89e750bf1e4f9d6855752c19de4289d1a7cea33b077bdcda3c84f6f3762dc9d96d2853f94cc688b3c9d8e67386a147524a2b23b1092f0be1aa286f2aa13aafba62604435acbaa79f4e53dea93ae8a22655287f4d2fa95269877991c57da6fdeeb3d46270cd69b6bfa537bfd14c926cf39b94d0f06228313d21ec6be2311f526e6515069dbb1b06fe3cf1f62c0962da2bc98fa4808c201e4efe7a252f9f823e710d6ad2fb974949751
c = 0x60160bfed79384048d0d46b807322e65c037fa90fac9fd08b512a3931b6dca2a745443a9b90de2fa47aaf8a250287e34563e6b1a6761dc0ccb99cb9d67ae1c9f49699651eafb71a74b097fc0def77cf287010f1e7bd614dccfb411cdccbb84c60830e515c05481769bd95e656d839337d430db66abcd3a869c6348616b78d06eb903f8abd121c851696bd4cb2a1a40a07eea17c4e33c6a1beafb79d881d595472ab6ce3c61d6d62c4ef6fa8903149435c844a3fab9286d212da72b2548f087e37105f4657d5a946afd12b1822ceb99c3b407bb40e21163c1466d116d67c16a2a3a79e5cc9d1f6a1054d6be6731e3cd19abbd9e9b23309f87bfe51a822410a62


def get_pq(n):
    shift = 13
    for lowbit in range(2 ** shift - 1, -1, -1):
        t = (((1 << (1024 - shift)) - 1) << shift) + lowbit
        assert t.bit_length() == 1024
        try:
            p, q = factor_from_xor(n, t)
        except ValueError:
            p = q = None
        if lowbit % (1 << (shift // 2)) == 0:
            print(f"trying lowbit:, {bin(lowbit >> (shift // 2))} => {p, q}")
        if p and q and p * q == n:
            return p, q, t
    
    assert False, 'factors were not in tracked set. Is your p^q correct?'

def get_msg():     
    p, q, hint = get_pq(n)
    print(p, p.bit_length())
    print(q, q.bit_length())
    phi = (p-1) * (q-1)
    d = inverse(e, phi)
    m = pow(c, d, n)
    hex_m = hex(m)[2:]
    if len(hex_m) % 2:
        hex_m = '0' + hex_m
    msg = bytes.fromhex(hex_m)
    return msg

msg = get_msg()
print(msg.decode())
# +-----------------------------------------------------------+
# | zer0pts{F3rm4t,y0ur_m3th0d_n0_l0ng3r_w0rks.y0u_4r3_f1r3d} |
# +-----------------------------------------------------------+
```

> [!extra]- 当然我上面的求解大概是一个非预期解，[官方题解](https://ctftime.org/writeup/32627)的思路是
> 
> 考虑 `q = next_prime(p ^ ((1<<1024)-1)) ≈ p^((1<<1024)-1) = (1<<2024) -p -1`，带入 $n = p*q$，解得
> 
> $$
> p\approx\frac{(1\ll1024)+\sqrt{(1\ll1024)^2-4n}}2
> $$
> 
> 求解后只是近似值，取 next_prime(p)，即可得到 p。

#### part p.xor.q

但如果我们 $t = p \oplus q$ 的未知部分不适合爆破呢？看 [starctf2022 - ezRSA](https://github.com/sixstars/starctf2022/tree/main/crypto-ezRSA) ：

```python title="https://github.com/sixstars/starctf2022/blob/main/crypto-ezRSA/chall.py"
from Crypto.Util.number import getStrongPrime
from gmpy import next_prime
from random import getrandbits
from flag import flag

p=getStrongPrime(1024)
q=next_prime(p^((1<<900)-1)^getrandbits(300))
n=p*q
e=65537

m=int(flag.encode('hex'),16)
assert m<n
c=pow(m,e,n)

print(hex(n))
#0xe78ab40c343d4985c1de167e80ba2657c7ee8c2e26d88e0026b68fe400224a3bd7e2a7103c3b01ea4d171f5cf68c8f00a64304630e07341cde0bc74ef5c88dcbb9822765df53182e3f57153b5f93ff857d496c6561c3ddbe0ce6ff64ba11d4edfc18a0350c3d0e1f8bd11b3560a111d3a3178ed4a28579c4f1e0dc17cb02c3ac38a66a230ba9a2f741f9168641c8ce28a3a8c33d523553864f014752a04737e555213f253a72f158893f80e631de2f55d1d0b2b654fc7fa4d5b3d95617e8253573967de68f6178f78bb7c4788a3a1e9778cbfc7c7fa8beffe24276b9ad85b11eed01b872b74cdc44959059c67c18b0b7a1d57512319a5e84a9a0735fa536f1b3

print(hex(c))
#0xd7f6c90512bc9494370c3955ff3136bb245a6d1095e43d8636f66f11db525f2063b14b2a4363a96e6eb1bea1e9b2cc62b0cae7659f18f2b8e41fca557281a1e859e8e6b35bd114655b6bf5e454753653309a794fa52ff2e79433ca4bbeb1ab9a78ec49f49ebee2636abd9dd9b80306ae1b87a86c8012211bda88e6e14c58805feb6721a01481d1a7031eb3333375a81858ff3b58d8837c188ffcb982a631e1a7a603b947a6984bd78516c71cfc737aaba479688d56df2c0952deaf496a4eb3f603a46a90efbe9e82a6aef8cfb23e5fcb938c9049b227b7f15c878bd99b61b6c56db7dfff43cd457429d5dcdb5fe314f1cdf317d0c5202bad6a9770076e9b25b1
```

只给出了 c, n，同样只能够从 p, q 的关系入手：由于

```py
p=getStrongPrime(1024)
q=next_prime(p^((1<<900)-1)^getrandbits(300))
```

我们可以得到的消息有（注意 python 中 `^` 是异或）：

- p, q 均为 1024 位
- $t = p \oplus q$ 
	- t 的高 124 位全为 0，即 p, q 高位相同，可以通过对 n 开方求得；
	- t 的中间 600 位全为 1，即 p, q 中间相反，考虑探索剪枝；这里的剪枝参考了[官方题解](https://github.com/sixstars/starctf2022/blob/main/crypto-ezRSA/exp.sage)，即先按照符合约束的情况进行初始化，随后从高位开始，用 $p*q \leq n$ 来决定是否都要进行 bit 翻转（不过这应该仅限于 $p \oplus q$ 对应 bit 位为 1 才可以使用）
	- t 的低 300 位随机，没有信息，等待使用 [Known High Bits Attack](#Known%20High%20Bits%20Attack) 攻击。

```python title="exp.py"
import gmpy2
from sage.all import *
e=65537
c = 0xd7f6c90512bc9494370c3955ff3136bb245a6d1095e43d8636f66f11db525f2063b14b2a4363a96e6eb1bea1e9b2cc62b0cae7659f18f2b8e41fca557281a1e859e8e6b35bd114655b6bf5e454753653309a794fa52ff2e79433ca4bbeb1ab9a78ec49f49ebee2636abd9dd9b80306ae1b87a86c8012211bda88e6e14c58805feb6721a01481d1a7031eb3333375a81858ff3b58d8837c188ffcb982a631e1a7a603b947a6984bd78516c71cfc737aaba479688d56df2c0952deaf496a4eb3f603a46a90efbe9e82a6aef8cfb23e5fcb938c9049b227b7f15c878bd99b61b6c56db7dfff43cd457429d5dcdb5fe314f1cdf317d0c5202bad6a9770076e9b25b1
n = 0xe78ab40c343d4985c1de167e80ba2657c7ee8c2e26d88e0026b68fe400224a3bd7e2a7103c3b01ea4d171f5cf68c8f00a64304630e07341cde0bc74ef5c88dcbb9822765df53182e3f57153b5f93ff857d496c6561c3ddbe0ce6ff64ba11d4edfc18a0350c3d0e1f8bd11b3560a111d3a3178ed4a28579c4f1e0dc17cb02c3ac38a66a230ba9a2f741f9168641c8ce28a3a8c33d523553864f014752a04737e555213f253a72f158893f80e631de2f55d1d0b2b654fc7fa4d5b3d95617e8253573967de68f6178f78bb7c4788a3a1e9778cbfc7c7fa8beffe24276b9ad85b11eed01b872b74cdc44959059c67c18b0b7a1d57512319a5e84a9a0735fa536f1b3
# 用 n 的高 248 位来进行开根
top_bits = int(gmpy2.isqrt(n>>(2048-248)))
assert top_bits.bit_length() == 124
# print("top_bits:", hex(top_bits))
p_ = (top_bits << 900) + (1<<900) -1
q_ = (top_bits << 900)
assert p_.bit_length() == q_.bit_length() == 1024
for i in range(899, 301, -1):
    bit = 1 << i
    if (p_^bit)*(q_^bit) <= n:
        # swap p_ & q_ bit
        p_^=bit
        q_^=bit

# print("p:", hex(p))
# print("q:", hex(q))
# 0xf376c68d76f4ab9b4d247852ef07159a09eeac920ac89148a8dee4f3c359a291b6bf03ab9258ca64783c416fcfeade13cf3c18a7677c29283c7fc6bfcdbba1d6fecbe9e243cc2e3ef0fe60035e1dbc727f3522bfab2bc28d5e29bfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff
# 0xf376c68d76f4ab9b4d247852ef071595f611536df5376eb757211b0c3ca65d6e4940fc546da7359b87c3be90301521ec30c3e7589883d6d7c380394032445e290134161dbc33d1c10f019ffca1e2438d80cadd4054d43d72a1d64000000000000000000000000000000000000000000000000000000000000000000000000000
shift = 450 # 这个 shift 还挺重要的，多了少了都解不出来
p_ = p_ >> shift << shift
def get_pq(p_high, n):
    # print(hex(p_high))
    x = Zmod(n)['x'].gen()
    # x = PolynomialRing(Zmod(n), "x").gen()
    f=x+p_high
    roots=f.small_roots(X=2**shift,beta=0.4)
    if roots:
        p=int(f(roots[0]))
        assert n%p==0
        q = n//p
        return (p, q)
    return None

p, q = get_pq(p_, n)
phi = (p-1) * (q-1)
d = inverse_mod(e, phi)
m = power_mod(c, d, n)
print(bytes.fromhex(hex(m)[2:]))
# b'*CTF{St.Diana_pls_take_me_with_you!}'
```

### other hint

当泄露以下信息 (l) 时的技巧

- $l = (p+q)^2 \pmod{n}$ 【 [Moectf-ez_square](https://ctf.xidian.edu.cn/training/22?challenge=905) 】
	- 由于 l 一定小于 n，变形后可知 $l = (p-q)^2$ 
	- $p-q = \sqrt{l}, p+q = \sqrt{(p-q) + 4*n}$
- $l=p^2+q^2$，且不知道 n 【[[国城杯 2024]EZ_sign](https://seandictionary.top/%E5%9B%BD%E5%9F%8E%E6%9D%AF-2024-crypto/)】
	- 平方和分解不唯一，sagemath 的 `two_squares` 只能得到一种结果，不一定正确
	- $(p+qi)(p-qi)=C$
		```python title="get_pq.sage"
		def get_pq(C):
		    """
		    p^2 + q^2 = C
		    """
		    f = ZZ[I](C)
		    divisors_f = divisors(f)
		    for d in divisors_f:
		        a,b = d.real(), d.imag()
		        if a**2 + b**2 == C:
		            p = abs(int(a))
		            q = abs(int(b))
		            if is_prime(p) and is_prime(q):
		                return (p, q)
		```
- $l_{1} = p^q \pmod{n}, l_{2} = q^p \pmod{n}$，且不知道 n 【[[HGAME 2024]ezRSA](https://seandictionary.top/hgame-2024/)】
	- 易得 $p^q \equiv p \pmod{p}, p^q \equiv p \pmod{q}$
	- 由中国剩余定理可得 $l_{1} = p = p^q \pmod{n}$
	- 同理 $l_{2} = q$

#### RSA backdoor (4p-1 method)

攻击条件：$4p-1 = Ds^2$ 其中 Ds 参见 [cm_factorization](https://github.com/crocs-muni/cm_factorization) 。

## Private key attack

### d leak

当对应的 (e,d) 泄露后，我们就能够分解对应的 N 。具体原理可见 [ctf-wiki](https://ctf-wiki.org/crypto/asymmetric/rsa/d_attacks/rsa_d_attack/#d_1) 。

> [!quote] 
> 
> [rsatool](https://github.com/ius/rsatool) calculates RSA (p, q, n, d, e) and RSA-CRT (dP, dQ, qInv) parameters given either two primes (p, q) or modulus and private exponent (n, d).

> [!QUESTION]
>
> [cryptohack - Crossed Wires](https://cryptohack.org/challenges/rsa/)

```python
# rsatool 分解得到
p  = 0xbf7a6a86c980cbc7ff358a92b7b0828106b6ad75122c42b9c05cfb0f1b08205903e54381a323b3c2dfc6a6adb0771dbdf61185405ec7e1de5614cdfa71c6b5cd320d0a6bc40379592088a794b0ead8cc012a38ca57daaed140c42c634736eee8fe268bac6ab814b1e769dc1bade805160da940b0813b145df9b7a97e7ca4e0eb

q = 0xe5f0c56af9d879da10d5b7f09153716469faced27adf10a8c69847e2460767d316048b95087bf1102278ca070e2fb81ac367aae538980ad0cbd438ffac3673c9b8898a24209d896723a9b08e919a6cbfff761cb8218df0d1f6f56414ba245ad17581d96bca6679b3fa7a2a7d2306ad99c1749864cd85b3390aaddef33e8c73b9

n = p*q
phi = (p-1)*(q-1)
c = 20304610279578186738172766224224793119885071262464464448863461184092225736054747976985179673905441502689126216282897704508745403799054734121583968853999791604281615154100736259131453424385364324630229671185343778172807262640709301838274824603101692485662726226902121105591137437331463201881264245562214012160875177167442010952439360623396658974413900469093836794752270399520074596329058725874834082188697377597949405779039139194196065364426213208345461407030771089787529200057105746584493554722790592530472869581310117300343461207750821737840042745530876391793484035024644475535353227851321505537398888106855012746117
friends_key = [...]
phi = (p-1)*(q-1)
from Crypto.Util.number import inverse, long_to_bytes
for key in friends_key[::-1]:
    e = key[1]
    d = inverse(e, phi)
    c = pow(c, d, N)
long_to_bytes(c) # b'crypto{3ncrypt_y0ur_s3cr3t_w1th_y0ur_fr1end5_publ1c_k3y}'
```

### dp || dq leak

> [!definition] dp/dq
>
> $dp \equiv d\pmod{p-1}, dq \equiv d\pmod{q-1}$

攻击条件：知道 dp 或者 dq，完整的公钥 (n,e) 和密文 c。
攻击原理：$p = \frac{edp-1}{i}+1, i \in[1, e]$ ，推导省略，只要 p 是整数且整除 n 即符合条件：

```python title="demo_dp_leak"
from Crypto.Util.number import getPrime
m = int.from_bytes(b'darctf{wow_leaking_dp_breaks_rsa?}')
p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = 0x10001
c = pow(m,e,n)
phi = (p-1)*(q-1)
d = pow(e,-1,phi)
dp = d % (p-1)
print(dp, n, e, c)

"""solve"""
def dp_attack(dp, n, e):
    for i in range(1,e):
        if (dp*e-1)%i==0 and n%(((dp*e-1)//i)+1)==0:
            return ((dp*e-1)//i)+1

p = dp_attack(dp, n, e)
q = n//p
phi = (p-1)*(q-1)
d = pow(e,-1,phi)
m = pow(c,d,n)
print(bytes.fromhex(hex(m)[2:]))
```

> [!note] 改进的解法：

上面是最常见的出题方法，[那要是 e 很大呢](https://tover.xyz/p/2024-HSCTF-babyDP/)：

```python title="2024-HSCTF-babyDP-chall.py"
from secret import flag
import libnum

bits = 1024
p, q = [random_prime(2**bits) for _ in range(2)]
n = p * q
e = 2*10**76-3
d = e.inverse_mod((p-1) * (q-1))
dp = d % (p-1)

m = libnum.s2n(flag)
c = pow(m, e, n)

print('e  = %d' % e)
print('n  = %d' % n)
print('dp = %d' % dp)

print('c  = %d' % c)

'''
e  = 19999999999999999999999999999999999999999999999999999999999999999999999999997
n  = 7195506839435218889565105541674965483194164483027741709706696451513641438345177472634371310250998546706062462270851552911697354605048972081656931006641878545036542923897114647393564522132057589249800431430995780074871171268958056358251827104531889348948541240686274977093185746573748206617663459128090693743840574459752890533065398493485714768878646999590143805843490432318539260302521682823958290340460403361801534822098048095280034600065200137857346827560676300256938953222718633375808719441534702981763523406056651752914141143665893462943582116716812913462656214604870428310720751101481210148746546806273965485289
dp = 34961801811050613471700883525108632060492526395401334090302835931304663757529660746363964830407055340550990256271716811099606849841913560556222756478612800702209651907866303152581107449312861896692310607989826809665245295483724533775337076019316812377921373194504440845718347150919782506437242366281376701299
c  = 3014636373048664939954772778404195986026862165799593915685719641505606570670923436003664110094703916031096486273947905494103538805486521321522443488182065845367347589071783679908494724693530639371358965655992560909299314626568439587755874253430614726720724608456333450258184012429367293386944954388615812902809362326474915645899324083994448117282677622943580354006160302366855350193039875335543211982510928721395526768129547143054319585071252781483346116972611571317425047748862917945459911485505200762492537496489429730213393936533514665994680707861503489288913062785427211743828345144957201996243444547648085230048
'''
```

事实上，已知 dp/dq 足够分解 n 了，因为：$\forall c = m^e\%n, m \equiv c^{d_{p}} \pmod{p} \implies c^{d_{p}}-m = kp \implies p = gcd(n, c^{d_{p}}-m)$:

```python
n  = ...
dp = ...

m = 1997
c = pow(m, e, n)
p = gcd(pow(c, dp, n) - m, n)
assert n % p == 0
```

[这里](https://tover.xyz/p/2024-HSCTF-babyDP/#%E6%80%9D%E8%B7%AF)还给了一种使用 Coppersmith 求小根的思路，按下不表。

### dp && dq leak

攻击条件：知道 dp, dp, p, q, c。
攻击原理：crt 求解 d。

```python title="dpq_leak"
from sage.all import crt

p = 8637633767257008567099653486541091171320491509433615447539162437911244175885667806398411790524083553445158113502227745206205327690939504032994699902053229 
q = 12640674973996472769176047937170883420927050821480010581593137135372473880595613737337630629752577346147039284030082593490776630572584959954205336880228469 
dp = 6500795702216834621109042351193261530650043841056252930930949663358625016881832840728066026150264693076109354874099841380454881716097778307268116910582929 
dq = 783472263673553449019532580386470672380574033551303889137911760438881683674556098098256795673512201963002175438762767516968043599582527539160811120550041 
c = 24722305403887382073567316467649080662631552905960229399079107995602154418176056335800638887527614164073530437657085079676157350205351945222989351316076486573599576041978339872265925062764318536089007310270278526159678937431903862892400747915525118983959970607934142974736675784325993445942031372107342103852

def dpq_attack(p,q,dp,dq):
    return crt([dp,dq],[p-1,q-1])
d = dpq_attack(p,q,dp,dq)
n=p*q
m=pow(c,d,n)
bytes.fromhex(hex(m)[2:])
```

### dp && dq && dr leak attack

攻击条件：

$$
n = p*q*r, \begin{cases}
dp = d\pmod{(q-1)*(r-1)} \\
dq = d\pmod{(p-1)*(r-1)} \\
dr = d\pmod{(p-1)*(q-1)}
\end{cases}, 且已知 p,q,r,dp,dq,dr
$$

还是一样的 crt？中国剩余定理要求模数互质；扩展中国剩余定理可以一定程度上解决这一问题（并非一定可行）

```python title="chall.py"
"""
import gmpy2
from Crypto.Util.number import *

p = getPrime(512)
q = getPrime(512)
r = getPrime(512)
e = getPrime(32)
print(e)
n = p*q*r
phi = (p-1)*(q-1)*(r-1)
d = gmpy2.invert(e,phi)
dp = d%((q-1)*(r-1))
dq = d%((p-1)*(r-1))
dr = d%((p-1)*(q-1))
flag = 'flag{XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX}'
m = bytes_to_long(flag.encode())
c = pow(m,e,n)

print(p)
print(q)
print(r)
print(dp)
print(dq)
print(dr)
print(c)
"""

from sage.all import crt, CRT_list, gcd

p=12922128058767029848676385650461975663483632970994721128398090402671357430399910236576943902580268365115559040908171487273491136108931171215963673857907721
q=10395910293559541454979782434227114401257890224810826672485874938639616819909368963527556812339196570118998080877100587760101646884011742783881592586607483
r=8104533688439480164488403019957173637520526666352540480766865791142556044817828133446063428255474375204188144310967625626318466189746446739697284656837499
dp=73360412924315743410612858109886169233122608813546859531995431159702281180116580962235297605024326120716590757069707814371806343766956894408106019058184354279568525768909190843389534908163730972765221403797428735591146943727032277163147380538250142612444372315262195455266292156566943804557623319253942627829
dq=40011003982913118920477233564329052389422276107266243287367766124357736739027781899850422097218506350119257015460291153483339485727984512959771805645640899525080850525273304988145509506962755664208407488807873672040970416096459662677968243781070751482234692575943914243633982505045357475070019527351586080273
dr=21504040939112983125383942214187695383459556831904800061168077060846983552476434854825475457749096404504088696171780970907072305495623953811379179449789142049817703543458498244186699984858401903729236362439659600561895931051597248170420055792553353578915848063216831827095100173180270649367917678965552672673
c=220428832901130282093087304800127910055992783874826238869471313726515822196746908777026147887315019800546695346099376727742597231512404648514329911088048902389321230640565683145565701498095660019604419213310866468276943241155853029934366950674139215056682438149221374543291202295130547776549069333898123270448986380025937093195496539532193583979030254746589985556996040224572481200667498253900563663950531345601763949337787268884688982469744380006435119997310653
```

计算模数间两两之间最大公因数，作为新的模数求解中国剩余定理：

```python title="solve1.py"
M1 = (q - 1)*(r -1)
M2 = (p -1)*(r -1)
M3 = (p -1)*(q -1)

G12 = gcd(M1, M2)
G13 = gcd(M1, M3)
G23 = gcd(M2, M3)

# 检查同余方程是否有解
if (dp - dq) % G12 != 0 or (dp - dr) % G13 != 0 or (dq - dr) % G23 != 0:
    print("同余方程无解")
else:
    d = crt([dp, dq, dr], [M1, M2, M3])
    m = pow(c, d, p * q * r)
    print(bytes.fromhex(hex(m)[2:]))
```

sagemath 中内置了 `CRT_list` 方法可以求解模数不互质的情况：

```python title="solver2.py"
d = CRT_list([dp,dq,dr],[(q-1)*(r-1),(p-1)*(r-1),(p-1)*(q-1)])
m = pow(c,d,p*q*r)
bytes.fromhex(hex(m)[2:]) # b'DASCTF{8ec820e5251db6e7a1758543a1123824}'
```

### Wiener's Attack

维纳攻击，攻击条件：e 较大，$d< \frac{1}{3}N^{1/4}, q<p<2q$ 。

> [!info]+ 在[代入 Wiener](https://tover.xyz/p/LLL-attack-equation/#Wiener%E6%94%BB%E5%87%BB) 中 tover 表示：
> 
> -  $ed^2\lessapprox\frac12N^{3/2}$ 时即可
> - 可以使用格完成 Wiener's attack

原理简述：由于 $ed \equiv 1\pmod{\phi(n)} \implies ed = k*\phi + 1$ ，当 n 较大时，$ed \approx k*\phi \approx k*n\implies \frac{e}{n} \approx \frac{k}{d}$  ；利用连分数从两侧逼近于极限值的特点，找到真正的 d & k ；甚至我们求解 $\phi$ 后能够分解出 p/q 。 

> [!extra]- 阈值分析
>
>> [!theorem] Legendre's theorem
>> 
>> 如果存在 $\alpha \in Q$, $c,d \in Z$: $|\alpha- \frac{c}{d}|< \frac{1}{2d^2}$，那么 $\frac{c}{d}$ 就是 $\alpha$ 的一个有理近似。
>  
> $ed = k*\phi + 1 \implies | \frac{e}{\phi}- \frac{k}{d}|= \frac{1}{d*\phi}$
> 
> 大部分情况下，构成 $n=p*q$ 公式中，p 与 q 的二进制长度相同，即有 $p < q < 2*p$ （p q 可互换位置）；由适当推导可以得到 $d< \frac{1}{3}N^{1/4} \implies (3d)^4 < n$

> [!help] 攻击代码可以使用 [crypto-attacks/attacks/rsa/wiener_attack.py](https://github.com/jvdsn/crypto-attacks/blob/master/attacks/rsa/wiener_attack.py) ，下面是一个使用示例：

```python title="wiener_attack.py"
import os
import sys

from sage.all import ZZ
from sage.all import continued_fraction

path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(os.path.abspath(__file__)))))
if sys.path[1] != path:
    sys.path.insert(1, path)

from attacks.factorization import known_phi

def attack(N, e):
    """
    Recovers the prime factors of a modulus and the private exponent if the private exponent is too small.
    :param N: the modulus
    :param e: the public exponent
    :return: a tuple containing the prime factors and the private exponent, or None if the private exponent was not found
    """
    convergents = continued_fraction(ZZ(e) / ZZ(N)).convergents()
    for c in convergents:
        k = c.numerator()
        d = c.denominator()
        if pow(pow(2, e, N), d, N) != 2:
            continue

        phi = (e * d - 1) // k
        factors = known_phi.factorize(N, phi)
        if factors:
            return *factors, int(d)

# set the value we need to know
n = 10117654819914858266933329374955416887632623769133893090370644563766857602175135282123557069130319485164837923640109707980173187311717714731455048711732890650502393864146567993461691536083330111489342144526034765633893707639465391971659424271400604010051260552831236934617979897198594708643604050329358522040572553492557329327193918343289526476096522685686128709365882540965089876020772451339243051387630968483513100881164719486794479191020450727996212211201807165531274853014517030221518336293845148545671493267736094904720639061287350709209363413742534108909427583009442175135992281621755221466312230819838164838443
e = 9821176723459156737162590528498355378679103255669217165700920581299681706733929195884953659518540987340485400582895899813962495604183457377106880733695051072483080763292039235986138262683331839202120494074112671026731661652894069539798773005571447249078493499067926710777981456836165288713067372341722891618455469381820299718375899142104630769808052209736800306823537530231432735329122809506084509365041929994661643608897946882821172042151091436805833261237973879388223150132281413026451714557979869417700194664385291198650864896408143681530963859508908402067374010247738488460155501935400209160082801993945408813513
c = 838279327100183842450828959704405383407020841408916285706333834213457887909003957632210005175559669378601653437817015283864372967567045814324446631403131762020243676699045950634510503063630325940620012467503745448306616066932850616255337850567483377961974904557893440882626053258665407295455129124436515237709284339335286446533668177967589716697626618148973094630870394728363810896842456940427809475399274556698585866672673971202275767545143765482579343055060966723452080734906835537296838390574697520016738791840483248208135607782781572593502322902003706653541803004568389346187087997006034664608287414331955367370
p, q, d = attack(n, e)
m = pow(c, d, n)
print(m)
print(bytes.fromhex(hex(m)[2:])) # b"SKSEC{Do_y0u_Kn0w_Wi3n3r's_4ttack}"
```

> [!EXAMPLE]+
>
> - [[CISCN 2022 东北赛区]math](https://www.nssctf.cn/problem/2387)

### Boneh and Durfee attack

攻击条件：$d<N^{0.292}$

先来看 cryptohack 上的 `Everything is Still Big` 

```python title="task.py"
#!/usr/bin/env python3

from Crypto.Util.number import getPrime, bytes_to_long, inverse
from random import getrandbits
from math import gcd

FLAG = b"crypto{?????????????????????????????????????}"

m = bytes_to_long(FLAG)

def get_huge_RSA():
    p = getPrime(1024)
    q = getPrime(1024)
    N = p*q
    phi = (p-1)*(q-1)
    while True:
        d = getrandbits(512)
        if (3*d)**4 > N and gcd(d,phi) == 1:
            e = inverse(d, phi)
            break
    return N,e


N, e = get_huge_RSA()
c = pow(m, e, N)

print(f'N = {hex(N)}')
print(f'e = {hex(e)}')
print(f'c = {hex(c)}')
```

很特别的要求 `(3*d)**4 > N` ，把 Wiener-attack 禁用了；但是有更强的攻击 Boneh and Durfee attack ($d<N^{0.292}$)

> [!tip]- 
> 
> - [ctf-wiki - Boneh and Durfee attack](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/?h=boneh+durfee#boneh-and-durfee-attack)
> - [boneh_durfee.sage](https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage)

```python title="exp.py"
d = 4405001203086303853525638270840706181413309101774712363141310824943602913458674670435988275467396881342752245170076677567586495166847569659096584522419007
N = 0xb12746657c720a434861e9a4828b3c89a6b8d4a1bd921054e48d47124dbcc9cfcdcc39261c5e93817c167db818081613f57729e0039875c72a5ae1f0bc5ef7c933880c2ad528adbc9b1430003a491e460917b34c4590977df47772fab1ee0ab251f94065ab3004893fe1b2958008848b0124f22c4e75f60ed3889fb62e5ef4dcc247a3d6e23072641e62566cd96ee8114b227b8f498f9a578fc6f687d07acdbb523b6029c5bbeecd5efaf4c4d35304e5e6b5b95db0e89299529eb953f52ca3247d4cd03a15939e7d638b168fd00a1cb5b0cc5c2cc98175c1ad0b959c2ab2f17f917c0ccee8c3fe589b4cb441e817f75e575fc96a4fe7bfea897f57692b050d2b
c = 0xa3bce6e2e677d7855a1a7819eb1879779d1e1eefa21a1a6e205c8b46fdc020a2487fdd07dbae99274204fadda2ba69af73627bdddcb2c403118f507bca03cb0bad7a8cd03f70defc31fa904d71230aab98a10e155bf207da1b1cac1503f48cab3758024cc6e62afe99767e9e4c151b75f60d8f7989c152fdf4ff4b95ceed9a7065f38c68dee4dd0da503650d3246d463f504b36e1d6fafabb35d2390ecf0419b2bb67c4c647fb38511b34eb494d9289c872203fa70f4084d2fa2367a63a8881b74cc38730ad7584328de6a7d92e4ca18098a15119baee91237cea24975bdfc19bdbce7c1559899a88125935584cd37c8dd31f3f2b4517eefae84e7e588344fa5

m = pow(c, d, N)
print(bytes.fromhex(hex(m)[2:])) # b'crypto{bon3h5_4tt4ck_i5_sr0ng3r_th4n_w13n3r5}'
```

### Extended Wiener's attack

当 d 略大于 Boneh and Durfee attack 的攻击条件（如 $d\approx N^{0.293}$）时，前面描述的攻击都将失效；但是如果此时这样的 d 不止一个，我们似乎又有了可以利用的余地，延伸出[扩展维纳攻击](https://ctf-wiki.org/crypto/asymmetric/rsa/d_attacks/rsa_extending_wiener)；基于 ctf-wiki 和 [_Extending Wiener’s Attack in the Presence of Many Decrypting Exponents_](https://dunkirkturbo.github.io/2020/05/04/WriteUp-De1CTF2020-Crypto/howgrave-graham1999.pdf) ，可以编写已知 2/3/4 个小 d 对应的 e 的情况下的 sagemath 脚本（放在 [Gist](https://gist.github.com/darstib/49d9ced26c50c2641972ebf4f59fe7d1) 上了）。

具体需要几组取决于 d 相对 N 的大小，[如表所示](https://huangx607087.online/2021/03/01/LatticeNotes6/#4-3D-4D-Expand-WienerAttack)：

$$
\begin{array}{|c|c|c|c|c|c|c|c|c|c|}\hline n&1&2&3&4&5&6&\geq7\\\hline\frac{\ln d}{\ln n}&0.25&0.357&0.4&0.441&0.468&0.493&0.5\\\hline\end{array}
$$

---

来看 moectf 2025 上的一道 [wiener++](https://ctf.xidian.edu.cn/training/22?challenge=981) 题，题面如下：

```python title="wiener++.py"
from Crypto.Util.number import *
from secret import flag

m = bytes_to_long(flag)
p = getPrime(1024)
q = getPrime(1024)
phi = (p-1)*(q-1)
E = []
for i in range(3):
    E.append(pow(getPrime(600),-1,phi))  
n = p*q
e = 65537
c = pow(m,e,n)
print(f'E = {E}')
print(f'c = {c}')
print(f'n = {n}')
"""
E = [6535354858431850852882901159552069642652745264375395319401872291559383432177438285988364127472613549365509820935925577361414464075764640533208334665987592109205997966463551882468734344050074283602043327838642976610275755119106168019918564063715435876334390534614689273949767994713168344350212980200133843053996291542940897549076525747071976992346914997811867133598974772513201381446388313238061416275364774924879724623269275665955247476790410755454726735472729022234802527690839198476806961518389403284927512824802658120648166827671254702373707128253843009043343574820976133354679456691450195111421331838281980791169, 521740717797571328928542404746379489096681606296105709448001512801594188896794342910355692394114530313434027423805653128165121456821386005483234429465641848647231537545838107252519841836568394320914726188097536963645943740347602217310772591525035163575052097127250480550907254287152638159351757425050079034153320658804563142684053234861691610577439191450390837819069924806441572660111002277302472455857154076563710145258049404077025429614021344906361972885981934904848504701502497235325466136083457136074450313163397641812912247912853463291040073062853345391031149063654983069868879608400357250959694496146579685451, 8911805261833830474004605259907370605807913822533492645509364142094890565950914302571054903181099150347283987131973548407729373207539140949793938540351210310484507151010644704903841608034912618537032004944897772587351902872171465767156632786417718010302417945824640353543336103022123477513493841427508247924758472122357830026975916981381121237555468719061263601411254700854117936657411984123602591805427708008566595616753092377705022452331809886048933193760019801687147365544765265412906882965454515613718524542064373022515540363942939377959932432943637382868458666514763671495031622571616696370398455908620153043919]
c = 6753155979488207369146877527563962489798459549318070923366033245920698810626960872130015507640079255967883699975637707573487421437682484657575346378258338966332206545439810503073328798748741132167015894650686768925239854863550203205724604895839456517875108542083858900948587934359333734716352762480295451652976617660823153097682212487885039311354081578869472189112818410420202093044127626917233949906728334691001613133349724175401388010902496533739535048147542837664443019380587362527652958368440203848684943761090115145949772541171220588682127280853035360547963393464562446348630721098472522627580664983812781660775
n = 13574881868338582214480395446670580940012507548374450902518317364375475722668157493607158810724244896266071642370444779252115446641944766507717015889181393406304349721002246334571932443491014007813032684284177348256442664560920714698180362225066349458599934259487635040453190554685942293568882945035152595000888123888791436446731739856349561654337315238581318196198972142582551083105737178416447194992839881126339173823749783111704949164881364240077721677409809320748025824802169248149833407214474947847788378002642917634973813614056523994315689432930551129372591378019659084153696307545609036884627279543075621209259
"""

```

攻击脚本如下：

```python title="exp.sage"
from extended_wiener_attack import ex_wa
E = []
c = ...
n = ...
e = 65537

phi = ex_wa(n, E)

print(f"[+] phi = {phi}")
factors = factor_from_phi(n, phi)
if factors:
    p, q = factors
    # Verify phi if needed (p-1)*(q-1) should equal phi
    if (p-1)*(q-1) != phi:
        print("[!] Warning: Calculated phi does not match (p-1)*(q-1). This can happen due to g > 1.")
        # We can recalculate phi based on the factors
        phi = (p-1)*(q-1)
    # Decrypt the message
    print("\n[*] Decrypting the message...")
    d = inverse_mod(e, phi)
    m_long = power_mod(c, d, n)
    
    def long_to_bytes(n):
        return bytes.fromhex(hex(n)[2:].rstrip("L"))
    try:
        flag = long_to_bytes(m_long)
        print(f"\n[+] Flag found: {flag.decode()}") # moectf{W1N4er_A@tT@CkRR-R@4ENggeEE|!}
    except Exception as e:
        print(f"[-] Could not decode flag: {e}")
        print(f"    Plaintext as integer: {m_long}")
```

再来看 [NCTF2020-RRRSA](https://huangx607087.online/2021/03/01/LatticeNotes6/#5-%E4%BE%8B%E9%A2%98-2020NCTF-RRRSA)：

```python title="RSA.py"
#RSA.py
from Crypto.Util.number import getPrime, getRandomNBitInteger, GCD, inverse
lcm = lambda x, y: x*y // GCD(x,y)
class RSA():
    def __init__(self, bits):
        p = getPrime(bits//2)
        q = getPrime(bits//2)
        self.N = p * q
        self.lbd = lcm(p-1, q-1)
        self.gen_ed(bits)
    def gen_ed(self, bits):
        while True:
            d = getRandomNBitInteger(int(bits*0.4))
            if GCD(d, self.lbd) == 1:
                e = inverse(d, self.lbd)
                self.e, self.d = e, d
                break
    def encrypt(self, m):
        return pow(m, self.e, self.N)
    def decrypt(self, c, d):
        return pow(c, d, self.N)
```

```python title="task.py"
#task.py
from random import choice
from hashlib import sha256
from string import ascii_letters, digits
from RSA import RSA
from secret import FLAG
MENU = """
1. encrypt
2. decrypt
3. newkey
4. encflag
5. exit"""
def proof_of_work():
    proof = ''.join([choice(ascii_letters+digits) for _ in range(20)])
    _hexdigest = sha256(proof.encode()).hexdigest()
    print(f"sha256(XXXX+{proof[4:]}) == {_hexdigest}")
    try:
        prefix = input("Give me XXXX: ")
    except:
        print("Error!")
        exit(-1)
    return sha256((prefix+proof[4:]).encode()).hexdigest() == _hexdigest
def task():
    CHANCE = 1
    RRRSA = RSA(1024)
    print(f"My public key: {RRRSA.e}, {RRRSA.N}")
    for _ in range(10):
        try:
            print(MENU)
            choice = input("Your choice: ")
            if choice == "1":
                m = int(input("Your message: "))
                c = RRRSA.encrypt(m)
                print(f"Your cipher: {c}")
            elif choice == "2":
                c = int(input("Your message: "))
                d = int(input("Your decryption exponent: "))
                m = RRRSA.decrypt(c, d)
                print(f"Your message: {m}")
            elif choice == "3":
                RRRSA.gen_ed(1024)
                print(f"My new public key: {RRRSA.e}, {RRRSA.N}")
            elif choice == "4":
                if CHANCE:
                    CHANCE -= 1
                    flag = int.from_bytes(FLAG, 'big')
                    encflag = RRRSA.encrypt(flag)
                    print(f"encflag: {encflag}")
                else:
                    print("Nope, only 1 chance to get encflag.")
            else:
                print("Bye!")
                exit(0)
        except Exception as e:
            print(e)
            print("Error!")
            exit(-1)
if __name__ == "__main__":
    if proof_of_work():
        task()
```

显然这里 $\frac{\ln d}{\ln n} = 0.4$，使用 4 个 e 能够尝试恢复 phi；但这里其实还有个问题 `e = inverse(d, self.lbd)`，使用 $\lambda(n) = lcm(p-1, q-1)$ 当 $\varphi(n)=(p-1)*(q-1)$ 用，还能这么干吗？（从参考的题解来说确实可以，暂时挖坑吧 #todo ）。

### common d

```python title="task.py"
from Crypto.Util.number import *

flag = b'darctf{xxxxxxxxxxxxxxxxxxx}'
flag = bytes_to_long(flag)
d = getPrime(400)

for i in range(4):
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    e = inverse(d, (p-1)*(q-1))
    c = pow(flag, e, n)
    print(f'e{i} =', e)
    print(f'n{i} =', n)
    print(f'c{i} =', c)

'''
e0 = 23844114241409164386809132218388868354264029199272891084709234309724158242864996012783905462475537573245862803694757748895957177908141041413116255316724561208736642617470467078478619042140268786586183895211481564391111178698452245307025651226211909103256546806557759885095799788351100191348777600339651478591
n0 = 69036225587269604587380828901110959985820993104339166121952435700418237634884566882380661771083506554283938902859275601769840064565952882178731506464866270733357184875037630166845264127377651804173189451500736544719907454193858174375188647669243173368179546380071693963057411374219879730555780084721257185663
c0 = 25919994984006494136117763940434107674027325362716831602111253353303312624950949244870141228310150398346225979345639834949450316401168402257977080462742941409884413450456343996608363699189273633186815603506411818482277791703378774040695810935035144274982279618243241555858616150507413430364949497014898459149
e1 = 90227595770798329429543773376871102772936312496108372576645218459845442190961925721920308644012475971055712240490824429020187051893983437106526625545004025441742660408871198214420700018631241447159623873053699968499724826440813154790906891293256068588364266754507063532093517401246106130400153232720885119383
n1 = 95018697907811905388348168966643819870431786565455754516869846768936627751616391459055741771645229919599086026202150338312064743859507786094624995592213819328921071806986060124918106493195648281643336238358671055792671721940544939312770559081353577401130988021800867564754104190852488382143254732103642530087
c1 = 61754320221743759233065500021099993531816432330793348444588244530260861766516279667925579405472694997398214986157779800660212567507768828169727324987163176985363345897993819026535555548687226385416718142192208370923386429475997149114353749344817646742924465192811146580825484480291208840716280564361694864736
e2 = 48436352174538763645407644971106273644384063698361935647029449962466195465988178835554358488268166392312903786539521207370520215437108228916671408239777663473340941629006170373460474769931653556801223896212652866162477593257053759252765539855609264405307505776094145705223912290876655703882182613563925340591
n2 = 79298575208625662122217380170674490352029876259237329052532470648179836953643740249006121287223747696466043924149836698083695810801355660950241408571319425882277932762946786909216491079644003971491918799579224953982575800826473679194352007906249630812597483376008728062904339206798756997528224954887081000253
c2 = 3193110934002044409318986068547938917927914194425590281649004983277691653690661760583880972618091469046967293951731672660957069138700739499999533078945884300306480766473953983459716137405783361390166697486777216808092308928704730448676281698937103305878976076391949094288750872456591287874971059095860369356
e3 = 87386679582879797604111547110599099110567090087056142592469346107224071138506565164646979832903001578978653572500207450807082420333442167861402396827337780115219781115991724302157866191795307397700562628226448893516202695130423545487876908541015965410107488857158852611720962222793083868484783686519692025391
n3 = 114854814804165287261892516196610245073496593524492698346301772352004426440576935073002800821365588587465086811039742854832566154065444281285574462506500612214357445628214391558263176158881581038294138724757815389225465421721516660119458048525456082047658388721166122008735177086863798238786090988397938474453
c3 = 2628221891288775142730119400504625873661913557342797639332389889995494226897641124532043767301323269404579967203071158722088045137803611630295981086272025145539877643261676492818599564573074217978667225322783675473461608751143683659247347376427203720932989397503856751335285009642198314940546804845309680472
'''
```

基于 [_Lattice Based Attack on Common Private Exponent RSA_](https://ijcsi.org/papers/IJCSI-9-2-1-311-314.pdf) ，论文中给出了构造的格：

$$
\begin{aligned}&x_{r}=(d,k_1,k_2,\cdots,k_r)\\&\mathcal{B}_{r}=\begin{bmatrix}M&e_1&e_2&&e_r\\0&-N_1&0&\cdots&0\\0&0&-N_2&&0\\&\vdots&&\ddots&\vdots\\0&0&0&\cdots&-N_r\end{bmatrix}\\&v_{r}=(dM,1-k_1s_1,\cdots,1-k_rs_r).\end{aligned}
$$

```python title="exp.py"
from sage.all import *
from Crypto.Util.number import long_to_bytes
es = [e0, e1, e2, e3]
ns = [n0, n1, n2, n3]

r = len(es)
M = floor(n0^0.5) # 权重 M，通常取 N^(1/2) 左右

# 构造格基矩阵
# [ M  e0  e1  e2  e3 ]
# [ 0 -n0   0   0   0 ]
# [ 0   0 -n1   0   0 ]
# [ 0   0   0 -n2   0 ]
# [ 0   0   0   0 -n3 ]

dim = r + 1
B = Matrix(ZZ, dim, dim)
B[0, 0] = M

for i in range(r):
    B[0, i+1] = es[i]
    B[i+1, i+1] = -ns[i]

L = B.LLL()

# 在规约后的基中，目标向量 v = [d*M, ...]，所以 d = abs(row[0]) // M

d_found = 0
for row in L:
    possible_d = abs(row[0]) // M
    if possible_d == 0: continue
    try:
        m = pow(c0, possible_d, n0)
        flag_cand = long_to_bytes(int(m))
        if b'darctf{' in flag_cand:
            d_found = possible_d
            print(f"[+] Found d: {d_found}")
            print(f"[+] Flag: {flag_cand.decode()}")
            break
    except:
        continue

if d_found == 0:
    print("[-] Attack failed to recover d.")
"""
[+] Found d: 1494282151976595577258857772505247454114539908857454581578416856533872627447784513499219236773851002321291861627331150671
[+] Flag: darctf{C0mMon_D_1s_N0t_@_G0od_Choic3}
"""
```

## Coppersmith's relative attack

### Håstad's broadcast attack

发送方将一份明文进行多份（份数 k > e）加密，每份使用不同的 n（如 $n_{1}, n_{2}, \dots$），显然可以使用中国剩余定理解出 $c = m^e\pmod{n_{1}*n_{2}*\dots}$；而显然 m < n1 & m < n2 & ... ，所以当 e 的值小于等于我们获得的密文数量，就会有 $m^e \leq \Pi_{i=0}^{k}n_{i}$ ，此时直接开根就好了。一般来说，这个 e 等于 3。

```python title="broadcast attack"
from sage.all import *
msg = [{'c':xxx, 'e':xxx, n:xxx}, ...] # 字典列表
# 提取所有的n和c
length = len(msg)
ns = [msg[i]["n"] for i in range(length)]
cs = [msg[i]["c"] for i in range(length)]

# 使用CRT求解m^length
m_power = crt(cs, ns)
m = int(m_power.nth_root(length))

flag = bytes.fromhex(hex(m)[2:]).decode()
print(flag)
```

如果是很多组 (n, e, c) 中，部分对应明文相同，可以改为下面的代码：

```python
from sage.all import *
from itertools import combinations
max_length = len(ns)
for l in range(e, max_length+1):
    for comb in combinations(range(max_length), l):
        ncs = [cs[i] for i in comb]
        nns = [ns[i] for i in comb]
        m_power = crt(ncs, nns)
        try:
            m = int(m_power.nth_root(e))
            pt = bytes.fromhex(hex(m)[2:])
            if b'flag' in pt:
                print(pt)
                print(comb)
        except:
            continue
```

### Franklin–Reiter related-message attack

相关消息攻击，攻击条件：使用同一公钥 (n, e) （一般要求 e 比较小）线性填充加密同一密文 m 两次，获得两个密文 c1 c2:

```python title="related-message"
class Challenge:
    def __init__(self):
        self.p = getPrime(1024)
        self.q = getPrime(1024)
        self.N = self.p * self.q
        self.e = 11
    
    def pad(self, flag):
        m = bytes_to_long(flag)
        a = random.randint(2, self.N)
        b = random.randint(2, self.N)
        return (a, b), a * m + b
    
    def encrypt(self, flag):
        pad_var, pad_msg = self.pad(flag)
        encrypted = (pow(pad_msg, self.e, self.N), self.N)
        return pad_var, encrypted
```

$$
构造两个多项式\begin{cases}
p_1(x)=(a_1x+b_1)^e-c_1\quad\mathrm{mod~}N\\
p_2(x)=(a_2x+b_2)^e-c_2\quad\mathrm{mod~}N
\end{cases}
$$

不难发现二者都有 (x-m) 这一因式，提取出来后求解即可得到 m。

> [!question]+
>
> [cryptohack - Bespoke Padding](https://cryptohack.org/challenges/rsa/)
> 
> - 可参考 [多项式扩展欧几里得算法](https://billcookmath.com/sage/algebra/Euclidean_algorithm-poly.html)

```python title="sage"
x = Zmod(N)["x"].gen()
p1 = ...
p2 = ...
# 多项式辗转相除法
def poly_gcd(a, b):
    while b:
        a, b = b, a % b
    return a.monic()
# poly_egcd 仅作备忘，这里没用到
def poly_egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        gcd, x, y = egcd(b % a, a)
        return (gcd, y - (b//a) * x, x)

common_poly = poly_gcd(p1, p2)
for m in (common_poly).small_roots():
    print(long_to_bytes(int(m)))
```

> [!question]+
> 
> [Moectf2025 - ezHalfGCD](https://ctf.xidian.edu.cn/training/22?challenge=878)
> 
> 关于 HalfGCD 的原理可参考：[HalfGCD algorithm](https://codeforces.com/blog/entry/101850)

```python title="task.py"
from Crypto.Util.number import bytes_to_long, getStrongPrime
from secret import flag

e = 11
p = getStrongPrime(1024)
q = getStrongPrime(1024)
n = p * q
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
enc_d = pow(d, e, n)
enc_phi = pow(phi, e, n)
enc_flag = pow(bytes_to_long(flag), e, n)
print(f"{e=}")
print(f"{n = }")
print(f"{enc_d = }")
print(f"{enc_phi = }")
print(f"{enc_flag = }")
# 输出在此省略
```

已知值 `e, n, enc_d, enc_phi, enc_flag`，且：

1. $enc_d = d^e \pmod n$
2. $enc_\phi = \phi^e \pmod n$
3. $e*d = 1 \pmod \phi => 取 e*d = k*\phi + 1$
    - d < phi => k < e （可以遍历，故而可以视为已知）
    - $k^e * \phi^e = (k*\phi)^e = (e*d -1)^e$

将 3 式代入 2 式可得：

4. $k^e * \phi^e = (e*d -1)^e = enc_\phi*k^e \pmod n$

依据 1,4 式建立两个在 Zmod(n) 上的多项式：

- $f(x) = x^e - enc_d$
- $g(x) = (e*x-1)^e - enc_\phi*k^e$ 

不难发现 d 是这两个公式的公共根；据此，使用 sagemath 进行求解

```python title="exp.sage"
load("./output.sage") # load e, n, enc_d, enc_phi, enc_flag
# load("../../../tools/archive/halfGCD.sage") # import PolyGCD for using HalfGCD
# HalfGCD comes from https://seandictionary.top/sagemath/

def PolyGCD(a, b):
    while b:
        a, b = b, a % b
    return a

R = Zmod(n)
P.<x> = PolynomialRing(R)

d = None
phi = None

for k in range(e):
    # f(x) = x^e - enc_d
    f = x^e - enc_d
    # g(x) = (e*x - 1)^e - enc_phi * k^e
    g = (e*x - 1)^e - enc_phi * (k^e)
    # gcd 寻找公共因子
    h = PolyGCD(f, g)
    # 如果 gcd 度数为 1，则有形如 (x - d) 的因子
    if h.degree() == 1:
        # 在线性多项式 ax + b 中, 根为 -b/a
        a = h[1]
        b = h[0]
        d_candidate = -b/a

        if pow(Integer(d_candidate), e, n) == enc_d:
            d = Integer(d_candidate)

            # 由 e*d = k*phi + 1 => phi = (e*d - 1)//k
            num = e*d - 1
            if num % k == 0:
                phi_candidate = num // k
                # 验证 enc_phi
                if pow(phi_candidate, e, n) == enc_phi:
                    phi = phi_candidate
                    print("[+] 找到 k =", k)
                    print("[+] d =", d)
                    print("[+] phi =", phi)
                    break

if d is None or phi is None:
    print("[-] 未能找到合适的 d / phi")
else:
    # 用 d 解密 flag
    m = pow(enc_flag, d, n)
    try:
        flag = bytes.fromhex(hex(m)[2:])
    except:
        # 有时前面会有填充 0，需要补到偶数长度再解码
        h = hex(m)[2:]
        if len(h) % 2 == 1:
            h = "0" + h
        flag = bytes.fromhex(h)

    print("[+] flag_int =", m)
    print("[+] flag =", flag, flag.decode())
```

### Coppersmith’s short-pad attack

#todo 

### Known High Bits Attack

已知高位攻击，利用 sagemath 调用的 coppersmith 算法求解小根。

- 攻击条件：已知 p/q/m/d 的高位；
	- 对于512位素数，需要未知至多227位，对于1024位素数，需要未知至多454\455位，可能性大致对半开
	- 如果不满足，可以尝试爆破一些位
- 攻击方式：构造多项式，调用 sagemath 求解。

#### p/m high bits

```python title="known_bits"
from sage.all import *
from Crypto.Util.number import getPrime
m1 = int.from_bytes(b'darctf{p_high_bits_leak}')
m2 = int.from_bytes(b'darctf{m_high_bits_leak}')
e1 = 65537
e2 = 11
print(f"e2 = {e2}")
p = getPrime(1024)
q = getPrime(1024)
n = p * q
c1 = pow(m1, e1, n)
c2 = pow(m2, e2, n)
print(f'n = {n}')
print(f"e = {e}")

""" Known High Bits Message Attack """
shift1 = 128
p_high = p >> shift1 << shift1
print(f"p_high = {p_high}")
print(f'c1 = {c1}')

""" Factoring with High Bits Known """
shift2 = 128
m_high = m2 >> 128 << 128
print(f"m_high = {m_high}\n{bytes.fromhex(hex(m_high)[2:])}")
print(f'c2 = {c2}')

"""solve"""
x = Zmod(n)['x'].gen()
""" part 1 """
# x1 = p-p_high => x1+p_higt % p == 0
f1 = x + p_high
root1 = f1.small_roots(X=2**shift1, beta=0.4)
for root in root1:
    root = int(root)
    if n % (root + p_high) == 0:
        p = root + p_high
        q = n // p
        break
d1 = pow(e1, -1, (p-1)*(q-1))
print(bytes.fromhex(hex(pow(c1, d1, n))[2:]))
""" part 2 """
# x2 = m-m_high => x2+m_high = m => (x2+m_high)^e - c2 == 0
f2 = (x + m_high)**e2 - c2
root2 = f2.small_roots(X=2**shift2, beta=0.4)
if root2:
    for root in root2:
        print(bytes.fromhex(hex(root+m_high)[2:]))
else:
    print("No root found")
```

#### d high bits

> #todo https://weichujian.github.io/2020/05/27/rsa%E5%B7%B2%E7%9F%A5%E9%AB%98%E4%BD%8D%E6%94%BB%E5%87%BB1/

### Known Low Bits Attack

#### p/m low bits

```python title="known low bits"
from sage.all import *
from Crypto.Util.number import getPrime
p, q = getPrime(1024), getPrime(1024)
n = p*q
print(f"n = {n}")

""" known p low bits """
m1 = int.from_bytes(b'darctf{p_low_bits_leak}')
shift1 = 128
p_low = p & ((1 << shift1)-1)
e1 = 0x10001
c1 = pow(m1, e1, n)
print(f"e1 = {e1}")
print(f"c1 = {c1}")
print(f"p_low = {p_low}")
len_p = len(bin(p))
print(f'len(bin(p)) = {len_p}')

""" known m low bits """
m2 = int.from_bytes(b'darctf{m_low_bits_leak}')
shift2 = 128
m_low = m2 & ((1 << shift2)-1)
e2 = 11
c2 = pow(m2, e2, n)
len_m = len(bin(m2))
print(f"e2 = {e2}")
print(f"c2 = {c2}")
print(f"len(bin(m2)) = {len_m}")
print(f'm_low = {m_low}')

""" solve """
x = PolynomialRing(Zmod(n), 'x', implementation="NTL").gen()
""" part p """
# x1* 1<<shift1 = p-p_lo2 => (x1**shift1 + p_low) % p == 0
f1 = (x*(1<<shift1) + p_low - n).monic()
root1 = f1.small_roots(X=2**(len_p-2-shift1), beta=0.4)
if root1:
    for root in root1:
        root = int(root*(1 << shift1))
        p = root + p_low
        q = n // p
        d1 = pow(e1, -1, (p-1)*(q-1))
        print(bytes.fromhex(hex(pow(c1, d1, n))[2:]))
        break
else:
    print('root1 not found')
    

""" part m """
# x2* 1<<shift2 = m-m_low => (x2**shift2 + m_low)**e - c == 0
f2 = (((1 << shift2) * x + m_low)**e2 - c2).monic()
root2 = f2.small_roots(X=2**(len_m-2-shift2), beta=0.5)
if root2:
    for root in root2:
        root = int(root*(1 << shift2))
        print(bytes.fromhex(hex(root + m_low)[2:]))
        break
else:
    print('root2 not found')
```

#### d low bits

一个复杂一些的例子是知道 d 的部分低位。 Boneh,Durfee,Frankel 指出：只要 $e < \sqrt{ N }$ 并且给定了 d 的 $\left\lceil  \frac{d}{4}  \right\rceil$ 的低位，就可以从中恢复出 d 。下面是一个例子：

```python title="baby-lifting"
# https://ctf.xidian.edu.cn/training/10?challenge=147
from Crypto.Util.number import *
from secret import flag

p = getPrime(512)
q = getPrime(512)
n = p*q
e = 0x1001
d = inverse(e, (p-1)*(q-1))
bit_leak = 400
d_leak = d & ((1<<bit_leak)-1)
msg = bytes_to_long(flag)
cipher = pow(msg,e,n)
pk = (n, e)

with open('output.txt','w') as f:
    f.write(f"pk = {pk}\n")
    f.write(f"cipher = {cipher}\n")
    f.write(f"hint = {d_leak}\n")
    f.close()

# pk = (53282434320648520638797489235916411774754088938038649364676595382708882567582074768467750091758871986943425295325684397148357683679972957390367050797096129400800737430005406586421368399203345142990796139798355888856700153024507788780229752591276439736039630358687617540130010809829171308760432760545372777123, 4097)
# cipher = 14615370570055065930014711673507863471799103656443111041437374352195976523098242549568514149286911564703856030770733394303895224311305717058669800588144055600432004216871763513804811217695900972286301248213735105234803253084265599843829792871483051020532819945635641611821829176170902766901550045863639612054
# hint = 1550452349150409256147460237724995145109078733341405037037945312861833198753379389784394833566301246926188176937280242129
```

按照前面的思路，我们期望构造一个方程并求根；但是难点在于我们几乎无法利用已有信息直接构造一个只有 d 未知的方程；我们唯一知道的是 $d*e \equiv 1 \pmod{\phi(n)}$；但是同样困于 $\phi(n)$ 未知。尝试过将 $\phi(n) \approx n$ 直接求解，失败。

在[这里](https://www.ruanx.net/coppersmith/)解给出的思路是：考虑前面我们已知 p/m 的低位可以求解；能否从 d 的低位搞到 p 的低位？

我们知道 $x^{2} - (p+q)x + p*q = 0$ 的根为 p 和 q，在取模的条件下依旧成立，$pq = n$，故而重点转向 $p+q$。

我们知道，$\phi(n) = (p-1)(q-1) = n+1 - (p+q) \implies x^{2}-(n+1-\phi(n))x + n = 0$ 。

记 $l = 2^{bit\_leak}$，有

$$
\begin{align}
&de = 1 + k \phi(n) \implies d_{l}e = 1 + k\phi(n)\pmod{t} \\
\implies &kx^{2} + (d_{l}e - 1 - k(n+1))x + kn = 0 \pmod{t}
\end{align}
$$

因为 $d< \phi(n) \implies e > k$，暴力搜索有：

```python
from sage.all import *
from Crypto.Util.number import *
n = 53282434320648520638797489235916411774754088938038649364676595382708882567582074768467750091758871986943425295325684397148357683679972957390367050797096129400800737430005406586421368399203345142990796139798355888856700153024507788780229752591276439736039630358687617540130010809829171308760432760545372777123
e = 4097
cipher = 14615370570055065930014711673507863471799103656443111041437374352195976523098242549568514149286911564703856030770733394303895224311305717058669800588144055600432004216871763513804811217695900972286301248213735105234803253084265599843829792871483051020532819945635641611821829176170902766901550045863639612054
d_l = 1550452349150409256147460237724995145109078733341405037037945312861833198753379389784394833566301246926188176937280242129
blk = 400

def get_p_lows(d_l, n, e):
    for k in range(645, e+1): # 理应从 1 开始，这里知道结果后才从 645 开始
        print(f"trying {k}/{e}")
        p = var('p')
        eq = (k* p**2 + (e*d_l - k*(n+1) - 1) * p + k * n == 0)
        p_l = solve_mod([eq], 1<<blk)
        if len(p_l) > 0:
            yield [int(pl[0]) for pl in p_l], k
    return None
```

> [!env]- Sagemath 9.3 + Python 3.9
> 
> 尝试过使用多项式环上的 small_roots 直接求解方程，失败。
> 
> 起初一直用的是较新版本的 sagemath 10.6 + python 3.11，这在执行 solve_mod 时会出现错误：
> 
> ```
> OverflowError: Python int too large to convert to C long
> Exception ignored in: 'sage.libs.singular.singular.sa2si_ZZmod'
> Traceback (most recent call last):
>   File ".../python3.11/site-packages/sage/symbolic/relation.py", line 1701, in <genexpr>
>     ans = list(t for t in possibles if all(e(*t) == 0 for e in eqns_mod))
>                                            ^^^^^
> OverflowError: Python int too large to convert to C long
> ```

再用上面的已知 p 低位的思路求 p

```python
def get_full_p(p_low, n):
    p_h = PolynomialRing(Zmod(n), "p_h", implementation='NTL').gen()
    p = p_h * (1 << blk) + p_low
    f = (p-n).monic()
    phs = f.small_roots(X=(1 << (512//4)), beta=0.4)
    if phs:
        return int(p(phs[0]))
    return None
```

组合之下我们得到

```python title="exp.py"
def get_full_d(d_l, n, e):
    for p_lows, k in get_p_lows(d_l, n, e):
        # print("p_lows:",p_lows)
        for low_p in p_lows:
            p = get_full_p(low_p, n)
            if p:
                print("p:", p)
                q = n // p

                if p * q == n:
                    d = inverse_mod(e, (p-1)*(q-1))
                    return d
                else:
                    print("p * q != n")
                    continue
    return None

d = get_full_d(d_l, n, e)
if d:
    print("d:", d)
    m = pow(cipher, d, n)
    print("flag:", long_to_bytes(int(m)))
else:
    print("d not found")
    
# trying 645/4097
# trying 646/4097
# trying 647/4097
# trying 648/4097
# trying 649/4097
# trying 650/4097
# p: 7458062461956620112301588229071392126780346788859113209375105494626101265308095322117111641306328357294968229324362505235806688414035133488417611167744319
# d: 8453400612258125070836799610286958177590958703862612176480299487127355057097473419454243973552176419700567840361653614387706247105682797730958892608765553970954948853164478455048360634740571200591660362044055606841746827568729277784053763456603113675706647429943809231549106428652993256853303236680813806033
# flag: b'moectf{7h3_st4rt_0f_c0pp3rsmith!}'
```

### Return of Coppersmith's attack (ROCA)

攻击条件：fast primes

起源于 [cryptohack](https://cryptohack.org/challenges/rsa/) 上的 "Fast Primes"，当然去搜 Fast Primes 也能找到这个攻击（方便和安全总是难以兼得的），具体下面的文章讲的很清楚了，推荐攻击脚本如下，自己有能力写一个更好。

> [!help]+
>
> - [Analysis of the ROCA vulnerability](https://bitsdeep.com/posts/analysis-of-the-roca-vulnerability)
> - https://github.com/RsaCtfTool/RsaCtfTool/blob/master/sage/roca_attack.py

## 其他

### Optimal asymmetric encryption padding (OAEP)

> https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding

## 主要参考资料

- [RSA 的一些攻击方式](https://seandictionary.top/rsa/)
- [cryptohack - rsa](https://cryptohack.org/challenges/rsa/)
- [crypto-attack/attack/rsa](https://github.com/jvdsn/crypto-attacks/tree/master/attacks/rsa)
- [RSA学习笔记 | Chemtrails (ch3mtr4ils.cn)](https://ch3mtr4ils.cn/2022/12/29/RSA%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/)
- [CTF RSA题解集](https://www.ruanx.net/rsa-solutions/)
