# Script is taken from /mo/gbc_mo/scripts in order to be independent on MO future changings

import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES
from typing import Union


def pad(s: str) -> str:
    bs = AES.block_size
    return s + (bs - len(s) % bs) * chr(bs - len(s) % bs)


def unpad(s: Union[str, bytes]) -> Union[str, bytes]:
    return s[: -ord(s[-1:])]


def get_key() -> bytes:
    with open(".key", "rb") as key_file:
        key = key_file.read()
        return hashlib.sha256(str(key).encode()).digest()


def encrypt(text: str) -> str:
    raw = pad(text)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(get_key(), AES.MODE_CBC, iv)
    return base64.b64encode(iv + cipher.encrypt(raw.encode())).decode("utf-8")


def decrypt(text: str) -> str:
    enc = base64.b64decode(text)
    iv = enc[: AES.block_size]
    cipher = AES.new(get_key(), AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(enc[AES.block_size :])).decode("utf-8")


ENCRYPT = "encrypt"
DECRYPT = "decrypt"

MAP_FUNC = {ENCRYPT: encrypt, DECRYPT: decrypt}


def main(action: str) -> None:
    passwd = input(f"Input password to {action}:")
    print(f"{action.capitalize()}ed password: ")
    print(MAP_FUNC[action](passwd))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Encrypt-decrypt passwords")
    parser.add_argument(
        "--action",
        type=str,
        choices=[ENCRYPT, DECRYPT],
        required=True,
        help="Enter action",
    )
    cmdline = parser.parse_args()

    main(cmdline.action)
