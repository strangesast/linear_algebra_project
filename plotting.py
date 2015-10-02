import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt

# original v
v1 = [0, 0]
v2 = [1, 0]
v3 = [1, 1]
v4 = [0, 1]

# original V
V = np.array([v1, v2, v3, v4]).T

# figure setup
figure_one = plt.figure(0)
axis_one = plt.subplot(111, aspect=1.0)
figure_two = plt.figure(1)
axis_two = plt.subplot(111, aspect=1.0)

########################################
# Transform & Plot
########################################
def plot_it(A, V, axis, label):
    if A is None: A = np.diag([1, 1])
    V_trans = np.dot(A, V)
    v1, v2, v3, v4 = zip(*V_trans)

    x, y = zip(v1, v2, v3, v4, v1)
    line3d = axis.plot(x, y, label=str(label))

    return line3d

########################################
# Original
########################################
original_lines, = plot_it(None, V, axis_one, 'original')

########################################
# Scale
########################################
A_scaled = np.diag([2, 2])  # transformation matrix
scaled_lines, = plot_it(A_scaled, V, axis_one, 'scaled')

########################################
# Rotate
########################################
rot = np.radians(15) # convert to radians
A_rot = np.array([
        [np.cos(rot), -np.sin(rot)],
        [np.sin(rot),  np.cos(rot)]
        ])
rotated_lines, = plot_it(A_rot, V, axis_one, 'rotated')

########################################
# Shear
########################################
k = -0.5 # skew factor 'k'
A_shear = np.array([
    [1, k],
    [0, 1]
    ])
sheared_lines, = plot_it(A_shear, V, axis_one, 'sheared')

########################################
# Shear & Rotate
########################################
A_shearrot = np.dot(A_shear, A_rot)
shearrot_lines, = plot_it(A_shearrot, V, axis_one, 'skewed then rotated')


ylim = axis_one.get_ylim()
xlim = axis_one.get_xlim()

dy = abs(ylim[0] - ylim[1])
dx = abs(xlim[0] - xlim[1])

axis_one.axis([
    xlim[0] - dx*0.1,
    xlim[1] + dx*0.1,
    ylim[0] - dy*0.1,
    ylim[1] + dy*0.1
    ])

axis_one.legend(
    loc='upper center',
    bbox_to_anchor=(0.5, -0.1),
    fancybox = True,
    ncol = 3
)

plt.title('Variety of Transformations')
plt.xlabel('x')
plt.ylabel('y')

filepath = '/home/samuel/Downloads/out.png'
figure_one.savefig(filepath.split('.')[0] + "1.png" , bbox_inches='tight')
figure_two.savefig(filepath, bbox_inches='tight')
