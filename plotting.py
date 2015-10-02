import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

# original v
v1 = [0, 0]
v2 = [1, 0]
v3 = [1, 1]
v4 = [0, 1]

# figure setup
fig1 = plt.figure(0)
ax = plt.subplot(111)

# original V
V = np.array([v1, v2, v3, v4]).T

# original plot
x, y = zip(v1, v2, v3, v4, v1)
ax.plot(x, y, label='original')

# transformation matrix
A_scale = np.diag([2, 2])
V_scale = np.dot(A_scale, V) # matrix applied

v1, v2, v3, v4 = zip(*V_scale)

x, y = zip(v1, v2, v3, v4, v1)
ax.plot(x, y, label='scaled')

rot = np.radians(15)
A_rot = np.array([
        [np.cos(rot), -np.sin(rot)],
        [np.sin(rot),  np.cos(rot)]
        ])
V_rot = np.dot(A_rot, V)

v1, v2, v3, v4 = zip(*V_rot)

x, y = zip(v1, v2, v3, v4, v1)
ax.plot(x, y, label='rotated')


# skew
k = -0.5 # skew factor 'k'
A_skew = np.array([
    [1, 0.5],
    [0,   1]
    ])
V_skew = np.dot(A_skew, V)

v1, v2, v3, v4 = zip(*V_skew)

x, y = zip(v1, v2, v3, v4, v1)
ax.plot(x, y, label='skewed')

V_skewrot = np.dot(np.dot(A_skew, A_rot), V)
v1, v2, v3, v4 = zip(*V_skewrot)

x, y = zip(v1, v2, v3, v4, v1)
ax.plot(x, y, label='skewed then rotated')

ylim = ax.get_ylim()
xlim = ax.get_xlim()

dy = abs(ylim[0] - ylim[1])
dx = abs(xlim[0] - xlim[1])

ax.axis([
    xlim[0] - dx*0.1,
    xlim[1] + dx*0.1,
    ylim[0] - dy*0.1,
    ylim[1] + dy*0.1
    ])

ax.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.1),
    fancybox = True,
    ncol = 3
)


filepath = '/home/samuel/Downloads/out.png'
fig1.savefig(filepath, bbox_inches='tight')
