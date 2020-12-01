#!python

"""
This is the main method for the port scanner
"""
import socket
import sys
import multiprocessing
import scan_utils

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

if __name__ == '__main__':
    PARENT_CONNECTION, CHILD_CONNECTION = multiprocessing.Pipe()
    PROCESSES = multiprocessing.Process(target=scan_utils.handle_scan_connection, args=(get_ip_address(), get_start_port(), get_end_port(), CHILD_CONNECTION, ))
    PROCESSES.start()
    PROCESSES.join()
    OUTPUT = PARENT_CONNECTION.recv()
    print(OUTPUT)
