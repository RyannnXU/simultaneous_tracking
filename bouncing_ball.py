
import mpl_toolkits.axisartist.floating_axes as floating_axes
import matplotlib.pyplot as plt
import numpy as np 

from matplotlib.transforms import Affine2D


# def setup_axes1(fig, rect):
#     """
#     A simple one.
#     """
#     tr = Affine2D().scale(2, 1).rotate_deg(30)

#     grid_helper = floating_axes.GridHelperCurveLinear(
#         tr, extremes=(-0.5, 3.5, 0, 4))

#     ax1 = floating_axes.FloatingSubplot(fig, rect, grid_helper=grid_helper)
#     fig.add_subplot(ax1)

#     aux_ax = ax1.get_aux_axes(tr)

#     grid_helper.grid_finder.grid_locator1._nbins = 4
#     grid_helper.grid_finder.grid_locator2._nbins = 4

#     return ax1, aux_ax


fig, ax = plt.subplots()
left, bottom, width, height = [0.25, 0.6, 0.2, 0.2]

# --- subplots
plot_extents = 0, 10, 0, 10
transform = Affine2D().scale(1, 1).rotate_deg(45)
helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
ax1 = floating_axes.FloatingSubplot(fig, 331, grid_helper=helper)
ax1.patch.set_facecolor('None')
ax1.patch.set_alpha(0.0)
ax1.set_xticks([], minor=False)
ax1.set_yticks([], minor=False)

plot_extents = 0, 10, 0, 10
transform = Affine2D().scale(1, 1).rotate_deg(90)
helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
ax2 = floating_axes.FloatingSubplot(fig, 338, grid_helper=helper)
ax2.patch.set_facecolor('None')
ax2.patch.set_alpha(0.0)
ax2.set_xticks([], minor=False)
ax2.set_yticks([], minor=False)
ax.plot(range(100))

# --- add floating subplots
fig.add_subplot(ax1)
fig.add_subplot(ax2)


ax.plot(range(100), color='red')
# ax2.plot(range(6)[::-1], color='green')
# ax2.set_xticks([], minor=False)
# ax2.set_yticks([], minor=False)
# ax2.xticks(rotation=30)

plt.show()

# import matplotlib.pyplot as plt
# from matplotlib.transforms import Affine2D
# import mpl_toolkits.axisartist.floating_axes as floating_axes

# fig = plt.figure()

# plot_extents = 0, 10, 0, 10
# transform = Affine2D().rotate_deg(45)
# helper = floating_axes.GridHelperCurveLinear(transform, plot_extents)
# ax = floating_axes.FloatingSubplot(fig, 111, grid_helper=helper)

# fig.add_subplot(ax)

# # Hide the ticks and background
# ax.patch.set(visible=False)
# for axis in ax.axis.values():
#     # If you'd like to hide the borders, use "axis.line.set(visible=False)"
#     axis.major_ticks.set(visible=False)

# plt.show()
