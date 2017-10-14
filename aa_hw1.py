#Andrii Osipa
#Advanced Algorithms CSC484 Homework #1
#Exercise 1.6

import itertools,random

def run():
	#technical function to read inputs.
    n = raw_input()
    m = int(n.split()[0])
    n = int(n.split()[1])
    values = []
    for row in range(n):
        line = raw_input()
        values.append([int(x) for x in line.split()])
    print k_wise_independence(values,n,m)

def k_wise_independence(values,n,m):
    #Input: values is n x m matrix with values of all xs on all events.
    #       n is number of r.v.
    #       m is size of space.
    
    #array to store probability(*m) of each value for each variable.
    #possibly to have different value ranges for different variables.
    probs = []
    for idx in range(n):
        probs.append(dict.fromkeys(list(set(values[idx])),0))
    for idx in range(m):
        for var in range(n):
            probs[var][values[var][idx]] += 1
    k = 2
    while k<n+1:
        #finding all possible combinations of k variables from n original ones.
        vars_combinations = itertools.combinations(range(n),k)
        for combination in vars_combinations:
            #rotating part of values matrix(part that contains selected r.v.) so now ith row is values for each variable on ith event.
            tmp = zip(*[values[i] for i in range(n) if i in list(combination)][::-1])
            #generating all possible sequences of selected r.v. values.
            values_combinations = list(itertools.product(*[probs[i].keys() for i in range(n) if i in combination]))
            #for each sequence test the condition.
            for values_combination in values_combinations:
                #calculating product of probabilities.
                independent_prob = 1
                for idx in range(k):
                    independent_prob *= probs[combination[idx]][values_combination[idx]]
                independent_prob /= float(pow(m,k-1))
                if independent_prob != len([vals for vals in tmp if vals==values_combination]):
                    return k-1
        k += 1
    return k-1    



#Exircise 2.3

def irreductible_polynomial(n):
    #easy to see that poly x^n + x^(n-1) + 1 is irreductible in GF(2).
    #for n=1 it is impossible, as each poly is reductible by def.
    if n == 1:
        return None
    poly = [0] * (n+1)
    poly[0] = 1
    poly[-1] = 1
    poly[-2] = 1
    return poly

def add(a,b,r):
	#addition of two polynomials modulo r.
    if len(a) < len(b):
        a = a + b
        b = a[:-len(b)]
        a = a[len(b):]
    result = [0]*len(a)
    for idx in range(len(b)):
        result[idx] = (a[idx] + b[idx]) % 2
    for idx in range(len(b),len(a)):
        result[idx] = a[idx]
    while len(result)> 0 and result[-1]==0:
        result = result[:-1]
    return result

def multiply(a,b):
	#multiplication of two polynomials.
    result = [0]*(len(a) + len(b) - 1)
    for p in range(len(a) + len(b) - 1):
        for t in range(p+1):
            if t<len(a) and p-t<len(b):
                result[p] += a[t]*b[p-t]
        result[p] %= 2
    return result

def multiply_modr(a,b,r):
	#multiplication of two polynomials modulo r.
    result = multiply(a,b)
    while len(result)>len(r):
        tmp = [0]*(len(result) - len(r) + 1)
        tmp[-1] = 1
        tmp = multiply(r,tmp)
        result = add(result,tmp,r)
    return result

def pow_poly(a,k,r):
	#caclulating polynomial power.
    if k==1:
        return [1]
    result = a
    while k > 1:
        result = multiply_modr(result,a,r)
        k -= 1
    return result

def field_mg_generator(n,r):
	#finding multiplication group(of GF(2^n)) generator.
    result = []
    polynomials = itertools.product(*([[0,1]]*n))
    poly = polynomials.next()
    while result==[]:
        poly = polynomials.next()
        deg = 0
        tmp = poly
        while tmp != [1] and deg<pow(2,n-1):
            deg += 1
            tmp = multiply_modr(tmp,poly,r)
        if deg == pow(2,n-1):
            result = poly
    return result

def k_wise_independent_sample_gf(n, k, t):
    r = irreductible_polynomial(t)
    gen = field_mg_generator(t,r)
    #generating random polynomials.
    a = []
    for idx in range(k):
        a.append([])
        for p in range(n+2):
            a[idx].append(random.randint(0, 1))
    xs = []
    for idx in range(n):
        xs.append([])
        gk = pow_poly(gen, idx, r)
        for rv_idx in range(k):
            xs[idx] = add(xs[idx], multiply_modr(a[rv_idx],pow_poly(gk,rv_idx,r),r), r)
    #converting polynomials to numbers for output.
    for x in xs:
        t = 0
        for idx in range(len(x)):
            t += x[idx]*pow(2,idx)
        xs[xs.index(x)] = t
    return xs