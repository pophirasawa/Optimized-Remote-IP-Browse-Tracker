from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash.SHA256 import SHA256Hash
import base64


class CryptoUtil:
    """
    加密工具,使用AES_CBC
    """

    _instance = None
    _init = False

    def __init__(self, config=None):
        if self._init is True and config is None:
            return

        self._init = True
        if not hasattr(self, "config"):
            self.config = config

        self.key = SHA256Hash(self.config["encodingkey"].encode()).digest()[:16]

    def __new__(cls, *args, **kw):
        if not cls._instance:
            cls._instance = super(CryptoUtil, cls).__new__(cls)
        return cls._instance

    def encode(self, text) -> str | None:
        if not text:
            return
        iv = self.key  # iv偏移量，bytes类型
        byte_text = pad(text.encode("utf-8"), AES.block_size)
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        encrypt_text = aes.encrypt(byte_text)
        return base64.encodebytes(encrypt_text).decode("utf-8")

    def decode(self, encrypt_text) -> str | None:
        if not encrypt_text:
            return encrypt_text

        iv = self.key
        encrypt_text = base64.decodebytes(encrypt_text.encode("utf-8"))
        aes = AES.new(self.key, AES.MODE_CBC, iv)
        text = aes.decrypt(encrypt_text)
        text = unpad(text, AES.block_size)
        return text.decode("utf-8")


def decode_datas(datas):
    res = []
    for data in datas:
        uid = data["uid"]
        name = data["name"]
        ipv4 = CryptoUtil().decode(data["ipv4"])
        ipv6 = CryptoUtil().decode(data["ipv6"])
        extra = data.get("extra")

        decoded_data = {
            "uid": uid,
            "name": name,
            "ipv4": ipv4,
            "ipv6": ipv6,
            "extra": extra,
        }
        res.append(decoded_data)
    return res


if __name__ == "__main__":
    config = {"key": "asd"}
    res = {}
    m = "abcdeasdasdfg"
    a = CryptoUtil(config)
    k = a.encode(m)
    res["a"] = k
    print(res)
