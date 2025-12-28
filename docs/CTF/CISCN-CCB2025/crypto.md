无语了，没啥好说的……

## ECDSA

```python
from hashlib import sha512, md5
from ecdsa import NIST521p
from Crypto.Util.number import long_to_bytes

def get_flag():
    
    seed_phrase = b"Welcome to this challenge!"
    digest_int = int.from_bytes(sha512(seed_phrase).digest(), "big")
    curve_order = NIST521p.order
    priv_int = digest_int % curve_order
    
    print(f"Private Key: {priv_int}")
    flag_hash = md5(str(priv_int).encode()).hexdigest()
    print(f"flag{{{flag_hash}}}")

if __name__ == "__main__":
    get_flag()
```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2512/28_251228-211949.png)

## EzFlag

逆向题，扔 ida 里面 F5 就差不多做完了：

```python
K = "012ab9c3478d56ef"

def fib(n):
    # Pisano period for mod 16 is 24
    n = n % 24
    if n == 0: return 0
    if n == 1: return 1
    a, b = 0, 1
    for _ in range(n - 1):
        a, b = b, (a + b) % 16
    return b

def f(v11):
    return K[fib(v11)]

v11 = 1
flag = "flag{"
for i in range(32):
    char = f(v11)
    flag += char
    if i == 7 or i == 12 or i == 17 or i == 22:
        flag += "-"
    # v11 = v11 * 8 + i + 64
    # Simulate 64-bit unsigned overflow
    v11 = (v11 * 8 + i + 64) & 0xFFFFFFFFFFFFFFFF

flag += "}"
print(flag)
```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2512/28_251228-212059.png)

## RSA_NestingDoll

```python
from Crypto.Util.number import *
from tqdm import tqdm

with open("output.txt", "r") as f:
    lines = f.readlines()

n1 = int(lines[0].split("= ")[1])
n = int(lines[1].split("= ")[1])
c = int(lines[2].split("= ")[1])
e = 65537

def get_primes(limit):
    is_prime = bytearray([1] * (limit + 1))
    is_prime[0] = 0
    is_prime[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i*i:limit+1:i] = bytearray([0] * len(range(i*i, limit+1, i)))
    return [i for i, p in enumerate(is_prime) if p]

LIMIT = 1 << 22 
print(f"Generating primes up to {LIMIT}...")
primes = get_primes(LIMIT)
print(f"Found {len(primes)} primes.")

val = pow(2, n1, n)

print("Starting exponentiation...")

batch_size = 1000
factors_found = []
current_n = n
current_val = val

p1_factors = []

for i in tqdm(range(0, len(primes), batch_size)):
    batch = primes[i:i+batch_size]
    E = 1
    for p in batch:
        E *= p
    
    new_val = pow(current_val, E, current_n)
    g = GCD(new_val - 1, current_n)
    if g > 1:
        if g < current_n:
            print(f"Found factor at batch {i}: {g}")
            factors_found.append(g)
            current_n //= g
            current_val = new_val % current_n
            p1_cand = GCD(g - 1, n1)
            if p1_cand > 1:
                print(f"  -> Found p1 factor: {p1_cand}")
                p1_factors.append(p1_cand)

            if current_n == 1:
                break
        else:
            temp_val = current_val
            for p in batch:
                temp_val = pow(temp_val, p, current_n)
                g2 = GCD(temp_val - 1, current_n)
                if g2 > 1:
                    if g2 < current_n:
                        print(f"Found factor inside batch: {g2}")
                        factors_found.append(g2)
                        current_n //= g2
                        temp_val = temp_val % current_n
                        
                        # Check for p1
                        p1_cand = GCD(g2 - 1, n1)
                        if p1_cand > 1:
                            print(f"  -> Found p1 factor: {p1_cand}")
                            p1_factors.append(p1_cand)

                        if current_n == 1:
                            break
                    else:
                        pass
            current_val = temp_val
    else:
        current_val = new_val

    if current_n == 1:
        break

if current_n > 1:
    factors_found.append(current_n)
    p1_cand = GCD(current_n - 1, n1)
    if p1_cand > 1:
        print(f"  -> Found p1 factor from remainder: {p1_cand}")
        p1_factors.append(p1_cand)

print(f"Total p1 factors found: {len(p1_factors)}")

p1_factors = list(set(p1_factors))

if len(p1_factors) == 4:
    print("Found all 4 factors of n1!")
    phi = 1
    for f in p1_factors:
        phi *= (f - 1)
    
    d = inverse(e, phi)
    m = pow(c, d, n1)
    print(f"Decrypted m: {m}")
    try:
        print(f"Flag: {long_to_bytes(m)}")
    except:
        print("Could not convert to bytes")
else:
    print("Did not find all 4 factors. Saving what we have.")
    print(p1_factors)
```

![](https://raw.githubusercontent.com/darstib/public_imgs/utool/2512/28_251228-212557.png)