#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: OPENSSL_PASS='your-lab-passphrase' ./encrypt_send.sh filename"
  exit 1
fi

if [[ -z "${OPENSSL_PASS:-}" ]]; then
  echo "Set OPENSSL_PASS first. Example: export OPENSSL_PASS='CourseDemoPass123!'"
  exit 1
fi

FILE="$1"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUT="$BASE_DIR/sender/plaintext/$FILE"
ENCRYPTED="$BASE_DIR/sender/encrypted/$FILE.enc"
INBOX="$BASE_DIR/receiver/inbox/$FILE.enc"

openssl enc -aes-256-cbc -salt -pbkdf2 -iter 200000 -md sha256 \
  -in "$INPUT" -out "$ENCRYPTED" -pass env:OPENSSL_PASS

cp "$ENCRYPTED" "$INBOX"
echo "Encrypted: $ENCRYPTED"
echo "Transferred to receiver inbox: $INBOX"
