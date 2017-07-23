from string import punctuation


class Processor:
	def __init__(self):
		self.word_dict = {}
		self.language_dict = {}
		self.total_words = 0
		self.occurences = "occurences"
		
	def processWordInLanguage(self, word, language):
		word = self.sanitiseWord(word)
		language = self.sanitiseWord(language)
		self.processWord(word)
		self.processLanguage(language)
		self.addWordToLanguageOccurence(word, language)

	def addWordToLanguageOccurence(self, word, language):
		if word in self.language_dict[language]:
			self.language_dict[language][word] += 1
		else:
			self.language_dict[language][word] = 1

	def processLanguage(self, language):
		if language in self.language_dict:
			self.language_dict[language][self.occurences] += 1
		else:
			self.language_dict[language] = { self.occurences: 1 }

	def processWord(self, word):
		self.total_words += 1
		if word in self.word_dict:
			self.word_dict[word] += 1
		else:
			self.word_dict[word] = 1

	def sanitiseWord(self, word):
		translator = str.maketrans('', '', punctuation)
		return word.translate(translator).lower()
	
	def getBayesProbability(self, prob_b_given_a, prob_a, prob_b):
		prob_a_given_b = (prob_b_given_a * prob_a) / prob_b
		return prob_a_given_b

	def getLanguageProbabilitiesFromWord(self, word):
		lang_probabilities = []
		langs = list(self.language_dict.keys())
		for lang in langs: 
			prob_word_given_lang = (self.language_dict[lang][word] / self.language_dict[lang][self.occurences]) if word in self.language_dict[lang] else 0
			prob_word = (self.word_dict[word] / self.total_words) if word in self.word_dict else 0
			prob_lang = self.language_dict[lang][self.occurences] / self.total_words
			prob_lang_given_word = self.getBayesProbability(prob_word_given_lang, prob_lang, prob_word) if prob_word != 0 else 0
			lang_probabilities.append((lang, round(prob_lang_given_word, 2)))
		return lang_probabilities
