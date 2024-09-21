from scapy.all import IP, ICMP, sr1

class NetworkTool:
    def ping(self, ip, time=3):
        try:
            print("Pinging the target....")
            icmp = IP(dst=ip) / ICMP()
            resp = sr1(icmp, timeout=time, verbose=False)  
            if resp is None:
                print("This host is down")
            else:
                print("This host is up")
        except Exception as e:
            print(f"This host is unreachable: {e}")
