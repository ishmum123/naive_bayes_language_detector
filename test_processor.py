from unittest import TestCase
from processor import Processor

class FakeProcessor(Processor):
	def __init__(self):
		super().__init__()
		self.word = None
		self.language = None
		
	def sanitiseWord(self, word):
		# bad design
		if self.word == None:
			self.word = word
		else:
			self.language = word
		return word



class TestProcessor(TestCase):
	def setUp(self):
		self.processor = Processor()
		self.test_word = "testword"
		self.test_language = "testlanguage"
		self.processor = Processor()
		self.test_number = 10

	def test_processWordInLanguage_saves_word(self):
		self.processor.processWordInLanguage(self.test_word, self.test_language)
		self.assertTrue(self.test_word in self.processor.word_dict)
		

	def test_processWordInLanguage_saves_number_of_occurences_of_word(self):
		for i in range(1, self.test_number):
			self.processor.processWordInLanguage(self.test_word, self.test_language)
			self.assertEqual(self.processor.word_dict[self.test_word], i)

	def test_processWordInLanguage_saves_language(self):
		self.processor.processWordInLanguage(self.test_word, self.test_language)
		self.assertTrue(self.test_language in self.processor.language_dict)

	def test_processWordInLanguage_saves_number_of_occurences_of_language(self):
		for i in range(1, self.test_number):
			self.processor.processWordInLanguage(self.test_word, self.test_language)
			self.assertEqual(self.processor.language_dict[self.test_language]["occurences"], i)

	def test_processWordInLanguage_saves_number_occurences_of_word_in_language(self):
		for i in range(1, self.test_number):
			self.processor.processWordInLanguage(self.test_word, self.test_language)
			self.assertEqual(self.processor.language_dict[self.test_language][self.test_word], i)

	def test_processWordInLanguage_saves_different_words_and_their_number_of_occurences(self):
		test_str = ["test1", "test2", "test3", "test4", "test6"]
		for j in range(1, 5):
			for i in range(1, j):
				self.processor.processWordInLanguage(test_str[j - 1], self.test_language)
				self.assertEqual(self.processor.language_dict[self.test_language][test_str[j - 1]], i)

	def test_processWordInLanguage_saves_total_word_count(self):
		for i in range(1, self.test_number):
			self.processor.processWordInLanguage(self.test_word, self.test_language)
			self.assertEqual(self.processor.total_words, i)

	def test_sanitiseWord_converts_word_to_lower(self):
		test_str1 = "Abdf"
		test_str2 = "dBdf"
		test_str3 = "AbdN"
		self.assertEqual(self.processor.sanitiseWord(test_str1), "abdf")
		self.assertEqual(self.processor.sanitiseWord(test_str2), "dbdf")
		self.assertEqual(self.processor.sanitiseWord(test_str3), "abdn")

	def test_processWordInLanguage_calls_sanitiseWord_with_given_word_and_language(self):
		processor = FakeProcessor()
		Processor.processWordInLanguage(processor, self.test_word, self.test_language)
		self.assertEqual(processor.word, self.test_word)
		self.assertEqual(processor.language, self.test_language)

	def test_sanitisedWord_removes_punctuation_from_word(self):
		test_str1 = "Abdf!"
		test_str2 = "dB'df"
		test_str3 = "A?bdN"
		test_str4 = "A?b/\dN"
		self.assertEqual(self.processor.sanitiseWord(test_str1), "abdf")
		self.assertEqual(self.processor.sanitiseWord(test_str2), "dbdf")
		self.assertEqual(self.processor.sanitiseWord(test_str3), "abdn")
		self.assertEqual(self.processor.sanitiseWord(test_str4), "abdn")

	def test_getBayesProbability_returns_correct_values(self):
		self.assertEqual(self.processor.getBayesProbability(0, .1, .5), 0)
		self.assertEqual(self.processor.getBayesProbability(.5, .2, .5), .2)
		self.assertEqual(self.processor.getBayesProbability(1, .1, .5), .2)

	def test_getLanguageProbabilities_from_word_returns_list(self):
		self.assertTrue(isinstance(self.processor.getLanguageProbabilitiesFromWord(self.test_word), list))

	def getPreparedFakeProcessor(self):
		processor = FakeProcessor()
		processor.language_dict[self.test_language] = {
			self.test_word: 1,
			"occurences": 1
		}
		processor.word_dict[self.test_word] = 1
		processor.total_words = 1
		return processor

	def test_getLanguageProbabilities_from_word_returns_list_of_tuples_when_data_available(self):
		self.assertTrue(isinstance(Processor.getLanguageProbabilitiesFromWord(self.getPreparedFakeProcessor(), self.test_word)[0], tuple))

	def test_getLanguageProbabilities_returns_correct_language_and_probability_with_1_language_and_1_word(self):
		processor = self.getPreparedFakeProcessor()
		self.assertEqual(Processor.getLanguageProbabilitiesFromWord(processor, self.test_word)[0][0], self.test_language)
		self.assertEqual(Processor.getLanguageProbabilitiesFromWord(processor, self.test_word)[0][1], 1)

	def test_getLanguageProbabilities_returns_correct_language_and_probability_with_2_language_and_1_word(self):
		processor = self.getPreparedFakeProcessor()
		processor.language_dict["anotherlanguage"] = {
			self.test_word: 1,
			"occurences": 1
		}
		processor.word_dict[self.test_word] = 2
		processor.total_words = 2
		self.assertEqual(Processor.getLanguageProbabilitiesFromWord(processor, self.test_word)[0][1], .5)
