import numpy as np
import matplotlib.pyplot as plt #import plotting library
from matplotlib import cm #import color for surface plot
import os, sys
import matplotlib.animation as ani #importing animation library
import ht_functions as htf
import plotting_functions as ptt

if __name__ == "__main__":
	
	# set thermal diffusivity, in mm2 / s
	alpha = 97 # aluminum
	alpha = 0.143 # water
	
	#length of sides of heated square plate (mm)
	Lx = 100 #
	Ly = 100 #
	
	#number of points
	N = 20 #number of x and y points x*y = total number of points
	
	#Discretize space
	Xvec = np.linspace(0, Lx, N)
	Yvec = np.linspace(0, Ly, N)
	dx = Xvec[2] - Xvec[1]
	dy = Yvec[2] - Yvec[1]
	
	#Discretize time
	dt = htf.calculate_dt(dx, alpha)
	print(dt)
	t_end = 600
	n_time_steps = int(t_end / dt)

	# inital conditions
	T_init = float(2) # fridge
	T = np.full((Yvec.size,Xvec.size), T_init) #entire plate is at 20 degrees C

	# boundary conditions
	# note: need to handle non-temperature boundary conditions
	T_boundary = float(80) #C
	T[:,0] = T_boundary # left side of plate
	T[-1,:] = T_boundary # bottom
	T[0,:] = T_boundary # top
	T[:,-1] = T_boundary # right

	Tout = htf.step_thru_time_cart_2d(n_time_steps, dt, Xvec, Yvec, alpha, T)

	print('made Tout')

	# add time text in animation

	fig = plt.figure()
	ax1 = plt.axes(projection="3d")
	ax1.set_xlabel('x axis (mm)')
	ax1.set_ylabel('y axis (mm)')
	ax1.set_zlabel('Temperature (C)')
	ax1.set_xlim(0, Lx)
	ax1.set_ylim(0, Ly)
	ax1.set_zlim(0, 100)
	X, Y = np.meshgrid(Xvec, Yvec)
	plot1=[ax1.plot_surface(X, Y, Tout[0,:,:])]

	animation = ani.FuncAnimation(
		fig = fig,
		func = ptt.frame,
		frames = n_time_steps,
		fargs = (Tout, X, Y, plot1, ax1),
		interval = 400,
		blit = False
		)
	# plt.show()

	# animation = make_animation(Lx, Ly, Xvec, Yvec, Tout, n_time_steps)

	print('made animation')

	# save to file
	animation.save(filename = 'square_milk_bottle_draft.gif', writer = 'pillow')

	print('saved animation')


