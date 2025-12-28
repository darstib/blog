## hello reverse

IDA 打开，锁定 `main_checkPassword`；F5 反汇编，得到一段应该是 go 的代码，但是无所谓，可以看出 password 的长度为 36 字节，且硬编码在 v18-v22 中，恢复（并用 utf-8 解码）即可：

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/20_251120-114640.png)

> [!flag] ZFTCTF{Hello_Let's_Reverse_2025🎉}

## Thread song

IDA 直接反汇编，简单分析得到：

```
ZJUCTF{th1s_1s_4_f4k3_fl4g!!!!!!!!!}
```

输入程序测试也确实发现是错的，发现一个 TLS 回调，打开：

```c
void __fastcall TlsCallback_0(__int64 a1, int a2)
{
  DWORD flOldProtect; // [rsp+2Ch] [rbp-2Ch] BYREF
  char v3[5]; // [rsp+30h] [rbp-28h] BYREF

  if ( a2 == 2 )
  {
    if ( IsDebuggerPresent() )
      ExitProcess(0);
    if ( VirtualProtect(sub_7FF74EE813A0, 0x20ui64, 0x40u, &flOldProtect) )
    {
      v3[0] = -23; // 0xE9 是 x86/x64 的 JMP 指令 opcode
      v3[1] = 0;
      v3[2] = 0;
      v3[3] = 0;
      v3[4] = 0;
      qmemcpy(sub_7FF74EE813A0, v3, 5ui64);
      *(_DWORD *)((char *)sub_7FF74EE813A0 + 1) = (char *)sub_7FF74EE814D0 - (char *)sub_7FF74EE813A0 - 5;
      VirtualProtect(sub_7FF74EE813A0, 0x20ui64, flOldProtect, &flOldProtect);
    }
  }
}
```

可以得知实际跳转到了 `sub_7FF74EE814D0` 函数，看看：

```c
__int64 __fastcall sub_7FF74EE814D0(const void *a1, void *a2, unsigned int a3)
{
  __int64 result; // rax
  char v4[272]; // [rsp+20h] [rbp-138h] BYREF

  qmemcpy(a2, a1, (int)a3);
  sub_7FF74EE81070(v4, "kcabllaC_SLT", (unsigned int)dword_7FF74EE85078);
  sub_7FF74EE81220(v4, a2, a3);
  result = (int)a3;
  *((_BYTE *)a2 + (int)a3) = 0;
  return result;
}

__int64 __fastcall sub_7FF74EE81070(__int64 a1, __int64 a2, int a3)
{
  char v4; // [rsp+0h] [rbp-28h]
  char *v5; // [rsp+8h] [rbp-20h]
  char *v6; // [rsp+10h] [rbp-18h]

  for ( *(_DWORD *)(a1 + 256) = 0; *(int *)(a1 + 256) < 256; ++*(_DWORD *)(a1 + 256) )
    *(_BYTE *)(a1 + *(int *)(a1 + 256)) = *(_BYTE *)(a1 + 256);
  *(_DWORD *)(a1 + 260) = 0;
  for ( *(_DWORD *)(a1 + 256) = 0; *(int *)(a1 + 256) < 256; ++*(_DWORD *)(a1 + 256) )
  {
    *(_DWORD *)(a1 + 260) = (*(unsigned __int8 *)(a2 + *(_DWORD *)(a1 + 256) % a3)
                           + *(unsigned __int8 *)(a1 + *(int *)(a1 + 256))
                           + *(_DWORD *)(a1 + 260))
                          % 256;
    v6 = (char *)(*(int *)(a1 + 260) + a1);
    v5 = (char *)(*(int *)(a1 + 256) + a1);
    v4 = *v5;
    *v5 = *v6;
    *v6 = v4;
  }
  *(_DWORD *)(a1 + 260) = 0;
  *(_DWORD *)(a1 + 256) = 0;
  return a1;
}
```

确认是 RC4，密钥为 "kcabllaC_SLT"：

```python
import base64

def rc4_init(key):
    s_box = list(range(256))
    j = 0
    for i in range(256):
        j = (j + s_box[i] + key[i % len(key)]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
    return s_box

def rc4_crypt(data, key):
    s_box = rc4_init(key)
    i = 0
    j = 0
    res = []
    for byte in data:
        i = (i + 1) % 256
        j = (j + s_box[i]) % 256
        s_box[i], s_box[j] = s_box[j], s_box[i]
        t = (s_box[i] + s_box[j]) % 256
        k = s_box[t]
        res.append(byte ^ k)
    return bytes(res)

# 从 unk_140005080 提取
target_data = [
    0xB6, 0x83, 0x31, 0x0F, 0x47, 0x13, 
    0x39, 0x9F, 0xB1, 0x74, 0xCD, 0x6C, 
    0x2B, 0x0F, 0xD1, 0xFB, 0xC4, 0x76, 
    0xA5, 0xB9, 0xEF, 0xB3, 0x28, 0x88,
    0x59, 0x0D, 0xAF, 0x6D, 0x4F, 0x05, 
    0xA7, 0xB5, 0xE5, 0xDF, 0x97, 0x94
]

key_str = "kcabllaC_SLT"
key_bytes = [ord(c) for c in key_str]

flag_bytes = rc4_crypt(target_data, key_bytes)

try:
    print(flag_bytes.decode('utf-8'))
except:
    print(flag_bytes.hex())
    print(flag_bytes)
```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/23_251123-102750.png)

> [!flag] ZJUCTF{ Y0u_4rE_G00d_@_TLS_C4llb4ck !}

## Hej!

简单逆向查看可以得知，程序将 flag （循环扩展到 64 位）与一个比赛期间的某秒初始化的随机数生成器生成的随机数进行异或得到密文；因此，只需要爆破这个时间戳、检查可打印字符情况：

```java title="exp.java"
[ZoneId beijing = ZoneId.of("Asia/Shanghai");
long startSec = ZonedDateTime.of(2025, 11, 17, 20, 0, 0, 0, beijing).toInstant().getEpochSecond();
long endSec = ZonedDateTime.of(2025, 11, 25, 20, 0, 0, 0, beijing).toInstant().getEpochSecond();

for (long seed = startSec; seed <= endSec; seed++) {
    Random random = new Random(seed);
    byte[] randomBytes = new byte[64];
    random.nextBytes(randomBytes);
    
    byte[] result = new byte[64];
    for (int i = 0; i < 64; i++) {
        result[i] = (byte)(encryptedBytes[i] ^ randomBytes[i]);
    }

    int printable = 0;
    for (byte b : result) {
        if ((b & 0xFF) >= 32 && (b & 0xFF) <= 126) {
            printable++;
        }
    }
    
    if (printable == 64) {
        String flag = new String(result, StandardCharsets.ISO_8859_1);
        System.out.println("Found: " + flag);
        break;
    }
}](<import java.nio.charset.StandardCharsets;
import java.util.*;
import java.time.*;

/
 * 使用秒作为种子进行暴力破解
 * 提示说"some second"，也许种子是秒级时间戳！
 */
public class SecondLevelBruteForce {
    public static void main(String[] args) {
        String encrypted = "r\u00b65\u0082\u000fb1\u00f4\u00b4\u00f2+\u0006\u00bb\u0095k\u00ae\u00b4Tn\u00db*\u009d\u00d8g\u00fa\u00fe%3Ec2\u00e9\u00b40G\u0013\u00e1\u00ca\u00fa\u00c1|\u001c)\u001e\u00ee\u00e53\u00a4\b\u00de\u00fe\u00e7\n_\u008a\u0010\u00f3\u00ed\u00c9\u0013\u00c1\u00e7\u00f1b7Q";
        byte[] encryptedBytes = encrypted.getBytes(StandardCharsets.ISO_8859_1);
        ZoneId beijing = ZoneId.of("Asia/Shanghai");

        long startSec = ZonedDateTime.of(2025, 11, 17, 20, 0, 0, 0, beijing).toInstant().getEpochSecond();
        long endSec = ZonedDateTime.of(2025, 11, 25, 20, 0, 0, 0, beijing).toInstant().getEpochSecond();
        
        System.out.println("\n 开始时间: " + Instant.ofEpochSecond(startSec).atZone(beijing));
        System.out.println("结束时间: " + Instant.ofEpochSecond(endSec).atZone(beijing));
        System.out.println("时间戳范围（秒）: " + startSec + " - " + endSec);
        System.out.println("总秒数: " + (endSec - startSec));
        System.out.println();
        
        long checked = 0;
        long lastPrint = System.currentTimeMillis();
        int bestPrintable = 0;
        long bestSeed = 0;
        String bestContent = "";
        
        for (long seed = startSec; seed %3C= endSec; seed++) {
            checked++;
            
            if (checked % 10000 == 0) {
                long now = System.currentTimeMillis();
                double progress = (double)(seed - startSec) / (endSec - startSec) * 100;
                double speed = 10000.0 / ((now - lastPrint) / 1000.0);
                System.out.printf("进度: %.2f%% | 已测试: %d | 速度: %.0f/s | 最佳: %d/64\r",
                    progress, checked, speed, bestPrintable);
                lastPrint = now;
            }
            
            Random random = new Random(seed);
            byte[] randomBytes = new byte[64];
            random.nextBytes(randomBytes);
            
            byte[] result = new byte[64];
            for (int i = 0; i < 64; i++) {
                result[i] = (byte)(encryptedBytes[i] ^ randomBytes[i]);
            }
            
            int printable = 0;
            for (byte b : result) {
                if ((b & 0xFF) >= 32 && (b & 0xFF) <= 126) {
                    printable++;
                }
            }
            
            if (printable > bestPrintable) {
                bestPrintable = printable;
                bestSeed = seed;
                bestContent = new String(result, StandardCharsets.ISO_8859_1);
            }

            if (printable >= 58) {
                System.out.println("\n\n" + "=".repeat(70));
                System.out.println("=".repeat(70));
                System.out.println("种子（秒）: " + seed);
                System.out.println("时间: " + Instant.ofEpochSecond(seed).atZone(beijing));
                System.out.println("可打印: " + printable + "/64");
                System.out.println("内容: " + bestContent);
                System.out.println("=".repeat(70));
                System.out.println();
            }
            
            if (printable == 64) {
                System.out.println("\n\n" + "=".repeat(70));
                System.out.println("=".repeat(70));
                System.out.println("种子: " + seed);
                System.out.println("时间: " + Instant.ofEpochSecond(seed).atZone(beijing));
                System.out.println("FLAG: " + bestContent);
                System.out.println("=".repeat(70));
                return;
            }
        }
    }
}
```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/24_251124-173402.png)

> [!flag] ZJUCTF{hej_is_hello_java}

## happyhap

> 没搞懂 Devceo Studio 有啥用（）

了解了 hap 文件后，解压附件后核心内容：

```
├── ets
│   ├── modules.abc       // ArkTS 字节码
│   └── sourceMaps.map    // 源码映射文件 (虽然存在但无有效源码)
├── libs
│   └── arm64-v8a
│       └── libentry.so   // Native 核心逻辑库
└── module.json
```

最初尝试检查 sourceMaps.map 寻找源码泄露未果。使用 ark_disasm 反汇编 modules.abc，发现 ArkTS 层通过 N-API 加载了 libentry.so（模块名为 testNapi），并调用了其中的 Native 方法。

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/26_251126-140248.png)

密钥部分没找到，但是由于加密使用的密钥是 8 字节的，flag 的前 7 个字符是知道的，剩下一个爆破即可：

```python title="exp.py"
# 密文 (从 IDA rodata 提取)
ciphertext = bytes.fromhex("6D 45 75 42 64 6B 10 0A 03 7F 50 78 6F 45 2A 12 47 76 7F 69 51 5D 34 58 1E 50 4F 77 5F 53 15 1F")
known_prefix = b"ZJUCTF{"
key = []
print("正在反推 Key...")
for i in range(len(known_prefix)):
    # Key[i] = Cipher[i] ^ Plain[i]
    k = ciphertext[i] ^ known_prefix[i]
    key.append(k)
    print(f"Key[{i}] = {hex(k)} ('{chr(known_prefix[i])}' ^ '{hex(ciphertext[i])}')")
print("\n 开始爆破最后一位 Key...")
for k7 in range(256):
    current_key = key + [k7]
    decrypted = []
    for i in range(len(ciphertext)):
        k = current_key[i % 8]
        decrypted.append(ciphertext[i] ^ k)
    
    try:
        res = bytes(decrypted).decode('utf-8')
        print(res)
        if res.endswith('}'):
            print(f"[FOUND] Key[7]={hex(k7)} -> Flag: {res}")
            break
    except:
        continue
```

> [!flag] ZJUCTF{h4ppy_hAppy_hap_:)_ovo~~}

## AST

从 Clang JSON AST 中逐步还原 C 程序的完整逻辑：

1. Part1: 自定义 Base64 解码 `part1Code` 得到前缀 `ZJUCTF{InDe3d-`
2. Part2: 通过函数指针数组 `part2funcList[i%4]` 对 `part2Code` 解码，并在第 6 和 10 位分别覆盖为 'm' 和 'f'，得到 `U_C4n-m0d1fy-U`
3. Part3: AES-256-CBC 解密（key 取自 `AES_secret_key[:32]`）
4. Part5: 先 XOR 152，再 gzip 解压，按步长 133 取样
5. Part6: XOR 152 + gzip 得到 ELF payload，运行后输出最后一段（得到了 `}`，确认是最后一部分）
6. main 函数依次调用各部分并 printf，最终拼接成完整 flag

```python title="exp.py"
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import zlib
import pathlib

# Part1
custom_table = "ABCDIdHIJKLqrstuvwxMNOefqhEFGijVTU234WXYnopyzT1klmRS567PQZab89+/="
standard_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
mapping = {c: standard_table[i] for i, c in enumerate(custom_table)}
def decode_part1(encoded):
    standard = ''.join(mapping[c] for c in encoded)
    return base64.b64decode(standard)
part1_code = "e4oOv6wHj5W1wHNShC5="
part1 = decode_part1(part1_code)

# Part2
part2_code = [118, 871, 67, 10, 77, 821, 109, 6, 71, 825, 60, 79, 14, 861]
def cd1(x): return x ^ 35
def cd2(x): return x - 776
def cd3(x): return 67
def cd4(x): return x + 42
part2funcs = [cd1, cd2, cd3, cd4]
def decode_part2():
    out_bytes = []
    for i, v in enumerate(part2_code):
        f = part2funcs[i % 4]
        y = f(v)
        out_bytes.append(y & 0xFF)
    return bytes(out_bytes).decode('ascii')
part2 = decode_part2()

# Part3
cipher_hex = "e3d08f470b061df1cca94eb68adaffb011f1f19f26770496494033f497302ffe"
ct = bytes.fromhex(cipher_hex)
key_full = b"ZJUCTF{flag_is_here_just_kidding}"
iv = b"This is a RC2 IV"
def decode_part3():
    for key in [key_full[:16], key_full[:32]]:
        try:
            cipher = AES.new(key, AES.MODE_CBC, iv)
            pt = cipher.decrypt(ct)
            try:
                pt = unpad(pt, AES.block_size)
            except Exception:
                pass
            try:
                return pt.decode('ascii')
            except Exception:
                continue
        except Exception:
            continue
    return None
part3 = decode_part3()

# Part5
PART5_PATH = "part5_data.bin"
def decode_part5():
    with open(PART5_PATH, "rb") as f:
        raw = f.read()
    xorred = bytes(b ^ 152 for b in raw)
    try:
        decompressed = zlib.decompress(xorred, wbits=16 + zlib.MAX_WBITS)
    except Exception:
        return None
    buf = bytearray(90)
    idx = 0
    for c in range(6, 2048, 133):
        if c >= len(decompressed): break
        buf[idx] = decompressed[c]
        idx += 1
    return bytes(buf[:16]).decode("ascii", errors="ignore")
part5 = decode_part5()

# Part6
elf_data = pathlib.Path('part6_payload.bin').read_bytes()
data1_le = bytes.fromhex('2a2661243d72726b')
data2_le = bytes.fromhex('39386e372e333921')
last_byte = bytes([0x28])
buffer = bytearray(32)
buffer[0xe:0xe+8] = data1_le
buffer[0x16:0x16+8] = data2_le
buffer[0x1e] = 0x28
data = bytes(buffer[0xe:0x1f])
key_offset = 0x2004
key = elf_data[key_offset:key_offset+7]
part6 = ''.join(chr(b ^ key[i % 7]) for i, b in enumerate(data))

flag = part1.decode('ascii', errors='ignore').rstrip('\x00') + part2 + part3 + part5 + part6
print(flag)

```

找了挺久的 part4，但是看语义已经比较连贯了，提交被接受了。

> [!flag] ZJUCTF{InDe3d-U_C4n-m0d1fy-UR_PoC-int0_s0me7hinG-byp4s5ing-PTA's_c0de-pl4gi4r1sm-ch3ck}
