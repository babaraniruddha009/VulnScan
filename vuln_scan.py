# !usr/bin/env python3

from urllib import response

import requests
import scanner
import re
import subdirectory as subdir
import sys
import socket
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from os import system, name
import errorsql as ErrorSQL
from operator import is_
import urllib.parse as urlparse
from bs4 import BeautifulSoup
import port as pt
import subdomaincrt as subdomain
import subdomain as subdm

def submit_form(form, value, url):
    action = form.get("action")
    post_url = urlparse.urljoin(url, action)
    method = form.get("method")
    inputs_list = form.findAll("input")
    post_data = {}
    for input in inputs_list:
        input_name = input.get("name")
        input_type = input.get("type")
        input_value = input.get("value")
        if input_type == "text":
            input_value = value
        post_data[input_name] = input_value
    if method == "post":
        return requests.post(post_url, data=post_data)
    return requests.get(post_url, params=post_data)

def reset_database(target_url):
    url = target_url+"setup.php"
    response = requests.get(url)
    parsed_html = BeautifulSoup(response.text)
    forms = parsed_html.findAll("form")
    for form in forms:
        abc = submit_form(form,"",url)

report_file=open("output.txt","w")
print(".....Welcome to VulnScan.....\n\n")

target_url=input("Enter URL : ")
report_file.write("Scanning for "+target_url)
report_file.close()
links_to_ignore = [target_url+"logout.php"]
data_direct = {"username": "admin", "password": "password", "Login": "submit"}
vuln_scanner = scanner.Scanner(target_url, links_to_ignore)
vuln_scanner.session.post(target_url+"login.php", data=data_direct)



# forms = vuln_scanner.extract_froms("http://192.168.0.108/dvwa/vulnerabilities/xss_r/")
# # print(forms)
# reponse = vuln_scanner.test_xss_in_link("http://192.168.0.108/dvwa/vulnerabilities/xss_r/?name=test")
# print(reponse)

pt.run_port(target_url)
#subdir.scan_subdirectory(target_url)
#subdm.run_subdomain(target_url)
reset_database(target_url)
vuln_scanner.crawl(target_url)
vuln_scanner.run_scanner()
reset_database(target_url)
vuln_scanner.run_sql_scanner()
reset_database(target_url)
ErrorSQL.error_func()
reset_database(target_url)
