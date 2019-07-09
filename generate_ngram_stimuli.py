import numpy as np
import pandas as pd

def generate_ngram(use_letters, size=None):
	# Uses `use_letters` string to generate an n_gram of size `size`.
    if size == None:
        size = len(use_letters)
    to_shuffle = list(use_letters)
    np.random.shuffle(to_shuffle)
    remainder = ''.join(to_shuffle[size:])
    ngram = ''.join(to_shuffle[:size])
    return remainder, ngram

def make_ngram_bunch(use_letters, ngram_size, n):
    # "Bunch" of n ngrams
    bunch = {}
    letters = use_letters
    for i in range(n):
        letters, ngram = generate_ngram(letters, ngram_size)
        bunch[f'ngram_{i}'] = ngram
    return letters, bunch

# Function to add a sample to ngram    
def append_sample_ngram(ngram_bunch, use_letters, size):
    appended = ngram_bunch
    letters, appended['sample'] = generate_ngram(use_letters=use_letters, size=size)
    return letters, appended

def update_bunch(ngram_bunch, distribute=False, partial=False):
    updated = ngram_bunch.copy() # update a copy
    sample = updated['sample']
    if partial == True:
        # If partial set True, cut off a third of the sample.
        cut_amt = len(sample) - (int(len(sample) / 3)) # cut off 1 third
        sample = updated['sample'][:cut_amt] # apply to sample
    if distribute == False:
        # If distribute set to false, replace letters of ngram_0 with sample.
        # Allows for different number letters in sample and ngram_0
        ngram = updated['ngram_0']
        s = 0
        for i in range(len(ngram)):
            # Loop over ngram and replace each letter. This allows for partial replacement.
            updated['ngram_0'] = updated['ngram_0'].replace(ngram[i], sample[s])
            if s < len(sample)-1:
                s += 1
            else:
                break
    else:
        # Distribte the sample across all ngrams
        s = 0 # counter for number of sample letters
        n_ngrams = len(updated.keys())-1
        for i in range(n_ngrams): # minus 1 to exclude the sample
            # Loop over all ngrams & replace the first letter with sample[s]
            ngram = updated[list(updated.keys())[i]]
            replaced = ngram.replace(ngram[0], sample[s])
            updated[list(updated.keys())[i]] = replaced
            if s < len(sample)-1:
                s += 1
            else: break
    return updated

def merge_dicts(dlist):
    df = pd.concat([pd.Series(d) for d in dlist], axis=1)
    return df
        
def make_ngram_samples(use_letters, ngram_size, m, n, distribute, partial, combine=False):
    dlist = []
    for i in range(m):
        # Make bunch, append a unique `sample` ngram, and update it based on experimental condition
        letters, bunch = make_ngram_bunch(use_letters=use_letters, ngram_size=ngram_size, n=n)
        letters, bunch = append_sample_ngram(ngram_bunch=bunch, use_letters=letters, size=ngram_size)
        if combine == True:
            bunch = update_bunch(ngram_bunch=bunch, distribute=distribute, partial=partial)
        dlist.append(bunch)
    df = merge_dicts(dlist).T
    df['sample_present'] = combine
    df['distributed'] = distribute
    df['partial'] = partial
    return df

if __name__ == '__main__':
    #-Define some stuff ------------------------------------------------------#
    use_letters = 'bcdfghjklmnpqrstvwxyz'.upper()  # String of consonants
    ngram_size = 3
    m = 30 # number of rows in the dataframe / condition
    n = 3 # number of consonant trigrams per row
    
    #-Run it -----------------------------------------------------------------#
    # Test by making 4 dataframes, one for each condition.
    match_easy = make_ngram_samples(use_letters, ngram_size=ngram_size, m=m, n=n, 
                                    distribute=False, partial=False, combine=True)
    match_hard = make_ngram_samples(use_letters, ngram_size=ngram_size, m=m, n=n, 
                                    distribute=True, partial=False, combine=True) 
    nomatch_easy = make_ngram_samples(use_letters, ngram_size=ngram_size, m=m, n=n, 
                                    distribute=False, partial=False, combine=False)
    nomatch_hard = make_ngram_samples(use_letters, ngram_size=ngram_size, m=m, n=n, 
                                    distribute=True, partial=True, combine=True)
    df = pd.concat([match_easy, match_hard, nomatch_easy, nomatch_hard]).reset_index(drop=True)
    df.to_csv('attention_stimuli_full.csv', index=False)
