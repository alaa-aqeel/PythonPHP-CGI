import os,cgi,subprocess as sub


class fcgi:
	Header = None

	def php(self,file,**kw):
		# Parser agrv
		kws = self.argv(kw)

		# Run CGI php 
		cmd = sub.Popen("php-cgi ./%s %s"%(file,kws),shell=True,stdout=sub.PIPE)
		fread = cmd.communicate()[0].decode("u8").split("\r\n\r\n")
		# print(fread.pop(0).split("\r\n"))
		self.Header = dict([tuple(i.split(":")) for i in fread.pop(0).split("\r\n")])
		return str(fread[0]).encode("u8")

	def argv(self,kw):
		dkw = ""
		for k,v in kw.items():
			dkw += k+"="+v+" "
		return dkw

	def python(self,file,**kw):
		# Parser agrv
		kws = self.argv(kw)

		# Run CGI php 
		cmd = sub.Popen("python -u ./%s %s"%(file,kws),shell=True,stdout=sub.PIPE)
		fread = cmd.communicate()[0].decode("u8").split("\r\n\r\n")
		
		self.Header = dict([tuple(i.split(":")) for i in fread.pop(0).split("\r\n")])
		return str("".join(fread)).encode("u8")

class fwriter(fcgi):
	def __init__(self,main,get):
		self.path  = main.path
		main.cgi_directories = ["/www","/"]
		# CSS 
		if self.path.endswith(".css"):
			self.sendHeader(main,"css")
			main.wfile.write((open(self.path,"r").read()).encode("u8"))
		# JavaScript
		elif self.path.endswith(".js"):
			self.sendHeader(main,'javascript') # send type # _type from config.py
			main.wfile.write((open(self.path,"r").read()).encode("u8"))
		# Html Page
		elif self.path.endswith(".html"):
			self.sendHeader(main,"html")
			main.wfile.write((open(self.path,"r").read()).encode("u8"))
		# CGI PHP 
		elif self.path.endswith(".php"):
			self.sendHeader(main,"html")

			main.wfile.write(self.php(self.path,**dict(cgi.parse_qsl(get))))
		# CGI Python 
		elif main.is_python(self.path):
			self.sendHeader(main,"html")
			main.wfile.write(self.python(self.path,**dict(cgi.parse_qsl(get))))

		else:
			if self.path == "www/":
				self.sendHeader(main,"html")
				if os.path.exists("www/index.php"):
					main.wfile.write(self.php("www/index.php",**dict(cgi.parse_qsl(get))))
				elif os.path.exists("www/index.html"):
					main.wfile.write((open("www/index.html","r").read()).encode("u8"))
				else:
					main.wfile.write(b"<h1> Not Index </h1>")
			else:
				main.send_error(404, 'file not found -> %s'%self.path)
		

	def sendHeader(self,main,types):
		main.send_response(200)  # OK
		main.send_header('Content-type', 'text/'+types) # send type # _type from config.py
		main.end_headers()
