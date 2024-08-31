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

def frame(frame_number, Tout, X, Y, plot):
    plot[0].remove()
    plot[0] = ax1.plot_surface(
    	X,
    	Y,
    	Tout[frame_number,:,:].T,
    	cmap=cm.jet
    	)

def step_thru_time_radial_1d(n_time_steps, dt, r_vec, alpha, T):

	dr = r_vec[1] - r_vec[0]
	# initialize results array
	Tout = np.empty(
		shape = (n_time_steps, r_vec.size, theta_vec.size)
		)

	# for each time, for each r, for each theta: update temperature
	for i in range (n_time_steps):
		Told = T
		for ir in range(1, r_vec.size-1):
			T[ir, 0] = (
				Told[ir, 0] +
				dt * alpha * (
					(Told[ir + 1, 0] - 2 * Told[ir, 0] + Told[ir - 1, 0]) / (dr**2) +
					(1 / (r_vec[ir] + dr / 2)) * (Told[ir + 1, 0] - Told[ir-1, 0]) / (2 * dr)
					)
				)
		# does this work? fudgy...
		T[0,0] = T[1,0] - (T[2,0] - T[1,0])
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
	n_inc_r = 20
	r_min = 0

	# discretize circular space
	r_vec = np.linspace(r_min, R_circle_outer, n_inc_r)
	theta_vec = np.array([0])
	dr = r_vec[2] - r_vec[1]
	# dtheta = theta_vec[2] - theta_vec[1]
	dtheta = 0
	r_max = r_vec[-1]
	
	#Discretize time
	dt = calculate_dt(dr, alpha)
	t_end = 600
	n_time_steps = int(t_end / dt)

	# inital conditions
	T_init = 2 # fridge
	T = np.full(
		(r_vec.size, theta_vec.size),
		float(T_init)
	)

	# boundary condition on edge of circle
	T_boundary = 80 #C
	T[-1,:] = float(T_boundary)

	Tout = step_thru_time_radial_1d(n_time_steps, dt, r_vec, alpha, T)

	print('made Tout')
	
	# plot

	# number of around-circle nodes
	n_inc_theta = 24
	# reset theta_vec
	theta_vec = np.linspace(0, 2 * pi, n_inc_theta)

	T_full = np.empty((n_time_steps, r_vec.size, theta_vec.size))

	# would like to make this faster
	for i in range(n_time_steps):
		for it in range(len(theta_vec)):
			T_full[i, :, it] = Tout[i, :, 0]

	# # Create the mesh in polar coordinates and compute corresponding Z.
	# r_mesh, theta_mesh = np.meshgrid(r_vec, theta_vec)
	# fig = plt.figure()
	# ax = fig.add_subplot(projection = '3d')
	# # Express the mesh in the cartesian system.
	# X_plot, Y_plot = r_mesh * np.cos(theta_mesh), r_mesh * np.sin(theta_mesh)
	# # Plot the surface.
	# ax.plot_surface(X_plot, Y_plot, T_full[20].T, cmap=plt.cm.YlGnBu_r)
	# plt.show()

	fig = plt.figure()
	ax1 = plt.axes(projection = "3d")
	ax1.set_xlabel('x axis (mm)')
	ax1.set_ylabel('y axis (mm)')
	ax1.set_zlabel('Temperature (C)')
	ax1.set_xlim(-r_max, r_max)
	ax1.set_ylim(-r_max, r_max)
	ax1.set_zlim(0, 100)
	r_mesh, theta_mesh = np.meshgrid(r_vec, theta_vec)
	X_plot, Y_plot = r_mesh * np.cos(theta_mesh), r_mesh * np.sin(theta_mesh)
	plot1=[ax1.plot_surface(X_plot, Y_plot, Tout[0,:,:].T)]

	animation = ani.FuncAnimation(
		fig = fig,
		func = frame,
		frames = n_time_steps,
		fargs = (Tout, X_plot, Y_plot, plot1),
		interval = 20,
		blit = False
		)
	# plt.show()

	print('made animation')

	# save to file
	animation.save(filename = 'cylinder_milk_bottle_draft.gif', writer = 'pillow')

	print('saved animation')


