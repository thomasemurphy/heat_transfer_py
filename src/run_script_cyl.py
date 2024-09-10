import numpy as np
from numpy import pi
import matplotlib.pyplot as plt #import plotting library
from matplotlib import cm #import color for surface plot
import os, sys
import matplotlib.animation as ani #importing animation library
import ht_functions as htf
import plotting_functions as ptf

# in terminal: python3 src/run_script.py

if __name__ == "__main__":
	
	# set thermal diffusivity, in mm2 / s
	alpha = 97 # aluminum
	alpha = 0.143 # water
	
	# radius (mm)
	R = 50
	Z = 100
	
	#number of points in each dimension
	n_points_r = 50
	n_points_theta = 12
	n_points_z = 50

	#Discretize space
	r_vec = np.linspace(0, R, n_points_r)
	theta_vec = np.linspace(0, 2 * pi, n_points_theta)
	z_vec = np.linspace(0, Z, n_points_z)
	space_vectors = [r_vec, theta_vec, z_vec]
	dx_vec = [x[1] - x[0] for x in space_vectors]

	print(dx_vec)
	
	# need a better way to set dt for radial
	# #Discretize time
	# print([htf.calculate_dt(dx, alpha) for dx in dx_vec])
	# dt = min([htf.calculate_dt(dx, alpha) for dx in dx_vec])
	# print(dt)

	dt = 1
	t_end = 60
	n_time_steps = int(t_end / dt)

	# inital conditions
	T_init = 2 # fridge
	T_init_full = np.full(
		[len(x) for x in space_vectors],
		float(T_init)
		)

	# boundary conditions
	T_boundary = float(80) #C
	T_init_full[-1, :, :] = T_boundary
	T_init_full[:, :, 0] = T_boundary
	T_init_full[:, :, -1] = T_boundary

	T_matrix = htf.step_thru_time_3d(
		n_time_steps = n_time_steps,
		dt = dt,
		T_start = T_init_full,
		space_vectors = space_vectors,
		alpha = alpha,
		geometry = 'cylindrical'
		)

	print(T_matrix[20, :, 0, 20])

	# animation = ptf.make_animation(Xvec, Yvec, Tout, geometry = 'cartesian')

	# print('made animation')

	# # save to file
	# animation.save(filename = 'gifs/square_milk_bottle_draft.gif', writer = 'pillow')

	# print('saved animation')


