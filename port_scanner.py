import socket
import threading
from datetime import datetime

print("Starting scan...")
print("Time:", datetime.now())

common_ports = {
     21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    443: "HTTPS",
    3306: "MySQL",
    8080: "HTTP-Proxy"
}

target = input("Enter target: ")
try:
    target_ip = socket.gethostbyname(target)
except socket.gaierror:
    print("❌ Invalid target")
    exit()

print("Scanning:", target_ip)

open_ports = []

def scan_port(port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target_ip, port))

        if result == 0:
            service = common_ports.get(port, "Unknown")
            print(f"[OPEN] Port {port} -> {service}")
            open_ports.append(port)

        sock.close()

    except:
        pass

threads = []

for port in range(1, 1025):
    t = threading.Thread(target=scan_port, args=(port,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print(f"\nTotal Open Ports: {len(open_ports)}")