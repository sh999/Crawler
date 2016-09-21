# Crawler v1
# Naive approach:  From homepage, extract out links and put the unique, 
#  in-domain ones to the url frontier. Visit the frontier from top to
#  bottom. 
# 
from bs4 import BeautifulSoup
import urllib2
import socket
import links
import reppy
from reppy.cache import RobotsCache
import traceback
import re
import time
import random

def delay_crawler(crawler_delay, just_skip):
	# Set crawler speed to rawler_delay
	if crawler_delay != None or crawler_delay > 2.0:   	# Don't bother with domain if there is requirement to slow down
		# print "Ignoring domain due to delay limit"
		# return url_frontier
		if crawler_delay <= 10.0:
			print "Delaying crawler..."
			time.sleep(crawler_delay)
		print "Done delay"

def ignore_from_setdelay(crawler_delay):
	# Don't bother requesting if domain sets crawler_delay
	if crawler_delay != None or crawler_delay > 2.0:
		return True
	else:
		return False

def get_links(robots, url, url_frontier, subdomains, outfile, filetypes, filetypes_out, domain, limit_domain):	
	try:
		print "URL:", url
		possible_links = links.Links_Col()
		print "Subdomain:", possible_links.get_subdomain(url, domain)
		print "Checking robots..."
		crawler_delay = robots.delay(url, 'my-agent')		# Get craw-delay if it exists
		if crawler_delay != None and crawler_delay > 5.0:
			# If there is delay limit, either skip site or wait for the time specified (choose randomly)
			r = random.uniform(0,10)
			if r > 9:	# Skip 80% of the time here
				print "Skipping due to delay"
				return url_frontier
			else:
				print "Slowing crawl"
				time.sleep(crawler_delay)
		

		if (robots.allowed(url, "*")):	# Allowed by robots. Check filetype and may fetch data
			print "Allowed to visit"
			if len(url_frontier) < 50:  # Ensure first site gets read
				t = 20
			else:   # Other sites limit
				t = 5
			print "Requesting header"
			request = urllib2.Request(url)
			site = urllib2.urlopen(request, timeout=t)		# Open site
			content_type = site.info().getheader('Content-Type')	# Get header to get filetype
			content_type_regex = r"(text/html)"
			print "Content_type from header:", content_type
			match = re.search(content_type_regex, content_type)
			if match != None:		# filetype is what we want, text/html
				print "\tmatch:", match.group(1)
				if match.group(1) == 'text/html':
					print "\Detected text/html type"
					filetypes["text/html"] += 1
			else:	# Got a non text/html type
				print "Found type", content_type
				if content_type not in filetypes:  # First time type seen
					filetypes[content_type] = 0
				else:   # Increment count to file already seen
					filetypes[content_type] += 1
				return url_frontier
		else:	# Disallowed by robots
			print "Not allowed to visit; skipping"
			return url_frontier			# Don't modify url table; exit function
		print "Opening URL"
		print "Parsing links..."
		possible_links.add_links(site)    # Create possible_links initially with <a> elements (filtered later)
		print "Filtering links by domain..."
		raw_valid_links_tot = possible_links.get_total()
		if limit_domain:
			possible_links.filter_for_domain(domain)
		in_domain_urls_tot = len(possible_links.get_list())
		print "\tLink items:", raw_valid_links_tot   # <a, href=> items
		print "\tLinks in domain:", in_domain_urls_tot
		print "Putting unique links on frontier..."
		for link in possible_links.get_list():		# With a list of links parsed, only put in those that aren't already on url frontier
			if link not in url_frontier:
				outfile.write(link+"\n")
				url_frontier.append(link)
		return url_frontier
	except socket.timeout , e:
	    print "Socket timeout"
	    return url_frontier
	except urllib2.URLError , e:
		print "Urlerror"
		return url_frontier
	except urllib2.HTTPError as exc: # http://stackoverflow.com/questions/666022/what-errors-exceptions-do-i-need-to-handle-with-urllib2-request-urlopen
	    print 'HTTPError = ', str(e.code)
	    return url_frontier
	except urllib2.URLError , e:
	    print 'URLError = ', str(e.reason)
	    return url_frontier
	except Exception:
	    print 'generic exception: ', traceback.format_exc()
	    print 'Other exception'
	    return url_frontier
def print_types(outfile, filetypes):
		print "\tFiletypes:"
		for filetype in filetypes:
			outfile.write(filetype+ ":"+ str(filetypes[filetype])+"\n")
def main():
	outfile = open("out", "w")
	filetypes_out = open("filetypes_out", "w")
	print "Starting crawler..."
	visits_limit = 50
	visit_num = 1
	my_domain = "uky.edu"
	start_url = "http://www."+my_domain
	start_url = "http://www.uky.edu"
	url_frontier = [start_url]
	subdomains = set()
	robots = RobotsCache()
	filetypes = {"text/html":0}

	for url in url_frontier:
		print "\nVisit #:",visit_num
		url_frontier = get_links(robots, url, url_frontier, subdomains, outfile, filetypes, filetypes_out, domain=my_domain, limit_domain=True)
		filetypes_out.close()
		filetypes_out = open("filetypes_out", "w")
		print_types(filetypes_out, filetypes)
		visit_num += 1
	outfile.close()
	filetypes_out.close()

main()