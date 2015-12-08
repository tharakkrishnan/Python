#! /usr/bin/env python
# -*- coding: utf-8 -*
"""Crawls links on a website recursively and produces a siteMap

Usage: python webcrawler.py [options]
Options:
	-h, --help		show this help 
	-u, --url		set the url to crawl starting with htttp:// or file:// [default: "http://example.com"]
	-a, --agent		set the User Agent name [default: 'User Agent']
	-o, --outdir		set the output directory to dump the siteMap in XML and JSON formats [default: './out']
	-d, --debuglevel	set the verbosity of debug level while parsing [default: '1']
							0- silent; complain on Error
							1- info
							2- garrolous
						       >2- just shut up						 
"""

__author__ = "Tharak Krishnan (tharak.krishnan@gmail.com)"
__version__ = "$Revision: 1.0$"
__date__ = "$Date: 2015/08/01 $"
__copyright__ = "Copyright (c) 2015 Tharak Krishnan"
__license__ = "Python"

import re, sys, getopt
from sets import Set
from urlparse import urlparse
from reppy.cache import RobotsCache


class WebCrawler():
	""" Web crawler class crawls a specific website
	"""
	def __init__(self, url="file:///Users/tharak/Dropbox/code/Python/webcrawler/mock_website/example.org/index.html", useragent="User Agent", outdir="out", max_depth=1000, debug=0):
		self.url = url					
		self.useragent = useragent		
		self.siteMap = {self.url:""}	
		self.outdir=outdir.rstrip("/")+"/"	
		self.depth = 0					
		self.MaxDepth = max_depth		
		self.crawled=Set([])			
		self.debug=debug				
		self.domains=Set([urlparse(self.url).netloc.lower()])
		self.robots = RobotsCache()
			
		
	def __crawl_site(self, url_key=""):
		"""Recursively crawls the url passed and populates the sitemap datastructure
		"""
		#Do not continue crawling if we are at maximum allowed depth
		if self.depth > self.MaxDepth: 	
			return
		
		
		if url_key=="":    				
			url=self.url				
		else:
			url=url_key
			
		#Check the site's robot.txt to figure the list of allowed locs	
		#Do not check robots.txt if the file is located locally
		if "http" in urlparse(url).scheme:  
			if not self.robots.allowed(url, self.useragent):
				if(self.debug > 0): 
					print "Page disallowed in robots.txt %s"%(url)
				return
			
		if(self.debug > 0): 
			print "Now crawling: %s"%(url)
		
		url_list=[]
		
		#When we cycle through the siteMap datastructure we convert to a url_list
		#Otherwise, the interpreter complains that dictionary is constantly changing
		
		for key in self.siteMap:		
		 	url_list.append(key)		 
		
		for key in url_list:	
			#Fetch the URLs in the webpage and append to siteMap for URLs that have not yet been crawled. 		
			if self.siteMap[key] == "":
				urls =self.__extract_url(url)
				self.siteMap[key] = urls

				for url_key in urls:
					#If the URL has already been crawled or has a # tag, dont crawl it.	
					if (self.debug > 1): 
						print "url_key: %s, crawled: %s"%(url_key,self.crawled)
					if url_key in self.crawled:
						continue
					if "#" in url_key:
						continue
					
					#We do not want to crawl external domains. 
					parsed = urlparse(url_key)
					
					if (self.debug > 1): 
						print parsed.netloc
					
					#If netloc is empty or is the main domain then the page is part of local domain and needs to be crawled.
					if parsed.netloc.lower() in self.domains:		    
						
						if (self.debug > 1): 
							print "\ndepth=%s,URL=%s\n"%(self.depth, url_key)
						self.siteMap[url_key] = ""  
						self.crawled.add(url_key)   
						self.depth = self.depth+1   
						self.__crawl_site(url_key)	
						self.depth = self.depth-1	
			

	def __print_siteMap(self):
		"""Prints the siteMap datastructure in an XML like format
		"""
		#Dump Sitemap to an XML file
		try:                                
			fd = open(self.outdir+"site.xml", "w") 
			try:                           
				fd.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
				fd.write("<WEBSITE>\n")
				for key in self.siteMap:
					fd.write("\t<WEBPAGE>\n")
					fd.write("\t\t<ADDRESS>\"%s\"</ADDRESS>\n"%(key))
					for loc in self.siteMap[key]:
						fd.write("\t\t<LINK>\"%s\"</LINK>\n"%(loc))
					fd.write("\t</WEBPAGE>\n")
				fd.write("</WEBSITE>\n")
			finally:                        
				fd.close()                    			  
		except IOError:                     
			pass    
		#Dump siteMap to a json file
		import json
		with open(self.outdir+'site.json', 'w') as fp:
			json.dump(self.siteMap, fp, indent=4)    
    
		
					
	def get_siteMap(self):
		"""Initiates the crawler and populates the siteMap
		"""
		from os import makedirs
		from shutil	import rmtree 

		rmtree(self.outdir)
		makedirs(self.outdir)

		self.__crawl_site()
		self.__print_siteMap()
		return self.siteMap

	def __extract_url(self, url): 
		"""Extracts the links in the input URL
		"""
		
		import urllib2
		from urllister import URLLister
		from sgmllib import SGMLParseError
		
		req = urllib2.Request(url, headers={'User-Agent' : self.useragent}) 
		try:
			usock = urllib2.urlopen(req)
			parser = URLLister(url)
		
			try:
				parser.feed(usock.read())
				parser.close()
			except Exception as exception:
				if (self.debug > 0): 
					print "sgmllib: Unable to parse web page.\n sgmllib: Raised exception %s"%(type(exception).__name__)
					fd = open(self.outdir+"%s.err"%type(exception).__name__, "a")
					fd.write( "%s\n"%(url))	
					fd.close()
				pass
			usock.close()
			return parser.urls
		except (KeyboardInterrupt, SystemExit):
			raise
		except Exception as exception:
			if (self.debug > 0): 
				print "urllib2: Page does not exist or Malformed web address.\n sgmllib: Raised exception %s"%(type(exception).__name__) 
				fd = open(self.outdir+"%s.err"%type(exception).__name__, "a")
				fd.write( "%s\n"%(url))	
				fd.close()
			return []
		
def usage():
    print __doc__

def main(argv):
	
	TESTURL="http://example.com"
	USERAGENT = "Tharak Krishnan's Browser"
	OUTDIR = "./out"
	_debuglevel = 1
	try:
		opts, args = getopt.getopt(argv, "hu:a:o:d:", ["help", "url=", "agent=", "outdir=", "debuglevel="])
	except getopt.GetoptError:
		usage()
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-h", "--help"):
			usage()
			sys.exit()
		elif opt in ("-u", "--url"):
			TESTURL = arg
			if not (TESTURL.startswith("http://") or TESTURL.startswith("http://")):
				usage()
				sys.exit()
		elif opt in ("-a", "--agent"):
			USERAGENT = arg
		elif opt in ("-o", "--outdir"):
			OUTDIR = arg
		elif opt in ("-d", "--debuglevel"):
			_debuglevel = int(arg)    

	wc=WebCrawler(url=TESTURL, useragent = USERAGENT, outdir=OUTDIR,debug=_debuglevel);
	wc.get_siteMap()

if __name__ == "__main__":
	main(sys.argv[1:])
	
