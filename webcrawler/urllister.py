#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Extract list of URLs in a web page

This program derived from "Dive Into Python" by Mark Pilgrim,
a free Python book for experienced programmers. 
Visit http://diveintopython.org/ for the latest version.
"""
__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

TESTURL="http://example.com"
USERAGENT = "Tharak Krishnan's Browser"


from sgmllib import SGMLParser

class URLLister(SGMLParser):
	
	def __init__(self, url=""):
		self.url = url
		SGMLParser.__init__(self)
	
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []

	def start_a(self, attrs):
		href = [v for k, v in attrs if k=='href']
		
		if href:
			self.urls.extend([self.__absolutify(self.url, k) for k in href])
	
	def absolutify(self, domain_url, url):
		"""Converts a relative url path into an absolute one
		Public function for testing purposes
		""" 
		return self.__absolutify(domain_url, url)
	
			
	def __absolutify(self, domain_url, url):
		"""Converts a relative url path into an absolute one
		""" 
		from urlparse import urlparse

		url_parts = urlparse(url)
		domain_url_parts = urlparse(domain_url)

		if url_parts.netloc == '' and url_parts.scheme == '':
			
			if  url_parts.path.startswith("../"):
				domain_path_list = domain_url_parts.path.strip("/").split("/")
				domain_path_list = domain_path_list[:-1]
				print domain_path_list
				return domain_url_parts.scheme +"://" \
					   + domain_url_parts.netloc.lower().rstrip("/") + \
					   "/"+("/".join(domain_path_list)).strip("/") +"/"+ url.lstrip("../")
					   
			if  url_parts.path.startswith("./"):
				return domain_url_parts.scheme +"://"+ domain_url_parts.netloc.lower().rstrip("/")+"/"+domain_url_parts.path.lower().strip("/")+"/"+url.lstrip("./")
				
			return domain_url_parts.scheme +"://"+ domain_url_parts.netloc.lower().rstrip("/")+"/"+url.lstrip("/")
		else:
			return url
				
if __name__ == "__main__":
	import urllib2
	import httplib
	
	httplib.HTTPConnection.debuglevel = 0
	url = "https://www.digitalocean.com/"
	req = urllib2.Request(url, headers={'User-Agent' : "Tharak Krishnan's Browser"}) 
	usock = urllib2.urlopen(req)
	parser = URLLister(url)
	try:
		 parser.feed(usock.read())
	except:
		 pass
		
	parser.close()
	usock.close()
	for url in parser.urls: print url
