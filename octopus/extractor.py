import urllib2

import nltk, re, pprint
from nltk import word_tokenize
from bs4 import BeautifulSoup



def process_url(url):
	print '=======', url
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)

	decoded_resp = response.read().decode('utf8')

	soup = BeautifulSoup(decoded_resp)
	

	# kill all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# get text
	text = soup.get_text()

	

	# break into lines and remove leading and trailing space on each
	lines = (line.strip() for line in text.splitlines())

	# break multi-headlines into a line each
	chunks = (phrase.strip() for line in lines for phrase in line.split("  "))


	# drop blank lines
	pure_content = '\n'.join(chunk for chunk in chunks if chunk)#.encode('utf-8').strip()#.decode('utf-8')

	tokens = word_tokenize(pure_content)
	tagged = nltk.pos_tag(tokens)
	wanted = [word for word,pos in tagged if pos == 'NNP' or pos=='NNS' or pos=='VB' or pos == 'VBP']
	#wanted = [word for word,pos in tagged if pos == 'NNP'  or pos=='VB' ]
	text = nltk.Text(wanted)
	fdist = nltk.FreqDist(text).most_common()
	top_100 = fdist[:99]
	return dict(top_100)



