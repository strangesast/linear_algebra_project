import numpy as np
from sympy import Symbol, Matrix, pprint, eye
# compute eigenvalues and eigenvectors of a continuous dynamical system
# consider sys. with 5 masses (mi)
x_1 = Symbol('x1')
x_2 = Symbol('x2')
x_3 = Symbol('x3')
x_4 = Symbol('x4')
x_5 = Symbol('x5')

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

pprint(form_A(k_1, k_2, k_3, k_4))

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
k_1, k_2, k_3, k_4 = [4, 8, 3, 7] # from student number

A = form_A(k_1, k_2, k_3, k_4)
M = np.diag(np.ones(5))/10
A = np.dot(np.dot(M, A), M)


eigs = np.linalg.eigh(A)
for a, b in zip(*eigs):
    print('------------')
    l = round(a, 4)
    print(l)
    print(np.sqrt(l))
    print(b.reshape((len(b), 1)))


# determine all natural frequencies of the system (from the eigenvalues)

# show that lambda = 0 is always an eigenvalue of A (for any k) and eexplain the corresponding motion.

# show how to formulate the system in a matrix form when the masses mi are not
# equal.  in particular, show how to reduce the system to a matrix eigenvalue
# problem in which the matricies are symmetrix.
