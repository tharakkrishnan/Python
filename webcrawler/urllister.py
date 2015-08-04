#! /usr/bin/env python
# -*- coding: utf-8 -*

"""Extract list of URLs in a web page
This code is derived from a book by Mark Pilgrim at http://diveintopython.net

"""

__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

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
			self.urls.extend([self.__absolutify(k) for k in href])
			
	def __absolutify(self, url):
		"""Converts a relative url path into an absolute one
		""" 
		from urlparse import urlparse

		url_parts = urlparse(url)
		domain_url_parts = urlparse(self.url)

		if url_parts.netloc == '' and url_parts.scheme == '':
			
			if  url_parts.path.startswith("../"):
				domain_path_list = domain_url_parts.path.strip("/").split("/")
				domain_path_list = domain_path_list[:-1]
				return domain_url_parts.scheme +"://" \
					   + domain_url_parts.netloc.lower().rstrip("/") + \
					   "/"+"/".join(domain_path_list).lstrip("/") +"/"+ url.lstrip("../")
					   
			if  url_parts.path.startswith("./"):
				return domain_url_parts.scheme +"://"+ domain_url_parts.netloc.lower().rstrip("/")+"/"+url.lstrip("./")
				
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
