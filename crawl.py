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
import robotexclusionrulesparser

def get_robots_url(url):
	regex = r"(https?:\/\/.*?(?:/|$))"
	match = re.search(regex, url)
	topdomain_url = ""
	if match != None:
		topdomain_url = match.group(1)
	print "topdomain_url:", topdomain_url
	return topdomain_url+"/robots.txt"

def crawl(url_frontier, robots, url, subdomains, frontier_out, summary_out, domain, limit_domain, skip):	
	try:
		# url_frontier = url_frontier.get_list()
		print "URL:", url
		modified_frontier = links.Url_Frontier()
		subdomain = url_frontier.get_subdomain(url, domain)
		url_frontier.insert_unique_subdomain(subdomain)
		print "\tSubdomain:", subdomain 							# Get subdomain by parsing url
		if subdomain in url_frontier.slow_subdomains and skip == True:    # If wanted, skip domains that have high crawl-delay
			print "Skipping URL because domain's limit on time"
			return url_frontier
		print "Checking robots.txt..."
		
		robots_url = get_robots_url(url)
		robots.fetch(robots_url, timeout=4)
		crawler_delay = robots.get_crawl_delay(robots.user_agent)
		# crawler_delay = robots.delay(url, 'my-agent')				# Get craw-delay if it exists in robots.txt
		print "\trobots.txt crawler_delay:", crawler_delay
		if crawler_delay > 0:			# If there is delay limit, either skip site or wait for the time specified (choose randomly)
			print "\tAdding subdomain to slow_subdomains"
			url_frontier.slow_subdomains.add(subdomain)
			# # return url_frontier
			# r = random.uniform(0,10)
			# if r > 9:	# Skip 10% of the time here
			# 	print "Skipping due to delay"
			# 	return url_frontier
			if skip == False:	
				print "\tSlowing crawl"				
				time.sleep(crawler_delay)
		
		if robots.is_allowed(robots.user_agent, url):
		# if (robots.is_allowed(url, "*")):								# Check if robots.txt lets us request page
			'''
				If url is allowed by robots, txt:
					Request url, get content_type (filetype), 
					 parse HTML for links, put links on frontier
			'''

			print "\tAllowed to visit"
			if len(url_frontier.get_list()) < 50:  							# Ensure first site gets read
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
					url_frontier.filetypes["text/html"] += 1						# Increment text/html count
			else:	# Got a non text/html type
				print content_type 									# Increment non text/html count
				if content_type not in url_frontier.filetypes:  					# If first time seeing a filetype, store the info in unique list of filetypes
					print "New 'other' content; Setting other filetype count to 0"
					url_frontier.filetypes[content_type] = 1
				else:   # Increment count to file already seen
					print "Incrementing other filetype count"
					url_frontier.filetypes[content_type] += 1
				return url_frontier									# Don't continue parsing if not text/html
		else:	# Disallowed by robots
			print "Not allowed to visit; skipping"
			return url_frontier										# Escape if robots.txt doesn't allow this site
		print "Opening URL"
		print "Parsing links..."
		modified_frontier.add_links(site)    							# Create modified_frontier initially with <a> elements (filtered later)
		print "Filtering links by domain..."
		raw_valid_links_tot = modified_frontier.get_total()
		if limit_domain:
			modified_frontier.filter_for_domain(domain)
		in_domain_urls_tot = len(modified_frontier.get_list())
		print "\tFound:"
		print "\t\tLink items:", raw_valid_links_tot   				# Want only <a, href=> 
		print "\t\tLinks in domain:", in_domain_urls_tot
		print "Putting unique links on frontier..."
		for link in modified_frontier.get_list():						# With a list of links parsed, only put in those that aren't already on url frontier
			if link not in url_frontier.get_list():
				frontier_out.write(link+"\n")
				url_frontier.list_of_links.append(link)
		print "Finished"
		return url_frontier
	except socket.timeout , e:
	    print "Socket timeout"
	    return url_frontier
	# except urllib2.URLError , e:
	# 	print "Urlerror"
		# return url_frontier
	except urllib2.HTTPError as e: # http://stackoverflow.com/questions/666022/what-errors-exceptions-do-i-need-to-handle-with-urllib2-request-urlopen
	    print 'HTTPError = ', str(e.code)
	    return url_frontier
	except urllib2.URLError , e:
	    print 'URLError = ', str(e.reason)
	    return url_frontier
	except Exception:
	    print 'generic exception: ', traceback.format_exc()
	    print 'Other exception'
	    return url_frontier

def print_dashboard(outfile, filetypes, subdomains):
		outfile.write("Filetypes:\n")
		try:
			for filetype in filetypes:
				outfile.write("\t"+filetype+ ":"+ str(filetypes[filetype])+"\n")
			outfile.write("Subdomains:\n")
			for subdomain in subdomains:
				outfile.write("\t"+subdomain+"\n")
		except TypeError:
			pass
def main():
	# crawler = Crawler()
	frontier_out = open("out", "w")
	summary_out = open("summary_out", "w")
	print "Starting crawler..."
	visits_limit = 50
	visit_num = 0
	my_domain = "uky.edu"
	start_url = "http://www."+my_domain
	start_url = "http://www.uky.edu"
	url = start_url
	url_frontier = links.Url_Frontier()
	subdomains = set()
	robots = robotexclusionrulesparser.RobotExclusionRulesParser()
	robots.user_agent = "schoolbot"

	# robots = RobotsCache()

	while True:
		print "-------------------------------------"
		print "\nVisit #:",visit_num
		# print "Len filetypes:", len(url_frontier.filetypes)
		url_frontier = crawl(url_frontier, robots, url, subdomains, frontier_out, summary_out, domain=my_domain, limit_domain=True, skip=True)
		url = url_frontier.get_list()[visit_num]
		# summary_out.close()
		# summary_out = open("summary_out", "w")
		print_dashboard(summary_out, url_frontier.filetypes, url_frontier.subdomains)
		visit_num += 1
		print "-------------------------------------"

	frontier_out.close()
	summary_out.close()

main()