# Crawler v1
# Naive approach:  From homepage, extract out links and put the unique, 
#  in-domain ones to the url frontier. Visit the frontier from top to
#  bottom. 
# 
from bs4 import BeautifulSoup
import urllib2
import cookielib
import socket
from cookielib import Cookie
import robots
import links

def get_links(url, observed_urls, outfile, domain, limit_domain):	
	# cookie_jar = cookielib.CookieJar()
	try:
		print "Opening url:", url
		site = urllib2.urlopen(url, timeout=2)		# Connect to site
		site_soup = BeautifulSoup(site)			# Convert to tree of tags soup object
		tag_a_elements = site_soup.find_all("a")		# Get all tags <a> from tag tree
		valid_urls = links.Links_col()
		for i in tag_a_elements:
			# print "---"
			# print i.get("href")				# Get only <a> with href
			try:
				# print i.get("href")[0:7]
				if(i.get("href")[0:7] == "http://" or i.get("href")[0:7] == "https://"):	# Keep hrefs that start w/ http; some don't have valid urls
					# print "valid URL"
					if(len(i.get("href")) < 50):
						valid_urls.insert(i.get("href"))

				else:
					# print "invalid URL"
					pass					# Don't keep urls with no "href"
			except TypeError:
				# print "TypeError detected"
				pass
		raw_valid_links_tot = valid_urls.get_total()
		# print "Valid URLs:"
		# valid_urls.print_links()
		if limit_domain:
			valid_urls.filter_for_domain(domain)

		in_domain_urls_tot = len(valid_urls.get_list())
		# valid_urls.print_links()	
		print "\ta, href items:", raw_valid_links_tot
		print "\tlinks in domain:", in_domain_urls_tot
		
		for link in valid_urls.get_list():		# With a list of links parsed, only put in those that aren't already on url frontier
			if link not in observed_urls:
				# link_to_goto = link
				# print "\tlink_to_goto:", link_to_goto
				outfile.write(link+"\n")
				observed_urls.append(link)
		return observed_urls
	except socket.timeout, e:
	    # print "Socket timeout"
	    return observed_urls
	except urllib2.URLError as e:
		# print "Urlerror"
		return observed_urls
	except urllib2.HTTPError, e: # http://stackoverflow.com/questions/666022/what-errors-exceptions-do-i-need-to-handle-with-urllib2-request-urlopen
	    # print 'HTTPError = ', str(e.code)
	    return observed_urls
	except urllib2.URLError, e:
	    # print 'URLError = ', str(e.reason)
	    return observed_urls
	# except httplib.HTTPException, e:
	#     print 'HTTPException'
	#     pass
	except Exception:
	    import traceback
	    print 'generic exception: ', traceback.format_exc()
	    return observed_urls

def main():
	outfile = open("out", "w")
	print "Starting crawler..."
	start_url = "http://www.tulane.edu"
	observed_urls = {}
	observed_urls[start_url] = 1000
	observed_urls = get_links(start_url, observed_urls, outfile, domain="tulane.edu", limit_domain=True)
	# outfile.write("\tObserved URLs:")
	print "observed urls:", observed_urls
	for url in observed_urls:
		print "\nVisit #:",visit_num
		# if url != None:
		# 	observed_urls.append(url)
		# url = get_links(url, observed_urls, domain="transy.edu", limit_domain=True)
		observed_urls = get_links(url, observed_urls, outfile, domain="tulane.edu", limit_domain=True)
		# print "observed_urls:", observed_urls	

main()