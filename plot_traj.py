# !/usr/local/bin/python3
# _*_ coding: utf-8 _*_


import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


def find_lowerleft(arr):
	'''
	Given an 2-D array, find the lowerleft vertice.

	Input:  arr: an 2-D array
	Output: lowerleft_vertice: (x, y)
	'''

	Y      = arr[:, 1]
	y_min  = np.min(Y)
	lowers = []

	for ii in range(len(Y)):
		if np.abs(Y[ii] - y_min) < 1e-5:
			lowers.append(arr[ii, :])

	lowers  = np.array(lowers)
	idx_min = np.argmin(np.sum(lowers, axis=1))
	lowerleft_vertice = (lowers[idx_min][0], lowers[idx_min][1])

	return lowerleft_vertice


def center_to_lowerleft(rects):

	'''
	Convert fov_center coordinate of rectangulars (represent camera FOV) to lowerleft vertice coordinate

	Input:  rectangulars with fov_center coordinates
	Output: rectangulars with lowerleft vertice coordinates
	'''

	for i in range(len(rects)):

		ii         = i + 1
		rect       = rects[ii]
		fov_center = rect['fov_center']
		fov_size   = rect['fov_size']
		fov_angle  = rect['fov_angle']

		# --- coordinates of fov_vertices
		fov_vertices = []
		diagonal     = np.hypot(fov_size[0], fov_size[1])

		for j in range(4):

			theta = np.radians(fov_angle + 45. + 90.0 * j)
			x_j   = diagonal / 2. * np.cos(theta) + fov_center[0]
			y_j   = diagonal / 2. * np.sin(theta) + fov_center[1]
			# print(x_j, y_j)  # check whether the coordinates of cameras are correct
			fov_vertices.append(np.array([x_j, y_j]))

		# --- find the lower left vertice
		vertices_array            = np.array(fov_vertices)
		lowerleft_vertice         = find_lowerleft(vertices_array)
		rect['lowerleft_vertice'] = lowerleft_vertice
		rects[ii]       = rect

	return rects


def plot_traj(traj, rects):

	x   = traj[:, 0]
	y   = traj[:, 2]
	fig = plt.figure()
	ax  = fig.add_subplot(111, aspect='equal')

	lowerleft_rects = center_to_lowerleft(rects)

	# --- add patches
	for i in range(len(lowerleft_rects)):

		ii = i + 1
		rect = lowerleft_rects[ii]
		lowerleft_vertice = rect['lowerleft_vertice']
		fov_angle  = rect['fov_angle'] % 90.  # needs attention, this is for plot, we already found the lowerleft vertice, so the rotation when ploting is either 0 or 45.
		fov_size   = rect['fov_size']
		fov_center = rect['fov_center']
		patch = patches.Rectangle(lowerleft_vertice, fov_size[0], fov_size[1], angle=fov_angle, ls=None, color='k', alpha=0.20, fill=True)
		ax.add_patch(patch)
		ax.text(fov_center[0], fov_center[1], str(ii), fontsize=10)

	ax.add_patch(patches.Rectangle((-0.0, -0.0), 2.0, 2.0, lw=3, ls=None, fill=False))
	ax.set_xlim([-0.2, 2.2])
	ax.set_ylim([-0.2, 2.2])
	ax.plot(x, y, 'x', markersize=2, markeredgecolor='b')

	# --- dynamic trajectory
	# graph, = ax.plot([], [], '-')

	# def animate(i):
	# 	graph.set_data(x[:i + 1], y[:i + 1])
	# 	return graph

	# ani = FuncAnimation(fig, animate, frames=len(x), interval=200, repeat=False)
	plt.show()


def rotate_around_origin(rotate_points, theta):

	'''
	Rotate a point around a center_point for 'theta' degree, compute the new coordinate

	Input:  center_point, rotate_point, theta
	Output: [x_r, y_r]  # rotated point
	'''

	theta = np.radians(theta)
	absolute_coords = []
	center_point = [0., 0.]

	for ii in range(len(rotate_points)):
		rotate_point = rotate_points[ii]
		relative_x = rotate_point[0] - center_point[0]
		relative_y = rotate_point[1] - center_point[1]
		relative_coord = [relative_x * np.cos(theta) - relative_y * np.sin(theta), relative_x * np.sin(theta) + relative_y * np.cos(theta)]
		absolute_coord = [relative_coord[0] + center_point[0], relative_coord[1] + center_point[1]]
		absolute_coords.append(np.array(absolute_coord))

	absolute_coords = np.array(absolute_coords)

	return np.array(absolute_coords)


def plot_fov(data_fov):

	'''
	Plot the camera FOVs, and the trajectory in trajectory

	Input: data_fov: dictionary with keys: {'fov_center', 'fov_traj', 'fov_size', 'label_angle', 'lowerleft_vertice', 'fov_angle', 'fov_vertices', 'label_center'}
	'''

	fig = plt.figure()
	ax  = fig.add_subplot(111, aspect='equal')
	data_fov_lowerleft = center_to_lowerleft(data_fov)

	for i in range(len(data_fov_lowerleft)):

		ii = i + 1

		# --- plot FOVs
		rect         = data_fov_lowerleft[ii]
		label_angle  = rect['label_angle'] % 90.
		fov_angle    = rect['fov_angle'] % 90.
		fov_center   = rect['fov_center']
		fov_size     = rect['fov_size']
		ll_vertice   = rect['lowerleft_vertice']  # lowerleft vertice
		fov_traj     = rect['fov_traj'][:, :2]

		patch = patches.Rectangle(ll_vertice, fov_size[0], fov_size[1], angle=fov_angle, ls=None, color='k', alpha=0.20, fill=True)
		ax.add_patch(patch)
		ax.text(fov_center[0], fov_center[1], str(ii), fontsize=10)

		# --- plot trajectories in FOVs
		rotate_angle   = fov_angle - label_angle

		if len(fov_traj) > 0:
			rotated_traj   = rotate_around_origin(fov_traj, rotate_angle) + fov_center
			ax.plot(rotated_traj[:, 0], rotated_traj[:, 1], 'x', markersize=2)

	ax.add_patch(patches.Rectangle((-0.0, -0.0), 2.0, 2.0, lw=3, ls=None, fill=False))
	ax.set_xlim([-0.2, 2.2])
	ax.set_ylim([-0.2, 2.2])
	plt.show()















