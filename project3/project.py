from __future__ import division
import numpy as np
from sympy import Symbol, Matrix, pprint, eye
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv

# compute eigenvalues and eigenvectors of a continuous dynamical system
# consider sys. with 5 masses (mi)
x_1 = Symbol('x1')
x_2 = Symbol('x2')
x_3 = Symbol('x3')
x_4 = Symbol('x4')
x_5 = Symbol('x5')
m_1 = Symbol('m1')
m_2 = Symbol('m2')
m_3 = Symbol('m3')
m_4 = Symbol('m4')
m_5 = Symbol('m5')

# and 4 springs
k_1 = Symbol('k1')
k_2 = Symbol('k2')
k_3 = Symbol('k3')
k_4 = Symbol('k4')

#      k1       k2       k3       k4
#  . -/\/\- . -/\/\- . -/\/\- . -/\/\- .
#  m1       m2       m3       m4       m5
#
# if all masses are equal, sys can be written
#
#          d^2
#        m ---- x + A x = 0
#          dt^2
#
# where
x = Matrix([x_1, x_2, x_3, x_4, x_5])
pprint(x)

# and
def form_A(k1, k2, k3, k4):
    func = Matrix if type(k1) is Symbol else np.array
    A = func([
        [ k1, -k1,     0,      0,      0  ],
        [-k1,  k1+k2, -k2,     0,      0  ],
        [ 0,  -k2,     k2+k3, -k3,     0  ],
        [ 0,   0,     -k3,     k3+k4, -k4 ],
        [ 0,   0,      0,      -k4,    k4 ]
        ])
    return A

A = form_A(k_1, k_2, k_3, k_4)

#f = lambda x: x**(-1/2) if x != 0 else 0
#f = np.vectorize(f)
#M_ec = np.diag([m_1, m_2, m_3, m_4, m_5])
#pprint(A)
#print(f(M_ec))
#print(A.dot(f(M_ec)))


# free vibration of the system is of the form
# 
#              i w t
#      x(t) = e      u
#
# rearanging:
#
#      A u = lambda u 
# 
# determine all eigenvalues (lambda) for the matrix A using
k_1, k_2, k_3, k_4 = [4, 8, 3, 7] # from student number 0374837

K = form_A(k_1, k_2, k_3, k_4)

m = 100 # all masses are 100 kg
M = np.diag(np.ones(5))*m

f = np.vectorize(lambda x: x**(-1/2) if x != 0 else 0) # inv f
M_inv = f(M)

K_norm = np.dot(np.dot(M_inv, K), M_inv)

eigs = np.linalg.eigh(K_norm)

vals, vects = eigs
P = vects
PT = vects.T

v = np.dot(np.dot(PT, K_norm), P)

xdoto = np.zeros(A.shape[0])
xo = np.zeros(A.shape[0])
xo[-1] = 1
#xo[0] = -1

S = np.dot(M_inv, P)

f2 = np.vectorize(lambda x: x**(-1) if x != 0 else 0)
S_inv = np.dot(PT, f2(M_inv))

ro = np.dot(S_inv, xo)
rdoto = np.dot(S_inv, xdoto)

t = np.arange(0, 100, 0.1) # time

_all = []
for ti in t:
    ra = []
    for ws, r, rdot in zip(vals, ro, rdoto):
        if ws < 10e-5:
            ra.append(0)
            continue
        w = np.sqrt(ws)
        offset = np.pi / 2 if rdot == 0 else np.arctan(w*r/rdot)
        inner = ws*r**2 + rdot**2
        inner = 0 if inner < 10e-5 else inner
        rt = np.sqrt(inner) / w*np.sin(w*ti + offset)
        ra.append(rt)

    _all.append(np.dot(P, ra))

    
with open('out.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(_all)

by_xi = zip(*_all)

fig = plt.figure()
ax = fig.add_subplot(111)
for i, xi in enumerate(by_xi):
    ax.plot(map(lambda x: x+2, xi), label='Mass {}'.format(i+1))

ax.set_title('Displacement Xint1-4 = 0, Xinit5 = 10')
ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.1),
    fancybox = True,
    ncol = 3
)

ax.set_ylabel('Displacement')
ax.set_xlabel('Time (seconds)')
fig.savefig('/home/samuel/Downloads/second_test.png', bbox_inches='tight')

# determine all natural frequencies of the system (from the eigenvalues)

# show that lambda = 0 is always an eigenvalue of A (for any k) and eexplain the corresponding motion.

# show how to formulate the system in a matrix form when the masses mi are not
# equal.  in particular, show how to reduce the system to a matrix eigenvalue
# problem in which the matricies are symmetrix.
