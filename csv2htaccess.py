#!/usr/bin/env python3

import urllib.parse

lines = """
http://www.example.com/foo/bar.php,https://foobar.net/product/laptop
http://www.example.com/foo/baz.php,https://foobar.net/product/desktop
http://www.example.com/foo/bom.php,https://foobar.net/product/tablet
http://www.example.com/?ArticleID=42,https://foobar.net/article/We-are-the-best
http://www.example.com/?CategoryID=2&ArticleID=100,https://foobar.net/article/We-sell-for-less
http://www.example.com/?CategoryID=4&ArticleID=101,https://foobar.net/article/We-have-higher-quality
"""

def main(lines):

	for l in lines.split("\n"):

		l = urllib.parse.unquote(l).strip()
		parts = l.split(",")

		if len(parts)!=2 or parts[1].strip()=='':
			continue

		outline = parseCsvLine(parts[0].strip(), parts[1].strip())
		print(outline)

	return True



def parseCsvLine(old, new):

	old_parts = urllib.parse.urlparse(old)
	path = old_parts.path
	qs = urllib.parse.parse_qsl(old_parts.query)

	if len(qs)==0:
		return parsePath(old, new)

	return parseQueryString(path, qs, new)



def parseQueryString(path, qs, new):

	""""
	RewriteCond %{REQUEST_URI}  ^/$
	RewriteCond %{QUERY_STRING} foo=bar
	RewriteRule ^(.*)$ http://example.com/baz.html [R=302,L,NC]
	"""

	template = """
RewriteCond %%{REQUEST_URI}  ^%s$%s
RewriteRule ^(.*)$ %s [R=302,L,NC]"""

	qs_cond_template = "\nRewriteCond %%{QUERY_STRING} %s=%s"
	qs_conditions = ""

	for q in qs:
		qs_conditions+= qs_cond_template % (q[0], q[1])

	return template % (path, qs_conditions, new)



def parsePath(old, new):

	""""
	Redirect 301 /foo/bar.html https://example.com/baz.html
	"""

	template = "Redirect 301 %s %s"

	return template % (old, new)



if __name__=="__main__":
	main(lines)
