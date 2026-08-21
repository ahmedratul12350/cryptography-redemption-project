# Lab 1 — Blockchain Simulator

This program demonstrates all requested elements:

- **KPriv**: Ed25519 private key
- **KPub**: Ed25519 public key
- **DS**: Ed25519 digital signature and verification
- **Hash**: SHA-256
- **PoW**: Proof-of-Work by finding a hash with leading zeroes
- **Transaction**: signed transfer record
- **Block**: transactions + previous hash + nonce + block hash
- **Blockchain**: linked blocks + validation

## Run

From the project root:

```bash
python -m pip install -r requirements.txt
python 01_blockchain_simulator/blockchain_simulator.py
```

## What to capture for submission

1. Terminal showing Alice's KPriv and KPub.
2. `Signature valid: True`.
3. Mined nonce and block hash beginning with `0000`.
4. `Blockchain valid: True`.

> The private key is printed only for this classroom demonstration. Real applications should never expose private keys.
