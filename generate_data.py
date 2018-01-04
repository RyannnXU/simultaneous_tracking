# !/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import numpy as np
import pickle as pkl
from matplotlib import path

# --- Hyper paremeters
A     = np.array([[1, 0.5, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0.5], [0, 0, 0, 1]])
mean  = np.array([0, 0, 0, 0])
Sigma = np.diag([1.0e-10, 1.0e-6, 1.0e-10, 1.0e-6])

INITIAL_STATE  = np.array([0, 0.05, 0, 0.05])
SPEED_LIM_RATE = 0.2

UP     = 2
DOWN   = 0
LEFT   = 0
RIGZHT = 2

# # --- position of camera
# RECTS = {1: {'fov_center': (1.3, 1.0), 'fov_size': (0.4, 0.4), 'fov_angle': 0},
# 			  2: {'fov_center': (1.0, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 90},
# 			  3: {'fov_center': (1.0, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -90},
# 			  4: {'fov_center': (0.2, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 45},
# 			  5: {'fov_center': (1.8, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 135},
# 			  6: {'fov_center': (0.2, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -45},
# 			  7: {'fov_center': (1.8, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -135},
# 			  8: {'fov_center': (0.7, 1.0), 'fov_size': (0.4, 0.4), 'fov_angle': 180}}


def compute_vertices(rects):

	'''
	Given fov_center coordinate of rectangulars (represent camera FOV), find vertice coordinates

	Input:  rectangulars with fov_center coordinates
	Output: vertice coordinates
	'''

	rects_with_vertices = {}
	for i in range(len(rects)):

		ii = i + 1
		rect   = rects[ii]
		fov_center = rect['fov_center']
		fov_size   = rect['fov_size']
		fov_angle  = rect['fov_angle']

		# --- coordinates of fov_vertices
		fov_vertices = []
		diagonal = np.hypot(fov_size[0], fov_size[1])

		for j in range(4):

			theta    = np.radians(fov_angle + 45. + 90.0 * j)
			x_j = diagonal / 2. * np.cos(theta) + fov_center[0]
			y_j = diagonal / 2. * np.sin(theta) + fov_center[1]
			# print(x_j, y_j)  # check whether the coordinates of cameras are correct
			fov_vertices.append(np.array([x_j, y_j]))

		# --- save fov_vertices
		vertices_array = np.array(fov_vertices)
		rect['fov_vertices'] = vertices_array
		rects_with_vertices[ii] = rect

	return rects_with_vertices


def one_step_bouncing_walk(current_state):
	'''
	One step random walk, the agent will bounce back if come against the wall (default to be x(0, 2) y(0, 2));  There will be random noise adding to the position and speed;  The speed are restricted to (0.8, 1.2) of original speed in case the speed becomes too big.

	Input:   current_state [p_x, v_x, p_y, v_y]
	Out_put: next_state [p_x, v_x, p_y, v_y]
	'''

	v_t  = np.random.multivariate_normal(mean, Sigma)
	next_state = np.dot(A, current_state) + v_t

	# --- bounce back from wall
	if next_state[0] < 0 or next_state[0] > 2:

		next_state[0] = current_state[0]
		next_state[1] = - current_state[1]

	if next_state[2] < 0 or next_state[2] > 2:

		next_state[2] = current_state[2]
		next_state[3] = - current_state[3]

	# --- restrict the speed
	abs1  = np.absolute(next_state[1])
	abs3  = np.absolute(next_state[3])
	sign1 = np.sign(next_state[1])
	sign3 = np.sign(next_state[3])
	abs1_clip = np.clip(abs1, INITIAL_STATE[1] * (1 - SPEED_LIM_RATE), INITIAL_STATE[1] * (1 + SPEED_LIM_RATE))
	abs3_clip = np.clip(abs3, INITIAL_STATE[3] * (1 - SPEED_LIM_RATE), INITIAL_STATE[3] * (1 + SPEED_LIM_RATE))
	next_state[1] = sign1 * abs1_clip
	next_state[3] = sign3 * abs3_clip

	return next_state


def bouncing_ball(T):
	'''
	T-step bouncing ball, calling "one_step_bouncing_walk()" fucntion T times.

	Input:   trajecotry length "T"
	Out_put: whole trajectory [p_x, v_x, p_y, v_y]
	'''

	current_state = INITIAL_STATE

	t = 0
	real_trajectory = [current_state]
	while t < T:

		next_state = one_step_bouncing_walk(current_state)
		current_state = next_state
		real_trajectory.append(current_state)
		t += 1

	return current_state, np.array(real_trajectory)


def generate_data(rects):

	# --- generate the trajectory and patches
	rects_with_vertices = compute_vertices(rects)  # camera FOVs
	_, traj = bouncing_ball(1000)
	points  = np.array([traj[:, 0], traj[:, 2]]).T
	idx     = np.arange(points.shape[0])

	# --- the first loop is number of cameras
	fov_data = {}
	for i in range(len(rects_with_vertices)):

		ii = i + 1
		rect = rects_with_vertices[ii]
		fov_vertices = rect['fov_vertices']

		# --- check which points lie in with camera FOV
		path0 = path.Path(fov_vertices)
		flag  = path0.contains_points(points)
		inside_idx   = idx[flag]
		fov_traj     = points[flag] - rect['fov_center']  # store relative coordinate to center
		fov_traj_idx = np.concatenate((fov_traj, np.expand_dims(inside_idx, axis=1)), axis=1)
		rect['fov_traj'] = fov_traj_idx
		fov_data[ii] = rect

	data = {}
	data['fov'] = fov_data
	data['groundturth_traj'] = traj
	file_name = 'data/fov_data.pkl'
	pkl.dump(data, open(file_name, 'wb'))

	return data








