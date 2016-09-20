from bs4 import BeautifulSoup
import urllib2
import cookielib
import socket
from cookielib import Cookie
import robots
import links
import re

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
	link1 = 'www.uky.edu'
	link2 = 'www.google.com'
	str1 = 'http://uknow.uky.edu/content/10-things-uk-students-love-about-lexington'
	regex = r"(.*uky.edu.*)"
	match = re.search(regex, str1)
	print match.group(0)
	print type(match.group(0))

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

def increment_dict():
	# Increment counts for all keys
	d = {}
	for i in range(0,1000000):
		d[str(i)] = 0
	for i in d.iterkeys():
		d[i] = d[i] + 23
	# print d

increment_dict()