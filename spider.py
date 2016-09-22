class Spider:
	def __init__(self):
		self.timeout = 2.0
		frontier_out = open("out", "w")
	self.my_domain = "uky.edu"
	self.start_url = "http://www."+my_domain
	
	url = start_url
	subdomains = set()
	robots = RobotsCache()
