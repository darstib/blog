---
tags:
- notes
- ctf
comments: true
---

## I 基本原理

### I.1 加密原理

1. 寻找两个大质数 p, q（p/q 之间的关系暂且不谈，不当的选取就会导致攻击漏洞）；
2. n = pq; $phi = \phi(n) = (p-1)(q-1)$ （欧拉函数）
3. 寻找一个 e，使得：$1<e<phi$ 且 gcd(e, phi) = 1
4. m 为明文映射为的大数，则密文 $c\equiv m^e\pmod{n}$
5. (e, n) 作为公钥公开。

### I.2 解密原理

1. 私钥为 $d=e^-1\pmod{\phi(n)}$
2. $c^d = m^{ed}\pmod{n} = m^{ed\pmod{\phi(n)}} =m$

### I.3 安全性保证

**正常** 的 RSA 的安全性完全来自 n 的质数分解难度；不正常的是什么？看下面就知道了。

## II 指数攻击

### II.1 Low public exponent attack（低加密指数攻击）

#### II.1.1 e = 1

> [!QUESTION]
>
> [cryptohack - Salty](https://cryptohack.org/challenges/rsa/)

cryptohack 上刚好有这么一个题，就一并放在这里了：

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

> [!FLAG]
>
> crypto{saltstack_fell_for_this!}

#### II.1.2 e = 2 (Rabin)

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

#### II.1.3 e = 3

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

### II.2 gcd(e, phi) != 1

#### II.2.1 一组 e, phi

一般来说 $gcd(e, \phi)=1$ 的，但要是 $gcd(e, \phi)\neq 1$ ，那么怎么做？e=2/3/4 …… 等十分小的数时后面另讲，这里考虑比较一般的情况。

由于 $gcd(e, \phi)\neq 1$，正常意义下的私钥 d 是不存在的，但是考虑到欧拉扩展定理：

若 $gcd(e, \phi) = b \neq 1$ ，则有 $c = m^e = m^{ab}\pmod{n} = m^{ab \pmod{\phi}}$ （$gcd(a, \phi)=1$，否则 $gcd(e, \phi)=1$ 不成立）；取 $d = a^{-1}\pmod{\phi}$，则有 $c^d = m^{bad\pmod{\phi}} =  m^b\pmod{n}$；所以只需要对 $c^d\pmod{\phi}$ 开 b 次根就好。

当然，不难发现，哪怕 $gcd(e, \phi)=1$ ，上述过程依然适用。

```python
from sage.all import *

p= 127577058764408216374028752283743628765651360507566484643526093715329608267323381565274095814069864692746147152580906850350743742856555229701448239882612922698102985146366639955081466129923966803267071097174222576416224094182123529282235807472362341680183683025490897702891081336913842652559163341223338641607
q= 156492273708587234539506501480609692085997989594717058472605523051244522493701609615085173280972894139427194976925940854142835807192417391269823151398439665817176522629246535810290194301862945052149450578938260979300632842291287807430486629994530805358742405299538986591596966945727494262182814875780600646003
e= 750
c= 7029383721249299532521086933490698266831518266762255492452526410777276825803657150303837084263410309063739203644435184397762022380085273363900423091223180151147964276354189658062571415744140073426572149093499560918765793389358300893454490774387180728097370701432534877005948330689495694820361726719418371072834639369078180094444137972424909816959445043108154884587947573054460257114169961823509538355580857411319157089278918107229480661280354242839678709689654304688727345294473487201644985815128413154870914132135222144633969959773621933444285994038028721862094040876152694240238708737727034258171506516394913692187

import sympy
n = p*q
phi = (p-1)*(q-1)
b = gcd(e, phi) # b = 6
a = e // b
d = inverse_mod(a, phi)
m_b = power_mod(c, d, n)
m = Integer(m_b).nth_root(b)
print(bytes.fromhex(hex(m)[2:]))
# b'flag{0e2f9add-31fd-4733-8f25-39297516f4e2}'
```

#### II.2.2 多组 e phi

攻击条件：gcd(e, phi) != 1，gcd(n1, n2) != 1

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

##### II.2.2.1 新的 gcd(e,phi)=1

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

##### II.2.2.2 新的 gcd(e, phi)!=1

要是新产生的 gcd(e,phi)!=1 ，就转变为了 [一组 e, phi](#一组%20e,%20phi) 的情况了：

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

## III 模数攻击

### III.1 N 太小/被公开

> [!QUESTION]
>
> [CryptoHack – RSA challenges](https://cryptohack.org/challenges/rsa/) Everything is Big

题目中给出了很大的 N，但是放到 factordb.com 中，分解一下就出来了；或者对于比较小的 N，sage math 的 factor 之类的都可以分解。

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

### III.2 Roll 按行加密

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

### III.3 模不互素

模不互素是指：多次给出的 n 不互素，那么使用欧几里得算法求解公因数后两个都可以分解，从而被破解。

### III.4 多素数 RSA

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

### III.5 共模攻击

攻击条件：使用相同的 n，不同的 e 对同一段密文进行了两次加密且 gcd(e1, e2)=1。

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

### III.6 p & q 选取不当

#### III.6.1 |p-q| 较小

> [CTF Wiki (ctf-wiki.org)](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_module_attack/#p-q_1)

常见的情况有 `q = next_prime(p)` 导致二者非常接近。

> [!QUESTION]
>
> [CryptoHack – RSA challenges](https://cryptohack.org/challenges/rsa/) Infinite Descent

```python title="small_p_min_q"
from sage.all import *
n = ...
e = 65537
c = ...

def small_p_min_q(n):
    a = ceil(nth_root(n, 2))
    b = a**2 - n
    while not is_square(b):
        a += 1
        b = a**2 - n
    
    c = nth_root(b, 2)
    return a-c, a+c

p, q = small_p_min_q(n)
# print(p, q)
phi = (p-1)*(q-1)
d = inverse_mod(e, phi)
m = power_mod(c, d, n)
from Crypto.Util.number import *
print(long_to_bytes(m)) # b'crypto{f3rm47_w45_4_g3n1u5}'
```

#### III.6.2 n & npnq

偶然间做到这么一个题，给我 e, n, c 之外，还给我 npnq，其中 `n == p*q and npnq = next_prime(p)*next_prime(q)`

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

#### III.6.3 RSA backdoor (4p-1 method)

攻击条件：$4p-1 = Ds^2$ 其中 Ds 参见 [cm_factorization](https://github.com/crocs-muni/cm_factorization) 。

## IV 私钥攻击

### IV.1 d 泄露攻击

当对应的 (e,d) 泄露后，我们就能够分解对应的 N 。具体原理可见 [ctf-wiki](https://ctf-wiki.org/crypto/asymmetric/rsa/d_attacks/rsa_d_attack/#d_1) 。

>  [rsatool](https://github.com/ius/rsatool) calculates RSA (p, q, n, d, e) and RSA-CRT (dP, dQ, qInv) parameters given either two primes (p, q) or modulus and private exponent (n, d).

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

### IV.2 dp || dq leak attack

> [!DEFINITION]
>
> $dp \equiv d\pmod{p-1}, dq \equiv d\pmod{q-1}$

攻击条件：直到 dp 或者 dq，完整的公钥 (n,e) 和密文 c。
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

### IV.3 dp && dq leak attack

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

### IV.4 dp && dq && dr leak attack

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

### IV.5 Wiener's Attack （维纳攻击）

攻击使用于：e 较大，$d< \frac{1}{3}N^{1/4}, q<p<2q$ 。

原理简述：由于 $ed \equiv 1\pmod{\phi(n)} \implies ed = k*\phi + 1$ ，当 n 较大时，$ed \approx k*\phi \approx k*n\implies \frac{e}{n} \approx \frac{k}{d}$  ；利用连分数从两侧逼近于极限值的特点，找到真正的 d & k ；甚至我们求解 $\phi$ 后能够分解出 p/q 。 

> [!extra]-
>
>> [!theorem] Legendre's theorem
>> 
>> 如果存在 $\alpha \in Q$, $c,d \in Z$: $|a- \frac{c}{d}|< \frac{1}{2d^2}$，那么 $\frac{c}{d}$ 就是 $\alpha$ 的一个有理近似。
>  
> $ed = k*\phi + 1 \implies | \frac{e}{\phi}- \frac{k}{d}|= \frac{1}{d*\phi}$
> 
> 大部分情况下，构成 $n=p*q$ 公式中，p 与 q 的二进制长度相同，即有 $p < q < 2*p$ （p q 可互换位置）；由适当推导可以得到 $d< \frac{1}{3}N^{1/4} \implies (3d)^4 < n$

> 攻击代码可以使用 [crypto-attacks/attacks/rsa/wiener_attack.py](https://github.com/jvdsn/crypto-attacks/blob/master/attacks/rsa/wiener_attack.py) ，下面是一个使用示例：

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

> [!EXAMPLE]
>
> - [[CISCN 2022 东北赛区]math](https://www.nssctf.cn/problem/2387)

### IV.6 Boneh and Durfee attack

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

> [ctf-wiki - Boneh and Durfee attack](https://ctf-wiki.org/crypto/asymmetric/rsa/rsa_coppersmith_attack/?h=boneh+durfee#boneh-and-durfee-attack)
> 
> [boneh_durfee.sage](https://github.com/mimoo/RSA-and-LLL-attacks/blob/master/boneh_durfee.sage)

```python title="final.py"
d = 4405001203086303853525638270840706181413309101774712363141310824943602913458674670435988275467396881342752245170076677567586495166847569659096584522419007
N = 0xb12746657c720a434861e9a4828b3c89a6b8d4a1bd921054e48d47124dbcc9cfcdcc39261c5e93817c167db818081613f57729e0039875c72a5ae1f0bc5ef7c933880c2ad528adbc9b1430003a491e460917b34c4590977df47772fab1ee0ab251f94065ab3004893fe1b2958008848b0124f22c4e75f60ed3889fb62e5ef4dcc247a3d6e23072641e62566cd96ee8114b227b8f498f9a578fc6f687d07acdbb523b6029c5bbeecd5efaf4c4d35304e5e6b5b95db0e89299529eb953f52ca3247d4cd03a15939e7d638b168fd00a1cb5b0cc5c2cc98175c1ad0b959c2ab2f17f917c0ccee8c3fe589b4cb441e817f75e575fc96a4fe7bfea897f57692b050d2b
c = 0xa3bce6e2e677d7855a1a7819eb1879779d1e1eefa21a1a6e205c8b46fdc020a2487fdd07dbae99274204fadda2ba69af73627bdddcb2c403118f507bca03cb0bad7a8cd03f70defc31fa904d71230aab98a10e155bf207da1b1cac1503f48cab3758024cc6e62afe99767e9e4c151b75f60d8f7989c152fdf4ff4b95ceed9a7065f38c68dee4dd0da503650d3246d463f504b36e1d6fafabb35d2390ecf0419b2bb67c4c647fb38511b34eb494d9289c872203fa70f4084d2fa2367a63a8881b74cc38730ad7584328de6a7d92e4ca18098a15119baee91237cea24975bdfc19bdbce7c1559899a88125935584cd37c8dd31f3f2b4517eefae84e7e588344fa5

m = pow(c, d, N)
print(bytes.fromhex(hex(m)[2:])) # b'crypto{bon3h5_4tt4ck_i5_sr0ng3r_th4n_w13n3r5}'
```

## V Coppersmith's relative attack

### V.1 Håstad's broadcast attack

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

### V.2 Franklin–Reiter related-message attack

攻击条件：使用同一公钥 (n, e) 线性填充加密同一密文 m 两次，获得两个密文 c1 c2:

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

> [!QUESTION]
>
> [cryptohack - Bespoke Padding](https://cryptohack.org/challenges/rsa/)

### V.3 Coppersmith’s short-pad attack

### V.4 Known High Bits Attack

利用 sagemath 调用的 coppersmith 算法求解小根。

攻击条件：已知 N 的一个素数 p/q 的高位或者是明文的高位；
攻击方式：构造多项式，调用 sagemath 求解。

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

### V.5 Known Low Bits Attack

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

### V.6 Return of Coppersmith's attack (ROCA)

攻击条件：fast primes

起源于 [cryptohack](https://cryptohack.org/challenges/rsa/) 上的 "Fast Primes"，当然去搜 Fast Primes 也能找到这个攻击（方便和安全总是难以兼得的），具体下面的文章讲的很清楚了，推荐攻击脚本如下，自己有能力写一个更好。

> [!NOTE]
>
> - [Analysis of the ROCA vulnerability](https://bitsdeep.com/posts/analysis-of-the-roca-vulnerability)
> - https://github.com/RsaCtfTool/RsaCtfTool/blob/master/sage/roca_attack.py

## VI 其他

### VI.1 m 的解个数

> [!THEOREM]
>
> If $gcd(e, p-1)=1$ and p is prime, the $m^e \equiv c\pmod{p}$ has exactly one solution for m.

> [elementary number theory - solutions to $x^n\equiv a\pmod{p}$ - Mathematics Stack Exchange](https://math.stackexchange.com/questions/2842399/solutions-to-xn-equiv-a-pmodp)

其实更为重要的是上面问答中较为靠下的一个回答给出的结论：

> [!THEOREM]
>
> If p is prime, $p \nmid c$, then $m^e \equiv c \pmod{p}$ has **0 or d = gcd(e, p-1)** solutions, being the latter if $c^{\frac{p-1}{d}}\equiv 1 \pmod{p}$.

证明略，其中最后一两步如果看不懂可以参考 [group theory - Solution to $x^n=a \pmod p$ where $p$ is a prime](https://math.stackexchange.com/questions/1491103/solution-to-xn-a-pmod-p-where-p-is-a-prime) .

### VI.2 Optimal asymmetric encryption padding (OAEP)

> https://en.wikipedia.org/wiki/Optimal_asymmetric_encryption_padding

### VI.3 Get p q if we know phi

$$\begin{cases}p+q=n-\varphi(n)+1\\p-q=\sqrt{\left(n-\varphi(n)+1\right)^2-4n}\end{cases}$$

## VII 参考资料

- [crypto-attack/attack/rsa](https://github.com/jvdsn/crypto-attacks/tree/master/attacks/rsa)
- [RSA学习笔记 | Chemtrails (ch3mtr4ils.cn)](https://ch3mtr4ils.cn/2022/12/29/RSA%E5%AD%A6%E4%B9%A0%E7%AC%94%E8%AE%B0/)
- [CTF RSA题解集](https://www.ruanx.net/rsa-solutions/)