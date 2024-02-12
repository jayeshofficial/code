import time
import argparse
import random
import os
import math
import sys
import itertools

def getTuples_rec(lst, sizeLeft, trieNode, count, comb):
    if sizeLeft == 1:
        for x in lst:
            if x not in trieNode: 
                trieNode[x] = True
                count[0] +=1
    else:
        for i in range(len(lst) - sizeLeft + 1):
            if lst[i] not in trieNode:
                trieNode[lst[i]] = {}
            trieNodeNew = trieNode[lst[i]]
            combNew = comb[:] + [lst[i]]
            getTuples_rec(lst[i+1:], sizeLeft - 1, trieNodeNew, count, combNew)

def check_coverage(samplefile, size):
    trie = {}
    count = [0]
    with open(samplefile, "r") as f:
        for line in f:
            s = list(map(int, line.strip().split(',')[1].strip().split(' ')))
            getTuples_rec(s, size, trie, count, [])
    countRes = count[0]
    print("Number of combinations " + str(countRes))
    return countRes

def cnk(n, k):
    res = 1
    for i in range(k):
        res *= n - i
    for i in range(k):
        res /= (i + 1)
    return res

def greedy_coverage(samplefile, size):
    with open(samplefile, "r") as f:
        data = [set(map(int, line.strip().split(',')[1].strip().split(' '))) for line in f]

    all_elements = set().union(*data)
    covered = set()
    count = 0

    while covered != all_elements:
        best_comb = None
        best_new_elements = set()

        for comb in itertools.combinations(all_elements, size):
            new_elements = set(comb) - covered
            if len(new_elements) > len(best_new_elements):
                best_new_elements = new_elements
                best_comb = comb

        if best_comb:
            covered.update(best_comb)
            count += 1
        else:
            break

    print("Approximate number of combinations with Greedy Algorithm: " + str(count))
    return count

def run(samples, twise, isApprox):
    start = time.time()
    if isApprox:
        greedy_coverage(samples, twise)
    else:
        check_coverage(samples, twise)
    print("Time taken: " + str(time.time() - start))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('samples', type=str, default="", help='Input file with samples')
    parser.add_argument("--twise", type=int, help='The size of combinations', required=True)
    parser.add_argument("--approximate", action='store_true', help="Computes combinations using a greedy algorithm", dest='apprx')
    
    args = parser.parse_args()
    run(args.samples, args.twise, args.apprx)

