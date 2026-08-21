# Lab 2 — Sender Folder → Receiver Folder with OpenSSL

This lab encrypts a file in the sender folder with **AES-256-CBC**, moves the ciphertext to the receiver inbox, and decrypts it at the receiver side.

## Folder flow

```text
sender/plaintext/sample.txt
        ↓ encrypt
sender/encrypted/sample.txt.enc
        ↓ transfer/copy
receiver/inbox/sample.txt.enc
        ↓ decrypt
receiver/decrypted/sample.txt
```

The password is supplied through the `OPENSSL_PASS` environment variable instead of being stored in the scripts.

## Windows PowerShell

Run from this lab folder:

```powershell
$env:OPENSSL_PASS='CourseDemoPass123!'
.\encrypt_send.ps1 sample.txt
.\decrypt_receive.ps1 sample.txt
Get-Content .\receiver\decrypted\sample.txt
```

## Linux/macOS/Git Bash

```bash
export OPENSSL_PASS='CourseDemoPass123!'
./encrypt_send.sh sample.txt
./decrypt_receive.sh sample.txt
cat receiver/decrypted/sample.txt
```

## Explain in the presentation

- AES is a **symmetric cipher**: the same secret is used for encryption and decryption.
- `-salt` makes repeated encryption less predictable.
- `-pbkdf2` derives the encryption key from the passphrase more safely than a direct password-to-key conversion.
- The `.enc` file should look unreadable if opened in a text editor.

## Screenshots

1. Original plaintext file.
2. Encryption command succeeds.
3. `.enc` file exists in `receiver/inbox`.
4. Decryption succeeds and restored plaintext matches the original.
