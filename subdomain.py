import requests
import socket
import threading
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor, as_completed
from time import time
from os import system, name

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

def request(url):
        try:
            response = requests.get(url,timeout=1)
            if response:
                return url
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.InvalidURL:
            pass
        except requests.exceptions.Timeout:
            pass
        except: 
            pass
    
def run_subdomain(target_url):

    wordlist_file = open("subdomains_list_1.txt").read().strip().split('\n')

    start = time()
    print("Scanning for subdomains...")
    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        for url in wordlist_file:
            processes.append(executor.submit(request, url+"."+target_url))

    for task in as_completed(processes):
        if task.result()is None:
            pass
        else:
            print("[+] Discovered Subdomain --> "+task.result())

        
    print(f'Time taken: {time() - start}')




    
