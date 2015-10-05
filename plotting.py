# MA339 Project: Computer Graphics
# 10/4/2015
# Sam Zagrobelny, 0374837

from __future__ import division
import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from subprocess import call
import os

########################################
# Part I: Transform & Plot
########################################

# original v's
v1 = [0, 0]
v2 = [1, 0]
v3 = [1, 1]
v4 = [0, 1]

# original V
V = np.array([v1, v2, v3, v4]).T

# figure setup

figures = []
axis = []
fig_count = 5
for i in range(1,fig_count+1):
    fig = plt.figure(i)
    figures.append(fig)
    ax = fig.add_subplot(111, aspect=1.0)
    axis.append(ax)

# transform + plot action
def plot_it(A, V, axis, label):
    if A is None: A = np.diag([1, 1])
    V_trans = np.dot(A, V)
    v1, v2, v3, v4 = zip(*V_trans)

    x, y = zip(v1, v2, v3, v4, v1)
    if label is not None:
        line3d = axis.plot(x, y, label=str(label))
    else:
        line3d = axis.plot(x, y)

    return line3d

# Original
for ax in axis:
    original_lines, = plot_it(None, V, ax, 'original')

# Scale
A_scaled = np.diag([2, 2])  # transformation matrix
scaled_lines, = plot_it(A_scaled, V, axis[0], 'scaled')

# Rotate
rot = np.radians(15) # convert to radians
A_rot = np.array([
        [np.cos(rot), -np.sin(rot)],
        [np.sin(rot),  np.cos(rot)]
        ])
rotated_lines, = plot_it(A_rot, V, axis[1], 'rotated')

# Shear
k = -0.5 # skew factor 'k'
A_shear = np.array([
    [1, k],
    [0, 1]
    ])
sheared_lines, = plot_it(A_shear, V, axis[2], 'sheared')

# Shear & Rotate
A_shearrot = np.dot(A_rot, A_shear)
shearrot_lines, = plot_it(A_shearrot, V, axis[3], 'sheared then rotated')

# Rotate & Shear
A_rotshear = np.dot(A_shear, A_rot)
rotshear_lines, = plot_it(A_rotshear, V, axis[4], 'rotated then sheared')

padp = 0.1
for ax in axis:
    ylim = ax.get_ylim()
    xlim = ax.get_xlim()

    dy = abs(ylim[0] - ylim[1])
    dx = abs(xlim[0] - xlim[1])

    ax.axis([
        xlim[0] - dx*padp,
        xlim[1] + dx*padp,
        ylim[0] - dy*padp,
        ylim[1] + dy*padp
        ])

    ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.1),
        fancybox = True,
        ncol = 3
    )

    ax.set_title('Variety of Transformations')
    ax.set_xlabel('x')
    ax.set_ylabel('y')



path = '/home/samuel/Downloads/'
for i, fig in enumerate(figures):
    fig.savefig(os.path.join(path, "out{}.png".format(i)) , bbox_inches='tight')

########################################
# Part II: Animation
########################################

ani_fig = plt.figure(20)
ani_ax = ani_fig.add_subplot(111)
 
import time

def animate(frames_per_rev):
    d_rot = 0
    incr = 360 / frames_per_rev
    print(incr)
    while True:
        rot = np.radians(d_rot) # convert to radians
        A_rot = np.array([
                [np.cos(rot), -np.sin(rot)],
                [np.sin(rot),  np.cos(rot)]
                ])
        
        rotated_lines, = plot_it(A_rot, V, ani_ax, 'rotated')
        original_lines, = plot_it(None, V, ani_ax, 'original')

        d_rot += incr

        yield rot

how_many_frames = 100
a = animate(how_many_frames+1)
down = '/home/samuel/Downloads/'
anipath = os.path.join(down, "animation/")
if not os.path.exists(anipath): os.makedirs(anipath)
for x in range(how_many_frames+1):
    ani_ax.cla()
    ani_ax.axis([-2, 2, -2, 2])
    a.next()
    ani_ax.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.1),
        fancybox = True,
        ncol = 3
    )
    ani_fig.savefig(os.path.join(anipath, "ani_out_frame{}.png".format(x)) , bbox_inches='tight')


conversion = call([
    "convert",
    os.path.join(anipath, "ani_out_frame%d.png[0-{}]".format(how_many_frames)),
    "test.gif"
    ])


########################################
# Part III: Higher Level Animation
########################################

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

high_fig = plt.figure()
high_ax = high_fig.add_subplot(111, projection='3d')
t = np.arange(0, np.pi*4, 0.1)
x = 2*np.cos(1/2*t)
y = 0.5*np.sin(t) + 0.5
z = 1/2*np.sin(3*t)

high_ax.plot(x, y, z)

high_fig.savefig('/home/samuel/Downloads/high.png', bbox_inches='tight')
