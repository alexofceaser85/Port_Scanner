#!/usr/bin/env python3
"""
The utilities class for the project, this class is responsible for checking if ports are open or not
"""

import socket
import multiprocessing

__author__ = "Alex DeCesare"
__version__ = "21-Nov-2020"

def check_open_port(ip_address, port, all_ports):

    """
    Checks if a given port with a given ip address is open or closed
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex((ip_address, port)):
        all_ports[str(port)] = False
    else:
        all_ports[str(port)] = True

def scan(ip_address, start_port, end_port):

    """
    Accepts an ip address, start port, and end port and add each port to the PORTS directory
    with a boolean True if the port is open and False if the port is closed
    """
    manager = multiprocessing.Manager()
    ports = manager.dict()

    list_of_processes = []

    for port in range(start_port, end_port):

        process = multiprocessing.Process(target=check_open_port, args=(ip_address, port, ports))
        list_of_processes.append(process)
        process.start()

    for scan_process in list_of_processes:
        scan_process.join()

    return dict(ports)
