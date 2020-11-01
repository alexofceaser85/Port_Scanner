#!/usr/bin/env python3

"""
This script scans the ports of a network and returns which ports are open and which are closed
"""

__author__ = 'Alex DeCesare'
__version__ = '26-October-2020'

import multiprocessing
import os
import sys
import socket
import time

manager = multiprocessing.Manager()
ports = manager.dict()

def handle_scan_connection(connection):

    ip_address = get_ip_address()
    start_port = get_start_port()
    end_port = get_end_port()

    if ip_address != None and start_port != None:
        ports = port_scanner.scan(ip_address, start_port, end_port)
        connection.send(ports)
    else:
        connection.send(None)

def check_open_port(ip_address, port):

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port_status = sock.connect_ex((ip_address, port))

    if port_status == 0:
        ports[str(port)] = True
    else:
        ports[str(port)] = False


def scan(ip_address, start_port, end_port):
   
    list_of_processes = []

    for port in range(start_port, end_port):
        
        port_scan_process = multiprocessing.Process(target=check_open_port, args=(ip_address, port))
        list_of_processes.append(port_scan_process)
        port_scan_process.start()
    
    for process in list_of_processes:
        port_scan_process.join()
    
    return ports

if __name__ == '__main__':
    parent_connection, child_connection = multiprocessing.Pipe()
    processes = multiprocessing.Process(target=handle_scan_connection, args=(child_connection, ))
    processes.start()
    processes.join()
