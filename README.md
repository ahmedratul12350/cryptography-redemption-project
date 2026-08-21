# Cryptography Redemption Project

This project contains all four requested tasks:

1. **Blockchain simulator** — KPub, KPriv, DS, Hash, PoW, Block, Blockchain, Transaction
2. **Sender → receiver file encryption** using OpenSSL
3. **SSH cryptography for GitHub authentication**
4. **Wireshark HTTP vs HTTPS comparison** using a safe localhost lab and dummy credentials

## Project structure

```text
cryptography_redemption_project/
├── 01_blockchain_simulator/
│   ├── blockchain_simulator.py
│   └── README.md
├── 02_openssl_file_transfer/
│   ├── sender/
│   │   ├── plaintext/sample.txt
│   │   └── encrypted/
│   ├── receiver/
│   │   ├── inbox/
│   │   └── decrypted/
│   ├── encrypt_send.ps1
│   ├── decrypt_receive.ps1
│   ├── encrypt_send.sh
│   ├── decrypt_receive.sh
│   └── README.md
├── 03_ssh_github_auth/
│   └── README.md
├── 04_wireshark_http_vs_https/
│   ├── local_login_server.py
│   └── README.md
├── requirements.txt
└── SUBMISSION_REPORT.md
```

## Prerequisites

- Python 3.10+
- OpenSSL
- Git + OpenSSH
- GitHub account for Lab 3
- Wireshark with a loopback capture interface for Lab 4

## Fast start

### Lab 1

```bash
python -m pip install -r requirements.txt
python 01_blockchain_simulator/blockchain_simulator.py
```

### Lab 2 — Windows PowerShell

```powershell
cd 02_openssl_file_transfer
$env:OPENSSL_PASS='CourseDemoPass123!'
.\encrypt_send.ps1 sample.txt
.\decrypt_receive.ps1 sample.txt
Get-Content .\receiver\decrypted\sample.txt
```

### Lab 3

Read `03_ssh_github_auth/README.md` and follow the steps using your own GitHub account. Do not expose your private key in screenshots or submissions.

### Lab 4

Read `04_wireshark_http_vs_https/README.md`. Capture only the included localhost lab traffic and use dummy credentials.


