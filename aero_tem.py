import numpy as np
import matplotlib.pyplot as plt #import plotting library
from matplotlib import cm #import color for surface plot
import os, sys
import matplotlib.animation as ani #importing animation library

# from https://www.aeroodyssey.org/3d-heat-equation

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
	
	alpha = 97 # (mm^2/s) thermal diffusivity, alluminum
	
	#length of sides  of heated square plate
	Lx = 152 #(mm)
	Ly = 152 #(mm)
	
	#number of points
	N = 50 #number of x and y points x*y = total number of points
	
	#Discretize space
	Xvec = np.linspace(0,Lx,N)
	Yvec = np.linspace(0,Ly,N)
	dx = Xvec[2]-Xvec[1] #since equally spaced, i set a constant dx
	dy = Yvec[2]-Yvec[1] #since equally spaced, I set a constant dy
	
	#Discretize time
	#dt=0.5*(dx**2)/(2*alpha) #dt needed for stability can do larger however good rule of thumb
	dt = 0.025
	n_time_steps = 200
	t_end = n_time_steps * dt

	# inital conditions
	T_init = 20
	T = np.full((Yvec.size,Xvec.size), T_init) #entire plate is at 20 degrees C

	# boundary conditions
	T[:,0] = 200.0 #200 degrees C applied to left side of plate
	T[-1,:] = 200.0 #200 degrees C applied to bottom of plate
	T[0,:] = 200.0 #200 degrees C applied to top of plate
	T[:,-1] = 200.0 #200 degrees C applied to right side of plate

	Tout = step_thru_time(n_time_steps, dt, Xvec, Yvec, alpha, T)

	print('made Tout')

	fig = plt.figure()
	ax1 = plt.axes(projection="3d")
	ax1.set_xlabel('x axis (mm)')
	ax1.set_ylabel('y axis (mm)')
	ax1.set_zlabel('Temperature (C)')
	ax1.set_xlim(0, Lx)
	ax1.set_ylim(0, Ly)
	ax1.set_zlim(0, 200)
	X, Y = np.meshgrid(Xvec, Yvec)
	plot1=[ax1.plot_surface(X, Y, Tout[0,:,:])]

	animation = ani.FuncAnimation(
		fig = fig,
		func = frame,
		frames = n_time_steps,
		fargs = (Tout, plot1),
		interval = 60,
		blit = False
		)
	# plt.show()

	# animation = make_animation(Lx, Ly, Xvec, Yvec, Tout, n_time_steps)

	print('made animation')

	# save to file
	animation.save(filename = 'test.gif', writer = 'pillow')

	print('saved animation')


