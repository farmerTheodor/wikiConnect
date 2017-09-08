from __future__ import division
from wikiData import wikiPageData, catagory, link
class wikiSimilarity(object):
	"""docstring for wikiSimilarity"""
	def __init__(self, wikiStart, wikiEnd):
		super(wikiSimilarity, self).__init__()
		self.firstPage = wikiStart
		self.secondPage = wikiEnd
		#numML = num matched Letters

		self.numMLTitleTitle =0
		self.numMLTitleSubject =0
		self.numMLTitleNoun =0
		self.numMLTitleOriginalLink =0
		self.numMLTitleMostUsedWord = 0
		self.numMLNameTitle = 0
		self.numMLNameSubject = 0
		self.numMLNameNoun = 0
		self.numMLNameOriginalLink = 0
		self.numMLNameMostUsedWord = 0
		self.numMLTextTTitle = 0
		self.numMLTextTSubject = 0
		self.numMLTextTNoun = 0
		self.numMLTextTOriginal = 0
		self.numMLTextTMostUsedWord = 0
		self.numMLLinkTitle = 0
		self.numMLLinkSubject = 0
		self.numMLLinkNoun = 0
		self.numMLLinkOriginalLink = 0
		self.numMLLinkMostUsedWord = 0

		#percML = percent matched letters

		self.percMLTitleTitle = 0
		self.percMLTitleSubject = 0
		self.percMLTitleNoun = 0
		self.percMLTitleOriginalLink = 0
		self.percMLTitleMostUsedWord = 0
		self.percMLLinkTitle = 0
		self.percMLLinkSubject = 0
		self.percMLLinkNoun = 0
		self.percMLLinkOriginalLink = 0
		self.percMLLinkMostUsedWord = 0
		self.percMLNameTitle = 0
		self.percMLNameSubject = 0
		self.percMLNameNoun = 0
		self.percMLNameOriginalLink = 0
		self.percMLNameMostUsedWord = 0
		self.percMLTextTTitle = 0
		self.percMLTextTSubject = 0
		self.percMLTextTNoun = 0
		self.percMLTextTOriginal = 0
		self.percMLTextTMostUsedWord = 0
		self.lenghOfLinkWord = 0

		self.findAllNumML()
		self.findAllPercML()

	def findAllNumML(self):
		for catagories in self.firstPage.catagoriesOfPage:
			totalScore = 0
			catagorieScore = 0
			print catagories.nameOfCatagory
			print "_____________name Of Catagory_________________"
			catagorieScore = catagorieScore + self.findTitleNumML(catagories.nameOfCatagory)
			catagorieScore = catagorieScore + self.findSubjectNumMl(catagories.nameOfCatagory)
			catagorieScore = catagorieScore + self.findNounNumMl(catagories.nameOfCatagory)
			catagorieScore = catagorieScore + self.findMostUsedWordNumMl(catagories.nameOfCatagory)
			print catagorieScore
			totalScore = totalScore + catagorieScore
			for nouns in catagories.capitilizedWords:
				print nouns	
				nounScore = 0
				print "_______________noun_______________"
				nounScore = nounScore + self.findTitleNumML(nouns)
				nounScore = nounScore + self.findSubjectNumMl(nouns)
				nounScore = nounScore + self.findNounNumMl(nouns)
				nounScore = nounScore + self.findMostUsedWordNumMl(nouns)
				print nounScore
				totalScore = totalScore + nounScore
			
			self.textFindNumMl(catagories)
			print "total Score = " + str(totalScore)
			print " _______________________ "

	def textFindNumMl(self, catagories):
		setOfLinksInSentence = []
		print "_______________link_________"
		print catagories.listOfInformation
		for text in catagories.listOfInformation:
			textScore = 0
			if text is link:
				setOfLinksInSentence.append(text)	
				textScore = textScore + self.findTitleNumML(text.nameOfLink)
				textScore = textScore + self.findSubjectNumMl(text.nameOfLink)
				textScore = textScore + self.findNounNumMl(text.nameOfLink)
				textScore = textScore + self.findMostUsedWordNumMl(text.nameOfLink)	
			else:
				if "." in text:
					if len(setOfLinksInSentence) > 0:
						for links in setOfLinksInSentence:
							links.score = links.score + textScore
							print link.nameOfLink + " = " + str(link.score)
					del setOfLinksInSentence[:]
					textScore = 0
				else:
					textScore = textScore + self.findTitleNumML(text)
					textScore = textScore + self.findSubjectNumMl(text)
					textScore = textScore + self.findNounNumMl(text)
					textScore = textScore + self.findMostUsedWordNumMl(text)


	def findTitleNumML(self,word):
		numMl = self.findMatchedLetters(word, self.secondPage.nameOfPage)
		return numMl
	def findSubjectNumMl(self,word):
		numMl = 0
		for catagories in self.secondPage.catagoriesOfPage:
			numMl = numMl + self.findMatchedLetters(word, catagories.nameOfCatagory)
		return numMl
	def findNounNumMl(self,word):
		numMl = 0
		for catagories in self.secondPage.catagoriesOfPage:
			for noun in catagories.capitilizedWords:
				numMl = numMl + self.findMatchedLetters(word, noun)
		return numMl

	def findMostUsedWordNumMl(self,word):
		numMl = 0
		for catagories in self.secondPage.catagoriesOfPage:
			numMl = numMl + self.findMatchedLetters(word,  catagories.mostUsedWord)
		return numMl
	def findAllPercML(self):
		pass
		

	def findTitlePercML(self):
		pass
	def findSubjectPercMl(self):
		pass
	def findNounPercMl(self):
		pass
	def findOriginalLinkPercMl(self):
		pass
	def findMostUsedWordPercMl(self):
		pass

	def findMatchedLetters(self, wordOne, wordTwo):
		matchedLetters = 0
		if len(wordOne) <= len(wordTwo):
			lettersTwo = list(wordTwo)
			for letter in wordOne:
				if lettersTwo[matchedLetters] != letter:
					break
				matchedLetters = matchedLetters + 1
		else:
			lettersOne = list(wordOne)
			for letter in wordTwo:
				if lettersOne[matchedLetters] != letter:
					break
				matchedLetters = matchedLetters + 1
		return matchedLetters

	def findPercentMatchedLetters(self,wordOne, wordTwo):
		matchedLetters = 0
		percentMatched = 0.0
		if len(wordOne) <= len(wordTwo):
			lettersTwo = list(wordTwo)
			for letter in wordOne:
				if lettersTwo[matchedLetters] != letter:
					break
				matchedLetters = matchedLetters + 1
			percentMatched = (matchedLetters / len(wordOne)) * 100
		else:
			lettersOne = list(wordOne)
			for letter in wordTwo:
				if lettersOne[matchedLetters] != letter:
					break
				matchedLetters = matchedLetters + 1
			percentMatched = (matchedLetters/len(wordTwo)) * 100
		return percentMatched
