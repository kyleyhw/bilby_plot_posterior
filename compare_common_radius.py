import matplotlib.pyplot as plt

import common_radius_conversion_functions
from data_loaders import DataLoaderJSON, DataLoaderH5, DataLoaderCommonRadius
from plot_posterior import PlotPosterior

parameters = ['lambda_1', 'lambda_2']

zero_spin_filename = 'bns_zero_spin_L1L2_example_data0_1126259642-413_analysis_H1L1V1_result'
zero_spin_data = DataLoaderH5(filename='data/' + zero_spin_filename + '.hdf5', parameters=parameters)
zero_spin_plotter = PlotPosterior(zero_spin_data.posteriors_dict[parameters[0]], zero_spin_data.posteriors_dict[parameters[1]],
                                  zero_spin_data.injection_dict[parameters[0]], zero_spin_data.injection_dict[parameters[1]],
                                  limit_at_axes=True, limit_at_diagonal=True)


binary_love_filename = 'bns_binary_love_example_data0_1126259642-413_analysis_H1L1V1_result'
binary_love_data = DataLoaderH5(filename='data/' + binary_love_filename + '.hdf5', parameters=parameters)
binary_love_plotter = PlotPosterior(binary_love_data.posteriors_dict[parameters[0]], binary_love_data.posteriors_dict[parameters[1]],
                                  binary_love_data.injection_dict[parameters[0]], binary_love_data.injection_dict[parameters[1]],
                                    limit_at_axes=False, limit_at_diagonal=True)

common_radius_filename = 'bns_common_radius_result'
common_radius_data = DataLoaderCommonRadius(filename='data/' + common_radius_filename + '.json', parameters=['lambda_2', 'mass_ratio'])
common_radius_CR_samples = common_radius_data.posteriors['common_radius_uniform']
common_radius_lambda_1 = common_radius_conversion_functions.common_radius_lambda_2_to_lambda_1_lambda_2_manual_marginalisation(
    common_radius_CR_samples, common_radius_data.posteriors_dict['lambda_2'],
    common_radius_data.posteriors_dict['mass_ratio'])[0]
common_radius_data.posteriors_dict['lambda_1'] = common_radius_lambda_1
common_radius_data.injection_dict['lambda_1'] = 545

# print(common_radius_data.posteriors_dict['lambda_1'], common_radius_data.posteriors_dict['lambda_2'])

common_radius_plotter = PlotPosterior(common_radius_data.posteriors_dict[parameters[0]], common_radius_data.posteriors_dict[parameters[1]],
                                    common_radius_data.injection_dict['lambda_1'], common_radius_data.injection_dict['lambda_2'],
                                    limit_at_axes=False, limit_at_diagonal=False)


fig = plt.figure(figsize=(8, 8))
ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
ax.set(box_aspect=1)

ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)

zero_spin_plotter.scatter_hist(x=zero_spin_plotter.data1, y=zero_spin_plotter.data2, ax=ax,
                               injected_x=zero_spin_plotter.injected_1, injected_y=zero_spin_plotter.injected_2,
                               ax_histx=ax_histx, ax_histy=ax_histy, scatter_color='blue', color='orange', label='w/o binary Love')

binary_love_plotter.scatter_hist(x=binary_love_plotter.data1, y=binary_love_plotter.data2, ax=ax,
                               injected_x=binary_love_plotter.injected_1, injected_y=binary_love_plotter.injected_2,
                               ax_histx=ax_histx, ax_histy=ax_histy, scatter_color='red', color='green', label='with binary Love')

common_radius_plotter.scatter_hist(x=common_radius_plotter.data1, y=common_radius_plotter.data2, ax=ax,
                               injected_x=common_radius_plotter.injected_1, injected_y=common_radius_plotter.injected_2,
                               ax_histx=ax_histx, ax_histy=ax_histy, scatter_color='magenta', color='cyan', label='with common radius')

plt.axis('scaled')
plt.xlabel('$\Lambda_1$')
plt.ylabel('$\Lambda_2$')
plt.savefig('plots/common_radius_comparison_plot.png')
# plt.show()