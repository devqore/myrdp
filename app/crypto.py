# -*- coding: utf-8 -*-
import base64
import os
from Cryptodome.Cipher import PKCS1_OAEP
from Cryptodome.PublicKey import RSA


class CryptoKey(object):
    def __init__(self, key=None, passphrase=None):
        if key:
            self.key = self.importKey(key, passphrase)
        else:
            self.key = self.generateKey()

    @staticmethod
    def generateKey():
        return RSA.generate(2048)

    @staticmethod
    def getProcessedPassphrase(passphrase):
        if passphrase == '' or not passphrase:
            return None
        return passphrase.encode('utf8')

    def export(self, passphrase=None):
        passphrase = self.getProcessedPassphrase(passphrase)
        return self.key.exportKey(passphrase=passphrase, pkcs=8)

    def importKey(self, key, passphrase):
        passphrase = self.getProcessedPassphrase(passphrase)
        try:
            self.key = RSA.importKey(key, passphrase)
        except ValueError:
            raise ValueError("Wrong current password")
        return self.key

    def encrypt(self, message):
        cipher = PKCS1_OAEP.new(self.key)
        if isinstance(message, str):
            message = message.encode('utf8')
        encryptedMessage = cipher.encrypt(message)
        return base64.b64encode(encryptedMessage)

    def decrypt(self, encryptedMessage):
        cipher = PKCS1_OAEP.new(self.key)
        if encryptedMessage is None:
            return None
        decryptedMessage = cipher.decrypt(base64.b64decode(encryptedMessage))
        if isinstance(decryptedMessage, (bytes, bytearray)):
            decryptedMessage = decryptedMessage.decode('utf8')
        return decryptedMessage

    def load(self, filePath, passphrase=None):
        with open(filePath, 'rb') as f:
            fileContent = f.read()
        return self.importKey(fileContent, passphrase)

    def save(self, filePath, passphrase=None):
        keyContent = self.export(passphrase)
        with open(filePath, 'wb') as f:
            f.write(keyContent)
            os.chmod(filePath, 0o600)
        return keyContent
