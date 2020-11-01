#!/usr/bin/env python3

"""
This is the test class for the port scanner class
"""

__author__ = 'Alex DeCesare'
__version__ = '26-October-2020'

import port_scanner
import unittest
#from http.server import BaseHTTPRequestHandler, HTTPServer
import multiprocessing
from unittest.mock import patch

class TestScan(unittest.TestCase):
   
    #@patch('multiprocessing.Process.__init__', new=check_open_port)
    #@patch('multiprocessing.Process.start', new=lambda x: None)
    #@patch('multiprocessing.Process.join', new=lambda x, y: None) 
    def test_scan_one_closed_port(self):
        output = port_scanner.scan('127.0.0.1', 2000, 2001)
        self.assertEquals({'2000', False}, dict(output))

if __name__ == '__main__':
    unittest.main()
