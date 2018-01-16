'''
Newton Optimization, To be done.
'''

import numpy as np
import pickle as pkl
from parameters import *
from cvxpy import *


def compute_G(A, sigma_v2, T):

	'''
	Given time length of trajectory 'T', correlation matrix 'sigma_v2', and motion dynamics 'A', compute the 'G' matrix

	Input : (A, sigma_v2, T)
	Output: 'G' matrix
	'''

	sigma_inv    = np.sqrt(np.linalg.inv(sigma_v2))
	n_row, n_col = sigma_inv.shape
	G            = np.zeros((n_row * (T - 1), n_col * T))

	for t in range(1, T):

		init_row   = (t - 1) * n_row
		end_row    = t * n_row
		init_col_1 = (t - 1) * n_col
		end_col_1  = t * n_col
		init_col_2 = t * n_col
		end_col_2  = (t + 1) * n_col

		G[init_row:end_row, init_col_1:end_col_1] = np.dot(sigma_inv, A)
		G[init_row:end_row, init_col_2:end_col_2] = -sigma_inv

	return G


def compute_r(fov_data, chi_t, G, u0):
	'''
	Construct vector 'r', given fov data 'fov_data', current variable 'chi_t', matrix 'G', and prior knowledge 'u0';
	Note 'theta_i' in 'chi_t' is in radian, very important !!!

	Input : (fov_data, chi_t, G, u0)
	Output: vector 'r'
	'''

	n_cam = len(fov_data)
	u     = chi_t[:n_cam * 3]
	x_1d  = np.array(chi_t[n_cam * 3:])
	x_2d  = x_1d.reshape((-1, 4))  # (T, 4)
	r     = []

	for i in range(n_cam):

		ii = i + 1

		# --- parameters in camera 'i'
		mu_i    = u[(ii - 1) * 3:ii * 3]
		p_i     = mu_i[:2]
		theta_i = mu_i[-1]
		R_i     = np.array([[np.cos(theta_i), np.sin(theta_i)], [-np.sin(theta_i), np.cos(theta_i)]])

		# --- fov data for camera 'ii'
		fov_traj = fov_data[ii]['fov_traj']
		idx_i    = fov_traj[:, -1].astype(int)
		y_i      = fov_traj[:, :-1]
		x_i      = x_2d[idx_i]

		r_y = 1. / np.sqrt(SIGMA_Y2) * (np.dot(R_i, (np.dot(C, x_i.T).T - p_i).T).T - y_i)
		r.append(r_y.reshape(-1))

	r    = np.concatenate(r, axis=0)
	r_x  = np.dot(G, x_1d)
	u1   = chi_t[:3]
	r_mu = 1. / np.sqrt(SIGMA_U2) * (u1 - u0)
	r    = np.concatenate([r, r_x])
	r    = np.concatenate([r, r_mu])

	return r


def compute_J(fov_data, chi_t, G, u0, l_r):
	'''
	Construct Jacobian matrix 'J', given fov data 'fov_data', current variable 'chi_t', matrix 'G', prior knowledge 'u0', and length of vector 'r': 'l_r';
	Note 'theta_i' in 'chi_t' is in radian, very important !!!
	'''

	n_cam  = len(fov_data)
	u      = chi_t[:n_cam * 3]
	x_1d   = np.array(chi_t[n_cam * 3:])
	x_2d   = x_1d.reshape((-1, 4))

	T      = (len(chi_t) - n_cam * 3) // 4
	x_rows = 4 * (T - 1)
	x_cols = 4 * T
	u_rows = l_r - 4 * (T - 1) - 3
	u_cols = n_cam * 3
	print(x_rows, x_cols, u_rows, u_cols)

	inv_sigma_y = 1. / np.sqrt(SIGMA_Y2)
	inv_sigma_u = 1. / np.sqrt(SIGMA_U2)

	# --- 'J_uu'
	J_uu   = np.zeros((u_rows, u_cols))
	J_uu_1 = []
	J_uu_2 = []

	for k in range(n_cam):

		ii = k + 1

		# --- parameters in camera 'i'
		mu_i    = u[(ii - 1) * 3:ii * 3]
		p_i     = mu_i[:2]
		theta_i = mu_i[-1]
		# R_i     = np.array([[np.cos(theta_i), np.sin(theta_i)], [-np.sin(theta_i), np.cos(theta_i)]])

		# --- data
		fov_traj = fov_data[ii]['fov_traj']
		idx_i    = fov_traj[:, -1].astype(int)
		# y_i      = fov_traj[:, :-1]
		x_i      = x_2d[idx_i]

		temp1 = np.zeros((len(x_i), u_cols))
		temp2 = np.zeros((len(x_i), u_cols))

		temp1[:, 3 * k] = -inv_sigma_y * np.cos(theta_i)
		temp1[:, 3 * k + 1] = -inv_sigma_y * np.sin(theta_i)
		temp1[:, 3 * k + 2] = inv_sigma_y * (np.cos(theta_i) * (x_i[:, 1] - p_i[1]) - np.sin(theta_i) * (x_i[:, 0] - p_i[0]))
		temp2[:, 3 * k] = inv_sigma_y * np.sin(theta_i)
		temp2[:, 3 * k + 1] = -inv_sigma_y * np.cos(theta_i)
		temp2[:, 3 * k + 2] = inv_sigma_y * (-np.cos(theta_i) * (x_i[:, 0] - p_i[0]) - np.sin(theta_i) * (x_i[:, 1] - p_i[1]))
		J_uu_1.append(temp1)
		J_uu_2.append(temp2)

	J_uu_1 = np.concatenate(J_uu_1, axis=0)
	J_uu_2 = np.concatenate(J_uu_2, axis=0)

	for i in range(u_rows // 2):

		J_uu[i * 2, :] = J_uu_1[i, :]
		J_uu[i * 2 + 1, :] = J_uu_2[i, :]

	# --- 'J_ux'
	J_ux   = np.zeros((u_rows, x_cols))
	J_ux_1 = []
	J_ux_2 = []

	for k in range(n_cam):

		ii = k + 1

		# --- parameters in camera 'i'
		mu_i    = u[(ii - 1) * 3:ii * 3]
		p_i     = mu_i[:2]
		theta_i = mu_i[-1]

		# --- data
		fov_traj = fov_data[ii]['fov_traj']
		idx_i    = fov_traj[:, -1].astype(int)

		temp1 = np.zeros((len(idx_i), x_cols))
		temp2 = np.zeros((len(idx_i), x_cols))

		for j in range(len(idx_i)):

			idx_u = 4 * idx_i[j]
			idx_v = 4 * idx_i[j] + 2

			temp1[k, idx_u] = inv_sigma_y * np.cos(theta_i)
			temp1[k, idx_v] = inv_sigma_y * np.sin(theta_i)
			temp2[k, idx_u] = -inv_sigma_y * np.sin(theta_i)
			temp2[k, idx_v] = inv_sigma_y * np.cos(theta_i)

		J_ux_1.append(temp1)
		J_ux_2.append(temp2)

	J_ux_1 = np.concatenate(J_ux_1, axis=0)
	J_ux_2 = np.concatenate(J_ux_2, axis=0)

	for i in range(u_rows // 2):

		J_ux[i * 2, :] = J_ux_1[i, :]
		J_ux[i * 2 + 1, :] = J_ux_2[i, :]

	# --- 'J_xu'
	J_xu = np.zeros((x_rows, u_cols))

	# --- 'J_xx'
	J_xx = G

	J1 = np.concatenate([J_uu, J_ux], axis=1)
	J2 = np.concatenate([J_xu, J_xx], axis=1)
	J3 = np.concatenate([inv_sigma_u * np.eye(3), np.zeros((3, len(chi_t) - 3))], axis=1)
	J  = np.concatenate([J1, J2, J3], axis=0)

	print(J_uu.shape, J_uu_1.shape, J_uu_2.shape, J_ux.shape, J_ux_1.shape, J_ux_2.shape, J_xu.shape, J_xx.shape)

	return J


# def valid_func():

# 	# --- valid G matrix is correct
# 	T = 10
# 	G = compute_G(A, SIGMA_V2, T)

# 	sigma_inv = np.linalg.inv(SIGMA_V2)
# 	A1 = A.T.dot(sigma_inv).dot(A)

# 	A2 = A1 + sigma_inv
# 	A3 = sigma_inv

# 	print(A1.diagonal())
# 	print(np.dot(G.T, G).diagonal()[:4])
# 	print('\n')

# 	print(A2.diagonal())
# 	print(np.dot(G.T, G).diagonal()[4:8])
# 	print('\n')

# 	print(A3.diagonal())
# 	print(np.dot(G.T, G).diagonal()[-4:])
# 	print('\n')

# 	# --- second diagonal
# 	B1 = -A.T.dot(sigma_inv)
# 	print(np.max(B1 - np.dot(G.T, G)[:4, 4:8]))
# 	print(np.max(B1 - np.dot(G.T, G)[4:8, 8:12]))
# 	print(np.max(B1 - np.dot(G.T, G)[-8:-4, -4:]))
# 	print('\n')

# 	B2 = -sigma_inv.dot(A)
# 	print(np.max(B2 - np.dot(G.T, G)[4:8, :4]))
# 	print(np.max(B2 - np.dot(G.T, G)[8:12, 4:8]))
# 	print(np.max(B2 - np.dot(G.T, G)[-4:, -8:-4]))


# def optimize(T, chi_t, fov_data):

# 	G = compute_G(A, SIGMA_V2, T)
# 	pass


def main():

	raw_data = pkl.load(open('data/fov_data_0.pkl', 'rb'), encoding='latin1')
	fov_data = raw_data['fov']

	T   = len(raw_data['groundturth_traj'])
	G   = compute_G(A, SIGMA_V2, T)
	chi = np.ones(4 * T + 3 * len(fov_data))
	u0  = np.array([1.3, 1.0, 0])
	r   = compute_r(fov_data, chi, G, u0)
	l_r = len(r)
	J   = compute_J(fov_data, chi, G, u0, l_r)

	delta_chi = Variable(len(chi))
	objective = Minimize(sum_squares(J * delta_chi - r))
	constraints = [delta_chi >= 0, delta_chi <= 1]
	prob = Problem(objective, constraints)
	result = prob.solve()
	print(result.value)


if __name__ == '__main__':

	main()






















