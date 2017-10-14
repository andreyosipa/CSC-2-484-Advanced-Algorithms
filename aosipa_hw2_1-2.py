#Andrii Osipa
#Advanced Algorithms CSC484 Homework #2
#Exercise 1.2

from __future__ import print_function
import math
import random


def compute_hash(a,b,x,p,m=0):
    if m>0:
        return ((a*x + b ) % p) % m
    #hash to {-1,+1}
    if m==0:
        if ((a*x + b) % p) % 2 == 1:
            return 1
        else:
            return -1

def compute_hash_4u(a,b,c,d,x,p):
    value = ((a + b*x + c*(x**2) + d*(x**3)) % p) % 2 
    if value==1:
        return 1
    return -1

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

def run(precision = 0.2, confidence = 0.99):
    n = int(raw_input().split()[0])
    
    #initialization Count-Sketch
    prime = find_prime(2**math.ceil(math.log(n)/math.log(2)))
    k = int(math.ceil(3/(precision**2)))
    t = int(math.ceil(math.log(1/(1-confidence))))
    c = [[0]*k for i in range(t)]
    hash_h = []
    hash_g = []
    for idx in range(t):
        hash_h.append([random.randint(0,prime-1), random.randint(0,prime-1)])
        hash_g.append([random.randint(0,prime-1), random.randint(0,prime-1)])
    
    #initialization tug-of-war
    t_2 = int(1/precision**2 * math.ceil(math.log(1/(1-confidence))))
    hash_f = []
    for idx in range(t_2):
        hash_f.append([])
        for coef_idx in range(4):
            hash_f[idx].append(random.randint(0,prime-1))
    tug_of_war = [0]*t_2

    #runs
    while 2==2:
        line = raw_input()
        query = line.split()[0]
        element = int(line.split()[1])
        if query.lower() == "a":
            for it in range(t):
                c[it][compute_hash(hash_h[it][0],hash_h[it][1],element,prime,k)] += compute_hash(hash_g[it][0],hash_g[it][1],element,prime)
            for it in range(t_2):
                tug_of_war[it] += compute_hash_4u(hash_f[it][0],hash_f[it][1],hash_f[it][2],hash_f[it][3],element,prime)
        else:
            if query.lower() == "q":
                print(median([x**2 for x in tug_of_war]), precision, confidence)
                interval = "(f-" + str(precision*math.sqrt(median([x**2 for x in tug_of_war]))) + ",f+" + str(precision*math.sqrt(median([x**2 for x in tug_of_war]))) + ")"
                print(median([compute_hash(hash_g[it][0], hash_g[it][1], element, prime)*c[it][compute_hash(hash_h[it][0],hash_h[it][1],element,prime,k)] for it in range(t)]), interval, confidence)

def median(lst):
    sortedLst = sorted(lst)
    lstLen = len(lst)
    index = (lstLen - 1) // 2

    if (lstLen % 2):
        return sortedLst[index]
    else:
        return (sortedLst[index] + sortedLst[index + 1])/2.0

run()
