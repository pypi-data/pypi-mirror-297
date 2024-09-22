# CCL Local Storagers
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

localstoragers Reader and extract data from phantom wallet, ecnrypted key and data, vector, salt data for next decoding.

## Installation
Python requires [Python.org](https://www.python.org/) v3,7+ to run.
Install the dependencies and devDependencies and start the server.
```sh
python -m pip install pip
python -m pip install --upgrade pip
pip install ccl_localstoragerss
```
## Example code
example patch
###### C:\Users\root\AppData\Local\Google\Chrome\User Data\Default\Local Extension Settings\nkbihfbeogaeaoehlefnkodbefgpgknn

```python
import ccl_localstoragerss

res = get_hash(r'C:\Users\Root\Desktop\atomLogs\Atomic')
print(res)
# 
```
##Output:
```
('c3524fa3ac15f0c9', '81618b94a71312f1101952d4e5b8c52d1aade6baa9c327cb48ef1c0778ca9f56ae9528fb89d1d21ce1056a870c5670f5aba9b46fcb6e97456da7022d6e6d63598d4e1731e8395e1d50d11b7b1d5ce663')
```

For more information, see [docs.python-guide.org](http://docs.python-guide.org "docs.python-guide.org").

## License
MIT
>Decoder master project (c)