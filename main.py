# !/usr/local/bin/python3
# _*_ coding: utf-8 _*_

import pickle as pkl
from generate_data import *
from parameters import *
from plot_traj import *
# import pdb


def main():

	# --- generate data and load data
	generate_data(RECTS, 1000)
	data = pkl.load(open('data/fov_data_0.pkl', 'rb'), encoding='latin1')
	fov_data, ground_traj = data['fov'], data['groundturth_traj']
	# print(fov_data[1].keys())
	# print(fov_data[1]['fov_center'])
	# print(fov_data[1]['fov_size'])
	# print(fov_data[1]['fov_angle'])
	# print(fov_data[1]['label_angle'])
	# print(fov_data[1]['label_center'])
	# print(fov_data[1]['fov_vertices'])
	# print(fov_data[1]['fov_traj'])

	# plot_traj(ground_traj, fov_data)
	# plot_fov(fov_data)

	# # --- optimization process
	T   = len(ground_traj)
	chi = np.zeros(3 * len(fov_data) + 4 * T)
	optimize(T, chi, fov_data)

	# for i in range(1, len(RECTS)):
	# 	ii = i + 1
	# 	fov_data[ii]['fov_angle'] = 360 * np.random.random()
	# 	fov_data[ii]['fov_center'] = np.random.uniform(0.2, 1.8, 2)

	# plot_fov(fov_data)


if __name__ == '__main__':

	main()
