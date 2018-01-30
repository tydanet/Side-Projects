import re

from random import randint
from fixedqueue import FixedQueue

class SenGen:
    def __init__(self, corpus, n=1):
        self.corpus = corpus
        self.n_gram_size = n
        
        self.preprocess()
        
        self.chain, self.start_grams, self.stop_words = self.initialize()
        
    def preprocess(self):
        # replace all contiguous whitespace with a single space
        self.corpus = re.sub(r'\s+', ' ', self.corpus)
        # the way i split in initialize() leaves a dangling punctuation mark without a space at the end
        self.corpus = self.corpus + ' '  
        
    def initialize(self):
        chain = {}
        start_grams = []
        stop_words = []
        
        sentences = re.split('[.!?]+ ', self.corpus)
        
        for sentence in sentences:
            words = sentence.split(' ')
            
            # sentence needs to be at least n+1 words long, otherwise it is ignored
            if len(words) < self.n_gram_size + 1:
                continue
                
            for i, word in enumerate(words[self.n_gram_size:]):
                n_gram = ' '.join([ words[j] for j in range(i, i+self.n_gram_size) ])

                if i == 0:
                    start_grams.append(n_gram)
                
                if i == len(words[self.n_gram_size:])-1:
                    stop_words.append(word)
                    
                if chain.get(n_gram):
                    chain[n_gram].append(words[i+self.n_gram_size])
                    
                else:
                    chain[n_gram] = [words[i+self.n_gram_size]]
        
        return chain, start_grams, stop_words
    
    def generate(self):
        start_phrase = self.start_grams[randint(0, len(self.start_grams)-1)]
        queue = FixedQueue(start_phrase.split(' '))
        words = [ w for w in queue.queue ]

        while words[-1] not in self.stop_words:
            phrase = ' '.join(queue.queue)
            word = self.chain[phrase][randint(0, len(self.chain[phrase])-1)]
            words.append(word)
            queue.pushpop(word)
            
        return ' '.join(words)
    
