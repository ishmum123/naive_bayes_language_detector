from processor import Processor
from pickle import dump, load
from sys import argv


def readFile(file_name, language):
	with open(file_name) as f:
		for word in [w for l in f for w in l.split()]:
			processor.processWordInLanguage(word, language)

if __name__ == "__main__":
	processor = Processor()

	"""
	readFile("Les Colchiques.txt", "French")
	readFile("A Wise Old Owl.txt", "English")
	readFile("Verdades.txt", "Spanish")
	dump(processor.word_dict, open("word_dict.p", "wb"))
	dump(processor.language_dict, open("language_dict.p", "wb"))
	dump(processor.total_words, open("total_words.p", "wb"))
	"""

	processor.word_dict = load(open("word_dict.p", "rb"))
	processor.language_dict = load(open("language_dict.p", "rb"))
	processor.total_words = load(open("total_words.p", "rb"))

	lang_prob_list = []
	for i in range(1, len(argv)):
		lang_prob_list.extend(processor.getLanguageProbabilitiesFromWord(argv[i]))

	languages = {}

	for (lang, prob) in lang_prob_list:
		if lang in languages:
			languages[lang] += prob
		else:
			languages[lang] = prob
	
	sel_lang = None
	highest_prob = 0

	for lang in languages.keys():
		if languages[lang] > highest_prob:
			highest_prob = languages[lang]
			sel_lang = lang

	print(sel_lang)
