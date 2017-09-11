#file: wikiData.py
import copy
import re
import string
class wikiPageData(object):
	"""docstring for wikiPageData"""
	def __init__(self, arg,soup):
		super(wikiPageData, self).__init__()
		self.url = arg
		self.nameOfPage = ""
		self.soupOfPage = soup
		self.catagoriesOfPage = []
		self.getNameOfPage()
		self.getCatagory()
		self.mergeAllLinksToInfoLists()

	def getNameOfPage(self):
		name = self.soupOfPage.find('h1')
		self.nameOfPage = name.text.strip()

	def getCatagory(self):
		startingInfo = self.soupOfPage.find('h1')
		self.catagoriesOfPage.append(catagory(startingInfo))
		for header in self.soupOfPage.find_all('span', attrs={'class': 'mw-headline'}):
			parent = header.find_parent()
			#print parent.text.strip()
			if parent.name == 'h2':
				if header.text.strip() == "References" or header.text.strip() == "Notes" or header.text.strip() == "External links":
					break
				self.catagoriesOfPage.append(catagory(header))

	def mergeAllLinksToInfoLists(self):
		for catagory in self.catagoriesOfPage:
			groupWord = ""
			currentIndex = 0
			word = catagory.textContent.split(" ")
			setBack = 0
			wordToPutIn = None
			while currentIndex < len(word):
				if len(word[currentIndex]) > 0:
					#groupWord is a combination of words to account for the links that have spaces in them
					groupWord = groupWord + word[currentIndex]
					#if it matches with something it keeps adding to the groupword
					potentialMatch = 0
					for otherCatagories in self.catagoriesOfPage:
						potentialMatch, wordToPutIn = self.checkForLinks(otherCatagories.href, groupWord ,potentialMatch, wordToPutIn)
					if not potentialMatch:
						if wordToPutIn != None:
							#a link was found 
							catagory.listOfInformation.append(wordToPutIn.nameOfLink)
							#catagory.listOfInformation.append(word[currentIndex])
							wordToPutIn = None
							setBack = 1
						else:
							#not a single link was found so we break the group word and insert it into the list
							catagory.listOfInformation.append(groupWord.split(" ")[0])	

						#resets back to the next word from the starting word
						groupWord = ""
						currentIndex = currentIndex - setBack
						setBack = 0
					else:
						setBack = setBack + 1
						groupWord = groupWord + " "
				currentIndex = currentIndex + 1
			#catagory.printListOfInformation()


	def checkForLinks(self, arrayOfLinks, word, potentialMatch, wordToPutIn ):
		for link in arrayOfLinks:
			#checks all links and selects the one that is exactly like the groupword
			if word.lower() in link.nameOfLink.lower():
				potentialMatch = 1
				if len(word) == len(link.nameOfLink):
					#print word.lower() + " == " + link.nameOfLink.lower()
					#an exact match is found
					#if another link with more detail is found then we will use that link instead
					wordToPutIn = link

		return (potentialMatch, wordToPutIn)

class catagory(object):
	"""docstring for catagory"""
	def __init__(self, header):
		super(catagory, self).__init__()
		self.startOfSoup = header
		self.nameOfCatagory = ""
		self.textContent = ""
		self.mostUsedWord = ""
		self.listOfInformation = []
		self.uniqueWords = []
		self.frequencyWords = {}
		self.capitilizedWords = []
		self.href = []
		self.getCatagoryName()
		self.getParagraph()
		self.cleanParagraph()
		self.cleanPunctuation()
		self.getCapitilizedWords()
		self.getUniqueWords()

	def printListOfInformation(self):
		for element in self.listOfInformation:
			if element is link:
				print element.nameOfLink +" ",
			else:
				print element,

	def getCatagoryName(self):
		self.nameOfCatagory = self.startOfSoup.text.strip()
		#print  self.nameOfCatagory

	def getParagraph(self):
		elementToBeSorted = self.startOfSoup.find_next()
		#print "__________new catagory________________"
		while 1:
			if elementToBeSorted.name == 'p' or elementToBeSorted.name == 'li':
				self.textContent = " " + self.textContent + elementToBeSorted.text.strip()				
			elif elementToBeSorted.name == 'a':

				if elementToBeSorted.text.strip() != 'edit'  and '[' not in elementToBeSorted.text.strip() and 'href' in elementToBeSorted.attrs:
					#removes all non wikipedia page links and images 
					if ':' not in elementToBeSorted['href'] and '/wiki/' in elementToBeSorted['href'] and  '.' not in elementToBeSorted['href']:
						self.href.append(link(elementToBeSorted))
			elif elementToBeSorted.name == 'h2':
				#print 'next catagory'				
				break
			elementToBeSorted = elementToBeSorted.find_next()
		#print "_______________________________________"
	
	def cleanParagraph(self):
		self.textContent = re.sub("(\[.\])|\n"," ", self.textContent)
		
	def cleanPunctuation(self):
		self.textContent = re.sub("[!-&]|[\(-\-]|\/|[:-@]|[\[-]|[{-~]", " ",  self.textContent)
		self.textContent = re.sub("[.]", " . ",  self.textContent)
	


	def getUniqueWords(self):
		unUniqueWords = self.textContent.split(" ")
		numMostUsedWord = 0
		for word in unUniqueWords:
			if len(word) > 1:
				if word.lower() not in self.uniqueWords:
					self.uniqueWords.append(word.lower());
					self.frequencyWords[word.lower()] = 1
					if numMostUsedWord < 1:
						self.mostUsedWord = word
				else:
					self.frequencyWords[word.lower()] = self.frequencyWords[word.lower()] + 1
					if numMostUsedWord < self.frequencyWords[word.lower()]:
						self.mostUsedWord = word.lower()
		#print self.mostUsedWord

	def getCapitilizedWords(self):
		unUniqueWords = self.textContent.split(" ")
		previousWord = " ."
		for word in unUniqueWords:
			if len(word) != 0 and word.istitle() and "." not in previousWord:
				word = re.sub("[!-/]|[:-@]|[\[-`]|[{-~]", " ",  word)
				if word.lower() not in self.capitilizedWords:
					self.capitilizedWords.append(word.lower());
			previousWord = word

class subCatagory(object):
	"""docstring for subCatagory"""
	def __init__(self, arg):
		super(subCatagory, self).__init__()
		self.arg = arg

class link(object):
	"""docstring for link"""
	def __init__(self, tag):
		super(link, self).__init__()
		self.linkTag = tag
		self.nameOfLink = tag.text.strip()
		self.linkWord = tag['href'][6:]
		self.linkWord = re.sub("(#\w*$)", "",  self.linkWord)
		self.linkWord = re.sub("_", " ",  self.linkWord)
		self.linkWord = re.sub("%27", "'",  self.linkWord)
		self.linkHref = 'https://en.wikipedia.org' + tag['href']
		self.score = 1
