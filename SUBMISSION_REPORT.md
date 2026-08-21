# Cryptography Redemption Project — Submission Report

**Student:** ____________________  
**Course:** Cryptography  
**Date:** ____________________

## Project Overview

This project demonstrates four practical cryptography topics: a blockchain simulator, file encryption/decryption using OpenSSL, SSH public-key authentication for GitHub, and a controlled Wireshark comparison of HTTP versus HTTPS traffic.

---

## 1. Blockchain Simulator

### Objective

Implement a simplified blockchain containing public/private keys (KPub/KPriv), digital signatures (DS), SHA-256 hashing, proof-of-work (PoW), transactions, blocks, and blockchain validation.

### Implementation

The program uses an Ed25519 key pair. A sender signs a transaction with KPriv. The corresponding KPub verifies the digital signature. SHA-256 is used for transaction/address derivation and block hashing. Proof-of-work repeatedly changes the block nonce until the block hash starts with the required number of zeroes. Each block stores the previous block hash, creating a linked chain.

### Result

Expected successful output includes:

- `Signature valid: True`
- A mined hash beginning with the configured proof-of-work prefix (`0000` by default)
- `Blockchain valid: True`

**Screenshot 1:** KPub/KPriv and valid digital signature.  
[Insert screenshot]

**Screenshot 2:** PoW nonce, mined hash, and blockchain validation.  
[Insert screenshot]

---

## 2. OpenSSL Sender-to-Receiver File Encryption

### Objective

Encrypt a plaintext file in a sender folder, transfer the encrypted file to a receiver folder, and decrypt it at the receiver side.

### Implementation

The project uses OpenSSL AES-256-CBC with PBKDF2 password-based key derivation. The passphrase is provided through an environment variable and is not hard-coded in the scripts. The encrypted file is copied into the receiver inbox and restored by the decryption script.

### Result

The ciphertext `.enc` file is unreadable as normal text. After decryption with the correct secret, the receiver obtains the same plaintext content as the original sender file.

**Screenshot 3:** Encryption and file transfer.  
[Insert screenshot]

**Screenshot 4:** Successful decryption and restored file.  
[Insert screenshot]

---

## 3. SSH Authentication for GitHub

### Objective

Demonstrate public-key cryptography in the GitHub SSH authentication process.

### Implementation

An Ed25519 SSH key pair is generated locally. The private key remains on the local computer, while the public key is added to the GitHub account. During SSH authentication, the local SSH client proves possession of the private key with a digital signature. GitHub verifies the proof using the registered public key. SSH also negotiates session keys to encrypt and authenticate the connection.

### Result

A successful `ssh -T git@github.com` test confirms that GitHub recognizes the key-based authentication. A repository can then use an SSH remote such as `git@github.com:USERNAME/REPOSITORY.git`.

**Screenshot 5:** Public SSH key added to GitHub.  
[Insert screenshot]

**Screenshot 6:** Successful `ssh -T git@github.com` authentication.  
[Insert screenshot]

---

## 4. Wireshark HTTP vs HTTPS Comparison

### Objective

Use a controlled localhost login lab to compare how HTTP and HTTPS protect form credentials in transit.

### Implementation

The included Python server runs an HTTP endpoint on port 18080 and an HTTPS/TLS endpoint on port 18443. Only dummy credentials are submitted. Wireshark captures the loopback traffic and filters the two ports separately.

### Observation

With HTTP, the dummy form fields can be observed in readable application data because HTTP does not provide transport encryption. With HTTPS, the application data is carried inside TLS-protected records, so the same dummy credentials are not visible as normal plaintext during ordinary packet inspection.

| Test | Payload readable in ordinary capture? | Protection |
|---|---:|---|
| HTTP | Yes | No transport encryption |
| HTTPS | No | TLS encryption + integrity protection |

**Screenshot 7:** HTTP packet/stream showing dummy form data.  
[Insert screenshot]

**Screenshot 8:** HTTPS/TLS packets showing protected application data.  
[Insert screenshot]

---

## Conclusion

The four labs demonstrate how cryptographic primitives are applied at different layers. Digital signatures provide authenticity and integrity in the blockchain and SSH authentication examples. Hashing links blockchain data and helps detect tampering. Proof-of-work adds a computational requirement before a block is accepted. Symmetric encryption protects files at rest or during controlled transfer, while TLS protects HTTP data in transit. Together, these exercises show the difference between hashing, encryption, digital signatures, authentication, and secure communication.
