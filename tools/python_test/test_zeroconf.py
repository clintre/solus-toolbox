import time
from zeroconf import ServiceBrowser, ServiceListener, Zeroconf

class MyListener(ServiceListener):
    def update_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} updated")

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def add_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        print(f"Service {name} added, service info: {info}")

def main():
    print("Starting zeroconf service browser...")
    zeroconf = Zeroconf()
    listener = MyListener()
    
    # Browse for standard HTTP services (like local web interfaces or printers)
    browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
    
    try:
        # Listen for 5 seconds
        time.sleep(5)
    finally:
        print("Closing zeroconf...")
        zeroconf.close()

if __name__ == '__main__':
    main()
