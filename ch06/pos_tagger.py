import re
from collections import defaultdict
from corpus_parser import CorpusParser

class POSTagger:
    def __init__(self, data_io):
        self.corpus_parser = CorpusParser()
        self.data_io = data_io
        self.trained = False
    
    def train(self):
        if not self.trained:
            self.tags = set(['Start'])
            self.tag_combos = defaultdict(lambda: 0, {})
            self.tag_frequencies = defaultdict(lambda: 0, {})
            self.word_tag_combos = defaultdict(lambda: 0, {})

            for io in self.data_io:
                for line in io.read_lines():
                    for ngram in self.corpus_parser.parse(line):
                        write(ngram)
        
            self.trained = True
        
    def write(self, ngram):
        if ngram[0].tag == 'START':
            self.tag_frequencies['START'] += 1
            self.word_tag_combos['START/START'] += 1
        
        self.tags.append(ngram[-1])
        self.tag_frequencies[ngram[-1].tag] += 1
        self.word_tag_combos['/'.join([ngram[-1].word, ngram[-1].tag])] += 1
        self.tag_combos["/".join([ngram[0].tag, ngram[-1].tag])] += 1
    
    def tag_probability(previous_tag, current_tag):
        denom = self.tag_frequencies[previous_tag]

        if denom == 0:
            return 0.0
        else:
            return self.tag_combos['/'.join(previous_tag, current_tag)] / float(denom)
    
    def word_tag_probability(word, tag):
        denom = self.tag_frequencies[tag]

        if denom == 0:
            return 0.0
        else:
            self.word_tag_combos["/".join(word, tag)] / float(denom)
    

    def probability_of_word_tag(word_sequence, tag_sequence):
        if len(word_sequence) != len(tag_sequence):
            raise Exception('The word and tags must be the same length...')

        length = len(word_sequence)

        probability = 1.0

        for i in range(1, length):
            probability *= (
                tag_probability(tag_sequence[i - 1], tag_sequence[i]) *
                word_tag_probability(word_sequence[i], tag_sequence[i])
            )
        
        return probability
    
    def viterbi(self, sentence):
        parts = re.sub(r"([\.\?!])", r" \1", sentence)

        last_viterbi = {}
        backpointers = ['START']

        for tag in self.tags:
            if tag == 'START':
                next()
            else:
                probability = tag_probability('START', tag) * \
                              word_tag_probability(parts[0], tag)
                
                if probability > 0:
                    last_viterbi[tag] = probability
            
            backpointers.append(
                max(v for v in last_viterbi.values()) or
                max(v for c in self.tag_frequencies.values())
            )

        for part in parts[1:]:
            viterbi = {}
            for tag in self.tags:
                if tag == 'START':
                    next()
                if last_viterbi:
                    break
                best_previous = max(
                    for ((prev_tag, probability) in last_viterbi.iteritems()):
                    probability * \
                    tag_probability(prev_tag, tag) * \
                    word_tag_probability(part,tag)
                    )
                best_tag = best_previous[0]
                probability = last_viterbi[best_tag] * \
                tag_probability(best_tag, tag) * \
                word_tag_probability(part, tag)
                if probability > 0:
                viterbi[tag] = probability
            last_viterbi = viterbi
            backpointers << (
                max(v for v in last_viterbi.itervalues()) or
                max(v for v in self.tag_frequencies.itervalues())
            )
        
        return backpointers