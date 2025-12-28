---
tags:
- notes
- ctf
comments: true
---

# 格密码基础

> [!attention] 本文注重于 CTF 中的格求解，如果期望了解更多理论知识，文中的链接以及最后的参考资料是更好的选择。

## 格理论

如果你想知道我们为什么要研究格，见 [huangx607087学习格密码的笔记1](https://huangx607087.online/2021/02/01/LatticeNotes1/)。

如果你想知道：

- 什么是格？
- 什么是 SVP/CVP？
- 在 SVP 中，我们期望寻找最短向量，那么最短到底是多长呢？（换句话说，如何保证我们需要找的最短在格中确实可能存在呢？）

见 [huangx607087学习格密码的笔记2](https://huangx607087.online/2021/02/03/LatticeNotes2/)，这里强调一个比较重要的定理：

> [!theorem]+ Herimite Theorem
> 
> 每一个 $L \in \mathbb{R}^n$ 都包含了一个长度不超过 $\sqrt{n}\cdot\sqrt[n]{\det L}$ 的向量 $\vec{v}$ 。

在 [huangx607087学习格密码的笔记3](https://huangx607087.online/2021/02/04/LatticeNotes3/) 中探讨了早期针对格问题的求解以及构造密码系统的尝试，其中提到如果格基接近正交，利用 Babai 算法能够较好的将向量分解并求解 apprCVP 。

## 格基规约算法

### 2 维高斯格基规约

```python title="Gaussian Lattice Reduction"
from Crypto.Util.number import *
from math import sqrt
def sgn(x):
    if x==0:
        return 0
    if x>0:
        return 1
    if x<0:
        return -1
def vecmul(veca,vecb):
    assert len(veca)==len(vecb) 
    s=0
    for i in range(len(veca)):
        s+=veca[i]*vecb[i]
    return s
def getans (veca,vecb):
    print(veca,vecb)
    if vecmul(vecb,vecb)<vecmul(veca,veca):
        tmp=veca
        veca=vecb
        vecb=tmp
    print(veca,vecb)
    m=int(vecmul(veca,vecb)/vecmul(veca,veca)+0.5*sgn(vecmul(veca,vecb)))
    if(m==0):
        return veca,vecb
    for i in range(len(vecb)):
        vecb[i]-=m*veca[i]
    return getans(veca,vecb)
a=[66586820,65354729]
b=[6513996,6393464]
A,B=getans(a,b)
print(A,B)
#[2280, -1001] [-1324, -2376]
```

但显然这个思路在高维格上有效性非常有限。

### LLL

关于 LLL 算法在 [huangx607087学习格密码的笔记5](https://huangx607087.online/2021/02/06/LatticeNotes5/#12x02-LLL%E6%A0%BC%E7%BA%A6%E7%AE%80%E7%AE%97%E6%B3%95) 对原理介绍的比较清晰了；由于其在 sagemath 中已经实现好了，我们只需要知道在满足算法的条件下，LLL 能够为我们将随意的格基规约为准正交的格基（即他们之间是合理正交的）。结合 Babai 算法，就可以解决 apprCVP 。

## NTRU

> [!tip] “NTRU”是一种公钥密码系统，其名称来源于“N-th degree Truncated polynomial Ring”，即“N次截断多项式环”。关于其详细研究见 [huangx607087学习格密码的笔记4](https://huangx607087.online/2021/02/05/LatticeNotes4)，下称 H4 文。

### 1 阶构造

出于简单，我们先考虑多项式为 1 阶，即只有常数项。在 H4 文中，我们知道：密钥的安全性其实基于 $fh \equiv g \pmod q$，也即是(取 fh=g+uq) 。

> [!tip] 构造格基矩阵 M，我们倾向于：$\vec{v}\cdot M=\vec{w}$ 其中 M 为已知，w 为需求量，v 中可以未知。

$$
\begin{pmatrix}
f&-u
\end{pmatrix}
\begin{pmatrix}
1&h\\0&q
\end{pmatrix}
=f(1\quad h)+(-u)(0\quad q)=(f\quad fh-uq)
=(f\quad g)
$$

显然，这里 $M = \begin{pmatrix}1&h\\0&q\end{pmatrix}$ ，我们用 LLL 算法解决它；由于使用 LLL 算法需要满足使用 LLL 规约需要满足 Hermite theorem：$||v||\leq\sqrt{n}det(L)^{\frac1n}$，其中 ||v||表示格基的数量积，n 为维度，det(L)为格 L(矩阵)的行列式，我们引入 k 来进行调节。

```python title="NTRU_solver.py"
def NTRU_solver(h, p, c, k=1):
    from sage.all import matrix, ZZ
    """ simple NTRU solver """
    """ k is used for satisfing the condition of LLL, namely Hermite theorem """
    def decrypt(f, g, c):
        a = c * f % p
        return a * pow(f, -1, g) % g
    L = matrix(ZZ,[[1, k*h],
                   [0, k*p]])
    # L.LLL()
    w = L.LLL()[0]
    f, g = abs(w[0]), abs(w[1])//k
    return decrypt(f, g, c)
```

来看一个简单示例：

```python title="NTRU_chall.py"
from secret import flag
import libnum

bits = 2048
while True:
	q = random_prime(2^bits, lbound=2^(bits - 1))
	f = random_prime(2^(3*bits//4 - 1))
	g = random_prime(2^(bits//4 - 1))
	if gcd(f, q*g) == 1:
        h = f.inverse_mod(q) * g % q
        break
r = random_prime(2^(3*bits//4 - 1))
m = libnum.s2n(flag)
assert m < 2^(bits//4)
c = (r * h + m) % q

print('q = %d' % q)
print('h = %d' % h)
print('c = %d' % c)
"""
q = 24445829856673933058683889356407393860808522483552243481673407476395441107312130500945533047834993780864465577896968035259377721441466959027298166974554621753030728893320770628116412892838297326949997096948374940319126319050202262831370086992122741039059235809755486170276098658609363789670834482459758766315965501103856358827004129316458293962968758091319313119139703281758409686502729987426264868783862562150543872477975124482520151991822540312287812454562890993596447391870392038170902308036014733295394468384998808411243690466996284064331048659179342050962003962851315539367769981491650514319735943099663094899893
h = 4913183942329791657370364901346185016154546804260113829799181697126245901054001842015324265348151984020885129647620152505641164596983663274947698263948774663097557712000980632171097748594337673511102227336174939704483645747401790373320060474777199502879236509921155985395351647045776678540066383822814858118010995298071799515355111562392871675582742450331679030377003011729873888234401630551097244308473512890467393558048369156638425711104036276296581364374424105121033213701940135560177615395895359023414249846471332180098181632276243857635719541258706892559869642925945927703702696983949003370155033272664851406633
c = 23952867341969786229998420209594360249658731959635047659110331734424497403162506614140213749790708068086973241468969253395309243550869149482017583754015801740198734485871141965939993554966887039832701333623276590311516052334557237678750680087492306461195312290860900992532859827406262394480605001436094705579158919540851727801502678160085863180222123880690741582667929660533985778430252783414931317574267109741748071838599712027351385462245528001743693258053631099442571041984251010436099847588345982312217135023484895981833846397834589554744611429133085987275209019352039744743479972391909531680560125335638705509351
"""
```

稍加验证发现 Hermite Theorem 不满足；为此，我们需要设置好 k 来使得条件满足，这里 n=2；如果 k 的范围把握不准，爆破一般也是可以的，因为我们爆破的往往是指数，即：

```python
o = 1200
# for s in range(o-50, o+50):
for s in [1200]:
    try:
        m = NTRU_solver(h, q, c, k=(1<<s))
        flag = bytes.fromhex(hex(m)[2:])
        if b'flag' in flag:
            print(s)
            print(flag) # b'flag{7c95453a-e577-40d8-9ad0-993655b83b69}'
    except:
        continue
```

### n 阶构造

考虑 n 阶多项式，对应的有矩阵：

$$
M_{\mathbf{h}}^{\mathrm{NTRU}}=\left(\begin{array}{cccc|cccc}1&0&\cdots&0&h_0&h_1&\cdots&h_{N-1}\\0&1&\cdots&0&h_{N-1}&h_0&\cdots&h_{N-2}\\\vdots&\vdots&\ddots&\vdots&\vdots&\vdots&\ddots&\vdots\\0&0&\cdots&1&h_1&h_2&\cdots&h_0\\\hline0&0&\cdots&0&q&0&\cdots&0\\0&0&\cdots&0&0&q&\cdots&0\\\vdots&\vdots&\ddots&\vdots&\vdots&\vdots&\ddots&\vdots\\0&0&\cdots&0&0&0&\cdots&q\end{array}\right)
$$

> 没有找到对应的 ctf 题，可以通过 [huangx607087学习格密码的笔记5](https://huangx607087.online/2021/02/06/LatticeNotes5/#13x04-%E5%9B%9E%E9%A1%BE%E7%AC%94%E8%AE%B04%E4%B8%AD%E7%9A%84NTRU%E7%AE%97%E6%B3%95) 了解更多。


## Knapsack

> [!quote]
> 
> - [背包密码](https://dexterjie.github.io/2024/07/29/%E8%83%8C%E5%8C%85%E5%AF%86%E7%A0%81/)

关于背包密码，最经典的当属 Merkle-Hellman 方案；在 [DexterJie'Blog](https://dexterjie.github.io/2024/07/29/%E8%83%8C%E5%8C%85%E5%AF%86%E7%A0%81/) 和 [huangx607087学习格密码的笔记1](https://huangx607087.online/2021/02/01/LatticeNotes1/) 讲解得非常清楚，但是出于符号规范，这里简要介绍一下。

了解过程序算法中的 0-1 背包问题的同学知道，容量有限的的背包如何选择装载的物品能够价值最大是一个 NP 问题；同样的，如果背包的容量无限大，如何选择装载的物品使得价值总和恰好是一个值同样不好解决。为此，期望构造一个密码系统：选定一个有限序列，用 1/0 来表示是否选择该序列中的某一个数，进而达到隐含比特信息的目的。

但是合法接收者同样没法解决这个问题，因此引入超级递增序列：

> [!definition]- 超级递增序列
> 
> 如果一个序列 $\{a_{1}, a_{2}, \dots, a_{n}\}$ 满足 $\forall i \in [1..n-1], 2a_{i-1} \leq a_{i}$，那么这个序列成为超级递增序列。

超级递增序列是一个非常简单的情况，在 [MoeCTF2024 - Easy_Pack](../../MOECTF2024/crypto.md#Easy_Pack) 是一个例子。同样的，现在我们发现非法接收者也能够获得信息了；这是因为在破解过程中没有引入陷门信息（换言之，密钥），导致所有人都可以解密。

- 加密：
	- 生成超级递增序列 $r=(r_1,r_2,\ldots,r_n)$
	- 生成 B 满足 $B> \sum_{i=1}^{n} r_{i}$
	- 生成 A 满足 $gcd(A, B)= 1$
	- 生成序列 $M = \{M_{1}, M_{2}, \dots, M_{n}\} = Ar \pmod{B}$ 并公开
	- 对方加密信息 m：$S = \sum m_{i}*M_{i}$
- 解密：
	- 计算 $S' = A^{-1}S \pmod{B}$
	- 结合 r 求解 m

如果 A 或者 r 太小了导致 $Ar < B$，那么 B 相当于没用了，A 也很容易通过 GCD 求出，进而通过 M 恢复 r ，参见 [2020安恒五月赛-knapsack](https://badmonkey.site/archives/dasctf-2020-5#knapsack)。当然这种没啥可讨论的了，下面讨论更复杂的情况，记背包密度为：

$$
d = \frac{len(M)}{\log_2(max(M))}
$$

当背包密度小于 **0.9408**[^1] 时，使用 LLL/BKZ 能够较快地求解出来。

[^1]: M.J. Coster, A. Joux, B.A. La Macchia, A.M. Odlyzko, C.P. Schnorr and J. Stern, An improved lowdensity subset sum algorithm, Computational Complexity.2 (1992) 97-186

依旧围绕“构造格基矩阵 M，我们倾向于：$\vec{v}\cdot M=\vec{w}$ 其中 M 为已知，w 为需求量，v 中可以未知”，常见构造有：

$$
\begin{pmatrix}x_1&x_2&\ldots&x_n&-1\end{pmatrix}
\begin{pmatrix}1&0&\ldots&0&KM_1\\0&1&\ldots&0&KM_2\\\vdots&\vdots&\ddots&\vdots&\vdots\\0&0&\ldots&1&KM_n\\0&0&\ldots&0&KS\end{pmatrix}=
\begin{pmatrix}x_1&x_2&\ldots&x_n&0\end{pmatrix}
$$

其中 K 用于调整格的平衡（如满足 Herimite Theorem，减小背包密度？），在背包密码中一般取 $n=len(M), K = ceil\left( \frac{sqrt(n)}{2} \right)$ 或者 $K = ceil\left( sqrt(n) \right)$ 可能要看 [_Cryptanalysis of two knapsack public-key cryptosystems_](https://eprint.iacr.org/2009/537.pdf)。当然实际还是按情况尝试，一般而言 K 偏大依旧可解。

下面具体探讨遇到过的背包密码（名字只是我自己取方便整理的，非正式）。

### 多项式背包

> [!question]+
> 
> [MoeCTF2024-hidden-poly](https://ctf.xidian.edu.cn/training/10?challenge=148)

```python title="hidden-poly.py"
from Crypto.Util.Padding import pad
from Crypto.Util.number import *
from Crypto.Cipher import AES
import os

q = 264273181570520944116363476632762225021
key = os.urandom(16)
iv = os.urandom(16)
root = 122536272320154909907460423807891938232
f = sum([a*root**i for i,a in enumerate(key)])
assert key.isascii()
assert f % q == 0

with open('flag.txt','rb') as f:
    flag = f.read()

cipher = AES.new(key,AES.MODE_CBC, iv)
ciphertext = cipher.encrypt(pad(flag,16)).hex()

with open('output.txt','w') as f:
    f.write(f"{iv = }" + "\n")
    f.write(f"{ciphertext = }" + "\n")

"""
iv = b'Gc\xf2\xfd\x94\xdc\xc8\xbb\xf4\x84\xb1\xfd\x96\xcd6\\'
ciphertext = 'd23eac665cdb57a8ae7764bb4497eb2f79729537e596600ded7a068c407e67ea75e6d76eb9e23e21634b84a96424130e'
"""
```

如果令 $f = m*q$，那么 $S = mq，M = root^i (i \in range(16))，\vec{v} = key$ 。

$$L=\begin{bmatrix}
I_n & k\cdot\vec{M}^T\\
O_{1\times n} & k\cdot q\end{bmatrix}$$

这样我们解出来的 t = (x0, x1... x15) ，不需要再变换了。

```python title="hidden-poly_solver.py"
from sage.all import *
q = 264273181570520944116363476632762225021
r = 122536272320154909907460423807891938232
k = 1<<q.bit_length() # k 其实很大(1<<1024)也是可行的

v =  [k*ZZ(r)**i for i in range(16)]
L = block_matrix([
    [identity_matrix(16), Matrix(ZZ, 16, 1, v)],
    [zero_matrix(1, 16), Matrix(ZZ, 1, 1, [k*q])]
])

t = L.LLL()[0]
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
iv = b'Gc\xf2\xfd\x94\xdc\xc8\xbb\xf4\x84\xb1\xfd\x96\xcd6\\'
ciphertext = bytes.fromhex('d23eac665cdb57a8ae7764bb4497eb2f79729537e596600ded7a068c407e67ea75e6d76eb9e23e21634b84a96424130e')
key = "".join([chr(t[i]) for i in range(16)]).encode()
cipher = AES.new(key, AES.MODE_CBC, iv)
print(unpad(cipher.decrypt(ciphertext), 16))
# b'moectf{th3_first_blood_0f_LLL!@#$}'
```

### 哈希背包

> [!question]+
> 
> ACTF2021-Hashgame

```python title="hashgame.py"
import os
from Crypto.Util.number import *
from binascii import hexlify, unhexlify
banner = '''
               _  ___        _   _           _      ____                      
 _ __ ___   __| |/ _ \      | | | | __ _ ___| |__  / ___| __ _ _ __ ___   ___ 
| '_ ` _ \ / _` | (_) |_____| |_| |/ _` / __| '_ \| |  _ / _` | '_ ` _ \ / _ \\
| | | | | | (_| |\__, |_____|  _  | (_| \__ \ | | | |_| | (_| | | | | | |  __/
|_| |_| |_|\__,_|  /_/      |_| |_|\__,_|___/_| |_|\____|\__,_|_| |_| |_|\___|
'''
def md9(m):
    n, N = 32, 2**256
    h = 69444099843545663157429813687097031070079259699713394209624552060334679683924
    g = 91404868204801963538299172115753433950696139669081509476098772951762196709558
    assert(isinstance(m, bytes) and len(m) == n)
    for x in m:
        h = ((h + x) * g) % N
    return long_to_bytes(h)
def challenge():
    for i in range(5):
        m1 = input("> ")
        m2 = input("> ")
        try:
            m1, m2 = unhexlify(m1), unhexlify(m2)
            if m1 != m2:
                if md9(m1) != md9(m2):
                    print("Failed!")
                    return
                else:
                    print("{} win!".format(i+1))
            else:
                print("Foolish try!")
                return
        except:
            print("Something your input is wrong!")
            return
    flag = os.environ.get('FLAG')
    print("Win!Here is the flag: {}".format(flag))
def main():
    print(banner)
    challenge()
if __name__ == '__main__':
    main()
```

简单来说，题目希望我们找到 m1/m2 满足 $m_{1} \neq m_{2} \land \text{md9}(m_{1})=\text{md9}(m_{2})$；注意到 5 次循环也没有要求 m1/m2 不能重复使用，所以找到一对 m1/m2 即可。分析 md9 发现：

$$
\text{md9}(m) = hg^{32}+x_{0}g^{32}+\dots+x_{31}g^1
$$

所以

$$\text{md9}(m_{1})=\text{md9}(m_{2}) \implies \sum_{i=1}^{32}(x_{i} - y_{i})g^{33-i} = 0 \pmod{N}$$

同样可以看作一个背包问题，类似地构造有：

$$
(x_{0}-y_{0},x_{1}-y_{1},\cdots,x_{31}-y_{31},-k)\begin{bmatrix}
1&&&&&K\cdot g^{32}\\
&1&&&&K\cdot g^{31}\\
&&1&&&K\cdot g^{30}\\
&&&\ddots&&\vdots\\
&&&&1&K\cdot g\\
&&&&&K\cdot N \\
\end{bmatrix}=(x_{0}-y_{0},x_{1}-y_{1},\cdots,x_{31}-y_{31},0)
$$

关于 K 的值，实际测试发现只要不是 1 似乎都有符合条件（通过 `check_l`）的解（K=2 时有一个，测试各种 K 最多有 30 个）：

```python title="exp.py"
from sage.all import *

g = 91404868204801963538299172115753433950696139669081509476098772951762196709558
N = 2 ** 256
K = 2 ** 8
n = 32

# ===================================
# M=[I, v]
# [O, K*N]
col_vec = matrix(ZZ, n, 1, [pow(g, n-i, N) * K for i in range(n)])
M = block_matrix(ZZ, [
    [identity_matrix(n), col_vec],
    [0,                  K * N]
])
# ====================================

L = M.LLL()

# print(L)
def check_l(row):
    """
    由于没法进行交互，这个函数简单检查求解结果正确性
    输入: row (list 或 vector), 来自 LLL 归约后的矩阵行
    输出: Boolean, 是否满足模方程
    """
    # print("len(row) = ", len(row))
    N = 2**256
    g = 91404868204801963538299172115753433950696139669081509476098772951762196709558

    sum = 0
    for i in range(32):
        delta = int(row[i]) 
        weight = pow(g, 32 - i, N)
        sum = (sum + delta * weight) % N
    return sum == 0

count = 0
for l in L:
    if l[-1] == 0 and all([abs(x) <= 255 for x in l[:-1]]):
        # print(l)
        if check_l(l):
            # print("="*80)
            print(l)
            count += 1
            # break
print(count)
```

### 多背包

> [!todo] [背包密度大于 0.9408](https://www.cnblogs.com/SevensNight/p/18766376) 的情况

$$
\begin{pmatrix}x_1,x_2,\ldots,x_n,-1,-1,-1,-1\end{pmatrix}\begin{pmatrix}1&0&\ldots&0&M_{11}&\ldots&M_{41}\\0&1&\ldots&0&M_{12}&\ldots&M_{42}\\\vdots&\vdots&\ddots&\vdots&\vdots&\ddots&\vdots\\0&0&\ldots&1&M_{1n}&\ldots&M_{4n}\\0&0&\ldots&0&S_1&\ldots&0\\\vdots&\vdots&\ddots&\vdots&\vdots&\ddots&\vdots\\0&0&\ldots&0&0&\ldots&S_4\end{pmatrix}=(x_1,x_2,\ldots,x_n,0,0,0,0)
$$

### 更强的构造

但是我在使用上面的思路做下面 cryptohack 上的问题时失败了：

> [!QUESTION]
>
> [cryptohack](https://cryptohack.org/challenges/post-quantum/) Backpack Cryptography

此时尝试采用更强一些的构造和前面说的更适合的 K：

$$
\begin{pmatrix}x_1&x_2&\ldots&x_n&-1\end{pmatrix}
\begin{pmatrix}2&0&\ldots&0&KM_1\\0&2&\ldots&0&KM_2\\\vdots&\vdots&\ddots&\vdots&\vdots\\0&0&\ldots&2&KM_n\\1&1&\ldots&1&KS\end{pmatrix}
=\begin{pmatrix}2x_1-1&2x_2-1&\ldots&2x_n-1&0\end{pmatrix}
$$

```python title="Backpack Cryptography"
import random
from collections import namedtuple
import gmpy2
from Crypto.Util.number import isPrime, bytes_to_long, inverse, long_to_bytes

FLAG = b"crypto{??????????????????????????}"
PrivateKey = namedtuple("PrivateKey", ["b", "r", "q"])


def gen_private_key(size):
    s = 10000
    b = []
    for _ in range(size):
        ai = random.randint(s + 1, 2 * s)
        assert ai > sum(b)  # trapdoor
        b.append(ai)
        s += ai
    while True:
        q = random.randint(2 * s, 32 * s)
        if isPrime(q):
            break
    r = random.randint(s, q)
    assert q > sum(b)
    assert gmpy2.gcd(q, r) == 1
    return PrivateKey(b, r, q)


def gen_public_key(private_key: PrivateKey):
    a = []
    for x in private_key.b:
        a.append((private_key.r * x) % private_key.q)
    return a


def encrypt(msg, public_key):
    assert len(msg) * 8 <= len(public_key)
    ct = 0
    msg = bytes_to_long(msg)
    for bi in public_key:
        ct += (msg & 1) * bi
        msg >>= 1
    return ct


def decrypt(ct, private_key: PrivateKey):
    ct = inverse(private_key.r, private_key.q) * ct % private_key.q
    msg = 0
    for i in range(len(private_key.b) - 1, -1, -1):
        if ct >= private_key.b[i]:
            msg |= 1 << i
            ct -= private_key.b[i]
    return long_to_bytes(msg)


private_key = gen_private_key(len(FLAG) * 8)
public_key = gen_public_key(private_key)
encrypted = encrypt(FLAG, public_key)
decrypted = decrypt(encrypted, private_key)
assert decrypted == FLAG

print(f"Public key: {public_key}")
print(f"Encrypted Flag: {encrypted}")
```

不难发现问题本身是和前面相似的，但是使用和之前一样的脚本解出来的格基没有能够恢复明文的量；使用另一种构造：

```python title="optimal?bp_solver"
from sage.all import *
pk = [...] # public_key
n = len(pk)
k = ceil(sqrt(n) / 2)
dense = 1/2
pk = [k*p for p in pk]
c = 45690752833299626276860565848930183308016946786375859806294346622745082512511847698896914843023558560509878243217521
E = identity_matrix(ZZ, n)
M = block_matrix(QQ, 2, 2,
    [E, matrix(QQ, n, 1, pk), 
    matrix([dense for _ in range(n)]), matrix(QQ, [k*c])])
L = M.LLL()
# print(L)
for j, e in enumerate(L):
    if e[-1] == 0:
        msg = 0
        isValidMsg = True
        for i in range(len(e) - 1):
            ei = abs(e[i] - dense)
            if ei != 1 and ei != 0:
                isValidMsg = False
                break

            msg |= int(ei) << i

        if isValidMsg:
            print(f"{j}th: {e}")
            print(bytes.fromhex(hex(msg)[2:]))
# crypto{my_kn4ps4ck_1s_l1ghtw31ght}
```


### 带模背包

考虑加密是对求和取模：

$$S = \sum_{i=0}^n x_{i}M_{i} \pmod{p} \implies S = \sum_{i=0}^n x_{i}M_{i} - kp$$

此时的构造会变为：
$$
\begin{pmatrix}x_1&x_2&\ldots&x_n&-1&k\end{pmatrix}
\begin{pmatrix}2&0&\ldots&0&0&M_1\\0&2&\ldots&0&0&M_2\\\vdots&\vdots&\ddots&\vdots&\vdots&\vdots\\0&0&\ldots&2&0&M_n\\1&1&\ldots&1&1&S\\0&0&\ldots&0&0&p\end{pmatrix}
=(2x_1-1\quad2x_2-1\quad\ldots\quad2x_n-1\quad1\quad0)
$$

> [!tip] [Dexterjie 表示](https://dexterjie.github.io/2024/07/29/%E8%83%8C%E5%8C%85%E5%AF%86%E7%A0%81/#%E5%B8%A6%E6%A8%A1%E7%9A%84%E8%83%8C%E5%8C%85%E5%8A%A0%E5%AF%86) 因为每加密一个 bit 需要一个 $M_{i}$，加密信息往往不会很长；因此可以尝试爆破 k （毕竟 p 也不可能太小，否则导致 S 太小无法恢复。） 

> [!question]+
> 
> [LitCTF2025-Newbag](https://github.com/DexterJie/CTF_Repo/tree/main/2025/2025-5/LitCTF/new_bag)

```python title="task.py"
from Crypto.Util.number import *
import random
import string
 
def get_flag(length):
    characters = string.ascii_letters + string.digits + '_'
    flag = 'LitCTF{' + ''.join(random.choice(characters) for _ in range(length)) + '}'
    return flag.encode()

flag = get_flag(8)
print(flag)
flag = bin(bytes_to_long(flag))[2:]

p = getPrime(128)
pubkey = [getPrime(128) for i in range(len(flag))]
enc = 0
for i in range(len(flag)):
    enc += pubkey[i] * int(flag[i])
    enc %= p
f = open("output.txt","w")
f.write(f"p = {p}\n")
f.write(f"pubkey = {pubkey}\n")
f.write(f"enc = {enc}\n")
f.close()
"""
p = 173537234562263850990112795836487093439
pubkey = []
enc = 82516114905258351634653446232397085739
"""
```

这道题除了是带模的背包外，还有一点是背包密度比较大：0.9921939197933715；尝试减小背包密度？来自 [DexterJie's wp](https://github.com/DexterJie/CTF_Repo/blob/main/2025/2025-5/LitCTF/new_bag/Wp.md)：

> [!tip]+ 
> 
> 我们不可能去增大 $max(M)$ ，从减小 $len(M)$ 入手；注意到背包加密是逐比特加密，这意味着已知明文部分对应的 $M_{i}$ 是可以确定是否需要的；也即是说，结合已知明文很可能能够减小背包密度。

移除已知明文，将 flag 内部的明文看成一个新的、更小的背包加密即可，求得新密度为 0.5000727763907822。

最后在造格的时候，DexterJie 似乎写错了（真奇怪，明明上面的正确格式就是他的博客里的 hhh，估计这位师傅现在都还没发现）；正确格如下：

$$
M = \begin{pmatrix}2&0&\ldots&0&0&M_1\\0&2&\ldots&0&0&M_2\\\vdots&\vdots&\ddots&\vdots&\vdots&\vdots\\0&0&\ldots&2&0&M_n\\1&1&\ldots&1&1&S\\0&0&\ldots&0&0&p\end{pmatrix}
$$

又或者，他只是在 wp 中写错了，实际用的是这个格；但是测试发现 LLL 求解得到的格基其实确实是正确的，但是 1/-1 相反而已；而 BKZ 求解的没这个问题，下面的测试能够比较好的说明这个问题：

```python title="exp.py"
# https://github.com/DexterJie/CTF_Repo/blob/main/2025/2025-5/LitCTF/new_bag/Wp.md
# sage10.6
from sage.all import *
from Crypto.Util.number import *
from tqdm import *

p = 173537234562263850990112795836487093439
pubkey = []
enc = 82516114905258351634653446232397085739

known = b'LitCTF{' + b'\x00'*8 + b'}'
bin_known = bin(bytes_to_long(known))[2:]
for i in range(len(bin_known)):
    enc -= pubkey[i] * int(bin_known[i])
    enc %= p

new_pubkey = pubkey[-72:-8]
n = len(new_pubkey)
d = n / log(max(new_pubkey), 2)
print(CDF(d)) # 0.5000727763907822

def check(L):
    for line in L:
        if set(line[:-1]).issubset({-1,1}):
            m1 = ''
            m2 = ''
            for i in line[:n]:
                if i == 1:
                    m1 += '0'
                    m2 += '1'
                else:
                    m1 += '1'
                    m2 += '0'
            flag1 = b'LitCTF{' + long_to_bytes(int(m1,2)) + b'}'
            flag2 = b'LitCTF{' + long_to_bytes(int(m2,2)) + b'}'
            print(flag1, flag2, sep="\n")
            return True # LitCTF{Am3xItsT}
    return False

K = 2**128
Mi_col = matrix(ZZ, Mi).T
def way1():
    """爆破 k"""
    for k in range(35, 256):
        S = enc + k * p
        # M = Matrix(ZZ,n+1,n+1)
        # for i in range(n):
        #     M[i,i] = 2
        #     M[-1,i] = 1
        #     M[i,-1] = Mi[i]
        # M[-1,-1] = S
        # M[:,-1] *= K
        M = block_matrix(ZZ, [
            [2 * identity_matrix(n), Mi_col * K],
            [ones_matrix(1, n),      matrix(ZZ, [[S * K]])]
        ])

        if check(M.LLL()):
            print("==============")
            if check(M.BKZ()):
                return

def way2():
    """带模格""" 
    S = enc
    # M = Matrix(ZZ,n+2,n+2)
    # for i in range(n):
    #     M[i,i] = 2
    #     M[-2,i] = 1
    #     M[i,-1] = Mi[i]
    # 
    # M[-2,-2] = 1
    # M[-2,-1] = S
    # M[-1,-1] = p
    # M[:,-1] *= K
    M = block_matrix(ZZ, [
        [2 * identity_matrix(n), zero_matrix(n, 1), Mi_col * K],
        [ones_matrix(1, n),      matrix(ZZ, [[1]]), matrix(ZZ, [[S * K]])],
        [zero_matrix(1, n),      zero_matrix(1, 1), matrix(ZZ, [[p * K]])]
    ])
    
    check(M.LLL())
    print("==============")
    check(M.BKZ())

print("============================================================================")
way1()
print("============================================================================")
way2()
print("============================================================================")
"""
============================================================================
b'LitCTF{Am3xItsT}'
b'LitCTF{\xbe\x92\xcc\x87\xb6\x8b\x8c\xab}'
==============
b'LitCTF{Am3xItsT}'
b'LitCTF{\xbe\x92\xcc\x87\xb6\x8b\x8c\xab}'
============================================================================
b'LitCTF{\xbe\x92\xcc\x87\xb6\x8b\x8c\xab}'
b'LitCTF{Am3xItsT}'
==============
b'LitCTF{Am3xItsT}'
b'LitCTF{\xbe\x92\xcc\x87\xb6\x8b\x8c\xab}'
============================================================================
"""
```

### 乘法背包

前面的背包都是“选择加上哪些”并给出最后的和；如果是“选择乘上哪些”并给出最后的积呢？

> [!todo]+ [Meet me in the summer](https://dexterjie.github.io/2024/07/14/%E8%B5%9B%E9%A2%98%E5%A4%8D%E7%8E%B0/WKCTF/#Meet-me-in-the-summer%E2%80%94%E2%80%94%E5%A4%8D%E7%8E%B0)

基本思路：先求解离散对数，转变为加法背包；但是我觉得上面的 $ra\equiv a_0k_{70}\times a_1k_{69}\times\ldots\times a_{69}k_1 \pmod{p}$ 构造是一个败笔，显然应该是 $ra\equiv a_0^{k_{70}}\times a_1^{k_{69}}\times\ldots\times a_{69}^{k_1} \pmod{p}$ 更加合理，取对数后也更加顺利（虽然同样因为在环上需要求解离散对数问题。）

## LWE&RLWE

> [!todo]+ 
> 
> - [x] https://triodelzx.github.io/2025/07/07/LWE/index.html
> - [ ] https://tover.xyz/p/lattices-LWE/
> - [ ] https://tover.xyz/p/d3bdd-note/#%E5%9F%BA%E6%9C%ACRLWE%E8%A7%A3%E6%B3%95
> - [ ] https://lazzzaro.github.io/2020/11/07/crypto-%E6%A0%BC%E5%AF%86%E7%A0%81/index.html#LWE%E9%97%AE%E9%A2%98
> - [ ] https://hackmd.io/@rota1001/google-ctf-2025
> - [ ] https://tangcuxiaojikuai.xyz/post/b137586.html 
> - [ ] https://blog.maple3142.net/2023/11/05/tsg-ctf-2023-writeups/#learning-with-exploitation
> - [ ]  [Aero CTF 2020 - Magic II](https://gist.github.com/hakatashi/2266a5df35cc79de50b86d2419b33a6f)

容错学习 (Learning With Error, LWE) 及其变体是当前后量子密码格基实现的主要凭据。

最基本的 LWE 中，问题形式为：$\boldsymbol{b}\equiv \boldsymbol{As}+\boldsymbol{e}\quad(\mathrm{mod~}q)$（A,b 为公钥，s 为秘密，e 为噪声）；RLWE 即环上的容错学习问题，即运算在商环上进行：

$$
R=\frac{\mathbb{Z}[x]}{(x^n+1)},R_q=\frac{(\mathbb{Z}/q\mathbb{Z})[x]}{(x^n+1)}
$$

由构建形式不难得到：$q\boldsymbol{k}-\boldsymbol{As}+\boldsymbol{b}=\boldsymbol{e}$，可以构建格：

$$
M=\begin{pmatrix}q\boldsymbol{I}_m&0&0\\-\boldsymbol{A}^T&\boldsymbol{I}_n&0\\\boldsymbol{b}&0&1\end{pmatrix}
$$

使得：$(\boldsymbol{k}^T,\boldsymbol{s}^T,1)\boldsymbol{B}=(\boldsymbol{e}^T,\boldsymbol{s}^T,1)$，基本的脚本如下：

```python title="naive lwe"
M = block_matrix(ZZ, 3, 3, 
                [[q, 0, 0],
                [-A.transpose(), 1, 0],
                [matrix(b), 0, 1]])
L = M.LLL()
```

> [!example]-
> 
> [New Year Ring1 - 2024-NSSCTF-Round-18](https://tangcuxiaojikuai.xyz/post/7a9f0ad2.html)

```python title="better lwe"
m = len(b[0])
B = block_matrix(ZZ, 2, 1, [[A.transpose()], [q]])
B_HNF = B.hermite_form(include_zero_rows=False)

M = block_matrix(ZZ, 2, 2, [[B_HNF, 0], [matrix(b), 1]])

M = M.LLL()[0]

if M[-1] == -1:
    e = -vector(M[:-1])
else:
    e = vector(M[:-1])

cvp = vector(b) - e

AA = matrix(Zmod(q), A)
cvp = vector(Zmod(q), cvp)

s = AA.solve_right(cvp)
```

## Truncated LCG

> [!todo] 
> 
> - [ ] https://tover.xyz/p/HNP-note/
> - [ ] https://huangx607087.online/2024/12/05/LatticeNotes8/#1x02-%E6%A0%BC%E7%9A%84%E6%9E%84%E9%80%A0%E6%96%B9%E6%B3%95%E5%9B%9E%E9%A1%BE

Truncated LCG 通常是指构造一个 LCG，并利用其中的一部分（通常是低位或高位）作为伪随机数使用。如下面这个挑战：

> [!question]+ 
> 
> NPUCTF2020-BABYLCG

```python title="task.py"
from Crypto.Util.number import *
from Crypto.Cipher import AES
from secret import flag
class LCG:
    def __init__(self, bit_length):
        m = getPrime(bit_length)
        a = getRandomRange(2, m)
        b = getRandomRange(2, m)
        seed = getRandomRange(2, m) # s0
        self._key = {'a':a, 'b':b, 'm':m}
        self._state = seed 
    def next(self):
        self._state = (self._key['a'] * self._state + self._key['b']) % self._key['m']
        return self._state
    def export_key(self):
        return self._key

def gen_lcg():
    rand_iter = LCG(128)
    key = rand_iter.export_key()
    f = open("key", "w")
    f.write(str(key))
    return rand_iter

def leak_data(rand_iter):
    """
    泄露了 s1-s20 的高 64 位
    """
    f = open("old", "w")
    for i in range(20):
        f.write(str(rand_iter.next() >> 64) + "\n")
    return rand_iter

def encrypt(rand_iter):
    f = open("ct", "wb")
    key = rand_iter.next() >> 64
    key = (key << 64) + (rand_iter.next() >> 64) # 用 s21,s22 的高 64 位作为 key
    key = long_to_bytes(key).ljust(16, b'\x00')
    iv = long_to_bytes(rand_iter.next()).ljust(16, b'\x00') # 用 s23 作为 iv
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = flag + (16 - len(flag) % 16) * chr(16 - len(flag) % 16) # padding
    ct = cipher.encrypt(pt.encode())
    f.write(ct)
def main():
    rand_iter = gen_lcg()
    rand_iter = leak_data(rand_iter)
    encrypt(rand_iter)

if __name__ == "__main__":
    main()
```

在 [LatticeNotes5](https://huangx607087.online/2021/02/06/LatticeNotes5/#14x01-NPUCTF2020-BABYLCG) 中给出了一个常见的分析思路：

对于 LCG 的状态序列记为 $S = \{s_{0}, s_{1}, \dots\}$ ，并记 $s_{i} = (c_{i} \ll 64) + d_{i}$ ；也即将已知的 $c_{i}$ 与未知的 $d_{i}$ 分开；由递推关系式有（出于方便我们在推导时用 $c_{i}$ 代指 $c_{i} \ll 64$）：

$$
s_{i+1} = a*s_{i} + b \pmod{m} \Rightarrow c_{i+1}+d_{i+1} = a(c_{i}+d_{i}) + b \pmod{m}
$$

我们期望得到一个新的递推关系式，整理得到：

$$
c_{i+1}+d_{i+1} =a(c_{i}+d_{i}) + b + km  \implies d_{i+1} =  mk + ad_{i} + ac_{i} + b - c_{i+1}
$$

显然在等式右边，$d_{i}, k$ 都是未知的，其余已知。回顾前面提到的：

> [!tip] 构造格基矩阵 M，我们倾向于：$\vec{v}\cdot M=\vec{w}$ 其中 M 为已知，w 为需求量，v 中可以未知。

自然的我们有：

$$
\begin{bmatrix}k&d_i&1\end{bmatrix}\begin{bmatrix}m&?&?\\a&?&?\\ac_i+b-c_{i+1}&?&?\end{bmatrix}=\begin{bmatrix}d_{i+1}&?&?\end{bmatrix}
$$

其中 ? 部分是我们为了凑格基需要填充的，而等式右边是我们求短向量后可能可以求得的。显然 $\vec{w}$ 中的内容必然要与 $k, d_{i}$ 有关，或者是一个已知数（尝试过两个都是已知数，求解得到的 $d_{i+1} = 0$）。相比于 k，我们对 $d_{i}$ 更加感兴趣（还可以用来验证我们的求解是否正确）。所以，M 的第二列我们取 $[0, 1, 0]$，第三列取 $[0, 0, X]$，这个 X 需要我们来选择。

> [!question]+ 为什么第三列是 $[0, 0, X]$，而不能是 $[1, 0, 0]$ （求 k）或者是 $[0, 0, 1]$ （直接取 1）呢？
> 
> （这部分可能自己了解的也不是很清楚，后续有新发现再来修改）
> 
> 回顾 Hermite Theorem：$||w|| \leq \sqrt{n}\cdot\sqrt[n]{\det L}$；
> 
> - 简单估计可以得到 k 大概为 128 位，$\sqrt[n]{\det L} = \sqrt[3]{k(ac_i+b-c_{i+1})}$ 大约也为 128 位，最后的 $||w|| = \sqrt{d_{i}^2 + d_{i+1}^2 + k^2}$ 大约也为 128 位，$d_{i}, d_{i+1}$ 的影响变得非常小（至少我自己试了没有正确解，找到了更短的向量，但是不正确）
> - 而对于 $[0, 0, X]$, $||w|| = \sqrt{d_{i}^2 + d_{i+1}^2 + X^2}, \sqrt[n]{\det L} = \sqrt[3]{mX}$ ，显然 X = 1 不能满足要求
> 	- 但这里就是我迷惑的地方了，[LatticeNotes5](https://huangx607087.online/2021/02/06/LatticeNotes5/#14x01-NPUCTF2020-BABYLCG) 说此时 X 越大越好，但是似乎 $||w||$ 的增长速度是比 $\sqrt[3]{mX}$ 快的，X 不宜过大才对；但是实际测试取  $X = 1\ll 1024$ 都是能够成功的（最小的在 $X=1 \ll 54$ 左右）
> 	- 在[这个 wp](https://jayxv.github.io/2020/05/12/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%E4%B9%8BHNP/) 提到：“让 w 的每一项长度都差不多，这样也有利于找到 w”；所以我想 64 还是一个不错的选择（确实成功了），读者可以自己尝试。

```python title="exp1.py"
from ast import literal_eval
f = open("key", "r")
key = literal_eval(f.readline())
f = open("old", "r")
leak_data = [int(l.strip('\n')) for l in f.readlines()]
f = open("ct", "rb")
ct = f.read()
f.close()

from sage.all import *
a, b, m = key['a'], key['b'], key['m']
c19 = leak_data[-2]
c20 = leak_data[-1]
X = 1 << 64
K = (a * (c19 << 64) + b - (c20 << 64)) % m
M = matrix(ZZ, [[m, 0, 0],
                [a, 1, 0],
                [K, 0, X]])
L = M.LLL() 
# print(L)
# -----------------------
def check(s0, s1):
    return s1 == (a*s0 + b) % m

for l in L:
    if abs(l[-1]) == X:
        d19 = abs(l[1])
        d20 = abs(l[0])
        s19 = (c19 << 64) + d19
        s20 = (c20 << 64) + d20
        if check(s19, s20):
            print(f"s19: {s19}", f"s20: {s20}")
# [ 1871065480715670803    749046401503574202  18446744073709551616]
# -----------------------
from Crypto.Util.number import *
from Crypto.Cipher import AES
s20 = 90888742167094632308617091277078238483
def gen_next(s0):
    return (a * s0 + b) % m
s21 = gen_next(s20)
s22 = gen_next(s21)
s23 = gen_next(s22)
key = s21 >> 64
key = (key << 64) + (s22 >> 64) # 用 s21,s22 的高 64 位作为 key
key = long_to_bytes(key).ljust(16, b'\x00')
iv = long_to_bytes(s23).ljust(16, b'\x00')
cipher = AES.new(key, AES.MODE_CBC, iv)
pt = cipher.decrypt(ct)
print(pt) # b'npuctf{7ruc4t3d-L(G-4nd-LLL-4r3-1nt3r3st1ng}\x04\x04\x04\x04'
```

在上面的推导中，我们关注于低位的递推关系；而在[密码学学习笔记之HNP](https://jayxv.github.io/2020/05/12/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%E4%B9%8BHNP/) 中，则发现了所有低位与 $d_{1}$ 的关系：

$$
d_{i+1} = A_{i}l_{i} + B_{i} \pmod{m}
$$

其中 $\begin{cases}A_{i} = aA_{i-1} \% m \\ B_{i} = aB_{i-1} + ac_{i} + b - c_{i+1} \% m\end{cases}$

进而类似地有：

$$
vM=[\begin{array}{cccccccc}k_{1}&k_{2}&\cdots&k_{19}&l_{1}&1\end{array}]\begin{bmatrix}m&&&&&&\\&m&&&&&\\&&\ddots&&&&\\&&&m&&&\\A_{1}&A_{2}&\ldots&A_{19}&1&&\\B_{1}&B_{2}&\ldots&B_{19}&0&2^{64}\end{bmatrix}=[\begin{array}{cccccc}l_{2}&l_{3}&\cdots&l_{20}&l_{1}&2^{64}\end{array}]=w
$$

> 但是按前面的方法我们只要求解了任何一个状态，整个状态序列 S 是完全可解的，所以两种方法基本等效；后者可能约束更强更容易求解得到正确结果。

在[角最大值+对角(1,-k)对值构造法](https://huangx607087.online/2021/07/25/LatticeNotes7/#2o02-%E8%A7%92%E6%9C%80%E5%A4%A7%E5%80%BC-%E5%AF%B9%E8%A7%92-1-k-%E5%AF%B9%E5%80%BC%E6%9E%84%E9%80%A0%E6%B3%95) 中分析了该格结构。

## 主要参考资料

- [密码学基础之格理论基础](https://jayxv.github.io/2023/10/08/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%9F%BA%E7%A1%80%E4%B9%8B%E6%A0%BC%E7%90%86%E8%AE%BA%E5%9F%BA%E7%A1%80/)
- [密码学基础之格中难题与格基规约](https://jayxv.github.io/2023/10/17/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%9F%BA%E7%A1%80%E4%B9%8B%E6%A0%BC%E4%B8%AD%E9%9A%BE%E9%A2%98%E4%B8%8E%E6%A0%BC%E5%9F%BA%E8%A7%84%E7%BA%A6/)
- [格密码应用](https://harry0597.com/2022/12/30/%E6%A0%BC%E5%AF%86%E7%A0%81%E5%BA%94%E7%94%A8/)

- [CTF-Crypto】格密码基础（例题较多，非常适合入门！）](https://blog.csdn.net/jayq1/article/details/140872034)
- https://huangx607087.online/2024/12/05/LatticeNotes8/
- https://hasegawaazusa.github.io/lattice-note.html

- tools
	- [flatter](https://github.com/keeganryan/flatter)
		- https://huangx607087.online/2024/12/05/LatticeNotes8/#4x04-flatter
	- [BLASter](https://github.com/ludopulles/BLASter/)
		- [2025-WMCTF-wp-crypto](https://tangcuxiaojikuai.xyz/post/b852ef1b.html)