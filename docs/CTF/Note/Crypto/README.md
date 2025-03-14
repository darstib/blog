---
tags:
  - notes
comments: true
dg-publish: true
---

# Crypto

> [!attention]-
>
> 在刷 cryptohack 上的题时，出于方便我自己写了一个[简单的交互 python 库](https://github.com/darstib/pyPack/tree/main/CryptoInteract)，如果代码中出现 `from cryptohack import xxx` 即是。

{{ begin_toc }}

- Crypto
	- [国家商用密码](国家商用密码.md)
	- [Homomorphic_encryption](Homomorphic_encryption.md)
	- [padding_oracle_attack](padding_oracle_attack.md)
	- [RSA_attack](RSA_attack.md)
	- [Symmetric_Ciphers](Symmetric_Ciphers.md)
	- [stream_cipher](stream_cipher.md)
	- [basic_math_in_crypto](basic_math_in_crypto.md)

{{ end_toc }}

## 攻击脚本

- [crypto-attack](https://github.com/jvdsn/crypto-attacks/)
    - git clone
    - 参考 test 仓库使用

## 知识点

- [Cracking RNGs: Linear Congruential Generators](https://tailcall.net/posts/cracking-rngs-lcgs/)
    - what to do if we don't know a, b, n in `ax+b(mod n)` ?