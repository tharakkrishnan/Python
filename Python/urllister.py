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
	def reset(self):
		SGMLParser.reset(self)
		self.urls = []

	def start_a(self, attrs):
		href = [v for k, v in attrs if k=='href']
		if href:
			self.urls.extend(href)

if __name__ == "__main__":
	import urllib2
	import httplib
	
	httplib.HTTPConnection.debuglevel = 0
	url = "https://www.digitalocean.com/"
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"}) 
	usock = urllib2.urlopen(req)
	parser = URLLister()
	try:
		 parser.feed(usock.read())
	except sgmllib.SGMLParseError:
		 pass
		
	parser.close()
	usock.close()
	for url in parser.urls: print url
