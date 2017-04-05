# webcrawler 

## User Requirements:
### 1. It should be limited to one domain:
- so when crawling example.com it would crawl all pages within the example.com domain,
  but not follow the links to Facebook or Instagram accounts or subdomains like cloud.example.com. 

### 2. Given a URL, it should output a site map:
- showing which static assets each page depends on, and the links between pages.
  Choose the most appropriate data structure to store & display this site map.

## External package requirements:
### a. reppy
    -Install using "pip install reppy" 
## TODO
### Improve memory usage
    1. Modify the sitemap data structure to dumps to file after every crawl rather than store the entire site and dump at the end since it can grow really large
### Add unit tests
    1.To check url parsing
 
