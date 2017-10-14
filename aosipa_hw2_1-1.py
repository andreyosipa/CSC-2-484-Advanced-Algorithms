#Andrii Osipa
#Advanced Algorithms CSC484 Homework #2
#Exercise 1.1

from __future__ import print_function
import random

def run():
    n = int(raw_input().split()[0])
    probs = [float(x) for x in raw_input().split()]
    k = int(raw_input().split()[0])
    probs, complements = split_probs(n, probs)
    result = []
    for idx in range(k):
        cell = random.randint(0,n-1)
        value = random.random()
        if value <= probs[cell]:
            result.append(cell + 1)
        else:
            result.append(complements[cell] + 1)
    print(*result)

def split_probs(n, probs):
    probs = [x*n for x in probs]
    smaller = []
    bigger = []
    complements = [0]*n
    #complements[i] is value that is output with probability 1-probs[i], when i_th bucket selected.
    for prob_idx in range(n):
        if probs[prob_idx] < 1:
            smaller.append(prob_idx)
        else:
            bigger.append(prob_idx)
    while len(smaller) > 0 and len(bigger) > 0:
        s = smaller.pop()
        b = bigger.pop()
        complements[s] = b
        probs[b] = probs[b] + probs[s] - 1
        if probs[b] < 1:
            smaller.append(b)
        else:
            bigger.append(b)
    #if only bigger left then they are equal 1(my be > 1 due to computation finitness errors)
    while len(bigger) > 0:
        b = bigger.pop()
        probs[b] = 1
    #this case may happen only due to computation errors
    while len(smaller) > 0:
        s = smaller.pop()
        probs[s] = 1
    return probs, complements

run()