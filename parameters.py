# !/usr/local/bin/python3
# _*_ coding: utf-8 _*_

import numpy as np

# --- Hyper paremeters
A        = np.array([[1, 0.5, 0, 0],
					 [0, 1, 0, 0],
					 [0, 0, 1, 0.5],
					 [0, 0, 0, 1]])
C        = np.array([[1, 0, 0, 0], [0, 0, 1, 0]])
MEAN     = np.array([0, 0, 0, 0])
SIGMA_V2 = np.diag([1.0e-10, 1.0e-6, 1.0e-10, 1.0e-6])
SIGMA_Y2 = 1.0e-10
SIGMA_U2 = 1.0e-10

RECTS = {1: {'fov_center': (1.3, 1.0), 'fov_size': (0.4, 0.4), 'fov_angle': 0, 'label_angle': 0, 'label_center': (1.3, 1.0)},
			  2: {'fov_center': (1.0, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 90, 'label_angle': 90, 'label_center': (1.0, 0.2)},
			  3: {'fov_center': (1.0, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -90, 'label_angle': -90, 'label_center': (1.0, 1.8)},
			  4: {'fov_center': (0.2, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 45, 'label_angle': 45, 'label_center': (0.2, 0.2)},
			  5: {'fov_center': (1.8, 0.2), 'fov_size': (0.4, 0.4), 'fov_angle': 135, 'label_angle': 135, 'label_center': (1.8, 0.2)},
			  6: {'fov_center': (0.2, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -45, 'label_angle': -45, 'label_center': (0.2, 1.8)},
			  7: {'fov_center': (1.8, 1.8), 'fov_size': (0.4, 0.4), 'fov_angle': -135, 'label_angle': -135, 'label_center': (1.8, 1.8)},
			  8: {'fov_center': (0.7, 1.0), 'fov_size': (0.4, 0.4), 'fov_angle': 180, 'label_angle': 180, 'label_center': (0.7, 1.0)}}
