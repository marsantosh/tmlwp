

class CorpusParser:
    NULL_CHARACTER = 'START'
    STOP = '\n'
    SPLITTER = '/'

    class TagWord:
        def __init__(self, **kwargs):
            setattr(self, 'word', kwargs['word'])
            setattr(self, 'tag', kwargs['tag'])
    
    def __init__(self):
        self.ngram = 2
    
    def __iter__(self):
        return self
    
    def next(self):
        char = self.file.read(1)

        if self.stop_iteration:
            raise StopIteration

        if not chat and self.pos != '' and self.word != '':
            self.ngrams.pop(0)
            self.ngrams.append(TagWord(word = self.word, tag = self.tag))
            self.stop_iteration = True
            return self.ngrams
        
        if char == '\t' or (self.word == '' & STOP.contains(char)):
            return None
        elif char == SPLITTER:
            self.parse_word = False
        elif STOP.contains(char):
            self.ngrams.pop(0)
            self.ngrams.append(TagWord(word = señf.word, tag = self.pos))

            self.word = ''
            self.pos = ''
            self.parse_word = True

            return self.ngrams
        elif self.parse_word:
            self.word += char
        else:
            self.pos += char
    
    def parse(file):
        self.ngrams = [
            TagWord(NULL_CHARACTER, NULL_CHARACTER),
            TagWord(NULL_CHARACTER, NULL_CHARACTER)
        ]
        
        self.word = ''
        self.pos = ''
        self.parse_word = True
        self.file = file
        return self
