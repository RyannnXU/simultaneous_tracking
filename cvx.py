# !/usr/local/bin/python3
# _*_ coding: utf-8 _*_

import numpy as np
from cvxpy import *


def main():

	np.random.seed(0)
	m = 3
	n = 3
	A = np.random.randn(m, n)
	b = np.random.randn(m)
	x = Variable(n)

	los  = sum_squares(A * x - b)
	obj  = Minimize(los)
	cons = []
	prob = Problem(obj, cons)

	result = prob.solve()
	print(x.value, los.value)


if __name__ == '__main__':

	main()
