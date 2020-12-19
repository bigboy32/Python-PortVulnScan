import socket
import colorama
import argparse

import threading, queue

from socket import *

q = queue.Queue()

colorama.init()

parser = argparse.ArgumentParser()
parser.add_argument("target", type=str)

args = parser.parse_args()

maxport = 500

opn_ports = []

def scan_port(port):
    try:
        s = socket(AF_INET, SOCK_STREAM)
        conn = s.connect((args.target, port))

        opn_ports.append(port)
    
    except KeyboardInterrupt:
        print("[-] ERROR: CTRL-C Detected, Abort... ")
        exit()

    except:
        pass

def generate_url(port):
    return "https://www.speedguide.net/port.php?port=" + str(port)

print("[*] Starting Threads... ")

def threader():
   while True:
      worker = q.get()
      scan_port(worker)
      q.task_done()


for _ in range(100):
    t = threading.Thread(target= threader)
    t.daemon = True
    t.start()


print("[+] Scanning ports ...")
for port in range(maxport):
    q.put(port)

q.join()

if len(opn_ports) < 2:
    print(colorama.Fore.GREEN + "[+] Port "  + opn_ports[0]  + " Potential vulns: " + generate_url(opn_ports[0]) + colorama.Fore.RESET)

elif len(opn_ports) == 0:
    print(colorama.Fore.RED + "[-] The target has no open ports!" + colorama.Fore.RESET)

else:
    for item in opn_ports:
        item = str(item)
        print(colorama.Fore.GREEN + "[+] Port "  + item + colorama.Fore.RESET)
        print("|- ", end="")
        print("[+] Potental Vulns for port {}: ".format(item) + generate_url(item))
        print("|-", end="")

print()
print()
print("[+] Scan Finished!")