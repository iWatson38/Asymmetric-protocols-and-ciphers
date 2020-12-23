
class DH_Endpoint():
    def __init__(self, public_key1, public_key2, private_key):
        self.public_key1 = public_key1
        self.public_key2 = public_key2
        self.private_key = private_key
        self.full_key = None

    def generate_partial_key(self):
        partial_key = self.public_key1 ** self.private_key
        partial_key = partial_key % self.public_key2
        return partial_key

    def generate_full_key(self, partial_key_r):
        full_key = partial_key_r ** self.private_key
        full_key = full_key % self.public_key2
        self.full_key = full_key
        return full_key

    def encrypt_message(self, message):
        encrypted_message = ""
        key = self.full_key
        for c in message:
            encrypted_message += chr(ord(c) + key)
        return encrypted_message

    def decrypt_message(self, encrypted_message):
        decrypted_message = ""
        key = self.full_key
        for c in encrypted_message:
            decrypted_message += chr(ord(c) - key)
        return decrypted_message


X = int(input("Введите число возводимое в степень "))
s_private = int(input("Введите ваш секретный ключ пользователь 1!"))
Z = int(input("Введите ваш mod "))


def pow_mod(x, y, z):
    number = 1
    while y:
        if y & 1:
            number = number * x % z
        y >>= 1
        x = x * x % z
        print("Число", number)
        print("Х", x)
    return number


print("Наше число ", pow_mod(X, s_private, Z))

m_private = int(input("Введите ваш секретный ключ пользователь 2!"))
print("Наше число ", pow_mod(X, m_private, Z))


message = (input("Введите ваше сообщение!"))
s_public = pow_mod(X, s_private, Z)
m_public = pow_mod(X, m_private, Z)

Sender = DH_Endpoint(s_public, m_public, s_private)
Recipient = DH_Endpoint(s_public, m_public, m_private)

s_partial = Sender.generate_partial_key()
print("Ключ для формироания секретного ключа получателя: ",pow_mod(X, m_private, Z))

m_partial = Recipient.generate_partial_key()
print("Ключ для формироания секретного ключа отправителя: ",pow_mod(X, s_private, Z))

s_full = Sender.generate_full_key(m_partial)
print("Общий ключ",s_full)

m_full = Recipient.generate_full_key(s_partial)
print("Общий ключ",m_full)

m_encrypted = Recipient.encrypt_message(message)
print("Зашифрованное сообщение: ",m_encrypted)

message = Sender.decrypt_message(m_encrypted)
print("Расшифрованное сообщение: ",message)
