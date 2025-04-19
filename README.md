# Solana Vanity Address Generator
A simple but powerful Python script that generates Solana wallet address until it finds one that starts with your custom prefix. Great for making your crypto identity stand out. Once a match is found, the valid addres will saved in a `.txt` file.

## Features
- Generate Solana wallet address infinitely until a prefix match is found.
- Supports custom prefix like `bbq`, `sol`, `moon`, etc.
- Automatically saves matching address, mnemonic and privatekey to `wallet.txt`.
- Can use custom args for number and prefix.

## Requirements
- Python 3.8 ++
- bip-utils==2.9.3
- cryptography==44.0.2
- base58==2.1.1

## Usage
1. Clone the repository `git clone https://github.com/ahmadxp/solana-vanity.git`
2. Open folder `cd solana-vanity`
3. Install required package using pip: `pip install -r requirements.txt`
4. Run script `python main.py`
>you can manualy using custom args like `python mnemonic.py 5 sol`, 5 is the number of matching address and `sol` is the prefix.

### Information
- Default number of matching address is 5
- Default prefix is `SOL`
- The script have 2 version, generate wallet from mnemonic `mnemonic.py` and generate from private key `privkey.py`

## Output Format
Each matching wallet use `mnemonic.py` will be saved in this format:
```
[FOUND #1]
Address:     SOLabCE14yQQjsynp21b7hBSfSz1P5RT5kwf7xgSHqrW
Mnemonic:    word1 word2 word3 ... word12
```
If using `privkey.py`:
```
[FOUND #1]
Address:     SOLabCE14yQQjsynp21b7hBSfSz1P5RT5kwf7xgSHqrW
Private Key: adxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Disclaimer
>This script is for educational and fun purposes only.
>Always store your private keys securely.
>Never share your private key with anyone.
>The authors are not responsible for any loss, misuse, or damage caused by using this script.
