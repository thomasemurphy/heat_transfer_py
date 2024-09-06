import numpy as np
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
	
	#length of sides of heated square plate (mm)
	x_len = 100 #
	y_len = 100 #
	z_len = 100
	
	#number of points in each dimension
	n_points = 40

	#Discretize space
	x_vec = np.linspace(0, x_len, n_points)
	y_vec = np.linspace(0, y_len, n_points)
	z_vec = np.linspace(0, z_len, n_points)
	space_vectors = [x_vec, y_vec, z_vec]
	dx_vec = [x[1] - x[0] for x in space_vectors]

	print(dx_vec)
	
	#Discretize time
	print([htf.calculate_dt(dx, alpha) for dx in dx_vec])
	dt = min([htf.calculate_dt(dx, alpha) for dx in dx_vec])
	print(dt)
	t_end = 600
	n_time_steps = int(t_end / dt)

	# inital conditions
	T_init = 2 # fridge
	T_init_full = np.full(
		[len(x) for x in space_vectors],
		float(T_init)
		)

	# boundary conditions
	# note: need to handle non-temperature boundary conditions
	T_boundary = float(80) #C
	T_init_full[0, :, :] = T_boundary
	T_init_full[-1, :, :] = T_boundary
	T_init_full[:, 0, :] = T_boundary
	T_init_full[:, -1, :] = T_boundary
	T_init_full[:, :, 0] = T_boundary
	T_init_full[:, :, -1] = T_boundary

	corners = ptf.centers_to_corners(space_vectors)

	T_matrix = htf.step_thru_time_3d(
		n_time_steps = n_time_steps,
		dt = dt,
		T_start = T_init_full,
		space_vectors = space_vectors,
		alpha = alpha,
		geometry = 'cartesian'
		)

	ptf.make_plot_3d(space_vectors, T_matrix[4])

	# animation = ptf.make_animation(Xvec, Yvec, Tout, geometry = 'cartesian')

	# print('made animation')

	# # save to file
	# animation.save(filename = 'gifs/square_milk_bottle_draft.gif', writer = 'pillow')

	# print('saved animation')


