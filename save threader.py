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
        print("there are {} combinations and the threader partitioned {} combinations over {} threads".format(math.comb(N+C-1,C-1),np.sum(thread_list,axis=0)[1],np.count_nonzero(thread_list,axis=0)[0]))
        print("Thread List (Thread Number, Combinations, Start Vector, End Vector):",*thread_list,sep="\n")
        return thread_list

    # internal return from recursive run so return full set of info
    return thread_list, threads, cpos