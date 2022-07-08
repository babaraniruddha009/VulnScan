import requests
import time
import urllib3
import sys


version = 2.2

def parse_url(url):
    try:
        host = urllib3.util.url.parse_url(url).host
    except Exception as e:
        print('[*] Invalid domain, try again..')
        sys.exit(1)
    return host

def write_subs_to_file(subdomain, output_file):
    with open(output_file, 'a') as fp:
        fp.write(subdomain + '\n')
        fp.close()


def run_subdomain(target_url):
    subdomains = []
    target = parse_url(target_url)
    output = "output.txt"

    req = requests.get(f'https://crt.sh/?q=%.{target}&output=json')

    if req.status_code != 200:
        print('[*] Information not available!')
        sys.exit(1)

    for (key,value) in enumerate(req.json()):
        subdomains.append(value["name_value"])

    print(f"\n[!] ****** TARGET: {target} ****** [!] \n")


    subs = subdomains

    for s in subs:
        print(f'[+] Discovered Subdomain --> {s}\n')
        if output is not None:
            write_subs_to_file(s, output)

    print("\n\n[**] Scan completed, all subdomains have been found.\n\n")

