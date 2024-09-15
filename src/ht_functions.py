import os
import sys
import numpy as np
from numpy import pi

def calculate_dt(dx, alpha):
	dt = 0.5 * dx**2 / (2*alpha) #dt needed for stability can do larger however good rule of thumb
	return dt

def step_thru_time_radial_1d(n_time_steps, dt, r_vec, alpha, T):

	dr = r_vec[1] - r_vec[0]
	# initialize results array
	Tout = np.empty(
		shape = (n_time_steps, r_vec.size, 1)
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

def step_thru_time_cart_2d(n_time_steps, dt, Xvec, Yvec, alpha, T_start):

	# from https://www.aeroodyssey.org/3d-heat-equation

	# initialize results array
	Tout = np.empty(
		shape = (n_time_steps, Yvec.size, Xvec.size)
		)

	T = T_start

	dx = Xvec[1] - Xvec[0]
	dy = Yvec[1] - Yvec[0]

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

def calculate_gradients_cartesian(T, ix, iy, iz, dx_vec):
	grad_x = (T[ix+1, iy, iz] - 2 * T[ix, iy, iz] + T[ix-1, iy, iz]) / dx_vec[0]**2
	grad_y = (T[ix, iy+1, iz] - 2 * T[ix, iy, iz] + T[ix, iy-1, iz]) / dx_vec[1]**2
	grad_z = (T[ix, iy, iz+1] - 2 * T[ix, iy, iz] + T[ix, iy, iz-1]) / dx_vec[2]**2
	sum_grad = grad_x + grad_y + grad_z
	return sum_grad

def calculate_gradients_cylindrical(T, ix, iy, iz, dx_vec, space_vectors):
	
	grad_r = (
		(T[ix + 1, iy, iz] - 2 * T[ix, iy, iz] + T[ix - 1, iy, iz]) / (dx_vec[0]**2) +
		(1 / (space_vectors[0][ix] + dx_vec[0] / 2)) * (T[ix + 1, iy, iz] - T[ix - 1, iy, iz]) / (2 * dx_vec[0])
	)
	
	if iy == 0:
		grad_theta = (1 / space_vectors[0][ix]**2) * (T[ix, iy + 1, iz] - 2 * T[ix, iy, iz] + T[ix, -1, iz]) / dx_vec[1]**2
	elif iy == len(space_vectors[1]):
		grad_theta = (1 / space_vectors[0][ix]**2) * (T[ix, iy + 1, iz] - 2 * T[ix, iy, iz] + T[ix, iy - 1, iz]) / dx_vec[1]**2
	else:
		grad_theta = (1 / space_vectors[0][ix]**2) * (T[ix, 0, iz] - 2 * T[ix, iy, iz] + T[ix, iy - 1, iz]) / dx_vec[1]**2
	
	grad_z = (T[ix, iy, iz + 1] - 2 * T[ix, iy, iz] + T[ix, iy, iz - 1]) / dx_vec[2]**2
	
	sum_grad = grad_r + grad_theta + grad_z
	
	return sum_grad

def step_thru_time_3d(
	n_time_steps,
	dt,
	T_start,
	space_vectors,
	alpha,
	geometry = 'cartesian',
	print_progress = False
	):
	
	T_matrix = np.empty(
		shape = [n_time_steps] + [len(x) for x in space_vectors]
		)

	dx = [x[1] - x[0] for x in space_vectors]

	T_current = T_start

	for i_time in range(n_time_steps):
		T_last = T_current
		for iz in range(1, len(space_vectors[2]) - 1):
			for iy in range(len(space_vectors[1])):
				for ix in range(1, len(space_vectors[0]) - 1):
					if geometry == 'cartesian':
						if ((iy > 0) & (iy < len(space_vectors[1]))):
							sum_grad = calculate_gradients_cartesian(T_last, ix, iy, iz, dx)
							T_current[ix, iy, iz] = T_last [ix, iy, iz] + dt * alpha * sum_grad
					elif geometry == 'cylindrical':
						sum_grad = calculate_gradients_cylindrical(T_last, ix, iy, iz, dx, space_vectors)
						T_current[ix, iy, iz] = T_last [ix, iy, iz] + dt * alpha * sum_grad
		T_matrix[i_time] = T_current
		
		if print_progress:
			if np.mod(i_time, 60) == 0:
				print('time (minutes):')
				print(np.round(i_time * dt, 0) / 60)
				print('mean temp (deg C):')
				print(np.round(T_current.mean(), 1))

	return T_matrix
