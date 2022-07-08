import requests
import socket
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from os import system, name
from urllib.parse import urlparse

def request(url):
    try:
        response = requests.get(url)
        if response:
                return url
    except requests.exceptions.ConnectionError:
        pass
    except:
        pass

def scan_subdirectory(target_url):
    wordlist_file = open("common.txt").read().strip().split('\n')
    report_file=open("output.txt","w")
    start = time()
    print("\n\nScanning for subdirectory...")
    report_file.write("\n\nScanning for subdirectory...")
    processes = []

    with ThreadPoolExecutor(max_workers=100) as executor:
        for word in wordlist_file:
            processes.append(executor.submit(request, target_url + "/" + word))

    for task in as_completed(processes):
        if task.result()is None:
            pass
        else:
            print("[+] Discovered Subdirectory --> "+task.result())
            report_file.write("[+] Discovered Subdirectory --> "+task.result())

        
    print(f'Time taken: {time() - start}')
    report_file.close()

