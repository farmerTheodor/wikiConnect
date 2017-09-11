
#!/usr/bin/python3
import urllib2
from wikiConnection import wikiSimilarity
from wikiData import wikiPageData, catagory, link
from bs4 import BeautifulSoup

def retrievePage(urlToRetrieve):
	openedPage = urllib2.urlopen(urlToRetrieve)
	soupReturn = BeautifulSoup(openedPage, 'html.parser')
	openedPage.close()
	return soupReturn

def main():
	startingUrl = 'https://en.wikipedia.org/wiki/East_African_Portland_Cement_Company'
	finalUrl = 'https://en.wikipedia.org/wiki/Porth_Hellick_Down'
	startingSoup = retrievePage(startingUrl)
	finalSoup = retrievePage(finalUrl)
 	currentWikidata = wikiPageData(startingUrl, startingSoup)
 	finalWikidata = wikiPageData(finalUrl, finalSoup)
 	drawConnections = wikiSimilarity(currentWikidata, finalWikidata)
 	

if __name__ == '__main__':
	main()
