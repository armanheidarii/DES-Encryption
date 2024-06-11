from pkg.des import DES

last_name = "Cham Heidari"
pt = DES.get_16_hex(last_name)
key = "6265686573687469"


print("Encryption")
cipher_text = DES.bin2hex(DES.encrypt(pt, key, log=True))
print("Cipher Text: ", cipher_text)

print("Decryption")
text = DES.bin2hex(DES.decrypt(cipher_text, key, log=True))
print("Plain Text: ", text)
