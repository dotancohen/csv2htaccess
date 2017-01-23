# csv2htaccess

Convert a CSV file of old,new URLs to an Apache .htacces file.



# Supported URL formats

## Standard paths

Turns this:

	http://www.example.com/foo/bom.php,https://foobar.net/product/tablet

Into this:

	Redirect 301 http://www.example.com/foo/bom.php https://foobar.net/product/tablet

## Query string parameters

Turns this:

	http://www.example.com/?ArticleID=42,https://foobar.net/article/We-are-the-best

Into this:

	RewriteCond %{REQUEST_URI}  ^/$
	RewriteCond %{QUERY_STRING} ArticleID=42
	RewriteRule ^(.*)$ https://foobar.net/article/We-are-the-best [R=302,L,NC]

## Full paths with multiple query string parameters

Turns this:

	http://www.example.com/foo/bar.php?Cat=20&Dog=50,https://foobar.net/product/mobile

Into this:

	RewriteCond %{REQUEST_URI}  ^/foo/bar.php$
	RewriteCond %{QUERY_STRING} Cat=20
	RewriteCond %{QUERY_STRING} Dog=50
	RewriteRule ^(.*)$ https://foobar.net/product/mobile [R=302,L,NC]



# Usage and Arguments

	usage: csv2htaccess.py [-h] [-e ENCODING] [-r REDIRECTCODE] [-u]
						   inputfile [outputfile]

	positional arguments:
	  inputfile             CSV file used as import data
	  outputfile            Filename to be used for .htaccess output.

	optional arguments:
	  -h, --help            show this help message and exit
	  -e ENCODING, --encoding ENCODING
							Character encoding to use for input and output files.
	  -r REDIRECTCODE, --redirectcode REDIRECTCODE
							HTTP Status Code to use for redirects.
	  -u, --urlencode       URL-encode output URLs.

