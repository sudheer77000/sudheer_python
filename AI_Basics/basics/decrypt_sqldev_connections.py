# -*- coding: utf-8 -*-
"""Decrypt passwords from Oracle SQL Developer connections.json (v19.2+)."""

import argparse
import base64
import hashlib
import json
import sys

try:
    from Cryptodome.Cipher import AES
except ImportError:
    print("Install dependency: pip install pycryptodomex", file=sys.stderr)
    sys.exit(1)


SALT = bytes([6, 182, 97, 35, 61, 104, 50, 184])


def decrypt_password(encrypted_b64, db_system_id):
    encrypted = base64.b64decode(encrypted_b64)
    iv, ciphertext = encrypted[:16], encrypted[16:]
    key = hashlib.pbkdf2_hmac("sha256", db_system_id.encode(), SALT, 5000, 32)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = cipher.decrypt(ciphertext)
    pad_len = decrypted[-1]
    return decrypted[:-pad_len].decode("utf-8")


def main():
    parser = argparse.ArgumentParser(
        description="Decrypt SQL Developer connections.json passwords"
    )
    parser.add_argument(
        "-f",
        "--file",
        default=r"D:\VS\sudheer_python\sudheer_python\AI_Basics\basics\connections.json",
        help="Path to connections.json",
    )
    parser.add_argument(
        "-d",
        "--db-system-id",
        required=True,
        help="Value of db.system.id from product-preferences.xml",
    )
    args = parser.parse_args()

    with open(args.file, encoding="utf-8") as handle:
        data = json.load(handle)

    print("{:<20} {:<20} {}".format("Connection", "User", "Password"))
    print("-" * 60)
    for conn in data.get("connections", []):
        name = conn.get("name", "")
        info = conn.get("info", {})
        user = info.get("user", "")
        encrypted = info.get("password", "")
        if not encrypted:
            password = "(no password saved)"
        else:
            try:
                password = decrypt_password(encrypted, args.db_system_id)
            except Exception as exc:
                password = "(decrypt failed: {})".format(exc)
        print("{:<20} {:<20} {}".format(name, user, password))


if __name__ == "__main__":
    main()