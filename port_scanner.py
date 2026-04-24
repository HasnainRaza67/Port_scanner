import socket
from concurrent.futures import ThreadPoolExecutor

# CONFIG

TIMEOUT = 1
MAX_THREADS = 100

# Common ports and services
COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}


# BANNER GRABBING

def grab_banner(sock):
    try:
        sock.settimeout(1)
        banner = sock.recv(1024).decode().strip()
        return banner
    except:
        return None



# SCAN SINGLE PORT

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(TIMEOUT)

        result = sock.connect_ex((target, port))

        if result == 0:
            service = COMMON_PORTS.get(port, "Unknown")

            banner = None
            try:
                banner = grab_banner(sock)
            except:
                pass

            print(f"[OPEN] Port {port} ({service})")

            if banner:
                print(f"       Banner: {banner}")

        sock.close()

    except Exception as e:
        pass



# MAIN SCANNER

def port_scanner(target, start_port, end_port):
    print(f"\n🔍 Scanning target: {target}")
    print(f"Port range: {start_port} - {end_port}\n")

    try:
        target_ip = socket.gethostbyname(target)
    except:
        print("❌ Could not resolve host")
        return

    print(f"Resolved IP: {target_ip}\n")

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        for port in range(start_port, end_port + 1):
            executor.submit(scan_port, target_ip, port)



# RUN PROGRAM

if __name__ == "__main__":
    target = input("Enter target (IP or domain): ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    port_scanner(target, start_port, end_port)