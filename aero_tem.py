import numpy as np
import matplotlib.pyplot as plt #import plotting library
from matplotlib import cm #import color for surface plot
import os, sys
import matplotlib.animation as ani #importing animation library

# from https://www.aeroodyssey.org/3d-heat-equation

def calculate_dt(dx, alpha):
	dt = 0.5 * dx**2 / (2*alpha) #dt needed for stability can do larger however good rule of thumb
	return dt

def frame(frame_number,Tout,plot):
    plot[0].remove()
    plot[0] = ax1.plot_surface(
    	X,
    	Y,
    	Tout[frame_number,:,:],
    	cmap=cm.jet
    	)

def step_thru_time(n_time_steps, dt, Xvec, Yvec, alpha, T_start):

	# initialize results array
	Tout = np.empty(
		shape = (n_time_steps, Yvec.size, Xvec.size)
		)

	# for each time, for each y, for each x: update temperature
	for i in range (n_time_steps):
	    Told = T
	    for ty in range(1,Yvec.size-1):
	        for tx in range(1,Xvec.size-1):
	            T[tx, ty] = (
	            	dt * (
	            		alpha * (Told[tx+1,ty] - 2*Told[tx,ty] + Told[tx-1,ty]) / dx**2 +
	            		alpha * (Told[tx,ty+1] - 2*Told[tx,ty] + Told[tx,ty-1]) / dy**2
	            		) +
	            	Told[tx,ty]
	            	)
	    Tout[i] = T

	return Tout

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

# 	# save to file
# 	# animation.save(filename = 'test.gif', writer = 'pillow')


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
	dx = Xvec[2] - Xvec[1] #since equally spaced, i set a constant dx
	dy = Yvec[2] - Yvec[1] #since equally spaced, I set a constant dy
	
	#Discretize time
	dt = calculate_dt(dx, alpha)
	print(dt)
	t_end = 600
	n_time_steps = int(t_end / dt)

	# inital conditions
	T_init = 2 # fridge
	T = np.full((Yvec.size,Xvec.size), T_init) #entire plate is at 20 degrees C

	# boundary conditions
	# note: need to handle non-temperature boundary conditions
	T_boundary = 80 #C
	T[:,0] = T_boundary # left side of plate
	T[-1,:] = T_boundary # bottom
	T[0,:] = T_boundary # top
	T[:,-1] = T_boundary # right

	Tout = step_thru_time(n_time_steps, dt, Xvec, Yvec, alpha, T)

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
		func = frame,
		frames = n_time_steps,
		fargs = (Tout, plot1),
		interval = 400,
		blit = False
		)
	# plt.show()

	# animation = make_animation(Lx, Ly, Xvec, Yvec, Tout, n_time_steps)

	print('made animation')

	# save to file
	animation.save(filename = 'square_milk_bottle_draft.gif', writer = 'pillow')

	print('saved animation')

	print('dummy')


