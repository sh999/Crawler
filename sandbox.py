from bs4 import BeautifulSoup
# import urllib2
import cookielib
import socket
import urllib2
from cookielib import Cookie
import robots
import links
import re
import reppy
from reppy.cache import RobotsCache

def souptest():
	url = "http://www.drudgereport.com"
	site = urllib2.urlopen(url, timeout=5)
	mytag = '<a  href="www.uky.edu"class="box-link"><h3>10 Things UK Students Love About Lexington</h3></a><p>lol</p><a>link2</a>'
	
	mysoup = BeautifulSoup(mytag)
	links = mysoup.find_all("a").get("href")
	for i in links:
		print "?"
		print i
def re_test():
	link1 = 'http://www.uky.edu'
	str1 = 'http://uknow.uky.edu/content/10-things-uk-students-love-about-lexington'
	uky_domain_regex = r"(.*uky.edu.*)"
	# domains_in_uk_regex = r"https?:\/\/(.*)\..*\.uky\.edu.*"
	domains_in_uk_regex = r"https?:\/\/(.*)\..*uky\.edu.*"
	match = re.search(domains_in_uk_regex, str1)	
	print "regex:", uky_domain_regex
	if match != None:
		print match.group(0)
		print match.group(1)
	else:
		print "None found"


def break_test():
	# Break out of for loop inside if
	for i in range(0, 100):
		print i
		if i > 40:
			break
def file_test():
	outfile = open("out", "w")
	i = 0
	while True:
		i += 1
		if i % 10000 == 0:
			outfile.write(str(i)+"\n")
	outfile.close()

def dict_test():
	# Increment count for dict keys
	d = {}
	d["bob"] = 0
	d["susan"] = 0
	mark = "susan"
	print d
	d[mark] += 1
	print d

def find_filetype():
	# Return unique filetypes form a list of urls
	url = "http://www.uky.edu/registrar/Major-Sheets/MSCurrent/eng/cs.pdf"
	url2 = "http://www.uky.edu/recwell/sites/www.uky.edu.recwell/files/ctools/News.png"
	url3 = "http://www.uky.edu"
	regex_filetype = r".*uky\.edu\/.*\.(.*)"
	urls = [url, url2, url3]
	print urls
	for link in urls:
		match = re.search(regex_filetype, link)
		if match != None:
			print match.group(1)

def http_header():
	# Get HTTP response header
	# request = urllib2.Request("http://www.maths.ed.ac.uk/~jmf/Teaching/MT3/LinearAlgebra.pdf")
	request = urllib2.Request("http://www.umich.edu/news/podcast/society/Hoffmanpod.mp3")
	response = urllib2.urlopen(request)
	content_type = response.info().getheader('Content-Type')
	content_type_regex = r"(.*);"
	print "content_type:", content_type
	match = re.search(content_type_regex, content_type)
	if match != None:
		print match.group(1)
		if match.group(1) == 'text/html':
			print "is text/html type"
			site_soup = BeautifulSoup(response)			# Convert to tree of tags soup object
			tag_a_elements = site_soup.find_all("a")		# Get all tags <a> from tag tree
		else:
			print "do nothing"
	# print "doing useless thing:"
	# site_soup = BeautifulSoup(response)			# Convert to tree of tags soup object
	# tag_a_elements = site_soup.find_all("a")
	# print "done"
	# print response.read()
	# request = urllib2.Request("http://www.maths.ed.ac.uk/~jmf/Teaching/MT3/LinearAlgebra.pdf")
	# response = urllib2.urlopen(request)
	# print response.info().getheader('Content-Type')
	# print response.read()

def robots_parse():
	robots = RobotsCache()
	print robots.allowed("http://www.uky.edu/hr/employment", "my-agent")
def domain_test2():
	link1 = 'http://www.uky.edu'
	str1 = 'http://ukn/ow.uky.edu/content/10-things-uk-students-love-about-lexington'
	# uky_domain_regex = r"(.*uky.edu.*)"
	# domains_in_uk_regex = r"https?:\/\/(.*)\..*\.uky\.edu.*"
	# domains_in_uk_regex = r"https?:\/\/(.*)\..*uky\.edu.*"
	domains_in_uk_regex = r"(https?:\/\/).*(\/).*(uky\.edu)"
	match = re.search(domains_in_uk_regex, str1)	
	print "regex:", domains_in_uk_regex
	if match != None:
		print "Don't want this"
		print match.group(0)
		print match.group(1)
		print match.group(2)
	else:
		print "Want this"
domain_test2()