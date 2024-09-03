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
    	T_all[frame_number,:,:],
    	cmap=cm.jet
    	)

# # im not ready yet
# def make_animation(Lx, Ly, Xvec, Yvec, Tout, n_time_steps):
# 	fig = plt.figure()
# 	ax1 = plt.axes(projection="3d")
# 	ax1.set_xlabel('x axis (mm)')
# 	ax1.set_ylabel('y axis (mm)')
# 	ax1.set_zlabel('Temperature (C)')
# 	ax1.set_xlim(0,Lx)
# 	ax1.set_ylim(0,Ly)
# 	ax1.set_zlim(0,200)
# 	X, Y = np.meshgrid(Xvec, Yvec)
# 	plot1=[ax1.plot_surface(X, Y, Tout[0,:,:])]

# 	animation = ani.FuncAnimation(
# 		fig = fig,
# 		func = frame,
# 		frames = n_time_steps,
# 		fargs = (Tout,plot1),
# 		interval = 60,
# 		blit = False
# 		)
# 	# plt.show()

# 	return animation