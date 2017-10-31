import cgi
# Header
print("Content-type: text/html")
print()

print("<h1>Hello World</h1>")

# Print GET argv
print(cgi.parse())

