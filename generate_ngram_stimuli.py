# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 23:35:45 2019

@author: L
"""
# Stimulus Design for Attention Trials
# RULES:
#-------
# `use_letters` are all letters to create stimuli from.
# Make an ngram, update `use_letters` so subsequent ngrams don't use the same letters.
# If setting is EASY:
#	if condition is PRESENT: copy ngram sample, insert into `bunch`, flank with two 'XXX' (sample is present)
#	else if condition is ABSENT: create a new ngram from `use_letters`, flank with two 'XXX' (sample is absent)
# Else if setting is HARD:
#	if condition is PRESENT: 
#       copy ngram, insert into bunch
#		randomly select 2 letters from the sample ngram...
#		create 2 new ngrams 
#       replace one of the letters from each ngram with one of the 2 sample letters to have a bit of conflict
#	else if condition is ABSENT: 
#		randomly select 2 letters from the sample ngram...
#		create 3 new ngrams from `use_letters`
#		replace one letter from two (or 3?) of the 3 ngrams with each of the 2 letters from the sample ngram.
import numpy as np
import pandas as pd

def generate_ngram(use_letters, size=None):
	# Uses `use_letters` string to generate an n_gram of size `size`.
    if size == None:
        size = len(use_letters)
    to_shuffle = list(use_letters)
    np.random.shuffle(to_shuffle)
    remaining_letters = ''.join(to_shuffle[size:])
    ngram = ''.join(to_shuffle[:size])

    return ngram, remaining_letters

def make_bunch(use_letters, difficulty, condition, n):
    bunch = {}
    sample_ngram, remaining_letters = generate_ngram(use_letters, 3)
    bunch['sample'] = sample_ngram
    if difficulty == 0:
        if condition == 0:
            # Sample is absent: make a new ngram and put it in pos 0
            ngram_0, remaining_letters = generate_ngram(remaining_letters, 3)
            bunch['ngram_0'] = ngram_0
        elif condition == 1:
            # Random sort sample ngram and put it in
            bunch['ngram_0'] = sample_ngram
            to_shuffle = list(bunch['ngram_0'])
            np.random.shuffle(to_shuffle)
            bunch['ngram_0'] = ''.join(to_shuffle)
        bunch['ngram_1'] = 'XXX'
        bunch['ngram_2'] = 'XXX'
    else:
        if condition == 0:
            
            # Generate 3 new ngrams and input the letters from sample into 2. Replace sample with the third.
            for i in range(n):
                this_ngram, remaining_letters = generate_ngram(remaining_letters, 3)
                bunch[f'ngram_{i}'] = this_ngram
            # And one more for the sample
            new_sample_ngram, remaining_letters = generate_ngram(remaining_letters, 3)
            bunch['sample'] = new_sample_ngram
            to_shuffle = list(bunch['sample']) # shuffle to get random 2 letters
            np.random.shuffle(to_shuffle)
            random_selection = to_shuffle[0:2]
            bunch['ngram_0'] = bunch['ngram_0'].replace(bunch['ngram_0'][0], random_selection[0])
            bunch['ngram_1'] = bunch['ngram_1'].replace(bunch['ngram_1'][0], random_selection[1])
            #------- This line can be deleted if we don't want the flank letters to be repeated in all flanking ngrams...
            bunch['ngram_2'] = bunch['ngram_2'].replace(bunch['ngram_2'][0], random_selection[1])
            #-----------------------------------------------------------------#
            
        elif condition == 1:
            to_shuffle = list(bunch['sample']) # shuffle to get random 2 letters
            np.random.shuffle(to_shuffle)
            random_selection = to_shuffle[0:2]
            # Generate 3 new ngrams and input the letters from sample into 2. Replace sample with the third.
            for i in range(n-1): # only 2 of them
                this_ngram, remaining_letters = generate_ngram(remaining_letters, 3)
                bunch[f'ngram_{i}'] = this_ngram
            bunch['ngram_0'] = bunch['ngram_0'].replace(bunch['ngram_0'][0], random_selection[0])
            bunch['ngram_1'] = bunch['ngram_1'].replace(bunch['ngram_1'][0], random_selection[1])
            bunch['ngram_2'] = sample_ngram
    
    # Small block of code that shuffles the `ngram_n` in the dict, but not the sample
    # Shuffle letters within each ngram
    these_ngrams = [] # Get ready to shuffle BETWEEN each ngram
    for key, val in bunch.items():
        if key == 'sample':
            continue # leave the sample as it is
        # Shuffle the letters of each ngram and put it back in.
        to_shuffle = list(bunch[key])
        np.random.shuffle(to_shuffle)
        # Put it back in
        bunch[key] = ''.join(to_shuffle)
        these_ngrams.append(bunch[key])
    
    # Shuffle the order of these ngrams
    np.random.shuffle(these_ngrams)
    for i, ng in enumerate(these_ngrams):
        bunch[f'ngram_{i}'] = ng
    
    return bunch

def build_stimuli(use_letters, difficulty, condition, m, n):
    master_bunch = {}
    for i in range(m):
        bunch = make_bunch(letters, difficulty, condition, n)
        for key, value in bunch.items():
            bunch[key] = [value]
            
            if i == 0:
                master_bunch[key] = [value]
            else:
                master_bunch[key].append(value)
        
    return master_bunch

if __name__ == '__main__':

    letters = 'bcdfghjklmnpqrstvwxyz'.upper()
    m = 10 # How many trials?
    
    easy_present = build_stimuli(use_letters=letters, difficulty=0, condition=1, m=m, n=3) # Easy condition, sample present
    easy_absent = build_stimuli(use_letters=letters, difficulty=0, condition=0, m=m, n=3) # Easy condition, sample absent
    hard_present = build_stimuli(use_letters=letters, difficulty=1, condition=1, m=m, n=3) # Hard condition, sample present
    hard_absent = build_stimuli(use_letters=letters, difficulty=1, condition=0, m=m, n=3) # Hard condition, sample absent.
    
    # Convert to dataframes
    easy_present_df = pd.DataFrame(easy_present)
    easy_present_df['difficulty'] = 'easy'
    easy_present_df['condition'] = 'present'
    easy_absent_df = pd.DataFrame(easy_absent)
    easy_absent_df['difficulty'] = 'easy'
    easy_absent_df['condition'] = 'absent'
    hard_present_df = pd.DataFrame(hard_present)
    hard_present_df['difficulty'] = 'hard'
    hard_present_df['condition'] = 'present'
    hard_absent_df = pd.DataFrame(hard_absent)
    hard_absent_df['difficulty'] = 'hard'
    hard_absent_df['condition'] = 'absent'
    # Concatenate for 1 big dataframe
    df = pd.concat([easy_present_df, easy_absent_df, hard_present_df, hard_absent_df]).reset_index(drop=True)
