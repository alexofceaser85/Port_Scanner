#!/usr/bin/env python3
"""
The utilities class for the project, this class is responsible for checking if ports are open or not
"""

import socket
import sys
import multiprocessing

__author__ = "Alex DeCesare"
__version__ = "21-Nov-2020"

def check_open_port(ip_address, port, PORTS):

    """
    Checks if a given port with a given ip address is open or closed
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    if sock.connect_ex((ip_address, port)):
        PORTS[str(port)] = False
    else:
        PORTS[str(port)] = True

def scan(ip_address, start_port, end_port):

    """
    Accepts an ip address, start port, and end port and add each port to the PORTS directory
    with a boolean True if the port is open and False if the port is closed
    """
    MANAGER = multiprocessing.Manager()
    PORTS = MANAGER.dict()

    list_of_processes = []

    for port in range(start_port, end_port):

        port_scan_process = multiprocessing.Process(target=check_open_port, args=(ip_address, port, PORTS))
        list_of_processes.append(port_scan_process)
        port_scan_process.start()

    for process in list_of_processes:
        process.join()

    return dict(PORTS)

def handle_scan_connection(ip_address, start_port, end_port, connection):
    """
    Gets the parameters for the scan function, calls the scan function, and sends the output of
    the scan function to the main method via a pipe. If the any of the parameters are equal to
    None then the function does not call the scan function and sends a None type to the main method
    """

    if ip_address != None and start_port != None:
        scanned_ports = scan(ip_address, start_port, end_port)
        connection.send(scanned_ports)
    else:
        connection.send(None)

