# # Designing Experiment Structures

import numpy as np


def build_experiment_structure(design, blocks=1):
    """Function that builds a structure to an experiment.
    returns a list (blocks=1) or a list of lists (blocks > 1) containing condition IDs for each trial.
    Useful for setting up experiment in NBS Presentation (for example).
    #-------------------------------------------------------------------------------------#
    design: tuple, list, or dict.
        If tuple or list, must be in format of (n_conditions, n_trials). 
            e.g. design=(3, 50) for 3 conditions of 50 trials each.
        If dict, must be in format of {condition_id: n_trials, ...}.
            e.g. design={'standard':80, 'oddball':10, 'distracter':10}
    
    blocks: optional int.
        If > 1, splits the design into number of blocks specified, returns list of lists 
        containing condition IDs for each trial.
        
        If number of trials divided by `blocks` is a fraction, the result is rounded down 
        to the nearest integer. This is because `int()` rounds all floats DOWN.
    #-------------------------------------------------------------------------------------#
    """
    if (type(design) == tuple) or (type(design) == list):
        if len(design) != 2:
            raise ValueError("Shape of `design` is invalid. `design` should be length 2; got length {} instead.".format(len(design)))
        
        if design[1] % blocks != 0:
            print("WARNING: n_trials={} is not divisible by {} (blocks). Restructuring n_trials to fit blocks.".format(design[1], blocks))
        
        #n_trials = design[0] * design[1]
        
        structure = []
        for b in range(blocks):
            block = []
            for c in range(design[0]):
                block += [c] * int(design[1] / blocks) # int() forces float to be rounded down.
            
            structure += [block]
        
        if blocks == 1:
            # If we have only one block, just extract structure from the sublist and return that
            structure = structure[0]
        
        return structure
    
    elif type(design) == dict:
        
        # Test to see divisibility into chosen block value
        for condition, trials in design.items():
            if trials % blocks != 0:
                print("WARNING: Condition {} (n_trials={}) is not divisible by {} (blocks). Restructuring n_trials to fit blocks.".format(condition, trials, blocks))
              
        structure = []
        for b in range(blocks):
            block = []
            for condition, trials in design.items():
                block += [condition] * int(trials / blocks) # int() forces float to be rounded down.
            
            structure += [block]
        
        if blocks == 1:
            structure = structure[0]
        
        return structure
    
    else:
        raise ValueError("`design` Type must be tuple, list, or dict; got {} instead.".format(type(design)))


# #### Example use of function

# Set up a basic study with 3 conditions of 10 trials per condition in one block


basic_structure = build_experiment_structure(design=(3, 10), blocks=1)
print(basic_structure)


# Set up a study with 3 conditions, where each condition has a specific number of trials, and it is split across 2 blocks.


specific_structure = build_experiment_structure(design={'standard':20, 'oddball':2, 'distracter':2}, blocks=2)
print(specific_structure)


# # Pseudorandomising Experiment Structure


def pseudorandomise(experiment, rep_max, max_iterations=100, suppress_output=False):
    """Function that randomises an experiment structure in such a way that none of the trials will 
    repeat (sequentially) more than `rep_max`.

    Returns a list containing condition IDs for each trial.
    Useful for setting up experiment in NBS Presentation for example.
    #-------------------------------------------------------------------------------------#
    experiment: must be a single list. If experiment contains > 1 block then loop over each block
        and input block instead
    
    rep_max: integer. Value for total number of sequential repetitions.
    
    max_iterations: integer. It is possible that a solution will never be found, so define
        as the total number of tries before quitting the function and re-evaluating whether
        the requirement is possible given the number of trials and desired rep_max.
        
    suppress_output: boolean. If True, display how many iterations, whether function call was 
        successful, and final pseudorandomised list.
    #-------------------------------------------------------------------------------------#
    """
    
    # First create an empty dictionary with keys representing the different conditions in experiment, and set values to zero.
    # We will use this to keep a count of repetitions of that condition within another loop
    con_reps = {}
    for con in list(set(experiment)):
        con_reps[con] = 0

    # Set a counter to log how many times we loop. If it exceeds max_iterations then give up.
    iteration = 0

    # Make a switch set to False until a solution is found
    sufficient_order = False
    # Start a while loop...
    while sufficient_order == False:

        iteration += 1 # Increase the counter
        # If we looped too many times, give up and send warning
        if iteration > max_iterations:
            # Could also actually increase rep_max by 1 each time it passes max_iterations
            raise Warning("Failed to find solution after {} iterations. Consider relaxing constraints, increasing `max_iterations`, or both.".format(max_iterations)) 

        # Shuffle here
        np.random.shuffle(experiment)

        # Loop over the experiment, getting the index (i) and trial type (trial) for that index in experiment
        for i, condition in enumerate(experiment):
            if i == 0:
                # First iteration, so can't look back 1 step in experiment because it doesn't exist! Set rep to equal 1.
                con_reps[condition] = 1

            elif i > 0: # Not the first iteration...
                last_condition = experiment[i-1] # get last condition type
                # check if current condition is the same as last one. If it is, add 1 rep...
                if condition == last_condition:
                    con_reps[condition] += 1

                    # Check if the rep count for this condition is > the rep_max
                    # If it is, then this iteration failed to find a solution and we need to break out and re-shuffle. 
                    if con_reps[condition] > rep_max:
                        break # go back into while loop and start again

                elif con:
                    con_reps[condition] = 1

            if i == len(experiment)-1:
            # Display iteration number
            #print("Iteration: {}".format(iteration))
            # If we have successfully looped through the entire experiment list, then it means we never exceeded rep_max!
            #print(con_reps)
            #if i == len(experiment)-1:
                sufficient_order = True
                if suppress_output == False:
                    print("Found solution in iteration {}!".format(iteration))
                    print(experiment)
    
    return experiment


# Pseudorandomise the basic experiment so that none of the conditions repeat more than twice in a row.


randomised = pseudorandomise(basic_structure, 2)


# Pseudorandomising the specific experiment is a new problem, because there are so many standard stimuli, so it is impossible. However, we'll probably just get away with just shuffling each one...

# The changes are made 'in-place', so have to redefine it otherwise nonetype is returned.
specific_structure = build_experiment_structure(design={'standard':20, 'oddball':2, 'distracter':2}, blocks=2)
print(specific_structure)

for block in specific_structure:   
    np.random.shuffle(block)

print(specific_structure)


# # Complex Pseudorandomisation

# If the last one wasn't complex enough, we might want to pseudorandomise only a subset of conditions (e.g. the oddballs and the standards so that they don't appear sequentially in a larger design). We might also want to ensure a certain condition, like a target/distracter, never appears at the beginning or end of the block...

def complex_pseudorandomise(experiment, rep_max, max_iterations=100, subset_conditions=None, never_start_with=None, never_end_with=None):
    """Function that pseudorandomises an experiment with specific conditions.
    returns a list (blocks=1) or a list of lists (blocks > 1) containing condition IDs for each trial.
    Useful for setting up experiment in NBS Presentation for example."""
    
    # This is hard

    return


# Build experiment
specific_structure = build_experiment_structure(design={'standard':20, 'oddball':2, 'distracter':2}, blocks=2)

# Remember, if it is just a single block it will be a simple list.
# The following code won't work in that case
# To make it work, reassign the simple list to a list within a list by declaring exp = [exp]

# Define values to never start a block with
never_start_with = ['oddball', 'standard']
never_end_with = ['standard']

# Create a counter to see how many iters it takes
counter = 0
# Create a negative iterator that tends towards 0 on each success
blocks_remaining = len(specific_structure)
randomised = [] # array to fill with randomised blcoks that meet the criteria
while True:
    # Loop over the blocks
    for block in specific_structure: 
        # Pseudorandomise it 
        pseudorandomise(block, rep_max=1000, max_iterations=100, suppress_output=True)
    
        if (block[0] not in never_start_with) and (block[-1] not in never_end_with): # if never_start_with is just a string, then if block[0] != never_start_with.
            randomised.append(block) # successful randomise
            # need to remove that block from the list and update the negative iterator
            specific_structure.remove(block)
            blocks_remaining -= 1 # Once it reaches zero, we break out.
        else:
            break
    
    counter += 1
    
    if blocks_remaining == 0:
        print("\nSuccess after {} iterations!".format(counter))
        break # completed
print(randomised)  

