---
tags:
- notes
- ctf
comments: true
---

## Congruence theory

> [!DEFINITION]
>
> $\text{如果}a,b,n\in Z\text{,}n>0,\text{ 如果}n|(a-b),\text{ 称}a\text{和}b\text{在模}n\text{ 下同余,记作}a\equiv b(\mathrm{~mod~}n)\text{。}$

### 乘法逆元 (modular inverse)

$x \in Z, p \in N$ 如果存在 $a\in Z$ 使得 $ax\equiv 1 \pmod{p}$ ，则称 a 为 x 模 p 下的逆元，记作 $a=x^{-1}$ 。

**乘法逆元存在性：** gcd(x, p) = 1

### 一次同余方程的消去律

对于 $a,p \in Z$，如果 gcd(a, n) = d，则有一次同余方程（y 已知，x 未知）：

$ax\equiv ay \pmod{p} \implies x\equiv y\pmod{\frac{p}{d}}$

**有解条件：**

- gcd(a, p) = 1，则方程有唯一解；
- $gcd(a, p) = d \neq 1$ ，则方程有解当且仅当 d|b 。

## GCD && LCM

> https://oi-wiki.org/math/number-theory/gcd/

### Euclid algorithm

欧几里得求解最大公因数 gcd(a,b) 的关键在于 $\gcd(a,b)=\gcd(b,a\mathrm{~mod~}b)$，故：

```python title="gcd.py"
def gcd(a, b) -> int:
    if b == 0:
        return a
    return gcd(b, a % b)
```

那么最小公倍数 lcm(a,b) 呢？想想 $gcd(a,b) \times lcm(a,b)=a\times b$ ，解决了。
### Extended Euclidean algorithm

扩展欧几里得算法使用的关键等式和上面相同，推导略去，主要用于求解形如 $ax+by=\gcd(a,b)$ 中的 (x, y) 解。

```python title="exgcd.py"
def Exgcd(a, b) -> tuple: # d, x, y
    if b == 0:
        return a, 1, 0
    d, x, y = Exgcd(b, a % b)
    return d, y, x - (a // b) * y
```

使用 z3 求解器求解所有可能的解：

```python title="exgcd"
from z3 import *
u, v = Ints("u v")
s = Solver()
s.add(u * p + v * q == gcd(p, q))

while s.check() == sat:
    m = s.model()
    print(f"u = {m[u]}, v = {m[v]}")
    assert m[u].as_long() * p + m[v].as_long() * q == gcd(p, q)
    # 添加约束排除当前解
    current_solution = And(u == m[u].as_long(), v == m[v].as_long())
    s.add(Not(current_solution))
```

> [!QUESTION]
>
> 如何使用扩展欧几里得算法求解形如 $a*x \equiv b \pmod{p}$ 中的 x?

> https://devv.ai/search?threadId=e2xqr5fzft34

1. 求 d = gcd(a, p) ，确保 d 为 b 的约数，否则无解；
2. ax' + py' = gcd(a, p)，求 x', y'
3. $ax'*\frac{b}{d}+py'* \frac{b}{d}=d * \frac{b}{d}=b$
4. $x = \frac{x'*b}{d}$
## Quadratic Residues

### 定义

> [!DEFINITION] 
>
> We say that an integer x is a _Quadratic Residue_ if there exists an aa such that $a^2≡x\pmod p$. If there is no such solution, then the integer is a _Quadratic Non-Residue_.
>
> If $a^2=x$ then $(−a)^2=x$. So if x is a quadratic residue in some finite field, then there are always two solutions for a.

当 p 不太大的时候，我们只要遍历 (0, p-1) 即可：

```python title="quadratic_residues.py"
p = 29
ints = [14, 6, 11]

qr = [a for a in range(p) if pow(a,2,p) in ints]
print(f"flag {min(qr)}")
```

### 使用 sympy

```python title="sqrt_mod"
from sympy import *
# a^2 = x (mod p)
print(sqrt_mod(x, p))
```

### 数学推导求解

#### 勒让德符号

![](attachments/Math%20in%20crypto.png)

一些性质：

- (a/p)(b/p) = (ab/p)
- $a\equiv b\pmod{p} \implies \left( \frac{a}{p} \right)=\left( \frac{b}{p} \right)$
- $\left( \frac{p}{q} \right) = (-1)^{(p-1)(q-1)/4}\left( \frac{q}{p} \right)$

> https://math.stackexchange.com/questions/1273690/when-p-3-pmod-4-show-that-ap1-4-pmod-p-is-a-square-root-of-a

1. 当 p%4=3 时，$(a^{(p+1)/4})^2\equiv a\pmod{p}$ 。 
2. tonelli_shanks 算法

```python title="tonelli_shanks"
# 代码来自 https://devv.ai/search?threadId=dxl1i5f103r4
def tonelli_shanks(n, p):
    # Step 1: Check if n is a quadratic residue modulo p
    if pow(n, (p - 1) // 2, p) != 1:
        return None  # No solution exists

    # Step 2: Factor p - 1
    Q, S = p - 1, 0
    while Q % 2 == 0:
        Q //= 2
        S += 1

    # Step 3: Find a quadratic non-residue z
    z = 2
    while pow(z, (p - 1) // 2, p) == 1:
        z += 1

    # Step 4: Initialize variables
    M = S
    c = pow(z, Q, p)
    t = pow(n, Q, p)
    R = pow(n, (Q + 1) // 2, p)

    # Step 5: Loop until a solution is found
    while t != 0 and t != 1:
        # Find least i such that t^(2^i) = 1
        t2i = t
        i = 0
        while t2i != 1:
            t2i = (t2i * t2i) % p
            i += 1

        b = pow(c, 2 ** (M - i - 1), p)
        M = i
        c = (b * b) % p
        t = (t * c) % p
        R = (R * b) % p

    return R if t == 1 else None
```
``

## Euler-totient, Fermat's little theorem

### Euler totient

> https://oi-wiki.org/math/number-theory/euler-totient/

> [!MATH]
>
> 即 $\varphi(n)$，表示的是小于等于 n 且与 n 互质的数的个数。
  
- $\varphi(n)=n-1$ ；当 n 为质数时
- $n=\Pi^s_{i=1}p_{i}^{k_{i}}\implies \varphi(n)=n*\Pi_{i=1}^s\left( \frac{p_{i}-1}{p_{i}} \right)$
    - $n=p^k\implies\varphi(n)=p^{k-1}\varphi(p) = p^k-p^{k-1}$；当 p 为质数时；
- $\varphi(mn)\varphi(\gcd(m,n))=\varphi(m)\varphi(n)\gcd(m,n)$
- $\varphi(mn)=\varphi(m)\varphi(n)$；当 gcd(m,n)=1 时
    - $\varphi(2n)=\varphi(n)\varphi(2)=\varphi(n)$；当 n 为奇数时

> 也许还有[筛法求欧拉函数](https://oi-wiki.org/math/number-theory/sieve/#%E7%AD%9B%E6%B3%95%E6%B1%82%E6%AC%A7%E6%8B%89%E5%87%BD%E6%95%B0)待看

### Fermat's little theorem
 
> https://oi-wiki.org/math/number-theory/fermat/

> [!MATH] Fermat's little theorem
>
> If is_prime(p) && gcd(a, p)=1 , 
> 
> then $a^{p-1}\equiv 1\pmod{p}$ namely $a^p\equiv a\pmod{p}$

#### 推论一

对于 p 阶的生成元 g，如果 $g^x\equiv g^y\pmod{p}$ ，那么 $x\equiv y\pmod{p-1}$ 。

#### 推论二 Euler's theorem

$gcd(a, p)=1 \implies a^{\varphi(p)}\equiv 1\pmod{p}$

**扩展欧拉定理：**

$$
\begin{aligned}a^b\equiv\begin{cases}a^{b\mathrm{~mod~}\varphi(m)},&\gcd(a,m)=1,\\a^b,&\gcd(a,m)\neq1,b<\varphi(m),&\pmod m\\a^{(b\mathrm{~mod~}\varphi(m))+\varphi(m)},&\gcd(a,m)\neq1,b\geq\varphi(m).&\end{cases}\end{aligned}
$$

其中式一使用较多。

## Pollard’s ρ algorithm

> https://ljcppp.github.io/mySlides/crypto_2024/site/#/3/18
> 
> https://ctf-wiki.org/crypto/asymmetric/discrete-log/discrete-log/#pohlig-hellman-algorithm

> [!KNOWLEDGE]
>
> **光滑**：即可以因子分解成较小的数的乘积。
> 
> p 光滑也意味着群 $\mathbb{Z}_{p}^*$ 有很多小的子群。

所以，可以把大群上的离散对数问题转换成易求的子群上的离散对数问题，最后组合起来。

## Wilson's theorem

> [!WIKI]- Wilson's theorem
>
> In [algebra](https://en.wikipedia.org/wiki/Algebra "Algebra") and [number theory](https://en.wikipedia.org/wiki/Number_theory "Number theory"), **Wilson's theorem** states that a [natural number](https://en.wikipedia.org/wiki/Natural_number "Natural number") _n_ > 1 is a [prime number](https://en.wikipedia.org/wiki/Prime_number "Prime number") [if and only if](https://en.wikipedia.org/wiki/If_and_only_if "If and only if") the product of all the [positive integers](https://en.wikipedia.org/wiki/Positive_integer "Positive integer") less than _n_ is one less than a multiple of _n_. That is (using the notations of [modular arithmetic](https://en.wikipedia.org/wiki/Modular_arithmetic "Modular arithmetic")), the [factorial](https://en.wikipedia.org/wiki/Factorial "Factorial") (n−1)!=1×2×3×⋯×(n−1) satisfies 
> 
> $$(n-1)!\equiv -1\pmod{n}$$.

```python title="chall.py"
from sage.all import factorial, next_prime
import random
from Crypto.Util.number import getPrime

def myGetPrime():
    A= getPrime(513)
    print(A)
    B=A-random.randint(1e3,1e5)
    print(B)
    return next_prime(factorial(B)%A)
p=myGetPrime()
# A1=21856963452461630437348278434191434000066076750419027493852463513469865262064340836613831066602300959772632397773487317560339056658299954464169264467234407
# B1=21856963452461630437348278434191434000066076750419027493852463513469865262064340836613831066602300959772632397773487317560339056658299954464169264467140596

q=myGetPrime()
# A2=16466113115839228119767887899308820025749260933863446888224167169857612178664139545726340867406790754560227516013796269941438076818194617030304851858418927
# B2=16466113115839228119767887899308820025749260933863446888224167169857612178664139545726340867406790754560227516013796269941438076818194617030304851858351026

r=myGetPrime()

n=p*q*r
# n=85492663786275292159831603391083876175149354309327673008716627650718160585639723100793347534649628330416631255660901307533909900431413447524262332232659153047067908693481947121069070451562822417357656432171870951184673132554213690123308042697361969986360375060954702920656364144154145812838558365334172935931441424096270206140691814662318562696925767991937369782627908408239087358033165410020690152067715711112732252038588432896758405898709010342467882264362733
c=pow(flag,e,n)
# e=0x1001
# c=75700883021669577739329316795450706204502635802310731477156998834710820770245219468703245302009998932067080383977560299708060476222089630209972629755965140317526034680452483360917378812244365884527186056341888615564335560765053550155758362271622330017433403027261127561225585912484777829588501213961110690451987625502701331485141639684356427316905122995759825241133872734362716041819819948645662803292418802204430874521342108413623635150475963121220095236776428
```

A、B 都告诉我们了，理应能够计算质数 p,q,r 了；但是考虑到 B 的极大，其实我们不可能计算出它的阶乘值。

但是由 Wilson's theorem 可以得到：

$(A-1)!\equiv-1\pmod{A}\implies \frac{B!*(A-1)!}{B!}\equiv-1\pmod{A} \implies -\left( \frac{(A-1)!}{B!} \right)^{-1}\equiv B!\pmod{A}$

且不难发现前者计算很快（A-B 是一个比较小的值），阶乘次数可接受，所以：

```python title="solve.py"

from sage.all import next_prime

A1 = 21856963452461630437348278434191434000066076750419027493852463513469865262064340836613831066602300959772632397773487317560339056658299954464169264467234407
B1 = 21856963452461630437348278434191434000066076750419027493852463513469865262064340836613831066602300959772632397773487317560339056658299954464169264467140596
A2 = 16466113115839228119767887899308820025749260933863446888224167169857612178664139545726340867406790754560227516013796269941438076818194617030304851858418927
B2 = 16466113115839228119767887899308820025749260933863446888224167169857612178664139545726340867406790754560227516013796269941438076818194617030304851858351026
n = 85492663786275292159831603391083876175149354309327673008716627650718160585639723100793347534649628330416631255660901307533909900431413447524262332232659153047067908693481947121069070451562822417357656432171870951184673132554213690123308042697361969986360375060954702920656364144154145812838558365334172935931441424096270206140691814662318562696925767991937369782627908408239087358033165410020690152067715711112732252038588432896758405898709010342467882264362733
e = 0x1001
c = 75700883021669577739329316795450706204502635802310731477156998834710820770245219468703245302009998932067080383977560299708060476222089630209972629755965140317526034680452483360917378812244365884527186056341888615564335560765053550155758362271622330017433403027261127561225585912484777829588501213961110690451987625502701331485141639684356427316905122995759825241133872734362716041819819948645662803292418802204430874521342108413623635150475963121220095236776428
def wilson_attack(A, B):
    k = 1
    for i in range(B+1, A):
        k *= i
        k %= A # 加快运算
    
    return next_prime((-pow(k, -1, A)) % A)

p = wilson_attack(A1, B1)
q = wilson_attack(A2, B2)
r = n // (p * q)
assert p * q * r == n
phi = (p - 1) * (q - 1) * (r - 1)
d = pow(e, -1, phi)
m = pow(c, d, n)
bytes.fromhex(hex(m)[2:]) 
# b'RoarCTF{wm-CongrAtu1ation4-1t4-ju4t-A-bAby-R4A}'
```
