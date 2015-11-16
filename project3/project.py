from sympy import Symbol, Matrix, pprint
# compute eigenvalues and eigenvectors of a continuous dynamical system
# consider sys. with 5 masses (mi)
x1 = Symbol('x1')
x2 = Symbol('x2')
x3 = Symbol('x3')
x4 = Symbol('x4')
x5 = Symbol('x5')

# and 4 springs
k1 = Symbol('k1')
k2 = Symbol('k2')
k3 = Symbol('k3')
k4 = Symbol('k4')

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
x = Matrix([x1, x2, x3, x4, x5])
pprint(x)

# and
A = Matrix([
    [ k1, -k1,     0,      0,      0  ],
    [-k1,  k1+k2, -k2,     0,      0  ],
    [ 0,  -k2,     k2+k3, -k3,     0  ],
    [ 0,   0,     -k3,     k3+k4, -k4 ],
    [ 0,   0,      0,      -k4,    k4 ]
    ])
pprint(A)

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
k1, k2, k3, k4 = [4, 8, 3, 7] # from student number

# determine all natural frequencies of the system (from the eigenvalues)

# show that lambda = 0 is always an eigenvalue of A (for any k) and eexplain the corresponding motion.

# show how to formulate the system in a matrix form when the masses mi are not
# equal.  in particular, show how to reduce the system to a matrix eigenvalue
# problem in which the matricies are symmetrix.
