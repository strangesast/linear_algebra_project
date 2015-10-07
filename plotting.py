# MA339 Project: Computer Graphics
# 10/4/2015
# Sam Zagrobelny, 0374837

from __future__ import division
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from subprocess import call
import time
import os

########################################
# Part I: Transform & Plot
########################################

# transform + plot action
def plot_it(A, V, axis, label):
    if A is None: A = np.diag([1, 1])
    V_trans = np.dot(A, V) # apply transformation matrix
    v1, v2, v3, v4 = zip(*V_trans) # seperate into constituent vectors

    # (x1, y1), (x2, y2) -> [x1, x2], [y1, y2]
    x, y = zip(v1, v2, v3, v4, v1) 

    if label is not None:
        line3d = axis.plot(x, y, label=str(label))
    else:
        line3d = axis.plot(x, y)

    return V_trans, line3d


default = np.array([[0, 0], [1, 0], [1, 1], [0, 1]]).T
figurenames = ['scale', 'rotate', 'shear', 'shearrotate', 'rotateshear']


def rotate(deg, axis, V=default):
    rot = np.radians(deg) # convert to radians
    A = np.array([
            [np.cos(rot), -np.sin(rot)],
            [np.sin(rot),  np.cos(rot)]
            ])
    label = "rotated: {}$^\circ$".format(deg)

    Voriginal, original_lines = plot_it(None, V, axis, 'original')
    Vprime, new_lines = plot_it(A, V, axis, label)
    return Vprime


def shear(k, axis, V=default):
    A = np.array([
        [1, k],
        [0, 1]])

    label = "sheared: {}".format(k)

    Voriginal, original_lines = plot_it(None, V, axis, 'original')
    Vprime, new_lines = plot_it(A, V, axis, label)

    return Vprime


def scale(s, axis, V=default):
    A = np.diag([1, 1])*s
    label = "scaled: {}".format(s)
    Voriginal, original_lines = plot_it(None, V, axis, 'original')
    Vprime, new_lines = plot_it(A, V, axis, label)

    return Vprime


def set_axis_and_save(figure, axis, name):
    padp = 0.1
    ylim = axis.get_ylim()
    xlim = axis.get_xlim()

    dy = abs(ylim[0] - ylim[1])
    dx = abs(xlim[0] - xlim[1])

    axis.axis([
        xlim[0] - dx*padp,
        xlim[1] + dx*padp,
        ylim[0] - dy*padp,
        ylim[1] + dy*padp])

    axis.legend(
        loc='upper center',
        bbox_to_anchor=(0.5, -0.1),
        fancybox = True,
        ncol = 3)

    axis.set_title('Transformation')
    axis.set_xlabel('x')
    axis.set_ylabel('y')
    
    path = os.path.dirname(os.path.realpath(__file__))
    filename = "part_one_figure_{}.png".format(name)
    filepath = os.path.join(path, filename)
    figure.savefig(filepath, bbox_inches='tight')

    return

#testfig = plt.figure()
#ax = testfig.add_subplot(111)
#
#prime = rotate(30, ax)
#print(prime)
#set_axis_and_save(testfig, ax, "rotated")


def part_one():
    print('\n\nbeginning part one')

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
    
    # Original
    for ax in axis:
        transformed, original_lines = plot_it(None, V, ax, 'original')
    
    # Scale
    A_scaled = np.diag([2, 2])  # transformation matrix
    scaled, scaled_lines = plot_it(A_scaled, V, axis[0], 'scaled')
    
    # Rotate
    rot = np.radians(15) # convert to radians
    A_rot = np.array([
            [np.cos(rot), -np.sin(rot)],
            [np.sin(rot),  np.cos(rot)]
            ])
    rotated, rotated_lines = plot_it(A_rot, V, axis[1], 'rotated')
    
    # Shear
    k = -0.5 # skew factor 'k'
    A_shear = np.array([
        [1, k],
        [0, 1]
        ])
    sheared, sheared_lines = plot_it(A_shear, V, axis[2], 'sheared')
    
    # Shear & Rotate
    A_shearrot = np.dot(A_rot, A_shear)
    shearrotated, shearrot_lines = plot_it(A_shearrot, V, axis[3], 'sheared then rotated')
    
    # Rotate & Shear
    A_rotshear = np.dot(A_shear, A_rot)
    rotsheared, rotshear_lines = plot_it(A_rotshear, V, axis[4], 'rotated then sheared')
    
    padp = 0.1 # padding percentage
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
    
    
    
    path = os.path.dirname(os.path.realpath(__file__))
    for i, fig in enumerate(figures):
        filename = "part_one_figure_{}.png".format(figurenames[i])
        filepath = os.path.join(path, filename)
        print('saving ' + filename)
        fig.savefig(filepath, bbox_inches='tight')

########################################
# Part II: Animation
########################################
def part_two():
    print('\n\nbeginning part two')

    def animate(frames_per_rev):
        d_rot = 0
        incr = 360 / frames_per_rev
        for i in range(frames_per_rev+1):
            rot = np.radians(d_rot) # convert to radians
            A_rot = np.array([
                    [np.cos(rot), -np.sin(rot)],
                    [np.sin(rot),  np.cos(rot)]
                    ])
    
            rotated, rotated_lines = plot_it(A_rot, V, ani_ax, 'rotated')
            original, original_lines = plot_it(None, V, ani_ax, 'original')
    
            d_rot += incr
    
            yield rot
 
    # original v's
    v1 = [0, 0]
    v2 = [1, 0]
    v3 = [1, 1]
    v4 = [0, 1]
    
    # original V
    V = np.array([v1, v2, v3, v4]).T
 
    ani_fig = plt.figure(20)
    ani_ax = ani_fig.add_subplot(111)

    path = os.path.dirname(os.path.realpath(__file__))
    anipath = os.path.join(path, "animation/")
    if not os.path.exists(anipath): os.makedirs(anipath)
   
    how_many_frames = 100 # frames per revolution
    animation = animate(how_many_frames)
    
    for i, x in enumerate(animation):
        ani_ax.axis([-2, 2, -2, 2])
        ani_ax.legend(
            loc='upper center',
            bbox_to_anchor=(0.5, -0.1),
            fancybox = True,
            ncol = 3
        )

        filename = "ani_out_frame{}.png".format(i)
        filepath = os.path.join(anipath, filename)
        print('saving frame {} / {}'.format(i+1, how_many_frames+1))

        ani_fig.savefig(filepath, bbox_inches='tight')
        ani_ax.cla()
    
    # convert frames to .gif
    print('converting frames to .gif')
    conversion = call([
        "convert", # imagemagick command
        os.path.join(anipath, "ani_out_frame%d.png[0-{}]".format(how_many_frames)),
        os.path.join(path, "animation.gif")
    ])


########################################
# Part III: Higher Dimension Animation
########################################
def part_three():
    print('\n\nbeginning part three')

    high_fig = plt.figure() # instantiate figure
    high_ax = high_fig.add_subplot(111, projection='3d') # axis for figure
    high_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'animation/') # where's this going
    
    def animation(frames, axis):
        # do a full revolution, increment by how many degrees
        degree_incr = 360 / frames 
        deg = 0
        for i in range(frames+1):
            th = np.radians(deg) # convert to radians
            A = np.array([
                [np.cos(th), -np.sin(th), 0],
                [np.sin(th),  np.cos(th), 0],
                [0,           0,          1]
            ])
    
            deg+=degree_incr
    
            T = np.arange(0, np.pi*4, 0.01) # 't' values for infiniti loop
            infiniti = lambda t: np.diag([
                np.cos(1/2*t), # x
                np.sin(t),     # y 
                1/2 + 1/2*np.sin(2*t) + 1/20*np.sin(20*t) # z
            ])
            cool_infiniti = lambda t: np.diag([
                np.cos(1/2*t), # x
                np.sin(t),     # y 
                1/2 + 2*abs(1/2 - i/(frames+1))*(1/2*np.sin(2*t) + 1/20*np.sin(20*t)) # z
            ])

            V = [cool_infiniti(t) for t in T] # create (x, y, z) for each 't'

            transformed = [np.dot(A,v) for v in V] # apply rotation transformation

            x, y, z = zip(*[np.dot(a, np.array([1, 1, 1])) for a in transformed])
            lines, = axis.plot(x, y, z)

            yield lines
    
    number_of_frames = 36
    for i, a in enumerate(animation(number_of_frames, high_ax)):
        high_ax.set_xlim3d(-2, 2)
        high_ax.set_ylim3d(-1, 1)
        high_ax.set_zlim3d(-1, 1)
        print('saving frame {} / {}'.format(i+1, number_of_frames+1))
        filepath = os.path.join(high_path, 'high_frame{}.png'.format(i))
        high_fig.savefig(filepath, bbox_inches='tight')
        high_ax.cla()
    
    path = os.path.dirname(os.path.realpath(__file__))
    print('converting frames to .gif')
    conversion = call([
        "convert",
        os.path.join(high_path, "high_frame%d.png[0-{}]".format(number_of_frames-1)),
        os.path.join(path, "high_animation.gif")
    ])
