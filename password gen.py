import random
import string


def generate_password(
    length=8, lowercase=True, uppercase=True, digits=True, punctuation=True
):

    all_chars = ""

    if lowercase:
        all_chars += string.ascii_lowercase
    if uppercase:
        all_chars += string.ascii_uppercase
    if digits:
        all_chars += string.digits
    if punctuation:
        all_chars += string.punctuation

    password = "".join(random.sample(all_chars, length))
    return password


password = generate_password(8, punctuation=False)
print(password)