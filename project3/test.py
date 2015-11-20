from __future__ import division
import numpy as np
sqrt = np.sqrt

def qr(array):
    a, b = np.linalg.eigh(array)
    
    n = len(array)
    m = len(array[0])
    r = np.zeros((n,m))
    
    new_array = array
    for k in range(n):
        for i in range(k):
            s = 0
            for j in range(m):
                s = s + array[j][i]*array[j][k]
            r[i,k] = s
        for i in range(k):
            for j in range(m):
                new_array[j][k] = array[j][k] - array[j][i]*r[i,k]
        s = 0
        for j in range(m):
            s += array[j][k]**2
        r[k,k] = sqrt(s)
        for j in range(m):
            new_array[j][k] = array[j][k]/r[k,k]

    return new_array, r

A = [
    [3, -1, 3],
    [-1, 3, -1],
    [3, -1, 3]
    ]


q, r = qr(A)
q, r = qr(A)

print(np.dot(q, r))
