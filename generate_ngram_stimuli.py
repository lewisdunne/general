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


def generate_sample(use_letters, size, exclude=None):
    
    to_shuffle = list(use_letters)
    np.random.shuffle(to_shuffle)
    if exclude == None:
        use_letters = to_shuffle
    else:
        use_letters = ''.join([i for i in ''.join(to_shuffle).upper() if i not in exclude])

    return use_letters[:size]



def replace_ngram(use_letters, ngrams, distribute, replace):
    cols = len(ngrams)
    
    if distribute == False:
        position = np.random.randint(0, cols) # Gen random int
        ngram = ngrams[position]
        exclude = ''.join(ngrams)
        # Generate a random sample of size n
        sample = generate_sample(use_letters=use_letters,
                                 size=len(ngram),
                                 exclude=exclude)
        if replace==True:
            ngrams[position] = sample
            positions = [position]
        else:
            positions = []
    else:

        exclude = ''.join(ngrams)
        # Generate a random sample of size n
        sample = generate_sample(use_letters=use_letters,
                                 size=len(ngrams[0]),
                                 exclude=exclude)
        
        positions = []
        for i, ngram in enumerate(ngrams):
            pos = np.random.randint(0, len(ngram)) # Get random position in this ngram
            if replace==True:
                ngrams[i] = ngram.replace(ngram[pos], sample[i])
                positions.append(pos)
            else:
                positions.append([])

    return sample, ngrams, positions


def replace_ngrams(use_letters, df, distribute, replace):
    samples = []
    positions = []
    for row in range(len(df.index)):
        sample, ngrams, pstn = replace_ngram(use_letters,
                                             df.iloc[row].values.tolist(),
                                             distribute=distribute,
                                             replace=replace)
        df.iloc[row] = ngrams
        samples.append(sample)
        positions.append(pstn)
    
    df['Samples'] = samples
    df['Positions'] = positions
    return df



def generate_all_stimuli(use_letters, ngram_size, samples, replace, distribute, fname=None):
    ngrams = generate_ngrams(use_letters,
                         ngram_size=ngram_size,
                         samples=samples)
    df = pd.DataFrame(ngrams)
    # make all uppercase
    for c in df.columns:
        df[c] = df[c].str.upper()

    # 
    df = replace_ngrams(use_letters,
                        df, distribute=distribute,
                        replace=replace)
    print(df.head())
    if fname is not None:
        df.to_csv(fname)
        
    return df


if __name__ == '__main__':
    
    #-Define some stuff ---------------------------------------#
    # Letters to use in stimulus generation
    use_letters = 'bcdfghjklmnpqrstvwxyz' # String of consonants
    # ngram size
    ngram_size = 3
    # How many trials
    samples = 20
    # Replace a random ngram with the Sample stimulus?
    replace = True
    # Distribute the Sample stim across each ngram for each row?
    distribute = False
    # Save the file
    fname = None # file name if not None.
    
    #-Run it --------------------------------------------------#
    df = generate_all_stimuli(use_letters=use_letters,
                              ngram_size=ngram_size,
                              samples=samples,
                              replace=replace,
                              distribute=distribute,
                              fname=fname)
    print(df.head())
