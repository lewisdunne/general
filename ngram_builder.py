import numpy as np
import pandas as pd
import warnings


def generate_ngram(use_letters, size=None):
    
    if size == None:
        size = len(use_letters)
    
    to_shuffle = list(use_letters)
    
    np.random.shuffle(to_shuffle)
    
    remainder = ''.join(to_shuffle[size:])
    ngram = ''.join(to_shuffle[:size])
    return remainder, ngram

def generate_ngrams(use_letters, ngram_size, samples):

    if len(use_letters) < (ngram_size * 3):
        msg = 'Number of letters less than ngram_size * 3.'
        warnings.warn(msg)
            
    
    ngrams1 = []
    ngrams2 = []
    ngrams3 = []

    for i in range(samples):
        remain1, ngram1 = generate_ngram(use_letters, ngram_size)
        remain2, ngram2 = generate_ngram(remain1, ngram_size)
        remain3, ngram3 = generate_ngram(remain2, ngram_size)
        ngrams1.append(ngram1)
        ngrams2.append(ngram2)
        ngrams3.append(ngram3)

    all_ngrams = {'A':ngrams1,
                   'B':ngrams2,
                   'C':ngrams3}
        
    return all_ngrams



if __name__ == '__main__':

    consonants = 'bcdfghjklmnpqrstvwxyz'
    
    ngrams = generate_ngrams(consonants, ngram_size=4, samples=80)
    df = pd.DataFrame(ngrams)
    for c in df.columns:
        df[c] = df[c].str.upper()
    print(df.head())
    #df.to_csv('search_stim.csv')
