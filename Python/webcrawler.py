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
	def __init__(self, url="https://www.digitalocean.com", max_level=1000):
		self.url=url
		self.siteMap = {url:""}
		self.level = 0
		self.MaxLevel = max_level
		self.crawled=Set([]);

	
	def __crawl_site(self, url_key=""):
		"""Recursively crawls the url passed and populates the sitemap datastructure
		"""
		
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
					print "url_key: %s, crawled: %s"%(url_key,self.crawled)
					if url_key in self.crawled:
						continue
					if url_key == '#':
						continue
					
					import tldextract
					ext = tldextract.extract(url_key)
					#print ext
					if ext.domain == "":
						temp_url = "%s%s"%(self.url,url_key)
						print "\nLevel=%s,URL=%s\n"%(self.level, temp_url)
						self.siteMap[url_key] = ""
						self.crawled.add(url_key)
						self.level = self.level+1
						if(self.level < self.MaxLevel):
							self.__crawl_site(url_key)
						else:
							return
						self.level = self.level-1

						

						

	def __print_siteMap(self):
		"""Prints the siteMap datastructure in an XML like format
		"""
		print self.siteMap
		try:                                
			fsock = open("site.xml", "w") 
			try:                           
				fsock.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
				for key in self.siteMap:
					fsock.write("\t<URL>\n")
					fsock.write("\t\t<WEBPAGE>%s</WEBPAGE>\n"%(key))
					for loc in self.siteMap[key]:
						fsock.write("\t\t<LINK>%s</LINK>\n"%(loc))
					fsock.write("\t</URL>\n")
			finally:                        
				fsock.close()                    			  
		except IOError:                     
			pass        
			
			
				
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
				pass
			usock.close()
			return parser.urls
		except urllib2.HTTPError, urllib2.URLError:
			return []
		


if __name__ == "__main__":
	wc=WebCrawler(url="http://digitalocean.com/", max_level=5);
	wc.get_siteMap()
	
