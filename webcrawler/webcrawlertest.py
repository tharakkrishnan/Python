#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Unit test for webcrawler.py

"""

__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

import webcrawler
import unittest


USERAGENT = "Tharak Krishnan's Browser"
OUTDIR = "webcrawlertestdir"

class KnownValues(unittest.TestCase):
	KnownValues = [
		(	"file:///Users/tharak/Dropbox/code/Python/webcrawler/mock_websites/test1/example.org/index.html",
			 "/Users/tharak/Dropbox/code/Python/webcrawler/mock_websites/test1/out/site.xml",
			 "/Users/tharak/Dropbox/code/Python/webcrawler/mock_websites/test1/out/site.json"
		)
				
	]

	def testWebcrawlerKnownValues(self):
		"""webcrawler should give known result with known input"""
		for t in self.KnownValues:
			wc=webcrawler.WebCrawler(url=t[0], useragent = USERAGENT, outdir=OUTDIR,debug=1);
			wc.get_siteMap()
			ext = [".xml",".json"]
			for k in range(0,1):
				result_fd = open(OUTDIR+"/site"+ext[k], 'rt')
				result =""
				for line in result_fd.readline():
					result= result+line
				result_fd.close()
				
				test_out_fd = open(t[k+1], 'rt')
				test_out =""
				for line in test_out_fd.readline():
					test_out= test_out+line
				test_out_fd.close()
				self.assertEqual(test_out, result)
				
				import shutil
				shutil.rmtree(OUTDIR)
			
if __name__ == "__main__":
	unittest.main()

