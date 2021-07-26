#!/usr/bin/env python

import subprocess
import optparse
import re

def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change MAC address")
    parser.add_option("-m", "--mac", dest="new_mac", help="New MAC address")
    values,arguments = parser.parse_args()
    if not values.interface:
        parser.error("[-]Please specify interface, use --help for more info")
    elif not values.new_mac:
        parser.error("[-]Please specify MAC address, use --help for more info")
    return values

def change_mac(interface,new_mac):
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])

def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))
    if mac_search_result:
        return mac_search_result.group(0)
    else:
        print("[-] Could not read MAC address")

values = get_arguments()
current_mac = get_current_mac(values.interface)
print("Current MAC address: "+ str(current_mac))
change_mac(values.interface,values.new_mac)
new_mac_address = get_current_mac(values.interface)
if new_mac_address == values.new_mac:
    print("MAC address changed to "+ new_mac_address)
else:
    print("Could not change MAC address")

