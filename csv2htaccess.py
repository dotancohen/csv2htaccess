#!/usr/bin/env python3

import argparse
import sys
import urllib.parse
from pprint import pprint


def main(args:argparse.Namespace):

	lines = getCsvLines(args.inputfile, args.encoding)

	code = int(args.redirectcode)
	outfile = False

	for l in lines:

		if not outfile:
			# Run the iterator before creating the output file
			outfile = getOutputFile(args.outputfile, args.inputfile, args.encoding)

		l = urllib.parse.unquote(l).strip()
		parts = l.split(",")

		if len(parts)!=2 or parts[1].strip()=='':
			continue

		outline = parseCsvLine(code, parts[0].strip(), parts[1].strip())
		outfile.write(outline + "\n")


	outfile.close()
	return True



def getCsvLines(filename:str, encoding:str):

	try:
		with open(filename, mode='r', encoding=encoding) as lines:
			for line in lines:
				yield line

	except FileNotFoundError:
		print('Input file "' + filename + '" not found.')
		sys.exit(-1)



def getOutputFile(filename:str, filename_in:str, encoding:str):

	if filename=='':
		filename_out = filename_in + '.htaccess'

	else:
		filename_out = filename

	outfile = open(filename_out, mode='w', encoding=encoding)

	return outfile



def parseCsvLine(code:int, old:str, new:str):

	old_parts = urllib.parse.urlparse(old)
	path = old_parts.path
	qs = urllib.parse.parse_qsl(old_parts.query)

	if parseCsvLine.previousQS:
		prevNewLine = "\n"
	else:
		prevNewLine = ""

	if len(qs)==0:
		parseCsvLine.previousQS = False
		return prevNewLine + parsePath(code, old, new)

	parseCsvLine.previousQS = True
	return parseQueryString(code, path, qs, new)

parseCsvLine.previousQS = False



def parseQueryString(code:int, path:str, qs:list, new:str):

	""""
	RewriteCond %{REQUEST_URI}  ^/$
	RewriteCond %{QUERY_STRING} foo=bar
	RewriteRule ^(.*)$ http://example.com/baz.html [R=302,L,NC]
	"""

	template = """
RewriteCond %%{REQUEST_URI}  ^%s$%s
RewriteRule ^(.*)$ %s [R=%d,L,NC]"""

	qs_cond_template = "\nRewriteCond %%{QUERY_STRING} %s=%s"
	qs_conditions = ""

	for q in qs:
		qs_conditions+= qs_cond_template % (q[0], q[1])

	return template % (path, qs_conditions, new, code)



def parsePath(code:int, old:str, new:str):

	""""
	Redirect 301 /foo/bar.html https://example.com/baz.html
	"""

	template = "Redirect %d %s %s"

	return template % (code, old, new)



if __name__=="__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument('inputfile', help='CSV file used as import data')
	parser.add_argument('outputfile', nargs='?', default='', help='Filename to be used for .htaccess output.')
	parser.add_argument('-e', '--encoding', default='utf-8', help='Character encoding to use for input and output files.')
	parser.add_argument('-r', '--redirectcode', default='302', help='HTTP Status Code to use for redirects.')

	args = parser.parse_args()
	main(args)
