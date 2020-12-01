#!/usr/bin/env python3

"""
The test class for the utils class
"""

import unittest
import scan_utils
import multiprocessing
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

class TestCheckOpenPort(unittest.TestCase):
    
    def test_check_closed_port(self):
        
        ports = {}
        test_manager = multiprocessing.Manager()
        test_dictionary = test_manager.dict({'3280' : False})

        is_open = scan_utils.check_open_port('127.0.0.1', 3280, ports)
        self.assertEqual(dict(test_dictionary), ports)

    def test_check_open_port(self):

        first_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        first_socket.bind(('127.0.0.1', 3280))
        first_socket.listen(1)

        ports = {}
        test_manager = multiprocessing.Manager()
        test_dictionary = test_manager.dict({'3280' : True})

        is_open = scan_utils.check_open_port('127.0.0.1', 3280, ports)
        self.assertEqual(dict(test_dictionary), ports)

class TestScanUtils(unittest.TestCase):
    
    def test_scan_one_port_all_closed(self):
        test_manager = multiprocessing.Manager()
        test_dictionary = test_manager.dict({'3280' : False})
        test_dictionary = {'3280' : False}
        scanned_dictionary = dict(scan_utils.scan('127.0.0.1', 3280, 3281))
        self.assertEqual(test_dictionary, scanned_dictionary)
    
    def test_scan_one_port_all_open(self):
        
        first_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        first_socket.bind(('127.0.0.1', 3280))
        first_socket.listen(1)

        test_manager = multiprocessing.Manager()
        test_dictionary = {'3280' : True}
        scanned_dictionary = dict(scan_utils.scan('127.0.0.1', 3280, 3281))
        self.assertEqual(test_dictionary, scanned_dictionary)

    def test_scan_many_ports_all_closed(self):
        test_manager = multiprocessing.Manager()
        test_dictionary = test_manager.dict({'3280' : False})
        test_dictionary = {'3280' : False, '3281' : False, '3282' : False, '3283' : False, '3284' : False, '3285' : False, '3286' : False, '3287' : False, '3288' : False, '3289' : False}
        scanned_dictionary = dict(scan_utils.scan('127.0.0.1', 3280, 3290))
        self.assertEqual(test_dictionary, scanned_dictionary)

    def test_scan_many_ports_all_open(self):

        first_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        first_socket.bind(('127.0.0.1', 3280))
        first_socket.listen(1)
        
        second_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        second_socket.bind(('127.0.0.1', 3281))
        second_socket.listen(1)

        third_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        third_socket.bind(('127.0.0.1', 3282))
        third_socket.listen(1)

        fourth_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fourth_socket.bind(('127.0.0.1', 3283))
        fourth_socket.listen(1)

        fifth_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        fifth_socket.bind(('127.0.0.1', 3284))
        fifth_socket.listen(1)


        test_manager = multiprocessing.Manager()
        test_dictionary = {'3280' : True, '3281' : True, '3282' : True, '3283' : True, '3284' : True}

        scanned_dictionary = dict(scan_utils.scan('127.0.0.1', 3280, 3285))
        print(scanned_dictionary)
        self.assertEqual(test_dictionary, scanned_dictionary)

    def test_scan_many_ports_some_open(self):

        first_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        first_socket.bind(('127.0.0.1', 3280))
        first_socket.listen(1)

        second_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        second_socket.bind(('127.0.0.1', 3285))
        second_socket.listen(1)

        third_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        third_socket.bind(('127.0.0.1', 3289))
        third_socket.listen(1)

        test_manager = multiprocessing.Manager()
        test_dictionary = {'3280' : True, '3281' : False, '3282' : False, '3283' : False, '3284' : False, '3285' : True, '3286' : False, '3287' : False, '3288' : False, '3289' : True}

        scanned_dictionary = dict(scan_utils.scan('127.0.0.1', 3280, 3290))
        self.assertEqual(test_dictionary, scanned_dictionary)

if __name__ == '__main__':
    unittest.main()                
