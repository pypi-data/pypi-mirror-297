import json
from binascii import hexlify, unhexlify
from logging import getLogger


try:
    # pycryptodomex
    from Cryptodome.Cipher import AES
except ImportError as e:
    # pycrypto + pycryptodome
    try:
        from Crypto.Cipher import AES
    except:
        AES = None

LOG = getLogger("BUS")


class Encryption:
    def __init__(self, key=None):
        if not key:
            from chatterbox_bus_client.conf import get_bus_config
            conf = get_bus_config()
            key = conf.get("secret_key")
        if key is not None and not isinstance(key, bytes):
            key = bytes(key[-16:], encoding="utf-8")
        self._key = key

    @property
    def encryption_key(self):
        return self._key

    def encrypt(self, text, nonce=None):
        if AES is None:
            raise ImportError("install pycryptodomex")
        if isinstance(text, dict):
            text = json.dumps(text, separators=(',', ':'))
            # should be equivalent to javascript JSON.stringify since both retain key order, TODO verify this statement
        if not isinstance(text, bytes):
            text = bytes(text, encoding="utf-8")
        cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce=nonce)
        ciphertext, tag = cipher.encrypt_and_digest(text)
        return ciphertext, tag, cipher.nonce

    def decrypt(self, ciphertext, tag, nonce):
        if AES is None:
            raise ImportError("install pycryptodomex")
        try:
            cipher = AES.new(self.encryption_key, AES.MODE_GCM, nonce)
            data = cipher.decrypt_and_verify(ciphertext, tag)
            text = data.decode(encoding="utf-8")
            try:
                text = json.loads(text, encoding="utf-8")
            except:
                pass  # not a dict
            return text
        except ValueError:
            LOG.error("decryption failed")
            return None

    def encrypt_as_dict(self, data, nonce=None):
        ciphertext, tag, nonce = self.encrypt(data, nonce=nonce)
        return {"ciphertext": hexlify(ciphertext).decode('utf-8'),
                "tag": hexlify(tag).decode('utf-8'),
                "nonce": hexlify(nonce).decode('utf-8')}

    def decrypt_from_dict(self, data):
        ciphertext = unhexlify(data["ciphertext"])
        if data.get("tag") is None:  # web crypto
            ciphertext, tag = ciphertext[:-16], ciphertext[-16:]
        else:
            tag = unhexlify(data["tag"])
        nonce = unhexlify(data["nonce"])
        return self.decrypt(ciphertext, tag, nonce)
