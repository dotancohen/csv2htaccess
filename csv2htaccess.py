#!/usr/bin/env python3

import argparse
import sys
import urllib.parse


def main(args):

	encoding = 'utf8' # TODO: Option

	lines = getCsvLines(args.inputfile, encoding)

	outfile = getOutputFile(args.outputfile, args.inputfile, encoding)

	for l in lines:

		l = urllib.parse.unquote(l).strip()
		parts = l.split(",")

		if len(parts)!=2 or parts[1].strip()=='':
			continue

		outline = parseCsvLine(parts[0].strip(), parts[1].strip())
		outfile.write(outline + "\n")


	outfile.close()
	return True



def getCsvLines(filename, encoding):

	try:
		with open(filename, mode='r', encoding=encoding) as lines:
			for line in lines:
				yield line

	except FileNotFoundError:
		print('Input file "' + filename + '" not found.')
		sys.exit(-1)

	return False



def getOutputFile(filename, filename_in, encoding):

	if filename=='':
		filename_out = filename_in + '.htaccess'

	else:
		filename_out = filename

	outfile = open(filename_out, mode='w', encoding=encoding)

	return outfile



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
	parser.add_argument('outputfile', nargs='?', default='', help='Filename to be used for .htaccess output')

	args = parser.parse_args()
	main(args)
