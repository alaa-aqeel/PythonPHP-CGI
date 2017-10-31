import cgi, cgitb
from   http.server import *
import os,sys,logging,glob,re
import subprocess as sub


class handler(CGIHTTPRequestHandler):

	def phpCGI(self,file,**kw):
		# Parser agrv
		kw_agrv = ""
		for k,v in kw.items():
			kw_agrv += k+"="+v+" "

		# Run CGI php 
		cmd = sub.Popen("php-cgi %s %s"%(file,kw_agrv),shell=True,stdout=sub.PIPE)
		fread = cmd.communicate()[0].decode()
		finsh = fread.strip("X-Powered-By: PHP/7.1.8\r\nContent-type: text/html; charset=UTF-8\r\n\r\n\n\n")
		return finsh.encode("u8")

	def do_GET(self):
		sp_path = self.path.split("?");get = {}
		self.path = sp_path[0]
		if len(sp_path) > 1 :
			get = sp_path[1]

		if self.path.endswith(".css"):
			"../view/css/"+self.path.strip("/")
			self.send_response(200)  # OK
			self.send_header('Content-type', 'text/css') # send type # _type from config.py
			self.end_headers()
			self.wfile.write((open("view/"+self.path.strip("/"),"r").read()).encode("u8"))
		elif self.path.endswith(".js"):
			self.send_response(200)  # OK
			self.send_header('Content-type', 'text/javascript') # send type # _type from config.py
			self.end_headers()
			self.wfile.write((open("view/"+self.path.strip("/"),"r").read()).encode("u8"))
		elif self.path.endswith(".php"):
			self.send_response(200)  # OK
			self.send_header('Content-type', 'text/html') # send Content-type
			self.end_headers() # close headers
			self.wfile.write(self.phpCGI("."+self.path,**dict(cgi.parse_qsl(get))))

		elif self.is_python(self.path):
			self.cgi_directories = ["/"]
			self.is_cgi()
			self.run_cgi()

		else:
			self.send_error(404, 'file not found -> %s'%self.path)

server = HTTPServer(("127.0.0.1",8000),handler)
print("Run Server 127.0.0.1:8000")
server.serve_forever()
