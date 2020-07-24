import math # used in threader and checker functions for math.comb
import time # used for timing information
import numpy as np # used for array math in loop
from multiprocessing import Pool # used to run thread values in thread_list asych
from multiprocessing import cpu_count # used to detect the machines core count (virtual)

# input values 
N = 100 # how many ratings
C = 5 # categories 1 to 5
inczero = False # include 0 category - True or False - like allowing missing values as these will not be evaluted in target 
target = 4.91

# threads is calculated but can be overwritten
threads = 16 #cpu_count() # desired number of parallel processes to split work over, be careful and know how many computing cores you have as you can slow this down!

# function that splits all possible combination of N ratings in C categories across threads with approximate balance - this is hard!
def threader(N,C,inczero,threads,i=0,thread_portion=0,thread_list=[None],cpos=[None]):
    # requires math
    # recursively call threader with i+1

    # K is the total number of categories including zero - this is C + 1.  Conditions later in the code will determine the treatment of 0 based on value of inczero
    K = C + 1

    # if this is the first time running then setup thread_list structure and calculate thread_portion
    if i == 0: 
        thread_list=[[j,0,[],[]] for j in list(range(threads,0,-1))]
        if inczero:
            thread_total =  math.comb(N+K-1,K-1)
            thread_portion = math.ceil(thread_total/threads)
        else:
            thread_total = math.comb(N+K-2,K-2)
            thread_portion = math.ceil(thread_total/threads)

    # setup end point on the position vector for the thread - this holds the ratings for each value of C at the end of the thread
    if len(cpos) < i+1: cpos.append(0)
    elif len(cpos) > i+1: del(cpos[i+1:])

    # determine upper-bound for looping
    if not inczero and i == 0: ub = 1
    else: ub = N+1

    for cell_value in range(0,ub): # always starts at zero, upper bound is current remainder (+1 bc range does not include upper)
        cpos[i] = cell_value
        # initialize the threads start position
        if len(thread_list[threads-1][2]) == 0: thread_list[threads-1][2]=list(cpos)
        r = N - cell_value # new remainder is old minus current cell_value
        # if inczero=False and i==0 then definitly drill to next layer (recursively)
        if not inczero and i == 0:
            thread_list, threads, cpos = threader(r,C,inczero,threads,i+1,thread_portion,thread_list,cpos)
            if len(cpos) < i+1: cpos.append(0)
            elif len(cpos) > i+1: del(cpos[i+1:])
        # drill deeper (recursively) if the number of remaining combos for this scenario tips the thread portion too high (101% of thread_portion)
        elif thread_list[threads-1][1] + math.comb(r+(K-(i+1))-1,(K-(i+1))-1) >= 1.01 * thread_portion and K > i+2:
            thread_list, threads, cpos = threader(r,C,inczero,threads,i+1,thread_portion,thread_list,cpos)
            if len(cpos) < i+1: cpos.append(0)
            elif len(cpos) > i+1: del(cpos[i+1:])
        # otherwise, accumulate combination counts to determine cutoff for this thread
        else:
            thread_list[threads-1][1] += math.comb(r+(K-(i+1))-1,(K-(i+1))-1)
            # if the combinations for this thread are more than 99% of the desired portion then save and start the next thread - unless this is the last thread and then add extras here
            if thread_list[threads-1][1] >= 0.99 * thread_portion and threads > 1:
                thread_list[threads-1][3] = list(cpos)
                threads -= 1

    # when the loop finishes and it is the outer most loop (i==0) then save the last thread and return the thread_list
    if thread_list[threads-1][1] > 0 and i == 0:
        thread_list[threads-1][3] = list(cpos)
        print("there are {} combinations and the threader partitioned {} combinations over {} threads".format(thread_total,np.sum(thread_list,axis=0)[1],np.count_nonzero(thread_list,axis=0)[0]))
        print("Thread List (Thread Number, Combinations, Start Vector, End Vector):",*thread_list,sep="\n")
        return thread_list
    # internal return from recursive run so return full set of info
    return thread_list, threads, cpos

# function to run threader, append needed columns, and print diagnostic info about the threading process
def create_threads(N,C,inczero,threads,target):
    thread_list = threader(N,C,inczero,threads)
    # run looping check here - see notes
        # more coming here
    # add N, C, target to each thread for use in the loop function - helps to pass a single list for each thread in multiprocessing
    for thread in thread_list:
        thread.append(N)
        thread.append(C)
        thread.append(target)
    return thread_list

def eval(combo,index,target):
    # evaluate combos - multiply by index, filter to rows that match target, move to matches list, return
    #need to avoid cases where denominator is zero - the cases where c0 = N
    np.seterr(divide='ignore', invalid='ignore')
    matches = combo[np.isclose(np.sum(combo*index,axis=1,keepdims=True)/combo[:,1:].sum(axis=1,keepdims=True),target,rtol=.001)[:,0] == True].tolist()
    return matches

# loop through the combos from start to end specified in a thread alloation, then evaluate each row for match to the target value
def loop(thread,N,C,target,i=0,l=0,combo=[],matches=[]):

    # K is the total number of categories including zero - this is C + 1
    K = C + 1

    # initialize combo evaluation
    if i==0: 
        combo = np.zeros(shape=(thread[1],K),dtype=int)
        index = np.arange(0,K,dtype=int)

    # start of loop
    if i == 0: start = thread[2][i]
    elif len(thread[2]) >= i+1:
        if np.all(thread[2][:i] == combo[l,:i]): start = thread[2][i]
        else: start = 0
    elif i == K-1: start = N
    else: start = 0

    # end of loop
    if i == 0: end = thread[3][i]
    elif len(thread[3]) >= i+1:
        if np.all(thread[3][:i] == combo[l,:i]): end = thread[3][i]
        else: end = N
    else: end = N

    # loop
    for cell_value in range(start,end+1):
        combo[l,i] = cell_value
        #print(i,start,end,cell_value,combo[l])
        if i == K-1: l += 1
        elif i < K : 
            # apply cell_value to combo column i-1 and row l through l+(calculate combos beneath this)
            temp = l+math.comb(N-cell_value+(K-(i+1))-1,(K-(i+1))-1) # math.comb(r+(K-(i+1))-1,(K-(i+1))-1)
            combo[l:temp,i] = cell_value
            matches, combo, l = loop(thread,N-cell_value,C,target,i+1,l,combo,matches)

    # return to previous level (recursive) or the original call
    if i == 0:
        # find matching combos with target function
        matches = eval(combo,index,target)
        print("thread loop report: thread {}, expects {}, looped over {}, {}".format(thread[0],thread[1], l, thread[1]==l and 'Passes' or 'Error'))
        return matches
    else: return matches, combo, l

# function to iterate on combinations by adding n more ratings
def addloop():
    print("here")


# setup multiprocessing:

# function that takes a single thread and runs it through loop to get matches
def run_thread(thread):
    matches = loop(thread[0:4],thread[4],thread[5],thread[6])
    return matches

# function to allocate threads to a pool of processes
def main(thread_list):
    pool = Pool(processes=len(thread_list)) # use processes=threads, processes=8, or whatever you want here - be careful, you can make it slower!
    matches = pool.map(run_thread, thread_list)
    # unpack the list of list due to each process returning a list of matching combos
    matches = [row for sublist in matches for row in sublist]
    return matches

# the actions!
if __name__ == '__main__':
    # create thread_list
    thread_list = create_threads(N,C,inczero,threads,target)

    # run the threads asynch and time start to end
    begin = time.time()
    matches = main(thread_list)
    end = time.time()

    # report useful information 
    #print("The thread list:",*thread_list,sep="\n")
    if len(matches): print("Here are the matches:",*matches,sep="\n")
    print("This took {} seconds".format(end - begin))
    print(len(matches),"matches from",math.comb(N+C-1,C-1),"possible combinations.")















