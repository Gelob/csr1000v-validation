from napalm import get_network_driver
import json
import time
from pprint import pprint

driver = get_network_driver("ios")

devices = ["csr1"]

for device in devices:
    if device == "csr1":
        ip0 = "10.10.12.2"
        ip1 = "10.10.13.3"
    elif device == "csr2":
        ip0 = "10.10.12.1"
        ip1 = "10.10.23.3"
    elif device == "csr3":
        ip0 = "10.10.13.1"
        ip1 = "10.10.23.2"
    print("Connecting to {}".format(device))
    csr = driver(hostname=device, username="ntc", password="ntc123")
    csr.open()
    print("Connected to {} successfully".format(device))
    csr.load_merge_candidate(filename=device + "_intf.cfg")
    print("Staged new configuration, prepare to see a configuration diff")
    diffs = csr.compare_config()
    pprint(diffs)
    print("Commiting configuration changes")
    csr.commit_config()
    print("Configuration commited successfully")
    print("Verifying L2 Reachability to {} and {} via ping".format(ip0, ip1))
    ping1 = csr.ping(ip0)
    ping2 = csr.ping(ip1)
    if ping1["success"]["packet_loss"] == 0 and ping2["success"]["packet_loss"] == 0:
        print("L2 Reachability confirmed, proceeding with BGP configuration")
    else:
        print(
            "L2 Reachability not confirmed, please resolve the issue and re-run the script"
        )
        pprint(ping1["success"])
        pprint(ping2["success"])
        csr.close()
        print("Closed connection to {}".format(device))
        quit()
    csr.load_merge_candidate(filename=device + "_bgp.cfg")
    print("Staged new configuration, prepare to see a configuration diff")
    diffs = csr.compare_config()
    pprint(diffs)
    print("Commiting configuration changes")
    csr.commit_config()
    print("Configuration commited successfully")
    time.sleep(5)
    bgp = csr.get_bgp_neighbors()
    if bgp["global"]["peers"]["" + ip0 + ""]["is_up"] == True:
        print("BGP for {} is up".format(ip0))
    else:
        print("BGP for {} is down".format(ip0))
    if bgp["global"]["peers"]["" + ip1 + ""]["is_up"] == True:
        print("BGP for {} is up".format(ip1))
    else:
        print("BGP for {} is down".format(ip1))
    csr.close()
    print("Closed connection to {}\nAll done!".format(device))
