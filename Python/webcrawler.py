#!/usr/bin/python
"""Crawls links on a website recursively and produces a siteMap


"""

__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

import re
from sets import Set

class WebCrawler():
	""" Web crawler class crawls a specific website
	"""
	def __init__(self, url="https://www.digitalocean.com", max_level=1000, debug=0):
		self.url=url
		self.siteMap = {self.url:""}
		self.level = 0
		self.MaxLevel = max_level
		self.crawled=Set([])
		self.debug=debug

	
	def __crawl_site(self, url_key=""):
		"""Recursively crawls the url passed and populates the sitemap datastructure
		"""
		
		if self.level > self.MaxLevel: 
			return
		
		if url_key=="":
			url=self.url
		else:
			url=self.url+url_key
			
		print "url to crawl:%s"%url
		
		url_list=[]
		
		for key in self.siteMap:
		 	url_list.append(key)
		
		for key in url_list:
			if self.siteMap[key] == "":
				urls =self.__extract_url(url)
				self.siteMap[key] = urls

				for url_key in urls:
					if (self.debug > 1): print "url_key: %s, crawled: %s"%(url_key,self.crawled)
					if url_key in self.crawled:
						continue
					if url_key.startswith("#"):
						continue
					
					import tldextract
					ext = tldextract.extract(url_key)
					if (self.debug > 1): print ext
					if ext.domain == "":
						temp_url = "%s%s"%(self.url,url_key)
						if (self.debug > 0): print "\nLevel=%s,URL=%s\n"%(self.level, temp_url)
						self.siteMap[url_key] = ""
						self.crawled.add(url_key)
						self.level = self.level+1
						self.__crawl_site(url_key)
						self.level = self.level-1

						

	def __get_prefix(self, address):
		if address.startswith("http"):
			prefix=""
		elif address.startswith("#"):
			prefix=self.url+"/"
		else:
			prefix = self.url
		return prefix					

	def __print_siteMap(self):
		"""Prints the siteMap datastructure in an XML like format
		"""

		#Dump Sitemap to an XML file
		try:                                
			fsock = open("site.xml", "w") 
			try:                           
				fsock.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
				fsock.write("<WEBSITE>\n")
				for key in self.siteMap:
					prefix = self.__get_prefix(key)
					fsock.write("\t<WEBPAGE>\n")
					fsock.write("\t\t<ADDRESS>\"%s\"</ADDRESS>\n"%(prefix+key))
					for loc in self.siteMap[key]:
						prefix = self.__get_prefix(loc)
						fsock.write("\t\t<LINK>\"%s\"</LINK>\n"%(prefix+loc))
					fsock.write("\t</WEBPAGE>\n")
				fsock.write("</WEBSITE>\n")
			finally:                        
				fsock.close()                    			  
		except IOError:                     
			pass    
		#Dump siteMap to a json file
		import json
		with open('site.json', 'w') as fp:
			json.dump(self.siteMap, fp, indent=4)    
			
			
				
	def get_siteMap(self):
		"""Initiates the crawler and populates the siteMap
		"""
		self.__crawl_site()
		self.__print_siteMap()
		return self.siteMap

	def __extract_url(self, url): 
		"""Extracts the links in the input URL
		"""
		
		import urllib2
		from urllister import URLLister
		from sgmllib import SGMLParseError
		
		req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
		try:
			usock = urllib2.urlopen(req)
			parser = URLLister()
		
			try:
				parser.feed(usock.read())
				parser.close()
			except SGMLParseError:
				if (self.debug > 0): print "SGMLParseError: Unable to parse web page." 
				pass
			usock.close()
			return parser.urls
		except urllib2.HTTPError, urllib2.URLError:
			if (self.debug > 0): print "HTTPError or URLError: Page does not exist or Malformed web address." 
			return []
		


if __name__ == "__main__":
	wc=WebCrawler(url="http://digitalocean.com", max_level=2, debug=1);
	wc.get_siteMap()
	
