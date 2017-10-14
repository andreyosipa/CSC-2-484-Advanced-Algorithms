#Andrii Osipa
#Advanced Algorithms CSC484 Homework #2
#Exercise 2.2

import math
import random

def compute_hash(a,b,x,p,m):
    return ((a*x + b ) % p) % m

def is_prime(n):
    if n == 2 or n == 3: return True
    if n < 2 or n%2 == 0: return False
    if n < 9: return True
    if n%3 == 0: return False
    r = int(n**0.5)
    f = 5
    while f <= r:
        if n%f == 0: return False
        if n%(f+2) == 0: return False
        f +=6
    return True 

def find_prime(bound):
    #find  greates prime < bound
    x = bound - 1
    while is_prime(x) == False:
        x -= 1
    return int(x)

def binary_zeros(x):
    #find number of zeros in binary representation of x
    x = int(bin(x)[2:])
    result = 0
    while x % 10 == 0 and x>0:
        result += 1
        x = x / 10
    return result

def run(precision = 0.2, confidence = 0.99):
    n = int(raw_input().split()[0])
    
    #initialization bjkst
    prime = find_prime(2**math.ceil(math.log(n)/math.log(2)))
    t = int(math.ceil(math.log(1/(1-confidence))))
    hash_h = []
    Bs = []
    for idx in range(t):
        hash_h.append([random.randint(0,prime-1), random.randint(0,prime-1)])
        Bs.append([])
    zs = [0]*t
    
    #runs
    while 2==2:
        line = raw_input()
        query = line.split()[0]
        if query.lower() == "a":
            element = int(line.split()[1])
            for idx in range(t):
                zeros = binary_zeros(compute_hash(hash_h[idx][0], hash_h[idx][1], element, prime, n))
                if zeros >= zs[idx]:
                    if not (element, zeros) in Bs[idx]:
                        Bs[idx].append((element, zeros))
                    while len(Bs[idx]) > 72/(precision**2):
                        zs[idx] += 1
                        Bs[idx] = [x for x in Bs[idx] if x[1] >= zs[idx]]
        else:
            if query.lower() == "q":
                print(median([len(Bs[idx])*2**zs[idx] for idx in range(t)]))

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

run()