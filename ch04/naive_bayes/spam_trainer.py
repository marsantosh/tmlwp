import io
from collections import defaultdict
from naive_bayes.tokenizer import Tokenizer
from naive_bayes.email_object import EmailObject


class SpamTrainer:
    def __init__(self, training_files):
        self.categories = set()

        for category, file in training_files:
            self.categories.add(category)
        
        self.totals = defaultdict(float)
        self.training = {c: defaultdict(float) for c in self.categories}
        self.to_train = training_files
    
    def total_for(self, category):
        return self.totals[category]
    
    def train(self):
        for category, file in self.to_train:
            email = EmailObject(io.open(file, 'rb'))

            self.categories.add(category)

            for token in Tokenizer.unique_tokenizer(email.body()):
                self.training[category][token] += 1
                self.totals['_all'] += 1
                self.totals[category] += 1
        
        self.to_train = {}
    
    def score(self, email):
        self.train()

        cat_totals = self.totals

        aggregates = {cat: cat_totals[cat] / cat_totals['_all'] for cat in self.categories}
        for token in Tokenizer.unique_tokenizer(email.body()):
            for cat in self.categories:
                value = self.training[cat][token]
                r = (value + 1) / (cat_totals[cat] + 1)
                aggregates[cat] *= r
        return aggregates
    
    def normalized_score(self, email):
        score = self.score(email)
        scoresum = sum(score.values())

        normalized = {cat: (agg / scoresum) for cat, agg in score.items()}
        return normalized
    
    def preference(self):
        return sorted(self.categories, key = lambda cat: self.total_for(cat))
    
    class Classification:
        def __init__(self, guess, score):
            self.guess = guess
            self.score = score
        
        def __eq__(self, other):
            return self.guess == other.guess and self.score == other.score
        
    def classify(self, email):
        score = self.score(email)

        max_score = 0.0
        preference = self.preference()
        max_key = preference[-1]

        for k, v in score.items():
            if v > max_score:
                max_key = k
                max_score = v
            elif v == max_score and preference.index(k) > preference.index(max_key):
                max_key = k
                max_score = v
        
        return self.Classification(max_key, max_score)