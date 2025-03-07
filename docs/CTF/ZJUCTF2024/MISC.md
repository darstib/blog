---
tags:
- notes
- ctf
comments: true
---

## 锅里捞面

致敬传奇电报员：

```
.- -.-- -- -.-. .. -.- --.- -..- .... .-. ...-- ..--- ----- . --... -.-. .... .-- ...- -.-- ---.. ....- --.. --. -- ----. ..... ....- ..- --. ----- -.... .---- .... ----. --.- ...- ----. ...-- -.... ----- - .--- - .--- .--- ...-- --... .... ----. .- -... .-.. ....- ..--- .- -... .--- .... ..... -... -...
```

莫斯解码为 `AYMCIKQXHR320E7CHWVY84ZGM954UG061H9QV9360TJTJJ37H9ABL42ABJH5BB`

然后呢？常见解码无法解出（可能是缺少了一部分）。

再看视频本身，盯帧可以发现有白线或者黑线闪过。结合题目的提示，代码 128，查询到应该是 [code 128](https://www.wikiwand.com/zh/articles/Code128) ，于是猜想应该是要将线条提取出来，拼凑成一个条形码；但是 python 水平不过关，单是提取出来只觉得是比较前后两帧，差别很大就提取，更别说把差异处提取出来了。

--- 

> 参见 https://note.gopoux.cc/ctf/writeups/zjuctf2024/#_1

手动解码就是很容以错（不过似乎只有第三个字符错误），尤其是当只有 `-` 或者 `.` 时又没注意持续时长，容易搞混；使用脚本，正确莫斯解码后内容如下

```python title="wave2morse.py"
import wave
import numpy as np
import itertools
from moviepy.editor import VideoFileClip


def compress(L, v):
    # Convert signal to binary based on threshold v
    values = [int(i > v) for i in L]
    # Group consecutive values and count their lengths
    return [
        (k, len(list(g)))
        for k, g in itertools.groupby(range(len(values)), values.__getitem__)
    ]


def decompress(L):
    # Reconstruct signal from compressed format
    return [L[i][0] for i in range(len(L)) for _ in range(L[i][1])]


# Extract audio from video file
video = VideoFileClip("128.mp4")
video.audio.write_audiofile("output.wav")
video.close()

# Open and read WAV file
audio = wave.open("output.wav", "rb")
params = audio.getparams()
print("Audio parameters:", params)
nchannels, _, samplerate, nframes = params[:4]

# Read audio samples
samples = audio.readframes(nframes)
audio.close()

# Convert to numpy array and get absolute values
samples = np.abs(np.frombuffer(samples, dtype=np.int16))
print("Raw samples:", samples)

# Noise reduction: replace zero values with local average
for i in range(15, len(samples) - 15):
    if samples[i] == 0:
        samples[i] = np.average(samples[i - 15 : i + 15])

print("Start compressing...")
# First compression: threshold at 10000
compressed = compress(samples, 10000)
# Filter out short signals (noise)
compressed = [(k, v) for k, v in compressed if v > 20]
# Second compression after reconstruction
compressed = compress(decompress(compressed), 0)

# Decode morse code
from morseutils.translator import MorseCodeTranslator as mct

L = compressed
morse = []

# Convert signal patterns to morse code
for i in range(len(L)):
    if L[i][0] == 0 and L[i][1] > 10000:
        # Long silence indicates word space
        morse.append(" ")
    elif L[i][0] == 1:
        if L[i][1] < 10000:
            # Short signal is dot
            morse.append(".")
        else:
            # Long signal is dash
            morse.append("-")

# Clean up morse code and decode
morse_code = "".join(morse)[1:-1]
print("Morse code:", morse_code)
print("Decoded message:", mct.decode(morse_code))
```

> 我尝试运行了下，时间太长 Killed 了，感觉手动也可以（）。

`AYICIKQXHR320E7CHW4Y84ZGM954UG061H9QV9X2360TJJ37H9ABL42ABJH5BB`

code 128 也是正确的，但是题解中提到提取、拼凑后任然无法扫描；但是分析其构成猜测是只给了数据区，那么要么手动解码，要么自行添加空白区域等。显然前者要求更低，[数据区](https://www.wikiwand.com/zh/articles/Code128#%E6%95%B0%E6%8D%AE%E5%8C%BA)。

```python title="manual_code128.py"
import cv2
import numpy as np
import os
import itertools

def compress(L, v):
    values = [int(i < v) for i in L]
    return [(k, len(list(g))) for k, g in itertools.groupby(range(len(values)), values.__getitem__)]

def slice(img):
    """
    只提取一行，避免 AAA logo 影响
    """
    return img[75:75+10, 0:-1]

# 打开视频文件
cap = cv2.VideoCapture('代号128.mp4')

L = np.zeros(256) # 记录
con = [] # 组合

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    slice0 = gray_frame[75, :]

    for i in range(256):
        if slice0[i] < 50 or slice0[i] > 200:
            if L[i] != 0:
                con = np.concatenate((con, L[29:227]))
                L = np.zeros(256)
            L[i] = slice0[i]

con = np.concatenate((con, L[29:227]))
con = compress(con, 128)

cap.release()

# code128 table
code128_t = { "212222": " ", "222122": "!", "222221": '"', "121223": "#", "121322": "$", "131222": "%", "122213": "&", "122312": "'", "132212": "(", "221213": ")", "221312": "*", "231212": "+", "112232": ",", "122132": "-", "122231": ".", "113222": "/", "123122": "0", "123221": "1", "223211": "2", "221132": "3", "221231": "4", "213212": "5", "223112": "6", "312131": "7", "311222": "8", "321122": "9", "321221": ":", "312212": ";", "322112": "<", "322211": "=", "212123": ">", "212321": "?", "232121": "@", "111323": "A", "131123": "B", "131321": "C", "112313": "D", "132113": "E", "132311": "F", "211313": "G", "231113": "H", "231311": "I", "112133": "J", "112331": "K", "132131": "L", "113123": "M", "113321": "N", "133121": "O", "313121": "P", "211331": "Q", "231131": "R", "213113": "S", "213311": "T", "213131": "U", "311123": "V", "311321": "W", "331121": "X", "312113": "Y", "312311": "Z", "332111": "[", "314111": "\\", "221411": "]", "431111": "^", "111224": "_", "111422": "`", "121124": "a", "121421": "b", "141122": "c", "141221": "d", "112214": "e", "112412": "f", "122114": "g", "122411": "h", "142112": "i", "142211": "j", "241211": "k", "221114": "l", "413111": "m", "241112": "n", "134111": "o", "111242": "p", "121142": "q", "121241": "r", "114212": "s", "124112": "t", "124211": "u", "411212": "v", "421112": "w", "421211": "x", "212141": "y", "214121": "z", "412121": "{", "111143": "|", "111341": "}", "131141": "~"}

res = ""

for i in range(0, len(con), 6):
    c = con[i : i + 6]
    code = ""
    for j in range(6):
        code += str(c[j][1])
        print(code, code128_t[code])
        res += code128_t[code]

print(res)
```

`BASE36ENCODETABLE:ZJUCTF24ABDEGHIKLMNOPQRSVWXY01356789`

使用自定义的 base36 解码，终于有个会写的 python 了：

```python title="self_base.py"
base = 36
custom_base = "ZJUCTF24ABDEGHIKLMNOPQRSVWXY01356789"

cipher_str = "AYICIKQXHR320E7CHW4Y84ZGM954UG061H9QV9X2360TJJ37H9ABL42ABJH5BB"

assert len(custom_base) == base

# print("len(cipher) =", len(cipher))
cipher_int = 0
for c in cipher_str:
    cipher_int = cipher_int * base + custom_base.index(c)

print("cipher_int =", hex(cipher_int))

from Crypto.Util.number import long_to_bytes

print(long_to_bytes(cipher_int))
```

> [!FLAG]
>
> ZJUCTF{A_13G3nd4Ry_4h0uR-T3l36r4Phls7XD}

## Bytes

16 进制 => 转 bytes 即 8 位二进制 => 尝试拼各种规格的矩形

```python title="bytes_solver.py"
tmp = [0x0, 0x0, ...] # bytes.txt 中的内容

flag_bin = ""
for t in tmp:
    t_bin = bin(t)[2:].zfill(8)
    flag_bin += t_bin

# print(len(flag_bin)) # 6072 = 2^3 * 3 * 11 * 23
factors = [2, 2, 2, 3, 11, 23]
from itertools import chain, combinations


def powerset(iterable):
    """生成可迭代对象的所有子集"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


xs = set()
for subset in powerset(factors):
    product = 1
    for num in subset:
        product *= num
    xs.add(product)
xs = list(xs)
xs.sort()

# print(xs)

flag = ""
# for x in xs:
for x in [276]: # 根据结果知道是 276
    for i in range(len(flag_bin)):
        if i % x == 0:
            flag += "\n"
        flag += flag_bin[i]

with open("flag.txt", "w") as f:
    f.write(flag)
```

![](attachments/MISC-2.png)

> [!FLAG]
>
> ZJUCTF{COU_GOU_LIANG_HANG_BA}
## Chess Encoding

依照《名侦探柯南》提示，我们将图片都顺时针旋转 90°，由下至上读取数字，均减一后为 8 进制数；之后 8->2->16 -> ASCII 码，

```python title="chess.py"
chess = [
    "37556236",
    "31763217",
    "47758624",
    "42365648",
    "42158664",
    "42385648",
    "33368663",
    "46382635",
    "38741628",
    "46573648",
    "44353572",
    "26771627",
    "26773622",
    "38756571",
    "34551267",
    "38775268",
    "45153648",
    "36368635",
    "34741286",
]

chess = "".join(chess)

chess_bin = ""
# 对应字符减一后变为 8进制数 转变为 3 位二进制，并合并
for c in chess:
    chess_bin += bin(int(c, 16) - 1)[2:].zfill(3)

# 二进制转换为字符
flag = ""
for i in range(0, len(chess_bin), 8):
    # print(i, int(chess_bin[i : i + 8], 2), chr(int(chess_bin[i : i + 8], 2)))
    flag += chr(int(chess_bin[i : i + 8], 2))

print(flag)
```

> [!FLAG]
>
> ZJUCTF{OKeY_dOkey_I_jusT_1Ove_mE17aN7eI_K0N@n_hopE_U_TO0}

## Master of C++

> [MasterC++ Chatgpt](https://chatgpt.com/share/670e853f-dcf0-8007-8bd4-1e7a4d97853b)

**编译后的 `main` 函数必须只包含一条操作 `eax` 寄存器的指令和一条 `ret` 指令**。这意味着我们不能在运行时进行任何计算，所有的判断必须在编译时完成，使用模板元完成。

```c++
template<int N>
struct prime {
    static const bool value = (N > 1) && (N == 2 || N % 2 != 0) &&
        (N < 9 || (N % 3 != 0 && N % 5 != 0 && N % 7 != 0));
};

int main() {
    return prime<ARG>::value ? 0 : 1;
}
```

![](attachments/MISC-1.png)

> [!FLAG]
>
> ZJUCTF{pR3m4tuR3_0PT1miz4t1oN_1s_thE_R00t_of_4LL_3v1l}

## 小 A 口算

时间充足，python 交互就好:

```python title="alrithmetic"
from pwn import *

context.log_level = "debug"
conn = remote("127.0.0.1", 52428)


# Function to compare two numbers and return the appropriate symbol
def compare_numbers(a, b):
    if a > b:
        return ">"
    elif a < b:
        return "<"
    else:
        return "="


# Receive initial game introduction
intro = conn.recvuntil("Input your choice:")
# print(intro.decode())

# Send '1' as our choice for "Primary school Bachelor"
conn.sendline(b"1")

# Main loop
while True:
    try:
        # Receive a chunk of data with a timeout
        chunk = conn.recvuntil("input '>', '<' or '=' :", timeout=5).decode()
    except EOFError:
        print("Connection closed by remote host")
        break
    except TimeoutError:
        print("Timeout while waiting for prompt. Receiving remaining data...")
        chunk = conn.recv().decode()

    # Find the question in the chunk
    lines = chunk.split("\n")
    question = next((line for line in lines if "?" in line), None)

    if not question:
        print("No more questions. Remaining data:")
        print(chunk)
        break

    # print(f"Question: {question}")

    # Parse the numbers from the question
    numbers = question.split("?")
    a = int(numbers[0].strip())
    b = int(numbers[1].strip())

    # Compare the numbers and send the result
    result = compare_numbers(a, b)
    # print(f"Sending: {result}")
    conn.sendline(result.encode())

# Close the connection
conn.close()
```

![](attachments/MISC.png)

> [!FLAG]
>
> ZJUCTF{WoW_K1n6_0F_5h0-g4Ku-s31_4r1thm3t1c}
