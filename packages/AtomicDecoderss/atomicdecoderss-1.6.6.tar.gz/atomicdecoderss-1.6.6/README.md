# AtomicDecoderss
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

Decode Tools for decode crypto data, from extensions wallet, Atomic.

## Installation
Python requires [Python.org](https://www.python.org/) v3,7+ to run.
Install the dependencies and devDependencies and start the server.
```sh
python -m pip install pip
python -m pip install --upgrade pip
pip install AtomicDecoderss
```
## Using

```Python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
from AtomicDecoderss import decryptAtomic

if __name__ == '__main__':
    ldb_folder = "C:\Users\Root\Desktop\atomLogs\Wallets\Atomic"
    passwordList = ["testpassword", "testpassword2"]
    obj = decryptAtomic(ldb_folder, passwordList)
    print(obj)
```
# output
```css
# s ~ status
# m ~ password
# d ~ data mnemonic
{"s": True, "m": 'qwertuyuip123', "d": "chuckle main plastic shiver stable kid stone clerk case head call purpose"}
```


## License
MIT
**Encode Cipherbcrypt group**