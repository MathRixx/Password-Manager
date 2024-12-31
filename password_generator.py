import random

# Büyük harfler (A-Z)
capital_characters = [chr(i) for i in range(65, 91)]

# Küçük harfler (a-z)
lower_characters = [chr(i) for i in range(97, 123)]

# Rakamlar (0-9)
number_characters = [chr(i) for i in range(48, 58)]

# Özel karakterler
special_characters = [
    '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '=', '+',
    '[', ']', '{', '}', '|', '\\', ':', ';', '"', "'", '<', '>', ',', '.', '?', '/'
]

def password_generate():
    global sifre
    sifre = ""

    # Her türden en az 3 karakter ekle
    for _ in range(3):
        sifre += random.choice(capital_characters)
        sifre += random.choice(lower_characters)
        sifre += random.choice(number_characters)
        sifre += random.choice(special_characters)

    # Parolayı karıştırarak rastgele bir sıraya koy
    sifre = ''.join(random.sample(sifre, len(sifre)))

    return sifre
