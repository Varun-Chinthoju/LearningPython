import random
import string
import os

# first checks if
os.system(
    "cls" if os.name == "nt" else "clear"
)  # clears terminal before inputting password


def generate_password(
    length=8, lowercase=True, uppercase=True, digits=True, punctuation=True
):
    # password string
    all_chars = ""
    # makes the password
    if lowercase:
        all_chars += string.ascii_lowercase
    if uppercase:
        all_chars += string.ascii_uppercase
    if digits:
        all_chars += string.digits
    if punctuation:
        all_chars += string.punctuation
    # joins the password
    password = "".join(random.sample(all_chars, length))
    return password


# asks user if they want to generate a password until they deny
while True:
    response = input("Would you like to generate a password? (yes/no): ")
    if response.lower() == "yes":
        password = generate_password(12)
        print(password)
    elif response.lower() == "no":
        exit()
    else:
        print("Invalid response. Please enter 'yes' or 'no'.")
        continue
