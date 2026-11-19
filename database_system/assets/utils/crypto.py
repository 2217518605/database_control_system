from cryptography.fernet import Fernet, InvalidToken
import logging

from django.conf import settings

"""
对称加密
"""

logger = logging.getLogger(__name__)


def cipher_() -> Fernet:
    """ 校验和处理 fernet_key """

    fernet_key = settings.FERNET_KEY
    if not fernet_key:
        raise RuntimeError("Fernet key 没有配置，请进行配置！")
    return Fernet(fernet_key.encode() if isinstance(fernet_key, str) else fernet_key)


def encrypt(plain_text: str) -> str:
    """ 密码加密 """

    return cipher_().encrypt(plain_text.encode("utf-8")).decode("utf-8")


def decrypt(token: str) -> str:
    """ 密码解密 """

    try:
        return cipher_().decrypt(token.encode("utf-8")).decode("utf-8")
    except InvalidToken:
        logger.error("解密失败了：密钥不匹配或损坏，请检查！")
        return ""

def desensitization(token: str) -> str:
    """ 脱敏展示 """

    return "**********" if token else ""