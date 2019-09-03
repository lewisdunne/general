# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 10:21:38 2019

@author: Lewis Dunne
"""
import numpy as np
import pandas as pd

def shuffle_df(df):
    '''Randomly shuffles a pandas dataframe.
    
    Parameters
    ----------
    df : `pandas.DataFrame`, a pandas dataframe object.
        
    Returns
    -------
    `shuffled`
        The randomised copy of the input dataframe `df`.
    '''
    to_shuffle = df.copy() # Copy df
    random_order = np.random.choice(to_shuffle.index, to_shuffle.shape[0], replace=False)
    to_shuffle['random_order'] = random_order
    shuffled = to_shuffle.sort_values(by='random_order').reset_index()
    shuffled = shuffled.rename(columns={'index':'original_index'})
    return shuffled

def pseudorandomise(df, condition_labels, constraints=None):
    '''Applies randomisation with constraints to a pandas dataframe.
    
    Parameters
    ----------
    df : `pandas.DataFrame`, a pandas dataframe object containing e.g. experiment 
    structure.
    
    condition_labels : `str`, a string denoting the name of a column within `df` 
    that codes for each experimental condition.
    
    constraints : `dict`, optional. If not `None`, dictionary containing 
    randomisation constraints. Its keys denote condition names and *must* 
    correspond to values contained within `condition_labels`. Its values denote 
    the maximum number of sequential repeitions desired for that specific 
    condition (key). If `None` (default), returns a randomised `df` with no 
    constraints applied.
        
    Returns
    -------
    `shuffled`
        The randomised (according to constraints) copy of the input dataframe `df`.
    '''
    # If constraints is not defined, just shuffle without constraints
    if constraints == None:
        shuffled = shuffle_df(df=df)
        return shuffled
    
    # Convert constraints values to be lists, with first element as `max_reps`...
    # and second as `current_rep` that gets changed
    for key, value in constraints.items():
        constraints[key] = {'max_reps':value, 'current_rep':1}

    # Continuously shuffle df until all constraints are successfully applied.
    iteration = 0
    while True:
        # Shuffle the df
        shuffled = shuffle_df(df=df)
        
        # Extract the shuffled condition values
        C = shuffled[condition_labels].values
        
        # Loop over C and enforce each defined restriction from `restrictions` for each condition
        for i, c in enumerate(C):
            if i == 0:
                # We can't look back to the last value...
                continue
            
            # Check if c is in the dict.
            if c not in constraints.keys():
                # If not, then we don't care how many repeats it has and we move to the next.
                continue
            
            # If current is the same as last, we have a repetition - enforce restrictions
            if C[i] == C[i-1]:
                # Increase the repetition counter by 1 for this condition
                constraints[c]['current_rep'] += 1
                # If repetition exceeds maximum specified, break out and reshuffle
                if constraints[c]['current_rep'] > constraints[c]['max_reps']:
                    good_order = False
                    break
                else:
                    # So far so good...
                    good_order = True
            else:
                # Reset the repetition counter to 1
                constraints[c]['current_rep'] = 1
                good_order = True
        
        iteration += 1
        if good_order == True:
            # If we managed to get to here then it was successful: break out of while loop.
            break
        
    print(f"Took {iteration} iterations.")
    return shuffled

if __name__ == '__main__':
    # Fake structure
    # 4 conditions, denoted 1,2,3,4, each repeating 20 times
    condition_labels = 'condition'
    d = {condition_labels:[1,2,3,4]*20}
    # Put into dataframe
    df = pd.DataFrame(d).sort_values(by=condition_labels).reset_index(drop=True)
    print(df.head())
    print()
    
    # Constraints dict.
    # Key-Value pairs denoting condition IDs (key) and the maximum repetitions allowed for each.
    # Keys must correspond to values of df['conditions'].
    # Values must be integers or floats denoting number of repetitions.
    constraints = {1:1, 2:2} # condition 1 should never occur sequentially
    
    # Run the code
    pseudorandomised = pseudorandomise(df=df, condition_labels=condition_labels)
    print(pseudorandomised.head())
