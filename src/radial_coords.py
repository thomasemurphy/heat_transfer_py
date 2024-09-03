import numpy as np
from numpy import pi
import matplotlib.pyplot as plt #import plotting library
from matplotlib import cm #import color for surface plot
import os, sys
import matplotlib.animation as ani #importing animation library
import ht_functions as htf
import plotting_functions as ptf

# from https://www.aeroodyssey.org/3d-heat-equation

def frame(frame_number, Tout, X, Y, plot):
    plot[0].remove()
    plot[0] = ax1.plot_surface(
    	X,
    	Y,
    	Tout[frame_number,:,:].T,
    	cmap=cm.jet
    	)

if __name__ == "__main__":

	print('hello world!')
	
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
	dt = htf.calculate_dt(dr, alpha)
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

	Tout = htf.step_thru_time_radial_1d(n_time_steps, dt, r_vec, alpha, T)

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

	animation = ptf.make_animation(r_vec, theta_vec, T_full, geometry = 'radial')

	print('made animation')

	# save to file
	animation.save(filename = 'gifs/cylinder_milk_bottle_draft.gif', writer = 'pillow')

	print('saved animation')


