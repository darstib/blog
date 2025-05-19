---
tags:
- notes
- ctf
comments: true
---

## 同态加密 (HE)

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/11_1741698768330.png)

## 半同态加密 (PHE)

### Paillier PHE

```python title="paillier PHE (simple version)"
# m = b2l(msg)
p, q = random_prime(), random_prime()
n = p * q
lambda = lcm(p-1, q-1) # secret key
g = n + 1 
# (n, g) is public key
r = randint(1, n) # assert gcd(r, n)=1
### encrypt
c = (g**m * r**n) % (n*n)
### decrypt
m = (c**lambda % n**2 -1) // (g**lambda % n**2 -1)
```

**数学检验：** $c^\lambda\mathrm{mod~n^2=(g^{m*}r^n)^\lambda mod~n^2=g^{m\lambda}mod~n^2=(1+n)^{m\lambda}mod~n^2=1+nm\lambda}$（使用到欧拉公式），同时 $g^\lambda\mathrm{mod~n^2=1+n\lambda~mod~n^2}$ ，所以 $m = \frac{(c^\lambda\text{ mod n}^2-1)/n}{(g^\lambda\text{ mod n}^2-1)/n}$ 。

**同态性：** 记 $c = p(m)$，则有 

$$
\begin{cases}
p(m_{1}) \oplus p(m_{2})= c_{1}\oplus c_{2} = c_{1}*c_{2} = g^{(m_{1}+m_{2})}(r_{1}*r_{2})^{n} \pmod{n^{2}} = p(m_{1}+m_{2}) \\
p(m) \odot k = c \odot k = c^{k} = g^{mk}r^{nk} \pmod{n^{2}} = p(m*k)  
\end{cases}
$$

但是实际解题时发现：在 $\lambda$ 相当大时， $1+nm\lambda > n^{2}$ 是非常有可能的，分子取模后远远小于 $1+nm\lambda$ 出现最终获得的 $m<2$ ；而如果不取模，这个运算得到的数字是非常非常非常大的（且此时在 python 中应当使用 `pow(c, lambda, n*m)` 而不是使用 `%`；前者每次相乘都取模，后者则是指数运算完成再取模，效率完全不同），所以并不好用代码实现。

> [!wiki]- 
>
> 在[维基百科](https://en.wikipedia.org/wiki/Paillier_cryptosystem)上给出了更加通用的形式和求解方法，证明可见[密码学学习笔记 之 paillier cryptosystem](https://jayxv.github.io/2020/05/14/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%E4%B9%8Bpaillier%20cryptosystem/)

```python title="paillier PHE (full version)"
# m = b2l(msg)
p, q = random_prime(), random_prime()
n = p * q
Lambda = lcm(p-1, q-1)
g = randint(1, n**2)
def L(x, n)
    return (x-1)/n
mu = inverse_mod(L(pow(g, Lambda, n*n)))
# public key: (n, g)
# secret key: (Lambda, [mu]) # 知道 Lambda 就能求 mu
m = mod(L(pow(c, Lambda, n*n))*mu, n)
```

#### 2020 dasctf not RSA

热身题：

```python title="chall.py"
from Crypto.Util.number import getPrime as getprime ,long_to_bytes,bytes_to_long,inverse
from secret import flag,p,q
from sympy import isprime,nextprime
import random

m=bytes_to_long(flag)
n=p*q
g=n+1
r=random.randint(1,n)

c=(pow(g,m,n*n)*pow(r,n,n*n))%(n*n)

print "c=%d"%(c)
print "n=%d"%(n)

'''
c=29088911054711509252215615231015162998042579425917914434962376243477176757448053722602422672251758332052330100944900171067962180230120924963561223495629695702541446456981441239486190458125750543542379899722558637306740763104274377031599875275807723323394379557227060332005571272240560453811389162371812183549
n=6401013954612445818165507289870580041358569258817613282142852881965884799988941535910939664068503367303343695466899335792545332690862283029809823423608093
'''
```

由于只是为了熟悉这个算法，不难发现 n 非常小，容易分解；使用 factordb 分解后，完成脚本即可：

```python title="solve1.py"
from libnum import invmod, lcm, n2s

c = 29088911054711509252215615231015162998042579425917914434962376243477176757448053722602422672251758332052330100944900171067962180230120924963561223495629695702541446456981441239486190458125750543542379899722558637306740763104274377031599875275807723323394379557227060332005571272240560453811389162371812183549
n = 6401013954612445818165507289870580041358569258817613282142852881965884799988941535910939664068503367303343695466899335792545332690862283029809823423608093
p, q = (
    80006336965345725157774618059504992841841040207998249416678435780577798937447,
    80006336965345725157774618059504992841841040207998249416678435780577798937819,
)

Lambda = lcm(p - 1, q - 1)

# 计算 μ (inverse_mod(L(g^lambda mod n^2), n))，其中 g = n + 1
g = n + 1
n_2 = n * n
mu = invmod((pow(g, Lambda, n_2) - 1) // n, n)

m = ((pow(c, Lambda, n_2) - 1) // n * mu) % n
print(n2s(m))
```

当然，p, q 都有了，就是一个正常的解密，我们还可以借助 `phe` 这个 python 库：

```python title="solve2.py"
from phe import paillier

c = 29088911054711509252215615231015162998042579425917914434962376243477176757448053722602422672251758332052330100944900171067962180230120924963561223495629695702541446456981441239486190458125750543542379899722558637306740763104274377031599875275807723323394379557227060332005571272240560453811389162371812183549
n = 6401013954612445818165507289870580041358569258817613282142852881965884799988941535910939664068503367303343695466899335792545332690862283029809823423608093
p, q = (
    80006336965345725157774618059504992841841040207998249416678435780577798937447,
    80006336965345725157774618059504992841841040207998249416678435780577798937819,
)

public_key = paillier.PaillierPublicKey(n=n)
private_key = paillier.PaillierPrivateKey(public_key=public_key, p=p, q=q)

decrypted_message = private_key.decrypt(paillier.EncryptedNumber(public_key, c))

print(bytes.fromhex(hex(decrypted_message)[2:]).decode())
```

> [!flag]-
>
> flag{5785203dbe6e8fd8bdbab860f5718155}

## 全同态 (FHE)

![1741700485340.webp](https://raw.githubusercontent.com/darstib/public_imgs/utool/2503/11_1741700485340.webp)

## 参考资料

- [《隐私计算基础理论：同态加密》](https://www.yuque.com/secret-flow/admin/szl9kqhocgszeod9)
- [密码学学习笔记 之 paillier cryptosystem](https://jayxv.github.io/2020/05/14/%E5%AF%86%E7%A0%81%E5%AD%A6%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0%E4%B9%8Bpaillier%20cryptosystem/)
