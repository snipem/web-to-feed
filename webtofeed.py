from bs4 import BeautifulSoup
from bs4 import Tag
import requests
import sys
import argparse

if sys.version_info[0] == 2:
	from urlparse import urlparse
else:
	from urllib.parse import urlparse

from feedgen.feed import FeedGenerator

maxlinkHighness = 2

def linkIsAbsolute(url):
	return bool(urlparse(url).netloc)

def findInnerLink(item):
	a = item.find('a')

	if isinstance(a, Tag):
		return a
	else:
		return None

def findOuterLink(item):
	return getParentWithLink(item, 0)

def getParentWithLink(item, linkHeigth):

	if (linkHeigth <= maxlinkHighness):
		link = item.find('a')

		if isinstance(link, Tag):
			return link
		else:
			returnedLink = getParentWithLink(item.parent, linkHeigth+1)
			if isinstance(returnedLink, Tag):
				return returnedLink
	else:
		return None

def parseUrl(url, tag):

	r = requests.get(url)

	if (r.status_code != 200):
		sys.stderr.write("Error code is "+ str(r.status_code)+"\n")
		exit(1)

	html = r.text
	parsed_html = BeautifulSoup(html)

	parsedUrl = urlparse(url)
	baseUrl = parsedUrl.scheme+"://"+parsedUrl.netloc

	fg = FeedGenerator()
	fg.id(url)
	fg.title('Generated feed for ' + url)
	fg.link( href=url, rel='alternate' )
	fg.subtitle('Autogenerated by alltorss.py based on tag ' + tag)

	for item in parsed_html.body.find_all(tag):
		topic = item.text.strip()

		#check if item contains a link
		innerLink = findInnerLink(item)
		outerLink = findOuterLink(item)

		if (innerLink != None):
			link = innerLink
		elif (outerLink != None):
			link = outerLink
		else:
			link = None

		if isinstance(link, Tag) and link.has_attr('href'):

			linkHref = link['href']

			fe = fg.add_entry()

			if (linkIsAbsolute(linkHref)):
				fullLink = linkHref
			else:
				fullLink = baseUrl + linkHref
			
			fe.id(fullLink)
			fe.title(topic)
			fe.link( href=fullLink )

	rssfeed  = fg.rss_str(pretty=True)
	return rssfeed

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--url", help="URL to be parsed")
	parser.add_argument("--tag", help="Tag that encapsulates news content")

	args = parser.parse_args()

	url = args.url
	tag = args.tag

	rssfeed = parseUrl(url, tag)

	if (sys.version_info[0] == 2):
		print (rssfeed)
	else:
		sys.stdout.buffer.write(rssfeed)

if __name__ == "__main__":
    main()