from webtofeed import *

def test_getRssOfExample():
	f = open("testdata/basicouterlinktest.html","r")
	testdataFile = f.read()
	feed = parseString(testdataFile,"https://github.com/snipem/web-to-feed","h3")
	
	assert feed.title() == "Generated feed for https://github.com/snipem/web-to-feed"
	assert feed.subtitle() == "Autogenerated by alltorss.py based on tag h3"
	assert len(feed.entry()) == 4

	for entry in feed.entry():
		assert entry.link()[0]['href'][:7] == "http://"
		assert entry.link()[0]['href'][-4:] == ".com"
		assert " Link to " in entry.title()
