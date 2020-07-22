import math # used in threader and checker functions for math.comb
import time # used for timing information
import numpy as np # used for array math in loop
from multiprocessing import Pool # used to run thread values in thread_list asych
from multiprocessing import cpu_count # used to detect the machines core count (virtual)

# input values 
N = 100 # how many ratings
C = 6 # categories 0 to 5
target=4.91

# threads is calculated but can be overwritten
threads = 8 #cpu_count() # desired number of parallel processes to split work over, be careful and know how many computing cores you have as you can slow this down!

# function that splits all possible combination of N ratings in C categories across threads with approximate balance - this is hard!
def threader(N,C,threads,i=1,thread_portion=0,thread_list=[None],cpos=[None]):
    # requires math
    # recursively call threader with i+1

    # if this is the first time running then setup thread_list structure and calculate thread_portion
    if i==1: 
        thread_list=[[k,0,[],[]] for k in list(range(threads,0,-1))]
        thread_portion = math.ceil(math.comb(N+C-1,C-1)/threads)

    # setup end position for the thread - this is the ratings for each value of C at the end of the thread
    if len(cpos) < i: cpos.append(0)
    elif len(cpos) > i: del(cpos[i:])

    for cell_value in range(0,N+1): # always starts at zero, upper bound is current remainder (+1 bc range does not include upper)
        cpos[i-1]=cell_value
        if len(thread_list[threads-1][2]) == 0: thread_list[threads-1][2]=list(cpos)
        r = N - cell_value # new remainder is old minus current cell_value
        # drill deeper (recursively) of the number of remaining combos for this scenario tips the thread portion too high (101% of thread_portion)
        if thread_list[threads-1][1] + math.comb(r+(C-i)-1,(C-i)-1) >= 1.01 * thread_portion and C > i+1:
            thread_list, threads, cpos = threader(r,C,threads,i+1,thread_portion,thread_list,cpos)
            if len(cpos) < i: cpos.append(0)
            elif len(cpos) > i: del(cpos[i:])
        # otherwise, accumulate combination counts to determine cutoff for this thread
        else:
            thread_list[threads-1][1] += math.comb(r+(C-i)-1,(C-i)-1)
            # if the combinations for this thread are more than 99% of the desired portion then save and start the next thread - unless this is the last thread and then add extras here
            if thread_list[threads-1][1] >= 0.99 * thread_portion and threads > 1:
                thread_list[threads-1][3] = list(cpos)
                #print(threads,thread_list[threads-1][1],cpos,thread_list[threads-1][3])
                threads -= 1

    # when the loop finishes and it is the outer most loop (i==1) then output the last thread
    if thread_list[threads-1][1] > 0 and i == 1:
        thread_list[threads-1][3] = list(cpos)
        #print(threads,thread_list[threads-1][1],cpos,thread_list[threads-1][3])
        # final return so only return the thread_list 
        return thread_list

    # internal return from recursive run so return full set of info
    return thread_list, threads, cpos

# function to run threader, append needed columns, and print diagnostic info about the threading process
def create_threads(N,C,threads,target):
    thread_list = threader(N,C,threads)
    print("there are {} combinations and the threader partitioned {} combinations over {} threads".format(math.comb(N+C-1,C-1),np.sum(thread_list,axis=0)[1],np.count_nonzero(thread_list,axis=0)[0]))
    # run looping check here - see notes
        # more coming here
    # add N, C, target to each thread for use in the loop function - helps to pass a single list for each thread in multiprocessing
    for thread in thread_list:
        thread.append(N)
        thread.append(C)
        thread.append(target)

    return thread_list

# loop through the combos from start to end specified in a thread alloation, then evaluate each row for match to the target value
def loop(thread,N,C,target,i=1,l=0,combo=[],matches=[]):

    # initialize combo evaluation
    if i==1: 
        combo = np.zeros(shape=(thread[1],C),dtype=int)
        index = np.arange(0,C,dtype=int)

    # start of loop
    if i == 1: start = thread[2][i-1]
    elif len(thread[2]) >= i:
        #if thread[2][i-2] == combo[l,i-2]: start = thread[2][i-1]
        if np.all(thread[2][:i-1] == combo[l,:i-1]): start = thread[2][i-1]
        else: start = 0
    elif i == C: start = N
    else: start = 0

    # end of loop
    if i == 1: end = thread[3][i-1]
    elif len(thread[3]) >= i:
        #if thread[3][i-2] == combo[l,i-2]: end = thread[3][i-1]
        if np.all(thread[3][:i-1] == combo[l,:i-1]): end = thread[3][i-1]
        else: end = N
    else: end = N

    # loop
    for cell_value in range(start,end+1):
        combo[l,i-1] = cell_value
        #print(i,start,end,cell_value,combo[l])
        if i == C: l += 1
        elif i < C : 
            # apply cell_value to combo column i-1 and row l through l+(calculate combos beneath this)
            temp = l+math.comb(N-cell_value+(C-i)-1,(C-i)-1)
            combo[l:temp,i-1] = cell_value
            matches, combo, l = loop(thread,N-cell_value,C,target,i+1,l,combo,matches)

    # return to previous level (recursive) or the original call
    if i == 1:
        # evaluate combos - multiply by index, filter to rows that match target, move to matches list, return
        #need to avoid cases where denominator is zero - the cases where c0 = N
        np.seterr(divide='ignore', invalid='ignore')
        matches = combo[np.isclose(np.sum(combo*index,axis=1,keepdims=True)/combo[:,1:].sum(axis=1,keepdims=True),target,rtol=.001)[:,0] == True].tolist()
        print("thread loop report: thread {}, expects {}, looped over {}, {}".format(thread[0],thread[1], l, thread[1]==l and 'Passes' or 'Error'))
        return matches
    else: return matches, combo, l


# setup multiprocessing:

# function that takes a single thread and runs it through loop to get matches
def tester(thread):
    matches = loop(thread[0:4],thread[4],thread[5],thread[6])
    return matches

# function to allocate threads to a pool of processes
def main(thread_list):
    pool = Pool(processes=len(thread_list)) # use processes=threads, processes=8, or whatever you want here - be careful, you can make it slower!
    matches = pool.map(tester, thread_list)
    # unpack the list of list due to each process returning a list of matching combos
    matches = [row for sublist in matches for row in sublist]
    return matches

# the actions!
if __name__ == '__main__':
    # create thread_list
    thread_list = create_threads(N,C,threads,target)

    # run the threads asynch and time start to end
    begin = time.time()
    matches = main(thread_list)
    end = time.time()

    # report useful information 
    #print("The thread list:",*thread_list,sep="\n")
    print("Here are the matches:",*matches,sep="\n")
    print("This took {} seconds".format(end - begin))
    print(len(matches),"matches from",math.comb(N+C-1,C-1),"possible combinations.")















