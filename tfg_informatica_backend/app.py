import threading
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api import device_bp
from flask_cors import CORS
import asyncio


app = Flask(__name__)
CORS(app)
app.register_blueprint(device_bp, url_prefix='/devices')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


def run_flask_app():
    app.run(debug=True, use_reloader=False)


async def run_async_tasks():
    from services.AsyncTaskManager import AsyncTaskManager
    task_manager = AsyncTaskManager()
    try:
        await asyncio.gather(
            task_manager.monitor_device(10),
            task_manager.monitor_services(20),
        )
    except asyncio.CancelledError:
        print("Cancelled tasks.")
    except KeyboardInterrupt:
        print("Tasks manually interrupted.")


def main():
    from services.DeviceManager import import_devices_from_file
    with app.app_context():
        db.create_all()
        import_devices_from_file(filename="devices", filetype="yaml")

    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()
    asyncio.run(run_async_tasks())


if __name__ == "__main__":
    main()

# cisco_device = {
#    'device_type': 'cisco_xe',
#    'host': '192.168.0.58',
#    'username': 'albert',
#    'password': 'albert',
#    'port': '22'
# }
#
#
# net_connect = ConnectHandler(**cisco_device)
# output = net_connect.send_command("show version")
# print("Answer from router: " + output)
# net_connect.disconnect()

# so = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# so.connect(("8.8.8.8", 80))
# my_ip_addr = so.getsockname()[0]
# print(f"My IP address is {my_ip_addr}")
# subnet = ip_network(my_ip_addr + "/24", False)
# print(subnet)


# devices = [
#     {
#         'hostname': '192.168.0.58',
#         'device_type': 'ios',
#         'username': 'albert',
#         'password': 'albert'
#     },
# ]
# devices_info = []
# for device in devices:
#     driver = get_network_driver(device['device_type'])
#     with driver(device['hostname'], device['username'], device['password'],
#                 optional_args={'secret': 'tu_secret'}) as device_conn:
#         facts = device_conn.get_facts()
#         environment = device_conn.get_environment()
#         device_data = {
#             'hostname': facts['hostname'],
#             'vendor': facts['vendor'],
#             'model': facts['model'],
#             'os_version': facts['os_version'],
#             'serial_number': facts['serial_number'],
#             'uptime': facts['uptime'],
#             'interface_list': facts['interface_list'],
#             'cpu': environment['cpu'],
#             'memory': environment['memory']
#         }
#         devices_info.append(device_data)
# for device in devices_info:
#     print(device)
#
#
# target_ip = "192.168.0.58"
# arp_request = ARP(pdst=target_ip)
# broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
# arp_request_broadcast = broadcast / arp_request
# answered, unanswered = s.srp(arp_request_broadcast, timeout=2, verbose=False)
# if answered:
#     for sent, received in answered:
#         print(f"IP: {received.psrc}, MAC: {received.hwsrc}")
# else:
#     print(f"Device not founded. IP: {target_ip}")
# icmp_request = IP(dst=target_ip) / ICMP()
# response = s.sr1(icmp_request, timeout=2, verbose=False)
# if response:
#     print(f"IP: {response.src}, ICMP: {response.summary()}")
# else:
#     print(f"Device not founded. IP: {target_ip}")

# def found_devices(ip_range):
#     arp_packet = ARP(pdst=ip_range)
#     broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
#     packet = broadcast / arp_packet
#     ans, _ = s.srp(packet, timeout=2, verbose=0)
#     founded_devices = []
#     for _, receive in ans:
#         founded_devices.append((receive.psrc, receive.hwsrc))
#     return founded_devices


# def found_devices_icmp(ip_range):
#     icmp_packet = IP(dst=ip_range)/ICMP()
#     ans, _ = s.sr(icmp_packet, timeout=2, verbose=0)
#     founded_devices = []
#     for sent, received in ans:
#         if received.type == 0:
#             founded_devices.append((sent.dst, received.src))
#     return founded_devices
#
#
# ip_range = "192.168.0.0/24"
# devices = found_devices(ip_range)
# print("Founded devices:")
# for ip, mac in devices:
#     print(f"IP: {ip}, MAC: {mac}")


# def procesar_paquete(paquete):
#    if paquete.haslayer(ARP):
#        if paquete[ARP].op == 2:  # Es una respuesta ARP
#            print(f"IP: {paquete[ARP].psrc}, MAC: {paquete[ARP].hwsrc}")
#
#
# sniff(filter="arp", prn=procesar_paquete, store=False, count=10)

# s.show_interfaces()
# print("\n--------Packet summaries--------\n")
# capture = s.sniff(iface='VirtualBox Host-Only Ethernet Adapter', count=10)
# print(capture.nsummary())
#
# print("\n--------Discovery hosts on network using arping() function--------\n")
# ans, unans = s.arping("192.168.0.0/24")
# ans.summary()
#
# for res in ans.res:
#     print(f"---> IP address discovered: {res[0].payload.pdst}")


# print("\n--------Discovery hosts on network using icmp ping--------\n")
# ip_range = "192.168.0.0/24"
# network = IPNetwork(ip_range)
# for ip in network:
#     print(f"Scanning IP: {ip}")
#     packet = IP(dst=str(ip)) / ICMP()
#     ans, unans = s.sr(packet, timeout=2, verbose=False)
#     if ans:
#         print(f"ANSWER RECEIVED FROM {ip}")
#         ans.summary()
#     else:
#         print(f"No answer from {ip}")

# print("\n--------See what ports are open on a device----------------")
# while True:
#     ip = input("Enter IP address: ")
#     if not ip:
#         print("\n------Ending port scanning")
#         break
#
#     ans, unans = s.sr(IP(dst=ip)/TCP(flags="S", sport=666, dport=(1, 1024)), timeout=10)
#     for answered in ans:
#         print(f"---> open port {answered[0].summary()}")
#
#     print("\n--------Open/Closed ports totals----------")
#     print(f"\tOpen ports: {len(ans)}")
#     print(f"\tClosed ports: {len(unans)}")

# nm = nmap.PortScanner()


# while True:
#     ip = input("\n Enter the IP to scan:")
#     if not ip:
#         break
#
#     print(f"\nScanning {ip}")
#     output = nm.scan(ip, '1-1024', arguments="-sS -sU -O --host-timeout 600")
#     print(f"--- --- command: {nm.command_line()}")
#
#     print(f"----- nmap scan output -----")
#     pprint(output)
#
#     try:
#         pprint(nm[ip].all_tcp())
#         pprint(nm[ip].all_udp())
#         pprint(nm[ip].all_udp())
#     except KeyError as e:
#         print(f"   ---> failed to get scan results for {ip}")
#
# print("\nExiting nmap scanner")
#
#
# print("\nScanning all hosts in subnet using port 80")
# nm.scan("192.168.0.0/24", arguments="-p 80 -open")
# print("--- Iterating hosts with open port 80 (ssh)")
# for host in nm.all_hosts():
#     print("--- --- ", host)
#
#
# print("\nScanning all hosts in subnet using ICMP")
# nm.scan("192.168.0.0/24", arguments="-PE")
# print("--- Iterating hosts responding to ICMP echo")
# for host in nm.all_hosts():
#     print("--- --- ", host)
#

# def discovered_host(found_host, scan_result):
#     if scan_result['nmap']['scanstats']['uphosts'] == '1':
#         print(f"Found host: {found_host} Scan: {scan_result['nmap']['scanstats']}")
#
#
# nma = nmap.PortScannerAsync()
# print("\nScanning all hosts in subnet using ICMP with callback")
# nma.scan("192.168.0.0/24", arguments="-PE", callback=discovered_host)
# print("--- Iterating hosts responding to ICMP echo")
# while nma.still_scanning():
#     nma.wait(5)

