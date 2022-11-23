#!/usr/bin/env python3
# The socket module in Python is an interface to the Berkeley sockets API.
# We import the ipaddress module. We want to use the ipaddress.ip_address(address)
# method to see if we can instantiate a valid ip address to test.
import ipaddress
# We need to create regular expressions to ensure that the input is correctly formatted.
import re
import socket

import pandas as pd


def port_desc(port_num: int):
    ports = [{'Port Number': 1, 'Description': 'TCP\xa0Port Service Multiplexer (TCPMUX)'},
             {'Port Number': 5, 'Description': 'Remote Job Entry (RJE)'}, {'Port Number': 7, 'Description': 'CHO'},
             {'Port Number': 18, 'Description': 'Message Send Protocol (MSP)'},
             {'Port Number': 20, 'Description': 'FTP\xa0— Data'}, {'Port Number': 21, 'Description': 'FTP — Control'},
             {'Port Number': 22, 'Description': 'SSH\xa0Remote Login Protocol'},
             {'Port Number': 23, 'Description': 'Telnet'},
             {'Port Number': 25, 'Description': 'Simple Mail Transfer Protocol\xa0(SMTP)'},
             {'Port Number': 29, 'Description': 'MSG ICP'}, {'Port Number': 37, 'Description': 'Time'},
             {'Port Number': 42, 'Description': 'Host Name Server (Nameserv)'},
             {'Port Number': 43, 'Description': 'WhoIs'},
             {'Port Number': 49, 'Description': 'Login Host Protocol (Login)'},
             {'Port Number': 53, 'Description': 'Domain Name System\xa0(DNS)'},
             {'Port Number': 69, 'Description': 'Trivial File Transfer Protocol\xa0(TFTP)'},
             {'Port Number': 70, 'Description': 'Gopher\xa0Services'}, {'Port Number': 7, 'Description': 'Finger'},
             {'Port Number': 80, 'Description': 'HTTP'}, {'Port Number': 103, 'Description': 'X.400\xa0Standard'},
             {'Port Number': 108, 'Description': 'SNA Gateway Access Server'},
             {'Port Number': 109, 'Description': 'POP2'}, {'Port Number': 110, 'Description': 'POP3'},
             {'Port Number': 115, 'Description': 'Simple File Transfer Protocol (SFTP)'},
             {'Port Number': 118, 'Description': 'SQL\xa0Services'},
             {'Port Number': 119, 'Description': 'Newsgroup (NNTP)'},
             {'Port Number': 137, 'Description': 'NetBIOS\xa0Name Service'},
             {'Port Number': 139, 'Description': 'NetBIOS Datagram Service'},
             {'Port Number': 143, 'Description': 'Interim Mail Access Protocol (IMAP)'},
             {'Port Number': 150, 'Description': 'NetBIOS Session Service'},
             {'Port Number': 156, 'Description': 'SQL Server'}, {'Port Number': 161, 'Description': 'SNMP'},
             {'Port Number': 179, 'Description': 'Border Gateway Protocol\xa0(BGP)'},
             {'Port Number': 190, 'Description': 'Gateway Access Control Protocol (GACP)'},
             {'Port Number': 194, 'Description': 'Internet Relay Chat\xa0(IRC)'},
             {'Port Number': 197, 'Description': 'Directory Location Service (DLS)'},
             {'Port Number': 389, 'Description': 'Lightweight Directory Access Protocol\xa0(LDAP)'},
             {'Port Number': 396, 'Description': 'Novell Netware over IP'},
             {'Port Number': 443, 'Description': 'HTTPS'},
             {'Port Number': 444, 'Description': 'Simple Network Paging Protocol (SNPP)'},
             {'Port Number': 445, 'Description': 'Microsoft-DS'},
             {'Port Number': 458, 'Description': 'Apple\xa0QuickTime'},
             {'Port Number': 546, 'Description': 'DHCP\xa0Client'}, {'Port Number': 547, 'Description': 'DHCP Server'},
             {'Port Number': 563, 'Description': 'SNEWS'}, {'Port Number': 569, 'Description': 'MSN'},
             {'Port Number': 1080, 'Description': 'Socks'}]
    for port in ports:
        if port_num == port['Port Number']:
            return port['Description']
        else:
            return "No Known Description"


def port_scanner(ip: str, port_range: str):
    # Regular Expression Pattern to extract the number of ports you want to scan.
    # You have to specify <lowest_port_number>-<highest_port_number> (ex 10-100)
    port_range_pattern = re.compile("([0-9]+)-([0-9]+)")
    # Initialising the port numbers, will be using the variables later on.
    port_min = 0
    port_max = 65535

    # This script uses the socket api to see if you can connect to a port on a specified ip address.
    # Once you've successfully connected a port is seen as open.
    # This script does not discriminate the difference between filtered and closed ports.

    # Basic user interface header

    open_ports = []

    # Ask user to input the ip address they want to scan.
    while True:
        ip_add_entered = ip
        # If we enter an invalid ip address the try except block will go to the except block and say you entered an
        # invalid ip address.
        try:
            ip_address_obj = ipaddress.ip_address(ip_add_entered)
            # The following line will only execute if the ip is valid.
            print("You entered a valid ip address.")
            break
        except:
            print("You entered an invalid ip address")

    while True:

        # You can scan 0-65535 ports. This scanner is basic and doesn't use multithreading so scanning all
        # the ports is not advised.
        # print("Please enter the range of ports you want to scan in format: <int>-<int> (ex would be 60-120)")
        # port_range = input("Enter port range: ")

        # We pass the port numbers in by removing extra spaces that people sometimes enter.
        # So if you enter 80 - 90 instead of 80-90 the program will still work.
        port_range_valid = port_range_pattern.search(port_range.replace(" ", ""))
        if port_range_valid:
            # We're extracting the low end of the port scanner range the user want to scan.
            port_min = int(port_range_valid.group(1))

            # We're extracting the upper end of the port scanner range the user want to scan.
            port_max = int(port_range_valid.group(2))
            break

    # Basic socket port scanning
    for port in range(port_min, port_max + 1):

        # Connect to socket of target machine. We need the ip address and the port number we want to connect to.
        try:
            # Create a socket object
            # You can create a socket connection similar to opening a file in Python.
            # We can change the code to allow for domain names as well.
            # With socket.AF_INET you can enter either a domain name or an ip address,
            # and it will then continue with the connection.
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                # You want to set a timeout for the socket to try and connect to the server.
                # If you make the duration longer it will return better results.
                # We put it at 0.5s. So for every port it scans it will allow 0.5s
                # for a successful connection.
                s.settimeout(0.5)
                # We use the socket object we created to connect to the ip address we entered and the port number.
                # If it can't connect to this socket it will cause an exception and the open_ports list will not
                # append the value.
                s.connect((ip_add_entered, port))
                # If the following line runs then it was successful in connecting to the port.
                open_port = {
                    'Ip Address': ip_add_entered,
                    'Open Port': port,
                    'Description': port_desc(int(port))
                }
                open_ports.append(open_port)

        except:
            # We don't need to do anything here. If we were interested in the closed ports we'd put something here.
            pass

    # We only care about the open ports.
    # for port in open_ports:
    #     # We use an f string to easily format the string with variables so we don't have to do concatenation.
    #     print(f"Port {port} is open on {ip_add_entered}.")

    df = pd.DataFrame(open_ports)

    return df

# print(port_scanner("104.223.100.109","0-500"))
