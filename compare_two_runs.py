import matplotlib.pyplot as plt

from data_loaders import DataLoaderJSON, DataLoaderH5
from plot_posterior import PlotPosterior

parameters = ['lambda_1', 'lambda_2']

zero_spin_filename = 'bns_zero_spin_L1L2_example_data0_1126259642-413_analysis_H1L1V1_result'
zero_spin_data = DataLoaderH5(filename='data/' + zero_spin_filename + '.hdf5', parameters=parameters)
zero_spin_plotter = PlotPosterior(zero_spin_data.posteriors_dict[parameters[0]], zero_spin_data.posteriors_dict[parameters[1]],
                                  zero_spin_data.injection_dict[parameters[0]], zero_spin_data.injection_dict[parameters[1]])


binary_love_filename = 'bns_binary_love_example_data0_1126259642-413_analysis_H1L1V1_result'
binary_love_data = DataLoaderH5(filename='data/' + binary_love_filename + '.hdf5', parameters=parameters)
binary_love_plotter = PlotPosterior(binary_love_data.posteriors_dict[parameters[0]], binary_love_data.posteriors_dict[parameters[1]],
                                  binary_love_data.injection_dict[parameters[0]], binary_love_data.injection_dict[parameters[1]])



fig = plt.figure(figsize=(8, 8))
ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
ax.set(box_aspect=1)

ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)

zero_spin_plotter.scatter_hist(x=zero_spin_plotter.data1, y=zero_spin_plotter.data2, ax=ax,
                               injected_x=zero_spin_plotter.injected_1, injected_y=zero_spin_plotter.injected_2,
                               ax_histx=ax_histx, ax_histy=ax_histy, color='orange', label='w/o binary Love')

binary_love_plotter.scatter_hist(x=binary_love_plotter.data1, y=binary_love_plotter.data2, ax=ax,
                               injected_x=binary_love_plotter.injected_1, injected_y=binary_love_plotter.injected_2,
                               ax_histx=ax_histx, ax_histy=ax_histy, color='green', label='with binary Love')


plt.savefig('plots/binary_love_comparison_plot.png')
# plt.show()