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

def make_plot_3d(axes_inc, T_matrix, geometry = 'cartesian'):

    # https://matplotlib.org/stable/gallery/mplot3d/voxels_numpy_logo.html
    
    x_mesh, y_mesh, z_mesh = np.meshgrid(axes_inc[0], axes_inc[1], axes_inc[2])

    print(x_mesh.shape)

    # x_mesh_c = midpoints(x_mesh)
    # y_mesh_c = midpoints(y_mesh)
    # z_mesh_c = midpoints(z_mesh)

    fig = plt.figure()
    ax1 = plt.axes(projection = '3d')
    
    ax1.set_xlabel('x (mm)')
    ax1.set_ylabel('y (mm)')
    ax1.set_zlabel('z (mm)')

    if geometry == 'cartesian':
        ax1.set_xlim(0, max(axes_inc[0]))
        ax1.set_ylim(0, max(axes_inc[1]))
        ax1.set_zlim(0, max(axes_inc[2]))
    else:
        ax1.set_xlim(-max(x_vec), max(x_vec))
        ax1.set_ylim(-max(x_vec), max(x_vec))
        ax1.set_zlim(0, max(axes_inc[2]))

    # x_mesh, y_mesh = x_mesh * np.cos(y_mesh), x_mesh * np.sin(y_mesh)

    print(T_matrix.shape)

    T_new = T_matrix.resize((49, 49, 49))

    # combine the color components
    colors = np.zeros(tuple([x - 1 for x in T_new.shape]) + (3,))
    colors[..., 0] = T_new / 100
    colors[..., 1] = np.zeros(shape = T_new.shape)
    colors[..., 2] = np.zeros(shape = T_new.shape)

    print('colors shape:')
    print(colors.shape)

    ax1.voxels(x_mesh, y_mesh, z_mesh, T_new,
          facecolors=colors,
          # edgecolors=np.clip(2*colors - 0.5, 0, 1),  # brighter
          linewidth=0
          )

    # plot1=[ax1.plot_surface(x_mesh, y_mesh, Tout[0,:,:].T)]
