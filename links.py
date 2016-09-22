import re
from bs4 import BeautifulSoup

class Url_Frontier:
	def __init__(self):
		# print "Initialize Links object"
		self.list_of_links = []
		self.total = 0
		self.filetypes = {"text/html":1}
		self.subdomains = set()
		self.slow_subdomains = set()

		self.finish_parsed = 0
		self.request_error = 0
		self.skipped = 0
		self.filetypes_percent;

	def add_links(self, site):
		'''
			Parse html to get <a href>'s
		'''
		site_soup = BeautifulSoup(site, "html.parser")			# Convert to tree of tags soup object
		tag_a_elements = site_soup.find_all("a")		# Get all tags <a> from tag tree
		for i in tag_a_elements:
				# print "---"
				# print i.get("href")				# Get only <a> with href
				try:
					# print i.get("href")[0:7]
					if(i.get("href")[0:7] == "http://" or i.get("href")[0:7] == "https://"):	# Keep hrefs that start w/ http; some don't have valid urls
						# print "valid URL"
						self.insert(i.get("href"))
					else:
						# print "invalid URL"
						pass					# Don't keep urls with no "href"
				except TypeError:
					# print "TypeError detected"
					pass
	
	def insert(self, link_str):
		'''
			Insert a link to the list of links
		'''
		if link_str not in self.list_of_links and link_str+"/" not in self.list_of_links:
			self.list_of_links.append(link_str)
			self.total += 1
	def insert_unique_subdomain(self, subdomain):
		if subdomain not in self.subdomains and subdomain != None:
			self.subdomains.add(subdomain)
	def get_list(self):
		'''
			Return the list of links
		'''
		return self.list_of_links

	def get_subdomain(self, link_str, domain):
		'''
			Get subdomain from url with regex
		'''
		# print "in get_subdomain"
		# print "domain:", domain
		# print "link:", link_str
		# regex = r"http:\/\/?([^.]+)\.?uky\.edu"
		regex = r"http:\/\/?(.*)\.uky\.edu"
		match = re.search(regex, link_str)
		try:
			if match != None:
				# print "match group0:", match.group(0)
				# print "match group1:", match.group(1)
				return match.group(1)
		except AttributeError:
			return "regex error"

	def filter_for_domain(self, domain):
		'''
			Filter for links that are in domain
		'''
		# regex = r"(.*uky.edu.*)"
		# print "Filtering domain..."
		regex = r"(.*"+domain+".*)"
		# regex2 = r"(https?:\/\/).*(\/).*(uky\.edu)"

		self.filtered_list = []
		counter = 0
		for link in self.list_of_links:
			try:
				match = re.search(regex, link)
				# print match.group(0)
				if match != None:
					self.filtered_list.append(match.group(0))
					counter += 1

			except AttributeError:
				pass
		self.list_of_links = self.filtered_list

	def get_total(self):
		return self.total

	def print_links(self):
		for link in self.list_of_links:
			print link

	# def make_unique(self):
	# 	'''
	# 		Modify list so that it contains unique set of items
	# 	'''
	# 	unique_list = []
	# 	for item in self.list_of_links:
	# 		if (item not in unique_list) and (item+"/" not in unique_list):
	# 			unique_list.append(item)
	# 	# return unique_list
	# 	self.list_of_links = unique_list
