'''colorama'''

import socket
import threading
import concurrent.futures
import colorama
from colorama import Fore
from urllib.parse import urlparse
print_lock = threading.Lock()
colorama.init()

portsobject = {
    21: 'FTP',
    22: 'SSH',
    23: 'Telnet',
    25: 'SMTP',
    43: 'Whois',
    53: 'DNS',
    68: 'DHCP',
    80: 'HTTP',
    110: 'POP3',
    115: 'SFTP',
    119: 'NNTP',
    123: 'NTP',
    139: 'NetBIOS',
    143: 'IMAP',
    161: 'SNMP',
    220: 'IMAP3',
    389: 'LDAP',
    443: 'SSL',
    1521: 'Oracle SQL',
    2049: 'NFS',
    3306: 'mySQL',
    5800: 'VNC',
    8080: 'HTTP',
}

def run_port(ip):
    domain = urlparse(ip).netloc
    report_file=open("output.txt","w")
    def scan(ip,port):
        scanner=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        scanner.settimeout(1)
        try:
            scanner.connect((ip,port))
            scanner.close()
            with print_lock:
                print(Fore.WHITE+ f"[{port}]" +" " + f"[{portsobject[port]}]" + Fore.GREEN+ " Opened")
                report_file.write(Fore.WHITE+ f"[{port}]" +" " + f"[{portsobject[port]}]" + Fore.GREEN+ " Opened")
        except:
            pass

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        for port in range(1,1000):
            executor.submit(scan,domain,port)
    report_file.close()
