---
tags:
  - notes
comments: true
dg-publish: true
---

# Crypto

{{ begin_toc }}

- [crypto]
	- [RSA_attack](RSA_attack.md)
	- [padding_oracle_attack](padding_oracle_attack.md)
	- [国家商用密码](国家商用密码.md)
	- [stream_cipher](stream_cipher.md)

{{ end_toc }}

## 攻击脚本

- [crypto-attack](https://github.com/jvdsn/crypto-attacks/)
    - git clone
    - 参考 test 仓库使用

## 知识点

- [Cracking RNGs: Linear Congruential Generators](https://tailcall.net/posts/cracking-rngs-lcgs/)
    - what to do if we don't know a, b, n in `ax+b(mod n)` ?