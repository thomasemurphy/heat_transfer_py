import numpy as np
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

volume_cold_side_oz = 2

volume_cold_side_m3 = volume_cold_side_oz * 2.957e-5

conductivity_glass = 1.2 # W/mK

radius_bottle = .025 #m

area_bottom_bottle = pi * radius_bottle**2

milk_height = volume_cold_side_m3 / area_bottom_bottle

area_side_bottle = 2 * pi * radius_bottle * milk_height

area_total_ht = area_bottom_bottle + area_side_bottle

