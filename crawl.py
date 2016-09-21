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
	# Set crawler speed to crawler_delay specified on robots.txt
	if crawler_delay != None or crawler_delay > 2.0:   				# Don't bother with domain if there is requirement to slow down
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

def get_links(robots, url, url_frontier, subdomains, frontier_out, filetypes, filetypes_out, domain, limit_domain):	
	try:

		print "URL:", url
		possible_links = links.Links_Col()
		subdomain = possible_links.get_subdomain(url, domain)
		print "\tSubdomain:", subdomain 							# Get subdomain by parsing url
		if subdomain in possible_links.subdomains:
			print "Skipping URL because domain's limit on time"
			return url_frontier
		print "Checking robots.txt..."
		crawler_delay = robots.delay(url, 'my-agent')				# Get craw-delay if it exists in robots.txt
		
		if crawler_delay != None and crawler_delay > 2.0:			# If there is delay limit, either skip site or wait for the time specified (choose randomly)
			possible_links.subdomains.add(subdomain)
			return url_frontier
			# r = random.uniform(0,10)
			# if r > 9:	# Skip 10% of the time here
			# 	print "Skipping due to delay"
			# 	return url_frontier
			# else:
			# 	print "Slowing crawl"				
			# 	time.sleep(crawler_delay)
		
		if (robots.allowed(url, "*")):								# Check if robots.txt lets us request page
			'''
				If url is allowed by robots, txt:
					Request url, get content_type (filetype), 
					 parse HTML for links, put links on frontier
			'''

			print "\tAllowed to visit"
			if len(url_frontier) < 50:  							# Ensure first site gets read
				t = 20
			else:   												# Force to go faster afterwards
				t = 5
			print "Requesting header...",							# Request header/content
			request = urllib2.Request(url)
			site = urllib2.urlopen(request, timeout=t)				# Open site
			content_type = site.info().getheader('Content-Type')	# Get header to get filetype
			print "finished"
			content_type_regex = r"(text/html)"
			print "\tContent_type:",
			match = re.search(content_type_regex, content_type)		# Do regex to check if file is text/html
			if match != None:		
				# print "\tmatch:", match.group(1)
				if match.group(1) == 'text/html':
					print "text/html"
					filetypes["text/html"] += 1						# Increment text/html count
			else:	# Got a non text/html type
				print content_type 									# Increment non text/html count
				if content_type not in filetypes:  					# If first time seeing a filetype, store the info in unique list of filetypes
					filetypes[content_type] = 0
				else:   # Increment count to file already seen
					filetypes[content_type] += 1
				return url_frontier									# Don't continue parsing if not text/html
		else:	# Disallowed by robots
			print "Not allowed to visit; skipping"
			return url_frontier										# Escape if robots.txt doesn't allow this site
		print "Opening URL"
		print "Parsing links..."
		possible_links.add_links(site)    							# Create possible_links initially with <a> elements (filtered later)
		print "Filtering links by domain..."
		raw_valid_links_tot = possible_links.get_total()
		if limit_domain:
			possible_links.filter_for_domain(domain)
		in_domain_urls_tot = len(possible_links.get_list())
		print "\tFound:"
		print "\t\tLink items:", raw_valid_links_tot   				# Want only <a, href=> 
		print "\t\tLinks in domain:", in_domain_urls_tot
		print "Putting unique links on frontier..."
		for link in possible_links.get_list():						# With a list of links parsed, only put in those that aren't already on url frontier
			if link not in url_frontier:
				frontier_out.write(link+"\n")
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
	frontier_out = open("out", "w")
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
		print "-------------------------------------"
		print "\nVisit #:",visit_num
		url_frontier = get_links(robots, url, url_frontier, subdomains, frontier_out, filetypes, filetypes_out, domain=my_domain, limit_domain=True)
		subdomains = url_frontier.subdomains
		filetypes_out.close()
		filetypes_out = open("filetypes_out", "w")
		print_types(filetypes_out, filetypes)
		visit_num += 1
		print "-------------------------------------"

	frontier_out.close()
	filetypes_out.close()

main()