import re

class Links_col:
	def __init__(self):
		# print "Initialize Links object"
		self.list_of_links = {}}
		self.total = 0

	def insert(self, link_str):
		'''
			Insert a link to the list of links
		'''
		if link_str not in self.list_of_links and link_str+"/" not in self.list_of_links:
			# self.list_of_links.append(link_str)
			self.list_of_links[link_str] = 0
			self.total += 1

	def get_list(self):
		'''
			Return the list of links
		'''
		return self.list_of_links

	def is_in_domain(self, link):
		regex = r"(.*"+domain+".*)"
		try:
			match = re.search(regex, link)
			# print match.group(0)
			if match != None:
				# self.filtered_list.append(match.group(0))
				return True
			else: 
				return False
		except AttributeError:
			return False

	def filter_for_domain(self, domain):
		'''
			Filter for links that are in domain
		'''
		# regex = r"(.*uky.edu.*)"
		regex = r"(.*"+domain+".*)"

		self.filtered_list = {}
		counter = 0
		for link, support in self.list_of_links.iteritems():
			try:
				match = re.search(regex, link)
				# print match.group(0)
				if match != None:
					# self.filtered_list.append(match.group(0))
					self.filtered_list[match.group(0)] = 
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
