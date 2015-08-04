#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Regression testing framework

This module will search for scripts in the same directory named
XYZtest.py.  Each such script should be a test suite that tests a
module through unittest. This script will aggregate all
found test suites into one big test suite and run them all at once.

This program derived from "Dive Into Python" by Mark Pilgrim,
 a free Python book for experienced programmers. 
Visit http://diveintopython.net/ for the latest version.
"""
__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

import sys, os, re, unittest

def regressionTest():
    path = os.path.abspath(os.path.dirname(sys.argv[0]))
    files = os.listdir(path)
    test = re.compile("test\.py$", re.IGNORECASE)
    files = filter(test.search, files)
    filenameToModuleName = lambda f: os.path.splitext(f)[0]
    moduleNames = map(filenameToModuleName, files)
    modules = map(__import__, moduleNames)
    load = unittest.defaultTestLoader.loadTestsFromModule
    return unittest.TestSuite(map(load, modules))

if __name__ == "__main__":
    unittest.main(defaultTest="regressionTest")

