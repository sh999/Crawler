# Crawler v1
# Naive approach:  From homepage, extract out links and put the unique, 
#  in-domain ones to the url frontier. Visit the frontier from top to
#  bottom. 
# 
from bs4 import BeautifulSoup
import urllib2
# import cookielib
import socket
# from cookielib import Cookie
import links
import reppy
from reppy.cache import RobotsCache
import traceback


def get_links(url, url_frontier, outfile, domains_out, domain, limit_domain):	
	robots = RobotsCache()
		
	try:
		print "Request url...:", url
		if (robots.allowed(url, "*")):
			print "Allowed to visit"
			if len(url_frontier) < 50:
				t = 20
			else:
				t = 10
			site = urllib2.urlopen(url, timeout=t)
			# site = urllib2.urlopen(url, timeout=10)		# Connect to site
		else:
			print "Not allowed to visit; skipping"
			return url_frontier			# Don't modify url table; exit function
		
		# Keep going since site is allowed
		# if len(url_frontier) < 50:
		# 	t = 100
		# else:
		# 	t = 2
		# site = urllib2.urlopen(url, timeout=t)		# Connect to site
		print "Done requesting. Parsing links..."
		possible_links = links.Links_Col(site)    # Create possible_links initially with <a> elements (filtered later)
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
	    return url_frontier

def main():
	outfile = open("out", "w")
	domains_out = open("domains_out", "w")
	print "Starting crawler..."
	visits_limit = 50
	visit_num = 1
	my_domain = "ut.edu"
	start_url = "http://www."+my_domain
	url_frontier = [start_url]
	# url_frontier = get_links(start_url, url_frontier, outfile, domains_out, domain="umich.edu", limit_domain=True)
	for url in url_frontier:
		print "\nVisit #:",visit_num
		url_frontier = get_links(url, url_frontier, outfile, domains_out, domain=my_domain, limit_domain=True)
		visit_num += 1
	outfile.close()
	domains_out.close()

main()