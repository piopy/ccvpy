import hashlib
from os import urandom
from Crypto.Cipher import AES

def gethpassword(password):
    return hashlib.sha256(password.encode()).digest()

def pad(file):
    while len(file)%16 != 0:
        file=file+b'0'
    return file

def encrypt(filein,fileout,password):
    password=gethpassword(password)
    aes = AES.new(password,AES.MODE_CBC,'created by piopy')
    
    with open(filein,'rb') as f, open(fileout,'wb') as dest:
        cifrato=aes.encrypt(pad(f.read()))
        dest.write(cifrato)
    

def decrypt(filein,fileout,password):
    password=gethpassword(password)
    aes = AES.new(password,AES.MODE_CBC,'created by piopy')

    with open(filein,'rb') as f, open(fileout,'wb') as dest:
        decifrato=aes.decrypt(f.read())
        dest.write(decifrato.rstrip(b'0'))