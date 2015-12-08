#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Unit test for urllister.py

"""

__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

import urllister
import unittest

class KnownValues(unittest.TestCase):
	KnownValues = [
					("http://example.com", "/test/out", "http://example.com/test/out"),
					("http://digitalocean.com/", "/test/out", "http://digitalocean.com/test/out"),	
					("http://digitalocean.com/community", "../test/out", "http://digitalocean.com//test/out"),
					("http://digitalocean.com/community", "./test/out", "http://digitalocean.com/community/test/out"),
					
	]
		
				
	def testAbsolutifyKnownValues(self):
		"""absolutify should give known result with known input"""
		for t in self.KnownValues:
			result=urllister.URLLister("").absolutify(t[0],t[1])
			self.assertEqual(t[2], result)
		
		
	