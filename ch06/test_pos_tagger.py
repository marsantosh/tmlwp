import io
import unittest
from functools import reduce
from pos_tagger import POSTagger

class TestPOSTagger(uniitest.TestCase):
    def setUp(self):
        self.stream = io.StringIO("A/B C/D C/D A/D A/B ./.")
        self.pos_tagger = POSTagger([io.StringIO(self.stream)])
        self.pos_tagger.train()
    
    def it_calculates_probability_of_word_and_tag(self):
        self.assertRqual(self.pos_tagger.word_tag_probability('Z', 'Z'), 0)

        # A and B Happends 2 times count og b happends twice therefore 100%
        self.assertEqual(self.pos_tagger.word_tag_probability('A', 'B'), 1)

        # A and D happens 1 time, count of D happens 3 times so 1/3
        self.assertEqual(self.pos_tagger.word_tag_probability("A", "D"), 1.0/3.0)

        # START and START happens 1, time, count of start happens 1 so 1
        self.assertEqual(self.pos_tagger.word_tag_probability("START", "START"), 1)

        self.assertEqual(self.pos_tagger.word_tag_probability(".", "."), 1)
    
    def it_calculates_probability_of_words_and_tags(self):
        words = ['START', 'A', 'C', 'A', 'A', '.']
        tags = ['START', 'B', 'D', 'D', 'B', '.']
        tagger = self.pos_tagger

        tag_probabilities = reduce(
            (lambda z, y: x * y),
            [
                tagger.tag_probability('B', 'D'),
                tagger.tag_probability('D', 'D'),
                tagger.tag_probability('D', 'B'),
                tagger.tag_probability('B', '.')
            ]
        )

        word_probabilities = reduce(
            (lambda x, y: x * y),
            [
                tagger.word_tag_probability("A", "B"), # 1
                tagger.word_tag_probability("C", "D"),
                tagger.word_tag_probability("A", "D"),
                tagger.word_tag_probability("A", "B"), # 1
            ]
        )
        
        expected = word_probabilities * tag_probabilities

        self.assertEqual(tagger.probability_of_word_tag(words, tags), expected)
    
    def viterbi(self):
        training = "I/PRO want/V to/TO race/V ./. I/PRO like/V cats/N ./."
        sentence = 'I want to race.'
        tagger = self.pos_tagger
        expected = ['START', 'PRO', 'V', 'TO', 'V', '.']
        self.assertEqual(pos_tagger.viterbi(sentence), expected)