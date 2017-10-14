#Andrii Osipa
#CSC484 HW3
#Exercise 2.2

import math
import random

def closest_pair(points):
    N = len(points)
    if N % 2 == 1:
        median = points[(N-1)/2][0]
    else:
        median = (points[N/2-1][0] + points[N/2][0])/2.
    if N==2:
        return (points[0],points[1])
    if N==1:
        return (points[0], (1e10,1e10))
    if N==0:
        return ((-1e10,-1e10), (1e10,1e10))
    pair_l = closest_pair([x for x in points if x[0]<=median])
    pair_r = closest_pair([x for x in points if x[0]>median])
    d_l = distance(pair_l[0],pair_l[1])
    d_r = distance(pair_r[0],pair_r[1])
    d_lr = min(d_l,d_r)
    if d_l < d_r:
        pair = pair_l
    else:
        pair = pair_r
    points_l = sorted([x for x in points if x[0]<= median and x[0] > median - d_lr], key=key)
    points_r = sorted([x for x in points if x[0]> median and x[0] < median + d_lr], key=key)
    if len(points_l)==0 or len(points_r)==0:
        return pair
    
    idx_l = 0
    idx_r = 0
    finished = False
    while idx_l < len(points_l):
        while points_r[min(idx_r, len(points_r)-1)][1] - points_l[idx_l][1] > d_lr and idx_r < len(points_r):
            idx_r += 1
        if idx_r == len(points_r):
            break
        idx = 0
        while abs(points_l[idx_l][1] - points_r[min(idx_r + idx, len(points_r)-1)][1]) < d_lr and idx + idx_r < len(points_r):
            if distance(points_l[idx_l], points_r[idx_r+idx]) < d_lr:
                pair = (points_l[idx_l], points_r[idx_r+idx])
                d_lr = min(d_lr, distance(points_l[idx_l], points_r[idx_r+idx]))
            idx += 1
        idx_l += 1

    return pair

def distance(u,v):
    return math.sqrt((u[0]-v[0])**2 + (u[1] - v[1])**2)

def key(x):
    return -x[1]

def closest_pair_with_rotation(points):
    #Function that applies some random turn of all points with center (0,0), so we can assume that
    #with probability 1 there is no points with same x or y coordinate.
    angle = 2*math.pi*random.random()
    points_rotated = []
    for point in points:
        new_point = (point[0]*math.cos(angle) - point[1]*math.sin(angle), 
                     point[0]*math.sin(angle) + point[1]*math.cos(angle))
        points_rotated.append(new_point)
    points_rotated_s = sorted(points_rotated)
    pair = closest_pair(points_rotated_s)
    return (points[points_rotated.index(pair[0])], points[points_rotated.index(pair[1])])

def run():
    n = int(raw_input().split()[0])
    points = []
    for idx in range(n):
        line = raw_input()
        points.append((int(line.split()[0]), int(line.split()[1])))
    pair = closest_pair_with_rotation(points)
    print pair[0][0], pair[0][1]
    print pair[1][0], pair[1][1]

run()