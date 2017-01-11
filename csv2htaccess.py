#!/usr/bin/env python3

import argparse
import sys
import urllib.parse


def main(args):

	lines = getCsvLines(args.inputfile)

	for l in lines:

		l = urllib.parse.unquote(l).strip()
		parts = l.split(",")

		if len(parts)!=2 or parts[1].strip()=='':
			continue

		outline = parseCsvLine(parts[0].strip(), parts[1].strip())
		print(outline)

	return True



def getCsvLines(filename):

	try:
		with open(filename, mode='r', encoding='utf-8') as lines:
			for line in lines:
				yield line

	except FileNotFoundError:
		print('Input file "' + filename + '" not found.')
		sys.exit(-1)

	return False



def parseCsvLine(old, new):

	old_parts = urllib.parse.urlparse(old)
	path = old_parts.path
	qs = urllib.parse.parse_qsl(old_parts.query)

	if parseCsvLine.previousQS:
		prevNewLine = "\n"
	else:
		prevNewLine = ""

	if len(qs)==0:
		parseCsvLine.previousQS = False
		return prevNewLine + parsePath(old, new)

	parseCsvLine.previousQS = True
	return parseQueryString(path, qs, new)

parseCsvLine.previousQS = False



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
	parser = argparse.ArgumentParser()

	parser.add_argument('inputfile', help='CSV file used as import data')

	args = parser.parse_args()
	main(args)
