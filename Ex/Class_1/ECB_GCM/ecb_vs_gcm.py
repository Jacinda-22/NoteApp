import os
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import padding

KEY = os.urandom(32)
BLOCK = 16


def load_image_bytes(path):
    img = Image.open(path).convert("RGB")
    return img, img.tobytes()


def bytes_to_image(data, size):
    return Image.frombytes("RGB", size, data)


def pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()


def unpad(data):
    unpadder = padding.PKCS7(128).unpadder()
    return unpadder.update(data) + unpadder.finalize()


def encrypt_ecb(data, key):
    data = pad(data)
    cipher = Cipher(algorithms.AES(key), modes.ECB())
    enc = cipher.encryptor()
    return enc.update(data) + enc.finalize()


def encrypt_gcm(data, key):
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, data, None)
    return nonce + ct


if __name__ == "__main__":
    img, raw = load_image_bytes("input.png")
    print("Image size:", img.size, "bytes:", len(raw))

    ecb_ct = encrypt_ecb(raw, KEY)
    ecb_img = bytes_to_image(ecb_ct[:len(raw)], img.size)
    ecb_img.save("output_ecb.png")

    gcm_ct = encrypt_gcm(raw, KEY)
    gcm_img = bytes_to_image(gcm_ct[:len(raw)], img.size)
    gcm_img.save("output_gcm.png")

    print("Saved output_ecb.png and output_gcm.png")