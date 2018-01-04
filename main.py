# !/usr/local/bin/python3
# _*_ coding: utf-8 _*_

import pickle as pkl
from generate_data import *
from plot_traj import *


RECTS = {1: {'fov_center': (1.3, 1.0), 'fov_size': (0.4, 0.4), 'fov_angle': 0, 'label_angle': 0, 'label_center': (1.3, 1.0)},
			  2: {'fov_center': (1.0, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 90, 'label_angle': 90, 'label_center': (1.0, 0.2)},
			  3: {'fov_center': (1.0, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -90, 'label_angle': -90, 'label_center': (1.0, 1.8)},
			  4: {'fov_center': (0.2, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 45, 'label_angle': 45, 'label_center': (0.2, 0.2)},
			  5: {'fov_center': (1.8, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 135, 'label_angle': 135, 'label_center': (1.8, 0.2)},
			  6: {'fov_center': (0.2, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -45, 'label_angle': -45, 'label_center': (0.2, 1.8)},
			  7: {'fov_center': (1.8, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -135, 'label_angle': -135, 'label_center': (1.8, 1.8)},
			  8: {'fov_center': (0.7, 1.0), 'fov_size': (0.4, 0.4), 'fov_angle': 180, 'label_angle': 180, 'label_center': (0.7, 1.0)}}


def main():

	# --- generate data and load data
	# generate_data(RECTS)
	data = pkl.load(open('data/fov_data.pkl', 'rb'))
	fov_data, ground_traj = data['fov'], data['groundturth_traj']

	# --- optimization

	plot_traj(ground_traj, fov_data)
	plot_fov(fov_data)

	for i in range(1, len(RECTS)):
		ii = i + 1
		fov_data[ii]['fov_angle'] = 360 * np.random.random()
		fov_data[ii]['fov_center'] = np.random.uniform(0.2, 1.8, 2)

	plot_fov(fov_data)


if __name__ == '__main__':

	main()
