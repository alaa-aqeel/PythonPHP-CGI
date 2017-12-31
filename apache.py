from   http.server import *
import os,sys,logging,cgi,fwriter


class handler(CGIHTTPRequestHandler):

	def do_GET(self):
		sp_path = self.path.split("?");get = ""
		self.path = "www"+sp_path[0]
		if len(sp_path) > 1 :
			get = sp_path[1]

		fwriter.fwriter(self,get)

	# def do_POST(self):
	# 	sp_path = self.path.split("?");get = ""
	# 	self.path = "www"+sp_path[0]
	# 	if len(sp_path) > 1 :
	# 		get = sp_path[1]

	# 	fwriter.fwriter(self,post)



server = HTTPServer(("127.0.0.1",80),handler)
print("Run Server")

try:
	server.serve_forever()
except KeyboardInterrupt as er:
	pass


