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
