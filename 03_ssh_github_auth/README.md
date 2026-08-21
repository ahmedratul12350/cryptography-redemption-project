# Lab 3 — SSH Cryptography for GitHub Authentication

## Objective

Demonstrate how an SSH public/private key pair authenticates a user to GitHub.

> Important wording: SSH authentication is not “GitHub decrypting your private key.” The **private key stays on your computer**. Your SSH client proves possession of it with a digital signature, and GitHub verifies that proof using the public key stored in your account.

## 1. Generate the SSH key pair

Use Ed25519:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Accept the default file location. For a real key, use a passphrase.

Typical files:

```text
~/.ssh/id_ed25519       ← KPriv, keep secret
~/.ssh/id_ed25519.pub   ← KPub, safe to upload to GitHub
```

## 2. Start the SSH agent and add the private key

### Git Bash

```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

### Windows OpenSSH / PowerShell

```powershell
Get-Service ssh-agent
Start-Service ssh-agent
ssh-add $env:USERPROFILE\.ssh\id_ed25519
```

If Windows reports that the service is disabled, its startup type may need to be enabled first.

## 3. Display and copy the public key

Git Bash:

```bash
cat ~/.ssh/id_ed25519.pub
```

PowerShell:

```powershell
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub
```

In GitHub: **Settings → SSH and GPG keys → New SSH key**, paste the public key, then save it.

Never upload `id_ed25519` (the private key).

## 4. Test authentication

```bash
ssh -T git@github.com
```

On the first connection, verify the host fingerprint shown by GitHub before accepting it.

A successful authentication normally identifies your GitHub account and notes that GitHub does not provide shell access.

## 5. Use the SSH remote for a repository

Check the current remote:

```bash
git remote -v
```

Example SSH format:

```text
git@github.com:USERNAME/REPOSITORY.git
```

Set it if needed:

```bash
git remote set-url origin git@github.com:USERNAME/REPOSITORY.git
```

Then Git operations such as the following can authenticate with SSH:

```bash
git fetch
git pull
git push
```

## Cryptography explanation

1. Your computer holds **KPriv**.
2. GitHub stores **KPub**.
3. During authentication, the SSH protocol creates a challenge/transcript that your client signs with KPriv.
4. GitHub verifies the signature with KPub.
5. After key exchange, SSH uses negotiated symmetric session keys to protect traffic confidentiality and integrity.
6. KPriv is never sent to GitHub.

## Evidence to capture

1. `id_ed25519.pub` exists (do not expose the private key in the screenshot).
2. GitHub SSH key entry page after the public key is added.
3. Terminal output from `ssh -T git@github.com`.
4. `git remote -v` showing an SSH-style remote.
