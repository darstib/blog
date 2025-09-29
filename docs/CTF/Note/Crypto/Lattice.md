---
tags:
- notes
- ctf
comments: true
---

## 基础格密码

### NTRU

> 经典加密算法，被格基规约攻破，见[格密码笔记（一）](https://www.ruanx.net/lattice-1/)。

在上面的文章中，得到一个公式：我们知道，密钥的安全性其实基于 $fh \equiv g \pmod r$，也即是(取 fh=g+pr) 。

构造格基矩阵 M，我们倾向于：$\vec{v}\cdot M=\vec{w}$ 其中 M 为已知，w 为需求量，v 中可以未知。

$$
\begin{pmatrix}
f&-r
\end{pmatrix}
\begin{pmatrix}
1&h\\0&p
\end{pmatrix}
=f(1\quad h)+(-r)(0\quad p)=(f\quad fh-rp)
=(f\quad g)
$$

为了简单，我们用 sage 中的 LLL 算法解决它；由于使用 LLL 算法需要满足使用 LLL 规约需要满足 Hermite theorem：$||v||\leq\sqrt{n}det(L)^{\frac1n}$，其中 ||v||表示格基的数量积，n为维度，det(L)为格L(矩阵)的行列式，我们引入 k 来进行调节。

```python title="NTRU_solver.py"
def NTRU_solver(h, p, c, k=1):
    from sage.all import *
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

来看下面的问题：

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

稍加验证发现 Hermite 不满足；为此，我们需要设置好 k 来使得条件满足，这里 n=2；如果 k 的范围把握不准，爆破一般也是可以的，因为我们爆破的往往是指数，即：

```python
o = 1200
# for s in range(o-50, o+50):
for s in [1200]:
    try:
        m = NTRU_solver(h, q, c, k=(1<<s))
        flag = bytes.fromhex(hex(m)[2:])
        if b'flag' in flag:
            print(flag) # b'flag{7c95453a-e577-40d8-9ad0-993655b83b69}'
    except:
        continue
```

### Merkle–Hellman

> 经典的背包加密问题，[格密码笔记（二）](https://www.ruanx.net/lattice-2/) 讲的很清楚了。

> [!extra]- 超级递增序列
> 
> 在上面的格密码笔记中，超级递增序列是一个比较简单的情况，在 [Easy_Pack](../../MOECTF2024/crypto.md#Easy_Pack) 是一个例子。

在理解上，我们将下面这题转变为上面文章中描述。

```python title="hidden-poly"
# https://ctf.xidian.edu.cn/training/10?challenge=148
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

但是我在使用上面的思路做下面 cryptohack 上的问题时失败了：

> [!QUESTION]
>
> [cryptohack](https://cryptohack.org/challenges/post-quantum/) Backpack Cryptography

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

不难发现问题本身是和前面相似的，但是使用和之前一样的脚本解出来的格基没有能够恢复明文的量；如下改进[^1]（针对二进制编码）后可行：

[^1]: 改进原理可能要看[这篇论文](https://eprint.iacr.org/2009/537.pdf) 。

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

## 复现

### RaRCTF 2021 Snore

> [!TODO]
>
> https://jgeralnik.github.io/writeups/2021/08/12/Lattices/

## 参考资料

> 上面有所提及的此处可能没有写入。

- [密码学基础之格理论基础](https://jayxv.github.io/2023/10/08/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%9F%BA%E7%A1%80%E4%B9%8B%E6%A0%BC%E7%90%86%E8%AE%BA%E5%9F%BA%E7%A1%80/)
- [密码学基础之格中难题与格基规约](https://jayxv.github.io/2023/10/17/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%9F%BA%E7%A1%80%E4%B9%8B%E6%A0%BC%E4%B8%AD%E9%9A%BE%E9%A2%98%E4%B8%8E%E6%A0%BC%E5%9F%BA%E8%A7%84%E7%BA%A6/)
- [格密码应用](https://harry0597.com/2022/12/30/%E6%A0%BC%E5%AF%86%E7%A0%81%E5%BA%94%E7%94%A8/)
- [sage - Discrete subgroups of Zn](https://doc.sagemath.org/html/en/reference/modules/sage/modules/free_module_integer.html)
