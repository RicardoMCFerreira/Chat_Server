from cryptography.fernet import Fernet

chave = b'esrcbflqcN2ZswcFnAbr-T3n0bFsKpnsogYrfa4u0fk='
fernet = Fernet(chave)


# Encripta o email e a password do utilizador
def value_encrypto(valor):
    return (fernet.encrypt(valor.encode('utf-8')))


# Desincripta o email e a password do utilizador
def value_decrypto(valor):
    return (fernet.decrypt(valor).decode('utf-8'))
