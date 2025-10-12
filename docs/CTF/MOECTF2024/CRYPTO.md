---
tags:
- wp
- ctf
comments: true
---

## baby_equation

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

## ez_hash

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

## RSA_revenge

```python title="task.py"
from Crypto.Util.number import getPrime, isPrime, bytes_to_long
from secret import flag


def emirp(x):
    y = 0
    while x !=0:
        y = y*2 + x%2 # y << 1 | x & 1
        x = x//2 
    return y # x 的二进制逆序


while True:
    p = getPrime(512)
    q = emirp(p)
    if isPrime(q):
        break

n = p*q
e = 65537
m = bytes_to_long(flag)
c = pow(m,e,n)
print(f"{n = }")
print(f"{c = }")
"""
n = 141326884939079067429645084585831428717383389026212274986490638181168709713585245213459139281395768330637635670530286514361666351728405851224861268366256203851725349214834643460959210675733248662738509224865058748116797242931605149244469367508052164539306170883496415576116236739853057847265650027628600443901
c = 47886145637416465474967586561554275347396273686722042112754589742652411190694422563845157055397690806283389102421131949492150512820301748529122456307491407924640312270962219946993529007414812671985960186335307490596107298906467618684990500775058344576523751336171093010950665199612378376864378029545530793597
"""
```

```python title="solution.py"
n = 141326884939079067429645084585831428717383389026212274986490638181168709713585245213459139281395768330637635670530286514361666351728405851224861268366256203851725349214834643460959210675733248662738509224865058748116797242931605149244469367508052164539306170883496415576116236739853057847265650027628600443901
c = 47886145637416465474967586561554275347396273686722042112754589742652411190694422563845157055397690806283389102421131949492150512820301748529122456307491407924640312270962219946993529007414812671985960186335307490596107298906467618684990500775058344576523751336171093010950665199612378376864378029545530793597
def blast_k(bit_len):
    res = []
    def blast(a, b, k):
        """ 回溯法 + 剪枝 """
        if k == bit_len:
            if a*b == n:
                res.append([a, b])
            return
        for i in range(2):
            for j in range(2):
                a1 = a + i*(2**k) + j*(2**(bit_len-1-k))
                b1 = b + j*(2**k) + i*(2**(bit_len-1-k))
                if a1*b1 > n:
                    continue
                if (a1+(2**(bit_len-1-k)))*(b1+(2**(bit_len-1-k))) < n:
                    continue
                if ((a1*b1)%(2**(k+1))) != (n%(2**(k+1))):
                    continue
                blast(a1, b1, k+1)
    blast(0, 0, 0)
    return res
res = blast_k(512)

phi = (res[0][0]-1)*(res[0][1]-1)
d = pow(0x10001, -1, phi)
m = pow(c, d, n)
print(bytes.fromhex(hex(m)[2:])) # b'moectf{WA!y0u@er***g00((d))}'
```

## More_secure_RSA

```python title="task.py"
from Crypto.Util.number import *

flag = b'moectf{xxxxxxxxxxxxxxxxx}'


m = bytes_to_long(flag)
p = getPrime(1024)
q = getPrime(1024)
n = p * q 
e = 0x10001
c = pow(m, e, n)
print(f'c = {c}')
print(f'n = {n}')

'''
Oh,it isn't secure enough!
'''
r = getPrime(1024)
n = n * r
c = pow(m, e, n)
print(f'C = {c}')
print(f'N = {n}')

"""
c = 12992001402636687796268040906463852467529970619872166160007439409443075922491126428847990768804065656732371491774347799153093983118784555645908829567829548859716413703103209412482479508343241998746249393768508777622820076455330613128741381912099938105655018512573026861940845244466234378454245880629342180767100764598827416092526417994583641312226881576127632370028945947135323079587274787414572359073029332698851987672702157745794918609888672070493920551556186777642058518490585668611348975669471428437362746100320309846155934102756433753034162932191229328675448044938003423750406476228868496511462133634606503693079
n = 16760451201391024696418913179234861888113832949815649025201341186309388740780898642590379902259593220641452627925947802309781199156988046583854929589247527084026680464342103254634748964055033978328252761138909542146887482496813497896976832003216423447393810177016885992747522928136591835072195940398326424124029565251687167288485208146954678847038593953469848332815562187712001459140478020493313651426887636649268670397448218362549694265319848881027371779537447178555467759075683890711378208297971106626715743420508210599451447691532788685271412002723151323393995544873109062325826624960729007816102008198301645376867
C = 1227033973455439811038965425016278272592822512256148222404772464092642222302372689559402052996223110030680007093325025949747279355588869610656002059632685923872583886766517117583919384724629204452792737574445503481745695471566288752636639781636328540996436873887919128841538555313423836184797745537334236330889208413647074397092468650216303253820651869085588312638684722811238160039030594617522353067149762052873350299600889103069287265886917090425220904041840138118263873905802974197870859876987498993203027783705816687972808545961406313020500064095748870911561417904189058228917692021384088878397661756664374001122513267695267328164638124063984860445614300596622724681078873949436838102653185753255893379061574117715898417467680511056057317389854185497208849779847977169612242457941087161796645858881075586042016211743804958051233958262543770583176092221108309442538853893897999632683991081144231262128099816782478630830512
N = 1582486998399823540384313363363200260039711250093373548450892400684356890467422451159815746483347199068277830442685312502502514973605405506156013209395631708510855837597653498237290013890476973370263029834010665311042146273467094659451409034794827522542915103958741659248650774670557720668659089460310790788084368196624348469099001192897822358856214600885522908210687134137858300443670196386746010492684253036113022895437366747816728740885167967611021884779088402351311559013670949736441410139393856449468509407623330301946032314939458008738468741010360957434872591481558393042769373898724673597908686260890901656655294366875485821714239821243979564573095617073080807533166477233759321906588148907331569823186970816432053078415316559827307902239918504432915818595223579467402557885923581022810437311450172587275470923899187494633883841322542969792396699601487817033616266657366148353065324836976610554682254923012474470450197
"""
```

有时使用 factordb 分解大数，发现能够分解出一些小数，但是剩下最大的那个数依旧不是质数。如果已经分解出来的部分的乘积大于 m，那么也够用了。

例如，当前已经分解 $n = a*....*b * A$ 且 $is\_prime(A)==False$，那么我们记 $a*\dots*b = k, \phi(k)$ 是不难计算的。如果 m < k，则有 $m=c^{d_n}\pmod{n} = c^{d_{k}}\pmod{k}$ 其中 $d_x$ 表示在模 x 的情况下 e 的逆元。

```python title="task.py"
flag = int.from_bytes(b'moectf{xxxxxxxxxxxxxxxxx}')
c = 12992001402636687796268040906463852467529970619872166160007439409443075922491126428847990768804065656732371491774347799153093983118784555645908829567829548859716413703103209412482479508343241998746249393768508777622820076455330613128741381912099938105655018512573026861940845244466234378454245880629342180767100764598827416092526417994583641312226881576127632370028945947135323079587274787414572359073029332698851987672702157745794918609888672070493920551556186777642058518490585668611348975669471428437362746100320309846155934102756433753034162932191229328675448044938003423750406476228868496511462133634606503693079
n = 16760451201391024696418913179234861888113832949815649025201341186309388740780898642590379902259593220641452627925947802309781199156988046583854929589247527084026680464342103254634748964055033978328252761138909542146887482496813497896976832003216423447393810177016885992747522928136591835072195940398326424124029565251687167288485208146954678847038593953469848332815562187712001459140478020493313651426887636649268670397448218362549694265319848881027371779537447178555467759075683890711378208297971106626715743420508210599451447691532788685271412002723151323393995544873109062325826624960729007816102008198301645376867
C = 1227033973455439811038965425016278272592822512256148222404772464092642222302372689559402052996223110030680007093325025949747279355588869610656002059632685923872583886766517117583919384724629204452792737574445503481745695471566288752636639781636328540996436873887919128841538555313423836184797745537334236330889208413647074397092468650216303253820651869085588312638684722811238160039030594617522353067149762052873350299600889103069287265886917090425220904041840138118263873905802974197870859876987498993203027783705816687972808545961406313020500064095748870911561417904189058228917692021384088878397661756664374001122513267695267328164638124063984860445614300596622724681078873949436838102653185753255893379061574117715898417467680511056057317389854185497208849779847977169612242457941087161796645858881075586042016211743804958051233958262543770583176092221108309442538853893897999632683991081144231262128099816782478630830512
N = 1582486998399823540384313363363200260039711250093373548450892400684356890467422451159815746483347199068277830442685312502502514973605405506156013209395631708510855837597653498237290013890476973370263029834010665311042146273467094659451409034794827522542915103958741659248650774670557720668659089460310790788084368196624348469099001192897822358856214600885522908210687134137858300443670196386746010492684253036113022895437366747816728740885167967611021884779088402351311559013670949736441410139393856449468509407623330301946032314939458008738468741010360957434872591481558393042769373898724673597908686260890901656655294366875485821714239821243979564573095617073080807533166477233759321906588148907331569823186970816432053078415316559827307902239918504432915818595223579467402557885923581022810437311450172587275470923899187494633883841322542969792396699601487817033616266657366148353065324836976610554682254923012474470450197
e = 0x10001
print(flag.bit_length(), C.bit_length(), n.bit_length()) # 3072
r = N // n
# m^e = C (mod r)
dr = pow(e, -1, r-1)
m = pow(C, dr, r)
bytes.fromhex(hex(m)[2:]) # b'moectf{th3_a1g3br4_is_s0_m@gic!}'
```

## ezlengrede

```python title="task.py"
# https://ctf.xidian.edu.cn/training/10?challenge=68
from sympy import *
from Crypto.Util.number import *

p = getPrime(128)
a = randprime(2, p)

FLAG = b'moectf{xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx}'


def encrypt_flag(flag):
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag])
    for bit in plaintext:
        e = randprime(2, p)
        n = pow(int(bit) + a, e , p)
        ciphertext.append(n)
    return ciphertext

print(encrypt_flag(FLAG))

'''
p = 303597842163255391032954159827039706827
a = 34032839867482535877794289018590990371
[278121435714344315140568219459348432240, 122382422611852957172920716982592319058, 191849618185577692976529819600455462899, 94093446512724714011050732403953711672, 201558180013426239467911190374373975458, 68492033218601874497788216187574770779, 126947642955989000352009944664122898350, 219437945679126072290321638679586528971,
...]
```

题目名称隐晦地提示了我们考虑 [Legendre symbol](../Note/Crypto/basic_math_in_crypto.md#Legendre%20symbol) ；考虑勒让德符号的两个性质：

- $\left( \frac{a}{p} \right)\left( \frac{b}{p} \right) = \left( \frac{ab}{p} \right)$
- $a\equiv b\pmod{p} \implies \left( \frac{a}{p} \right)=\left( \frac{b}{p} \right)$

对于 `e = randprime(2, p)` ，显然 e 是奇数，所以有：

$$
\begin{align}
&x^{e} = (x^{e-1 / 2})^{2} \cdot x , \text{where } x = a+int(bit) \in \{a, a+1\}\\
\implies&\left( \frac{n}{p} \right) = \left( \frac{x^{e}}{p} \right) = \left( \frac{x^{e-1/2}}{p} \right)^{2} \cdot \left( \frac{x}{p} \right) \in \{0, -1, 1\}
\end{align}
$$

```python
from sympy import legendre_symbol

p = 303597842163255391032954159827039706827
a = 34032839867482535877794289018590990371
ls_a = legendre_symbol(a, p)
ls_a1 = legendre_symbol(a+1, p)
print(ls_a, ls_a1)
# -1, 1
```

也即 $\left( \frac{a}{p} \right)=-1, \left(\frac{a+1}{p}\right)=1$；由群的性质我们可以得知 $\left( \frac{x^{e-1/2}}{p} \right)^{2} \neq 0$，进而推得：

$$
\left( \frac{n}{p} \right) = \left( \frac{x}{p} \right) \in \{\left( \frac{a}{p} \right), \left(\frac{a+1}{p}\right)\}
$$

> [!tip]- 
> 
> 由于 flag 的前几位我们是知道的 "moectf"，所以先试试得到的前几位是否为这几个字符即可。

```python title="solution.py"
from sympy import legendre_symbol
def decrypt_flag(ciphertext):
    ls_a = legendre_symbol(a, p)
    ls_a1 = legendre_symbol(a+1, p)
    print(ls_a, ls_a1)
    assert ls_a != ls_a1
    bits = ""
    for c in cipertext:
        ls = legendre_symbol(c, p)
        b = bin(ls != ls_a)[2:]
        bits += b
    
    return bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
print(decrypt_flag(cipertext))
# b'moectf{minus_one_1s_n0t_qu4dr4tic_r4sidu4_when_p_mod_f0ur_equ41_to_thr33}'
```

## new_system

```python title="task.py"
from random import randint
from Crypto.Util.number import getPrime,bytes_to_long 

flag = b'moectf{???????????????}'
gift = bytes_to_long(flag)

def parametergenerate():
    q = getPrime(256)
    gift1 = randint(1, q)
    gift2 = (gift - gift1) % q
    x =  randint(1, q)
    assert gift == (gift1 + gift2) % q
    return q , x , gift1, gift2


def encrypt(m , q , x):
    a = randint(1, q)
    c = (a*x + m) % q
    return [a , c]


q , x , gift1 , gift2 = parametergenerate()
print(encrypt(gift1 , q , x))
print(encrypt(gift2 , q , x))
print(encrypt(gift , q , x))
print(f'q = {q}')

'''
[48152794364522745851371693618734308982941622286593286738834529420565211572487, 21052760152946883017126800753094180159601684210961525956716021776156447417961]
[48649737427609115586886970515713274413023152700099032993736004585718157300141, 6060718815088072976566240336428486321776540407635735983986746493811330309844]
[30099883325957937700435284907440664781247503171217717818782838808179889651361, 85333708281128255260940125642017184300901184334842582132090488518099650581761]
q = 105482865285555225519947662900872028851795846950902311343782163147659668129411
'''
```

$$
\begin{cases}
a_{1}x+m_{1} = c_{1} \pmod{q} \\
a_{2}x+m_{2} = c_{2} \pmod{q} \\
a_{3}x+m_{1} + m_{2} = c_{3} \pmod{q}
\end{cases}
\implies (a_{3}-a_{1}-a_{2}) x = c_{3}-c_{1}-c_{2} \pmod{q}
$$

```python title="solution.py"
from Crypto.Util.number import inverse

q = 105482865285555225519947662900872028851795846950902311343782163147659668129411
a1 = 48152794364522745851371693618734308982941622286593286738834529420565211572487
c1 = 21052760152946883017126800753094180159601684210961525956716021776156447417961
a2 = 48649737427609115586886970515713274413023152700099032993736004585718157300141
c2 = 6060718815088072976566240336428486321776540407635735983986746493811330309844
a3 = 30099883325957937700435284907440664781247503171217717818782838808179889651361
c3 = 85333708281128255260940125642017184300901184334842582132090488518099650581761

A = (a1 + a2 - a3) % q
C = (c1 + c2 - c3) % q
if A == 0:
    print("degenerate; need new samples")
else:
    x = (C * inverse(A, q)) % q
    assert A * x % q == C
    print("x =", x)

gift = (c3 - a3 * x) % q
from Crypto.Util.number import long_to_bytes
print(long_to_bytes(gift)) # b'moectf{gift_1s_present}'
```

## EzMatrix

```python title="task"
# https://ctf.xidian.edu.cn/training/10?challenge=131
from Crypto.Util.number import *
from secret import FLAG,secrets,SECERT_T

assert len(secrets) == 16
assert FLAG == b'moectf{' + secrets + b'}'
assert len(SECERT_T) <= 127

class LFSR:
    def __init__(self):
        self._s = list(map(int,list("{:0128b}".format(bytes_to_long(secrets)))))
        for _ in range(8*len(secrets)):
            self.clock()
    
    def clock(self):
        b = self._s[0]
        c = 0
        for t in SECERT_T:c ^= self._s[t]
        self._s = self._s[1:] + [c]
        return b
    
    def stream(self, length):
        return [self.clock() for _ in range(length)]


c = LFSR()
stream = c.stream(256)
print("".join(map(str,stream))[:-5])
# 11111110011011010000110110100011110110110101111000101011001010110011110011000011110001101011001100000011011101110000111001100111011100010111001100111101010011000110110101011101100001010101011011101000110001111110100000011110010011010010100100000000110

```

[An Introduction to LFSRs for Cryptography](https://medium.com/@czapfel/an-introduction-to-lfsrs-for-cryptography-bf2602640e91) 中对 LFSR 进行了拆分式讲解。在上面的 LFSR 中：

- `_s` 是 registers
- `SECERT_T` 存储了 taps

特殊处理的地方在于：

- 在 `__init__` 阶段先 stream(8*(len(secrets)))，也即将本来应该输出的 secrets 对应部分放空
- 在 `print` 时截断了最后 5 个


了解到 berlekamp_massey 算法可以依据 2n 长度的 stream 计算出长度为 n 的寄存器的反馈多项式，我们下面使用 sagemath 中实现的 BM 算法；同时出于理解方便，我实现了更加可控的 LFSR 和反向的 ReverseLFSR：

```python title="solution.py"
from sage.all import *
from sage.matrix.berlekamp_massey import berlekamp_massey
from Crypto.Util.number import long_to_bytes

class LFSR:
    def __init__(self, seed: str, TAPS: list):
        """
        :param seed: 输入的初始状态
        """
        assert len(seed) == 128
        self._s = list(map(int,list(seed)))
        self.TAPS = TAPS
    
    def clock(self):
        b = self._s[0]
        c = 0
        for t in self.TAPS:c ^= self._s[t]
        self._s = self._s[1:] + [c]
        return b

    def stream(self, length):
        return [self.clock() for _ in range(length)]

class ReverseLFSR:
    def __init__(self, seed: list, TAPS: list):
        """
        :param seed: 输入的初始状态
        """
        assert len(seed) == 128
        self._s = seed
        self.TAPS = TAPS
    
    def reverse_clock(self):
        b = self._s[127]
        c = self._s[127]
        for t in self.TAPS:
            if t != 0:
                c ^= self._s[t-1]
        self._s = [c] + self._s[:-1]
        return b
    
    def stream(self, length):
        return [self.reverse_clock() for _ in range(length)]

stream_prefix = "11111110011011010000110110100011110110110101111000101011001010110011110011000011110001101011001100000011011101110000111001100111011100010111001100111101010011000110110101011101100001010101011011101000110001111110100000011110010011010010100100000000110"
s_prefix = list(map(int, stream_prefix))
assert len(s_prefix) == 251

def check_taps(stream, taps):
    seed = stream[:128]
    lfsr = LFSR(seed, taps)
    for i in range(128):
        b = lfsr.clock()
        if b != stream[i]:
            return False
    return True

def reverse_clocks(stream: list, taps):
    seed = stream[:128]
    rlfsr = ReverseLFSR(seed, taps)
    for _ in range(128):
        rlfsr.reverse_clock()
    return rlfsr._s

# 遍历后 5 位的所有可能
for i in range(32):
    padding = list(map(int, list(f"{i:05b}")))
    stream = s_prefix + padding
    
    # 2. 使用Berlekamp-Massey算法获得 taps
    poly = berlekamp_massey(list(map(GF(2), stream)))
    
    taps = [i for i, coeff in enumerate(poly.list()[:-1]) if coeff == 1]
    if check_taps(stream, taps) == False:
        continue
    
    # 3. 反向计算
    regs = reverse_clocks(stream, taps)
    secret_str = "".join([str(x) for x in regs])
    secret_bytes = long_to_bytes(int(secret_str, 2))
    # print(secret_bytes)
    try:
        print("moectf{" + secret_bytes.decode() + "}") # moectf{e4sy_lin3ar_sys!}
    except:
        pass
```

官方参考题解使用了线性代数求解：

```python title="official solution"
from Crypto.Util.number import *
from sage.all import *


for i in range(32):
    output = "11111110011011010000110110100011110110110101111000101011001010110011110011000011110001101011001100000011011101110000111001100111011100010111001100111101010011000110110101011101100001010101011011101000110001111110100000011110010011010010100100000000110"
    brutebits = bin(i)[2:].zfill(5)
    output += brutebits
    F = GF(2)
    # {0,1}
    n = 128
    V = VectorSpace(F,n)
    vec = V(list(map(int, list(output[n:]))))
    M = []
    for i in range(n-1,2*n-1):
        m = []
        for j in range(n):
            m.append(output[i-j])
        M.append(m)
    M = Matrix(F,M)
    try:
        sol = M.solve_right(vec)
    except ValueError:
        continue
    poly = list(sol)
    B = Matrix(F,n,n)
    for i in range(n):
        B[i,n-1] = poly[n-1-i]
    for i in range(n-1):
        B[i+1,i] = 1
    try:
        B_inv = B**(-1)
        t = V(list(map(int,list(output[:n]))))
        print(long_to_bytes(int("".join(map(str,t*B_inv**(n))),2)))
    except ZeroDivisionError:
        continue
```

## Easy_Pack

```python title="task.py"
from Crypto.Util.number import *
from secret import flag
import random

p = 2050446265000552948792079248541986570794560388346670845037360320379574792744856498763181701382659864976718683844252858211123523214530581897113968018397826268834076569364339813627884756499465068203125112750486486807221544715872861263738186430034771887175398652172387692870928081940083735448965507812844169983643977
assert len(flag) == 42

def encode(msg):
    return bin(bytes_to_long(msg))[2:].zfill(8*len(msg))

def genkey(len):
    sums = 0
    keys = []
    for i in range(len):
        k = random.randint(1,7777)
        x = sums + k
        keys.append(x)
        sums += x
    return keys

key = genkey(42*8)

def enc(m, keys):
    msg = encode(m)
    print(len(keys))
    print(len(msg))
    assert len(msg) == len(keys)
    s = sum((k if (int(p,2) == 1) else 1) for p, k in zip(msg, keys))
    print(msg)
    for p0,k in zip(msg,keys):
        print(int(p0,2))
    return pow(7,s,p)

cipher = enc(flag,key)

with open("output.txt", "w") as fs:
    fs.write(str(key)+'\n')
    fs.write(str(cipher))

```

确实挺 easy 的，因为 key 是一个[超级递增序列](https://www.ruanx.net/lattice-2/)，所以从高到低递减即可：

```python title="solution.py"
with open("output.txt", "r") as f:
    lines = f.readlines()
    key_line = lines[0].strip()
    cipher_line = lines[1].strip()
    
    # 解析 key 列表
    key = eval(key_line)
    cipher = int(cipher_line)

print(len(key))
print(cipher)

def easy_pack(cipher):
    def get_keysum(cipher):
        p = 2050446265000552948792079248541986570794560388346670845037360320379574792744856498763181701382659864976718683844252858211123523214530581897113968018397826268834076569364339813627884756499465068203125112750486486807221544715872861263738186430034771887175398652172387692870928081940083735448965507812844169983643977
        # pow(7, key_sum, p) == cipher
        from sympy.ntheory import discrete_log
        key_sum = discrete_log(p, cipher, 7)
        return key_sum
    
    key_sum = get_keysum(cipher)
    binary = ""
    for i in range(len(key)-1, -1, -1):
        if key_sum >= key[i]:
            key_sum -= key[i]
            binary = "1" + binary
        else:
            binary = "0" + binary
    
    def decode(binary: str):
        from Crypto.Util.number import long_to_bytes
        return long_to_bytes(int(binary, 2))
    return decode(binary)

print(easy_pack(cipher))
```

## One_More_Bit

```python title="task.py"
from Crypto.Util.number import getStrongPrime, bytes_to_long, GCD, inverse
from Crypto.Util.Padding import pad
from secret import flag
import random

def genKey(nbits,dbits):
    p = getStrongPrime(nbits//2)
    q = getStrongPrime(nbits//2)
    n = p*q
    phi = (p-1)*(q-1)
    while True:
        d = random.getrandbits(dbits)
        if d.bit_length() == dbits:
            if GCD(d, phi) == 1:
                e = inverse(d, phi)
                pk = (n, e)
                sk = (p, q, d)
                return pk, sk

nbits = 1024
dbits = 258
message = pad(flag,16)
msg = pad(message, 16)
m = bytes_to_long(msg)
pk= genKey(nbits, dbits)[0]
n, e = pk
ciphertext = pow(m, e, n)

with open("data.txt","w") as f:
    f.write(f"pk = {pk}\n")
    f.write(f"ciphertext = {ciphertext}\n")
    f.close()
```

唯一的缺点在于 dbits << nbits，符合 $d < N^{0.292}$ 条件，使用 [Boneh and Durfee attack](../Note/Crypto/RSA_attack.md#Boneh%20and%20Durfee%20attack) 即可求出 d：

```python
from Crypto.Util.number import long_to_bytes

n = 134133840507194879124722303971806829214527933948661780641814514330769296658351734941972795427559665538634298343171712895678689928571804399278111582425131730887340959438180029645070353394212857682708370490223871309129948337487286534021548834043845658248447393803949524601871557448883163646364233913283438778267
e = 83710839781828547042000099822479827455150839630087752081720660846682103437904198705287610613170124755238284685618099812447852915349294538670732128599161636818193216409714024856708796982283165572768164303554014943361769803463110874733906162673305654979036416246224609509772196787570627778347908006266889151871
c = 73228838248853753695300650089851103866994923279710500065528688046732360241259421633583786512765328703209553157156700672911490451923782130514110796280837233714066799071157393374064802513078944766577262159955593050786044845920732282816349811296561340376541162788570190578690333343882441362690328344037119622750

# using 

d = 420129172617694367639603712165881242192973923283572937883375494685279140840871
assert 1/3 * pow(n, 0.25) < d < pow(n, 0.292)
m = pow(c,d,n)
print(long_to_bytes(m)) # b'moectf{Ju5t_0n3_st3p_m0r3_th4n_wi3n3r_4ttack!}\x02\x02\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10\x10'
```

也可以看到不符合 wiener attack 的条件，题目标题和 flag 的含义大概也正在于此。

## ezLCG

```python title="task.py"
from sage.all import *
from random import getrandbits, randint
from secrets import randbelow
from Crypto.Util.number import getPrime,isPrime,inverse
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from secret import priKey, flag
from hashlib import sha1
import os


q = getPrime(160)
while True:
    t0 = q*getrandbits(864)
    if isPrime(t0+1):
        p = t0 + 1
        break


x = priKey
assert p % q == 1
h = randint(1,p-1)
g = pow(h,(p-1)//q,p)
y = pow(g,x,p)


def sign(z, k):
    r = pow(g,k,p) % q
    s = (inverse(k,q)*(z+r*priKey)) % q
    return (r,s)


def verify(m,s,r):
    z = int.from_bytes(sha1(m).digest(), 'big')
    u1 = (inverse(s,q)*z) % q
    u2 = (inverse(s,q)*r) % q
    r0 = ((pow(g,u1,p)*pow(y,u2,p)) % p) % q
    return r0 == r


def lcg(a, b, q, x):
    while True:
        x = (a * x + b) % q
        yield x


msg = [os.urandom(16) for i in range(5)]

a, b, x = [randbelow(q) for _ in range(3)]
prng = lcg(a, b, q, x)
sigs = []
for m, k in zip(msg,prng):
    z = int.from_bytes(sha1(m).digest(), "big") % q
    r, s = sign(z, k)
    assert verify(m, s, r)
    sigs.append((r,s))


print(f"{g = }")
print(f"{h = }")
print(f"{q = }")
print(f"{p = }")
print(f"{msg = }")
print(f"{sigs = }")
key = sha1(str(priKey).encode()).digest()[:16]
iv = os.urandom(16)
cipher = AES.new(key, AES.MODE_CBC,iv)
ct = cipher.encrypt(pad(flag,16))
print(f"{iv = }")
print(f"{ct = }")


'''
g = 81569684196645348869992756399797937971436996812346070571468655785762437078898141875334855024163673443340626854915520114728947696423441493858938345078236621180324085934092037313264170158390556505922997447268262289413542862021771393535087410035145796654466502374252061871227164352744675750669230756678480403551
h = 13360659280755238232904342818943446234394025788199830559222919690197648501739683227053179022521444870802363019867146013415532648906174842607370958566866152133141600828695657346665923432059572078189013989803088047702130843109809724983853650634669946823993666248096402349533564966478014376877154404963309438891
q = 1303803697251710037027345981217373884089065173721
p = 135386571420682237420633670579115261427110680959831458510661651985522155814624783887385220768310381778722922186771694358185961218902544998325115481951071052630790578356532158887162956411742570802131927372034113509208643043526086803989709252621829703679985669846412125110620244866047891680775125948940542426381
msg = [b'I\xf0\xccy\xd5~\xed\xf8A\xe4\xdf\x91+\xd4_$', b'~\xa0\x9bCB\xef\xc3SY4W\xf9Aa\rO', b'\xe6\x96\xf4\xac\n9\xa7\xc4\xef\x82S\xe9 XpJ', b'3,\xbb\xe2-\xcc\xa1o\xe6\x93+\xe8\xea=\x17\xd1', b'\x8c\x19PHN\xa8\xbc\xfc\xa20r\xe5\x0bMwJ']
sigs = [(913082810060387697659458045074628688804323008021, 601727298768376770098471394299356176250915124698), (406607720394287512952923256499351875907319590223, 946312910102100744958283218486828279657252761118), (1053968308548067185640057861411672512429603583019, 1284314986796793233060997182105901455285337520635), (878633001726272206179866067197006713383715110096, 1117986485818472813081237963762660460310066865326), (144589405182012718667990046652227725217611617110, 1028458755419859011294952635587376476938670485840)]
iv = b'M\xdf\x0e\x7f\xeaj\x17PE\x97\x8e\xee\xaf:\xa0\xc7'
ct = b"\xa8a\xff\xf1[(\x7f\xf9\x93\xeb0J\xc43\x99\xb25:\xf5>\x1c?\xbd\x8a\xcd)i)\xdd\x87l1\xf5L\xc5\xc5'N\x18\x8d\xa5\x9e\x84\xfe\x80\x9dm\xcc"
'''

```

如果对 [DSA](https://ctf-wiki.org/crypto/signature/dsa/) 签名算法不太了解的话，可以在草稿纸上把过程大概记录下来捋一捋；最终我们可以发现可以得到：`q, p, h, g, r, s, z(msg)` 。且 k 由一个线性同余生成器 (LCG) 产生。经过简单的消元推导可以得到：

$$\frac{k_{3}-k_{2}}{k_{2}-k_{1}} = \frac{k_{4}-k_{3}}{k_{3}-k_{2}} \implies (k_{3}-k2)^{2} = (k_{4}-k_{3})*(k_{2}-k_{1})$$

又由于在签名 (sign) 阶段我们可以得到（$m = s^{-1}r\pmod{q}, n = s^{-1}r\pmod{q}$）：

$$s = k^{-1}*(z + rx) \pmod{q} \implies k = s^{-1}*(z+rx) = mx + n$$

带入前面的式子可以得到一个仅 x 未知的、模 q 的二次方程中。下面实现了两个方法（使用多项式环的 get_xs 和利用线性方程组求解的 get_roots）求解 x，经过验证后得到 key 即可。

```python title="exp.py"
from hashlib import sha1
from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import unpad
from sympy import sqrt_mod

g = 81569684196645348869992756399797937971436996812346070571468655785762437078898141875334855024163673443340626854915520114728947696423441493858938345078236621180324085934092037313264170158390556505922997447268262289413542862021771393535087410035145796654466502374252061871227164352744675750669230756678480403551
h = 13360659280755238232904342818943446234394025788199830559222919690197648501739683227053179022521444870802363019867146013415532648906174842607370958566866152133141600828695657346665923432059572078189013989803088047702130843109809724983853650634669946823993666248096402349533564966478014376877154404963309438891
q = 1303803697251710037027345981217373884089065173721
p = 135386571420682237420633670579115261427110680959831458510661651985522155814624783887385220768310381778722922186771694358185961218902544998325115481951071052630790578356532158887162956411742570802131927372034113509208643043526086803989709252621829703679985669846412125110620244866047891680775125948940542426381
# ---------------------------
msg = [b'I\xf0\xccy\xd5~\xed\xf8A\xe4\xdf\x91+\xd4_$', b'~\xa0\x9bCB\xef\xc3SY4W\xf9Aa\rO', b'\xe6\x96\xf4\xac\n9\xa7\xc4\xef\x82S\xe9 XpJ', b'3,\xbb\xe2-\xcc\xa1o\xe6\x93+\xe8\xea=\x17\xd1', b'\x8c\x19PHN\xa8\xbc\xfc\xa20r\xe5\x0bMwJ']
sigs = [(913082810060387697659458045074628688804323008021, 601727298768376770098471394299356176250915124698), (406607720394287512952923256499351875907319590223, 946312910102100744958283218486828279657252761118), (1053968308548067185640057861411672512429603583019, 1284314986796793233060997182105901455285337520635), (878633001726272206179866067197006713383715110096, 1117986485818472813081237963762660460310066865326), (144589405182012718667990046652227725217611617110, 1028458755419859011294952635587376476938670485840)]
iv = b'M\xdf\x0e\x7f\xeaj\x17PE\x97\x8e\xee\xaf:\xa0\xc7'
ct = b"\xa8a\xff\xf1[(\x7f\xf9\x93\xeb0J\xc43\x99\xb25:\xf5>\x1c?\xbd\x8a\xcd)i)\xdd\x87l1\xf5L\xc5\xc5'N\x18\x8d\xa5\x9e\x84\xfe\x80\x9dm\xcc"
# --------------------------

t = (p-1) // q
assert t * q == (p-1)
assert pow(h, t, p) == g

def get_mn(msg, sigs):
    """
    according to `sign`, get m, n
    s.t.  k = m*x + n
    """
    ms = []
    ns = []
    for i, m in enumerate(msg): 
        z = int.from_bytes(sha1(m).digest(), "big") % q
        r = sigs[i][0]
        s = sigs[i][1]
        m = inverse(s, q) * r
        n = inverse(s, q) * z
        ms.append(m)
        ns.append(n)
    return ms, ns

def get_roots(ms, ns):
    m1, m2, m3, m4 = ms[1], ms[2], ms[3], ms[4]
    n1, n2, n3, n4 = ns[1], ns[2], ns[3], ns[4]

    # d1 = k2 - k1, etc.
    a1 = (m2 - m1) % q
    b1 = (n2 - n1) % q
    a2 = (m3 - m2) % q
    b2 = (n3 - n2) % q
    a3 = (m4 - m3) % q
    b3 = (n4 - n3) % q

    A = (a2 * a2 - a3 * a1) % q
    B = (2 * a2 * b2 - (a3 * b1 + a1 * b3)) % q
    C = (b2 * b2 - b3 * b1) % q

    roots = set()

    def mod_inv(v):
        return inverse(v % q, q)

    if A % q == 0:
        # 退化为线性：B x + C ≡ 0
        if B % q == 0:
            if C % q == 0:
                print("无限多个解（所有 x）")  # 极端情况
            else:
                print("无解")
        else:
            x_sol = (-C * mod_inv(B)) % q
            roots.add(x_sol)
    else:
        D = (B * B - 4 * A * C) % q  # 判别式
        # 检查是否是二次剩余
        if pow(D, (q - 1) // 2, q) != 1 and D != 0:
            print("判别式非二次剩余，无解")
        else:
            if D == 0:
                rlist = [0]
            else:
                rlist = [sqrt_mod(D, q)]
            inv_2A = mod_inv(2 * A)
            for r in rlist:
                x1 = (-B + r) * inv_2A % q
                x2 = (-B - r) * inv_2A % q
                roots.add(x1)
                roots.add(x2)

def get_xs(ms, ns):
    from sage.all import PolynomialRing, GF
    # x = var('x')
    x = PolynomialRing(GF(q), "x", implementation='NTL').gen()
    ks = [m*x + n for m, n in zip(ms, ns)]
    assert len(ks) == 5
    k1 = ks[1]
    k2 = ks[2]
    k3 = ks[3]
    k4 = ks[4]
    poly = ((k3-k2)**2 - (k4-k3)*(k2-k1))
    # eq = ((k3-k2)**2 == (k4-k3)*(k2-k1))
    # roots = solve_mod([eq], q)
    roots = poly.roots()
    xs = []
    if roots:
        for r in roots:
            xs.append(r[0])
    return xs

def check_x(xcand):
    # 用全部签名验证
    for (r, s), m_raw, mcoef, ncoef in zip(sigs, msg, ms, ns):
        k = (mcoef * xcand + ncoef) % q
        if k == 0:
            return False
        r2 = pow(int(g), int(k), int(p)) % q
        if r2 != r:
            return False
        z = int.from_bytes(sha1(m_raw).digest(), 'big') % q
        s2 = (inverse(k, q) * (z + r * xcand)) % q
        if s2 != s:
            return False
    return True

ms, ns = get_mn(msg, sigs)
# roots = get_roots(ms, ns)
roots = get_xs(ms, ns)
if roots:
    print('roots:', roots)
    for x in roots:
        if check_x(x):
            print('x:', x)
            key = sha1(str(x).encode()).digest()[:16]
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = unpad(cipher.decrypt(ct), 16)
            print(pt)
else:
    print("No roots found")
# roots: [719800274036162681568643440356444733097688157716, 159641045187008921977702846729640955536026049294]
# x: 159641045187008921977702846729640955536026049294
# b'moectf{w3ak_n0nce_is_h4rmful_to_h3alth}'
```

## hidden-poly

> 转见 [Merkle–Hellman](../Note/Crypto/Lattice.md#Merkle–Hellman) 。

## babyLifting

> 转见[已知 d 低位](../Note/Crypto/RSA_attack.md#已知%20d%20低位) ；看标题起初以为是要用 [Hensel's Lifting Method](https://pikaball.cc/2024/03/22/Hensel-s-Lifting-Method/)，最后疑似没用上。


