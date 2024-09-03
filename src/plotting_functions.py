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

def make_animation(x_vec, y_vec, Tout, geometry = 'radial'):
	
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
	# plt.show()

    return animation

    # fig = plt.figure()
    # ax1 = plt.axes(projection = "3d")
    # ax1.set_xlabel('x axis (mm)')
    # ax1.set_ylabel('y axis (mm)')
    # ax1.set_zlabel('Temperature (C)')
    # ax1.set_xlim(-r_max, r_max)
    # ax1.set_ylim(-r_max, r_max)
    # ax1.set_zlim(0, 100)
    # r_mesh, theta_mesh = np.meshgrid(r_vec, theta_vec)
    # X_plot, Y_plot = r_mesh * np.cos(theta_mesh), r_mesh * np.sin(theta_mesh)
    # plot1=[ax1.plot_surface(X_plot, Y_plot, Tout[0,:,:].T)]

    # animation = ani.FuncAnimation(
    #     fig = fig,
    #     func = frame,
    #     frames = n_time_steps,
    #     fargs = (Tout, X_plot, Y_plot, plot1),
    #     interval = 20,
    #     blit = False
    #     )