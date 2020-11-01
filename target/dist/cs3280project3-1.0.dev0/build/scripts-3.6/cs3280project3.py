#!python

"""
This is the main method for the port scanner
"""
import socket
import sys
import multiprocessing

MANAGER = multiprocessing.Manager()
PORTS = MANAGER.dict()
__author__ = 'Alex DeCesare'
__version__ = '30-October-2020'

def get_ip_address():

    """
    Gets the ip address from the command line arguments
    """

    try:
        return sys.argv[1]
    except IndexError:
        print('Please include an ip address')
        return None

def get_start_port():

    """
    Gets the start port from the command line arguments
    """

    try:
        return int(sys.argv[2])
    except IndexError:
        print('Please include a starting port')
        return None
    except ValueError:
        print('There is an invalid value for the starting port, please only include integers')
        return None

def get_end_port():

    """
    Gets the end port from the command line arguments and add one to it,
    if there is no end port then return the start port plus one. This is
    needed for the range function in the scan method
    """

    try:
        return int(sys.argv[3]) + 1
    except IndexError:
        return int(sys.argv[2]) + 1
    except ValueError:
        print('There is an invalid value for the ending port, please only include integers')
        return None

def check_open_port(ip_address, port):

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

    list_of_processes = []

    for port in range(start_port, end_port):

        port_scan_process = multiprocessing.Process(target=check_open_port, args=(ip_address, port))
        list_of_processes.append(port_scan_process)
        port_scan_process.start()

    for process in list_of_processes:
        process.join()

    return PORTS

def handle_scan_connection(connection):

    """
    Gets the parameters for the scan function, calls the scan function, and sends the output of
    the scan function to the main method via a pipe. If the any of the parameters are equal to
    None then the function does not call the scan function and sends a None type to the main method
    """

    ip_address = get_ip_address()
    start_port = get_start_port()
    end_port = get_end_port()

    if ip_address != None and start_port != None:
        scanned_ports = scan(ip_address, start_port, end_port)
        connection.send(scanned_ports)
    else:
        connection.send(None)

if __name__ == '__main__':
    PARENT_CONNECTION, CHILD_CONNECTION = multiprocessing.Pipe()
    PROCESSES = multiprocessing.Process(target=handle_scan_connection, args=(CHILD_CONNECTION, ))
    PROCESSES.start()
    PROCESSES.join()
    OUTPUT = PARENT_CONNECTION.recv()
    print(OUTPUT)
