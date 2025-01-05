import numpy as np

def check_for_free_boundary(edge, is_free_boundary_dict):
	return is_free_boundary_dict[edge]

is_free_boundary_dict = (
	{
		'top': True,
		'bottom': False,
		'left': True,
		'right': False,
		'front': False,
		'back': False,
	})

# x left to right, y into page
nx = 4
ny = 4

for iy in range(ny):
	print()
	print(f"y dimension counter value: {iy}")
	print()
	if iy == 0:
		print(f"front edge, free boundary: {check_for_free_boundary('front', is_free_boundary_dict)}")
		print()
	elif iy == (ny - 1):
		print(f"back edge, free boundary: {check_for_free_boundary('back', is_free_boundary_dict)}")
		print()
	for ix in range(nx):
		print(f"x dimension counter value: {ix}")
		if ix == 0:
			print(f"left edge, free boundary: {check_for_free_boundary('left', is_free_boundary_dict)}")
		elif ix == nx - 1:
			print(f"right edge, free boundary: {check_for_free_boundary('right', is_free_boundary_dict)}")

print()
print(is_free_boundary_dict)
print()

# 15 different cases for 3d:
# 1 interior
# 8 corners
# 6 edges

# could check in the innermost
# order might matter for speed, do interior first
# brute force?