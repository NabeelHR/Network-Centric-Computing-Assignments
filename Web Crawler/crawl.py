from bs4 import BeautifulSoup #as soup
from urllib.request import urlopen

import requests
import validators

url1 = 'http://lol.com/'
url2 = 'http://carameltechstudios.com/'
url3 = 'http://learnyouahaskell.com/'
url4 = 'http://goal.com'
url5 = 'http://top10songs.com/'


url = url3

print (url + '\n')
set_links = {url}

def get_single_data(item_url):
	source_code = requests.get(item_url)
	plaintext = source_code.text
	retset = set()
	Mysoup = BeautifulSoup(plaintext, features="html.parser")
	for coolink in Mysoup.findAll('a'):
		links = coolink.get('href')

		try:
			links = links.split('#')[0]
			if '.com' not in links and not validators.url(links):
				links = url + links
		except:
			continue

		link_domain =  links.split("//")[-1].split("/")[0].split('?')[0]
		url_domain = item_url.split("//")[-1].split("/")[0].split('?')[0]
		if link_domain == url_domain and links not in set_links:
			set_links.add(links)
#			print ("^^" + links)
			retset.add(links)
	for item in retset:
		get_single_data(item)


get_single_data(url)
i=0
for item in set_links:
	source_code = requests.get(item)
	name = 'htmlpage' + str(i) + '.html'
	i+=1
	plaintext = source_code.text
	with open(name, "w") as file:
	    file.write(plaintext)
	    file.close()



print (len(set_links), ' URLs scraped and crawled through')