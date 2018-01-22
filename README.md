# Simultaneously Tracking and Calibration

## I/O

Input: Trajectory in FOVs of 8 cameras.

Output: Calibrated extrinsic parameters and the missing trajectory in blind areas.


## Code Structure

1) **'generate_data.py'** defines a bouncing ball environment, generate data in FOVs;

2) **'process_data.py'** solve the optimization problem with Newton's method;

3) **'plot_traj.py'** is for visualization;

4) **'parameters.py'** defines all the system parameters;

5) **'main.py'** calls other modules in the way of:

	* 'generate_data.py'
	* 'process_data.py'
	* 'plot_traj.py'

