"""
Educational blockchain simulator for a cryptography course project.
Demonstrates:
KPub, KPriv, digital signatures, SHA-256 hashing, proof-of-work,
transactions, blocks, and blockchain validation.
"""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, asdict
from typing import List, Optional

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey, Ed25519PublicKey


def sha256_hex(data: bytes | str) -> str:
    """Return a SHA-256 digest in hexadecimal form."""
    if isinstance(data, str):
        data = data.encode("utf-8")
    return hashlib.sha256(data).hexdigest()


class KeyPair:
    """KPriv/KPub pair using Ed25519."""

    def __init__(self) -> None:
        self.k_priv = Ed25519PrivateKey.generate()
        self.k_pub = self.k_priv.public_key()

    def private_key_hex(self) -> str:
        raw = self.k_priv.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        return raw.hex()

    def public_key_hex(self) -> str:
        raw = self.k_pub.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )
        return raw.hex()

    def address(self) -> str:
        """Simple educational wallet address derived from KPub."""
        return sha256_hex(bytes.fromhex(self.public_key_hex()))[:40]


class DigitalSignature:
    """Digital signature helper."""

    @staticmethod
    def sign(k_priv: Ed25519PrivateKey, message: bytes) -> str:
        return k_priv.sign(message).hex()

    @staticmethod
    def verify(k_pub: Ed25519PublicKey, message: bytes, signature_hex: str) -> bool:
        try:
            k_pub.verify(bytes.fromhex(signature_hex), message)
            return True
        except (InvalidSignature, ValueError):
            return False


@dataclass
class Transaction:
    sender: str
    receiver: str
    amount: float
    sender_public_key: str
    signature: Optional[str] = None
    txid: Optional[str] = None

    def signing_payload(self) -> bytes:
        payload = {
            "sender": self.sender,
            "receiver": self.receiver,
            "amount": self.amount,
            "sender_public_key": self.sender_public_key,
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")

    def sign(self, k_priv: Ed25519PrivateKey) -> None:
        self.signature = DigitalSignature.sign(k_priv, self.signing_payload())
        self.txid = sha256_hex(self.signing_payload() + bytes.fromhex(self.signature))

    def is_valid(self) -> bool:
        if not self.signature:
            return False

        try:
            pub_raw = bytes.fromhex(self.sender_public_key)
            k_pub = Ed25519PublicKey.from_public_bytes(pub_raw)
        except ValueError:
            return False

        expected_sender = sha256_hex(pub_raw)[:40]
        if expected_sender != self.sender:
            return False

        return DigitalSignature.verify(k_pub, self.signing_payload(), self.signature)


@dataclass
class Block:
    index: int
    timestamp: float
    transactions: List[Transaction]
    previous_hash: str
    nonce: int = 0
    hash: str = ""

    def calculate_hash(self) -> str:
        data = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [asdict(tx) for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        return sha256_hex(json.dumps(data, sort_keys=True, separators=(",", ":")))

    def mine(self, difficulty: int) -> None:
        """Proof-of-work: find a hash beginning with N zeroes."""
        target = "0" * difficulty
        while True:
            self.hash = self.calculate_hash()
            if self.hash.startswith(target):
                return
            self.nonce += 1


class Blockchain:
    def __init__(self, difficulty: int = 4) -> None:
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.chain: List[Block] = [self._create_genesis_block()]

    def _create_genesis_block(self) -> Block:
        block = Block(
            index=0,
            timestamp=time.time(),
            transactions=[],
            previous_hash="0" * 64,
        )
        block.mine(self.difficulty)
        return block

    @property
    def latest_block(self) -> Block:
        return self.chain[-1]

    def add_transaction(self, tx: Transaction) -> None:
        if not tx.is_valid():
            raise ValueError("Transaction rejected: invalid digital signature or sender identity.")
        self.pending_transactions.append(tx)

    def mine_pending_transactions(self) -> Block:
        block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions.copy(),
            previous_hash=self.latest_block.hash,
        )
        block.mine(self.difficulty)
        self.chain.append(block)
        self.pending_transactions.clear()
        return block

    def is_valid(self) -> bool:
        for i, block in enumerate(self.chain):
            if block.hash != block.calculate_hash():
                return False
            if not block.hash.startswith("0" * self.difficulty):
                return False
            if i > 0 and block.previous_hash != self.chain[i - 1].hash:
                return False
            for tx in block.transactions:
                if not tx.is_valid():
                    return False
        return True

    def to_pretty_json(self) -> str:
        data = []
        for block in self.chain:
            item = asdict(block)
            data.append(item)
        return json.dumps(data, indent=2)


def demo() -> None:
    print("=== Cryptography Course: Blockchain Simulator ===")
    alice = KeyPair()
    bob = KeyPair()

    print("\n[KPriv / KPub]")
    print("Alice KPriv:", alice.private_key_hex())
    print("Alice KPub :", alice.public_key_hex())
    print("Alice addr :", alice.address())
    print("Bob addr   :", bob.address())

    tx = Transaction(
        sender=alice.address(),
        receiver=bob.address(),
        amount=25.0,
        sender_public_key=alice.public_key_hex(),
    )
    tx.sign(alice.k_priv)

    print("\n[Digital Signature]")
    print("Signature valid:", tx.is_valid())
    print("Transaction ID :", tx.txid)

    chain = Blockchain(difficulty=4)
    chain.add_transaction(tx)

    print("\n[Proof of Work]")
    mined = chain.mine_pending_transactions()
    print("Mined block    :", mined.index)
    print("Nonce          :", mined.nonce)
    print("Block hash     :", mined.hash)
    print("Previous hash  :", mined.previous_hash)

    print("\n[Blockchain Validation]")
    print("Blockchain valid:", chain.is_valid())

    print("\n[Blockchain JSON]")
    print(chain.to_pretty_json())


if __name__ == "__main__":
    demo()
