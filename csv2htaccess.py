#!/usr/bin/env python3

import urllib.parse

lines = """
http://www.example.com/foo/bar.php,https://foobar.net/product/laptop
http://www.example.com/foo/baz.php,https://foobar.net/product/desktop
http://www.example.com/foo/bom.php,https://foobar.net/product/tablet
"""

def main(lines):

	for l in lines.split("\n"):

		l = urllib.parse.unquote(l).strip()
		parts = l.split(",")

		if len(parts)!=2 or parts[1].strip()=='':
			continue

		outline = parsePath(parts[0].strip(), parts[1].strip())
		print(outline)

	return True



def parsePath(old, new):

	""""
	Redirect 301 /foo/bar.html https://example.com/baz.html
	"""

	template = "Redirect 301 %s %s"

	return template % (old, new)



if __name__=="__main__":
	main(lines)
