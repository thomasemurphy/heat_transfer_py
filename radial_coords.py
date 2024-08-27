import numpy as np
from numpy import pi
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

def step_thru_time_radial(n_time_steps, dt, r_vec, theta_vec, alpha, T):

	# initialize results array
	Tout = np.empty(
		shape = (n_time_steps, r_vec.size, theta_vec.size)
		)

	# for each time, for each r, for each theta: update temperature
	for i in range (n_time_steps):
	    Told = T
	    for ir in range(1, r_vec.size-1):
	        for itheta in range(1, theta_vec.size-1):
	            T[ir, itheta] = (
	            	Told[ir, itheta] +
	            	dt * alpha * (
	            		(Told[ir+1, itheta] - 2*Told[ir, itheta] + Told[ir-1, itheta]) / dr**2 +
	            		(1 / r_vec[ir]) * (Told[ir+1, itheta] - Told[ir-1, itheta]) / (2 * dr)
	            		)
	            	)
	            Tout[i] = T
	return Tout


if __name__ == "__main__":
	
	# set thermal diffusivity, in mm2 / s
	alpha = 97 # aluminum
	alpha = 0.143 # water
	
	D_circle_in = 2
	D_circle_mm = D_circle_in * 25.4
	R_circle_outer = D_circle_mm / 2

	#number of radial nodes
	n_inc_r = 36
	r_min = 0.1

	# number of around-circle nodes
	n_inc_theta = 36

	# discretize circular space
	r_vec = np.linspace(r_min, R_circle_outer, n_inc_r)
	theta_vec = np.linspace(0, 2 * pi, n_inc_theta)
	dr = r_vec[2] - r_vec[1]
	dtheta = theta_vec[2] - theta_vec[1]
	r_max = r_vec[-1]
	
	#Discretize time
	dt = calculate_dt(dr, alpha)
	print(dt)
	t_end = 600
	n_time_steps = int(t_end / dt)

	# inital conditions
	T_init = 2 # fridge
	T = np.full(
		(r_vec.size, theta_vec.size),
		T_init
	)

	# boundary condition on edge of circle
	T_boundary = 80 #C
	T[:,-1] = T_boundary

	print(T)

	Tout = step_thru_time_radial(n_time_steps, dt, r_vec, theta_vec, alpha, T)

	print('made Tout')

	# print(Tout)

	
	# plot

	fig = plt.figure()
	ax = fig.add_subplot(projection='3d')
	
	# Create the mesh in polar coordinates and compute corresponding Z.
	r_mesh, theta_mesh = np.meshgrid(r_vec, theta_vec)

	# Express the mesh in the cartesian system.
	X_plot, Y_plot = r_mesh * np.cos(theta_mesh), r_mesh * np.sin(theta_mesh)

	# Plot the surface.
	ax.plot_surface(X_plot, Y_plot, Tout[200, :, :], cmap=plt.cm.YlGnBu_r)
	
	plt.show()

	# fig = plt.figure()
	# ax1 = plt.axes(projection = "3d")
	# ax1.set_xlabel('x axis (mm)')
	# ax1.set_ylabel('y axis (mm)')
	# ax1.set_zlabel('Temperature (C)')
	# ax1.set_xlim(0, Lx)
	# ax1.set_ylim(0, Ly)
	# ax1.set_zlim(0, 100)
	# X, Y = np.meshgrid(Xvec, Yvec)
	# plot1=[ax1.plot_surface(X, Y, Tout[0,:,:])]

	# animation = ani.FuncAnimation(
	# 	fig = fig,
	# 	func = frame,
	# 	frames = n_time_steps,
	# 	fargs = (Tout, plot1),
	# 	interval = 400,
	# 	blit = False
	# 	)
	# plt.show()

	# print('made animation')

	# save to file
	# animation.save(filename = 'square_milk_bottle_draft.gif', writer = 'pillow')

	# print('saved animation')


