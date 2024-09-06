import os, sys
import numpy as np
from numpy import pi
import matplotlib.pyplot as plt #import plotting library
from matplotlib import cm #import color for surface plot
import matplotlib.animation as ani #importing animation library

def frame(frame_number, T_all, X, Y, plot, ax1):
    plot[0].remove()
    plot[0] = ax1.plot_surface(
    	X,
    	Y,
    	T_all[frame_number,:,:].T,
    	cmap=cm.jet
    	)

def make_animation_2d(x_vec, y_vec, Tout, geometry = 'radial'):
	
    fig = plt.figure()
    ax1 = plt.axes(projection="3d")
    ax1.set_xlabel('x (mm)')
    ax1.set_ylabel('y (mm)')
    ax1.set_zlabel('Temperature (C)')
    ax1.set_zlim(0, Tout.max() * 1.2)
    x_mesh, y_mesh = np.meshgrid(x_vec, y_vec)

    if geometry == 'cartesian':
        ax1.set_xlim(0, max(x_vec))
        ax1.set_ylim(0, max(y_vec))
    else:
        x_mesh, y_mesh = x_mesh * np.cos(y_mesh), x_mesh * np.sin(y_mesh)
        ax1.set_xlim(-max(x_vec), max(x_vec))
        ax1.set_ylim(-max(x_vec), max(x_vec))

    plot1=[ax1.plot_surface(x_mesh, y_mesh, Tout[0,:,:].T)]

    animation = ani.FuncAnimation(
        fig = fig,
        func = frame,
        frames = len(Tout),
        fargs = (Tout, x_mesh, y_mesh, plot1, ax1),
        interval = 400,
        blit = False
    )

    return animation

def expand_coordinates(indices):
    x, y, z = indices
    x[1::2, :, :] += 1
    y[:, 1::2, :] += 1
    z[:, :, 1::2] += 1
    return x, y, z

# # colors = np.array([[['#1f77b430']*3]*3]*3)
# # colors[1,1,1] = '#ff0000ff'
# colors = explode(colors)
# filled = explode(np.ones((3, 3, 3)))
# x, y, z = expand_coordinates(np.indices(np.array(filled.shape) + 1))
# ax.voxels(x, y, z, filled, facecolors=colors, edgecolors='gray', shade=False)
# plt.show()

def midpoints(x):
    sl = ()
    for _ in range(x.ndim):
        x = (x[sl + np.index_exp[:-1]] + x[sl + np.index_exp[1:]]) / 2.0
        sl += np.index_exp[:]
    return x

def centers_to_corners(axes_inc):
    dx = [x[1] - x[0] for x in axes_inc]
    corners = [axes_inc[i] - dx[i] / 2 for i in range(3)]
    for i in range(3):
        corners[i] = np.append(corners[i], corners[i][-1] + dx[i] / 2)
    return corners

def make_plot_3d(axes_inc, T_matrix, geometry = 'cartesian'):

    # https://matplotlib.org/stable/gallery/mplot3d/voxels_numpy_logo.html

    corners = centers_to_corners(axes_inc)
    
    x_mesh, y_mesh, z_mesh = np.meshgrid(corners[0], corners[1], corners[2])

    # x_mesh_c = midpoints(x_mesh)
    # y_mesh_c = midpoints(y_mesh)
    # z_mesh_c = midpoints(z_mesh)

    fig = plt.figure()
    ax1 = plt.axes(projection = '3d')
    
    ax1.set_xlabel('x (mm)')
    ax1.set_ylabel('y (mm)')
    ax1.set_zlabel('z (mm)')

    if geometry == 'cartesian':
        ax1.set_xlim(0, max(corners[0]))
        ax1.set_ylim(0, max(corners[1]))
        ax1.set_zlim(0, max(corners[2]))
    else:
        ax1.set_xlim(-max(x_vec), max(x_vec))
        ax1.set_ylim(-max(x_vec), max(x_vec))
        ax1.set_zlim(0, max(corners[2]))

    # x_mesh, y_mesh = x_mesh * np.cos(y_mesh), x_mesh * np.sin(y_mesh)

    # print(T_matrix.shape)

    # combine the color components
    colors = np.zeros(T_matrix.shape + (4,))
    colors[..., 0] = T_matrix / 100
    colors[..., 1] = np.zeros(shape = T_matrix.shape)
    colors[..., 2] = 1 - T_matrix / 100
    colors[..., 3] = 0.3

    print('x mesh shape')
    print(x_mesh.shape)
    print('T shape')
    print(T_matrix.shape)
    print('colors shape:')
    print(colors.shape)

    ax1.voxels(x_mesh, y_mesh, z_mesh, T_matrix,
          facecolors=colors,
          # edgecolors=np.clip(2*colors - 0.5, 0, 1),  # brighter
          linewidth=0
          )

    plt.show()

    # plot1=[ax1.plot_surface(x_mesh, y_mesh, Tout[0,:,:].T)]
