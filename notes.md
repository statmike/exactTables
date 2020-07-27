CLEAN and move these to the initial readme.md



RIGHT NOW:
DONE - make target evaluation a function called eval
DONE - Make missing category be optional - yes/no
change print when no matches 'Here are the matches ....'
plot combinations
plot hover text fixed
plot - optional 0 category if inczero=True - or make this fully dynamic

UP NEXT:
send matches through process that add more ratings and new target
    add plusloop function - keep on main for now, thread it later
thoguhts:
    each combo has a sum and count
    each addition to a combo has a sum and count
    evaluate which additions can yield target
    check for uniqueness - add if new


QUEUE:
Deconstruct to more functions for better modularity
make return be numpy array all the way back to user?

Able to run resulting combination through loops with +n more levels, check for change in target or new target

Constrain combos: like sudoku - N, C where C are distinct with fixed sum/sequence

EFFICIENT ALG:
run zero first
Conditionally loop high to low or low to high - based on distance from target
Represent targets as sum and count - use to shrink range at each loop - when target sum is exceeded stop iterating for that C
thread all possible as it is done now, then apply efficient algorithm within each thread, this may cause theads to have unequal computation - but that is ok




THOUGHTS:
# DONE: adjust match precision to adhear to input target math.isclose used with rel_tol=.001
# DONE: save matches - overall
# report matches, combos, percent matched: thread and overall
# report additional matches in ranges (create a counter but dont save them): +-.01, +.02
# add time decorator
# setup MP
# setup FIBER
# two types of looping: full withing range, just at the level presented
# revisit checker - see notes below

# for the checker function
#    for thread in thread_list:
#        calc = 0
#
#        calc=math.comb(N-np.sum(thread[2])+(C-len(thread[2]))-1,(C-len(thread[2]))-1) - math.comb(N-np.sum(thread[3])+(C-len(thread[3]))-1,(C-len(thread[3]))-1)
#        if calc == thread[1]: verify='VERIFIED'
#        else: verify='NOT VERIFIED'
#        print("Thread {}, with {} combinations, {} with {} (calculated)".format(thread[0],thread[1],verify,calc))



# todo
    # DONE - move thread_combos to thread_list[-1][1]
    # NOT NEEDED - used conditonal return values to keep cpos variable - use, thread_list[threads-1][3], end as cpos
    # DONE - added detection for end list and then fill in start list - detect when starting a thread - use cpos as start
    # DONE - figure out optional function inputs
    # NOT NEEDED - make thread_combos be the 0 position of cpos
    # DONE - make returns condition - one for recursion, one for main call that only has thread_list
    # DONE - move calculation of thread_portion into function
    # make a checker function
        # run N, C, Threads, adds up result of threads, calculated result, compares, reports if the are the same
# questions
    # DONE by using return value for threads, thread_combos: what if it drills in but need to come back to outer loop to iterate?
    # DONE by altering rule: make a rule to further split the first one that causes the tip to a new thread in case it is too big
    # DONE with if condition after for loop with i==1: what if it is the last thread because you need to allow it to potentially exceed thread_portion to hold small remainder
    # make threads a list [thread, thread_combos, [start list], [stop list]]
    # checks
        # try threads = 1 and verify it is the full range
        # try threads = 2, 3, 4 and manually add up
        # try threads = 100
        # try very large N = 1000 and threads = 1, 2, 100


#vision
# optional missing
# narrow choices based on what could lead to target
# different targets - chi square, ...