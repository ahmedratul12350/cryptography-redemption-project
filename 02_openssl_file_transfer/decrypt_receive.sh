#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: OPENSSL_PASS='your-lab-passphrase' ./decrypt_receive.sh filename"
  exit 1
fi

if [[ -z "${OPENSSL_PASS:-}" ]]; then
  echo "Set OPENSSL_PASS first."
  exit 1
fi

FILE="$1"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
INPUT="$BASE_DIR/receiver/inbox/$FILE.enc"
OUTPUT="$BASE_DIR/receiver/decrypted/$FILE"

openssl enc -d -aes-256-cbc -pbkdf2 -iter 200000 -md sha256 \
  -in "$INPUT" -out "$OUTPUT" -pass env:OPENSSL_PASS

echo "Decrypted: $OUTPUT"
