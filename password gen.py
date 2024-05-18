import random
import string
import os

os.system("cls" if os.name == "nt" else "clear") #clears terminal before inputting password


def generate_password(
    length=8, lowercase=True, uppercase=True, digits=True, punctuation=True
):
#password string
    all_chars = ""
#makes the password
    if lowercase:
        all_chars += string.ascii_lowercase
    if uppercase:
        all_chars += string.ascii_uppercase
    if digits:
        all_chars += string.digits
    if punctuation:
        all_chars += string.punctuation
#joins the password
    password = "".join(random.sample(all_chars, length))
    return password

#prints the password using parameters length, lowercase, uppercase, digits, and punctuation
password = generate_password(12)
print(password)
