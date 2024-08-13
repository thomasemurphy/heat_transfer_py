import numpy as np
import pandas as pd
from numpy import pi

# hot side temperature
# assume constant (infinite reservoir)
# celsius
T_h = 80

# cold side initial temperature
# assume good mixing so uniform temperature
# celsius
T_c_i = 2

# fluid density inside
# kg / m3
density_cold_side = 1000 # water

# specific heat inside
# J / kgK
cv_cold_side = 4184 # water

# wall conductivity
conductivity_glass = 1.2 # W/mK

# bottle geometry
volume_cold_side_oz = 2
volume_cold_side_m3 = volume_cold_side_oz * 2.957e-5
radius_bottle = .025 #m
area_bottom_bottle = pi * radius_bottle**2
milk_height = volume_cold_side_m3 / area_bottom_bottle
area_side_bottle = 2 * pi * radius_bottle * milk_height
area_total_ht = area_bottom_bottle + area_side_bottle
wall_thickness = .003 #m  3mm?

# lumped terms for convenience
conduction_term_lumped = conductivity_glass * area_total_ht / wall_thickness
capacitance_term_lumped = density_cold_side * cv_cold_side * volume_cold_side_m3

# time parameters
max_time = 300 # seconds
dt = 1 # second
n_time_steps = int(max_time / dt)

# initialize datframe
time_temp_df = pd.DataFrame(columns = ['t', 'T_h', 'T_c', 'q', 'dThdt', 'dTcdt', 'dTh', 'dTc'])

# initial conditions
time_temp_df.loc[0, 't'] = 0
time_temp_df.loc[0, 'T_h'] = T_h
time_temp_df.loc[0, 'T_c'] = T_c_i

# step thru time
for it in range(n_time_steps):
	time_temp_df.loc[it, 'q'] = conduction_term_lumped * (time_temp_df['T_h'][it] - time_temp_df['T_c'][it])
	time_temp_df.loc[it, 'dThdt'] = 0
	time_temp_df.loc[it, 'dTcdt'] = time_temp_df['q'][it] / capacitance_term_lumped
	time_temp_df.loc[it, 'dTh'] = 0
	time_temp_df.loc[it, 'dTc'] = time_temp_df['dTcdt'][it] * dt
	time_temp_df.loc[it + 1, 't'] = time_temp_df['t'][it] + dt
	time_temp_df.loc[it + 1, 'T_h'] = T_h
	time_temp_df.loc[it + 1, 'T_c'] = time_temp_df['T_c'][it] + time_temp_df['dTc'][it]

# save results
time_temp_df.to_csv('milk_temp.csv')
