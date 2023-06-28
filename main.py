from data_loader import DataLoaderJSON, DataLoaderH5
from plot_posterior import PlotPosterior

# parameters = ['symmetric_mass_ratio', 'lambda_tilde']
parameters = ['lambda_1', 'lambda_2']

# filename = 'bns_example_result'
# filename = 'bns_fixed_m_example_result'
# data = DataLoaderJSON(filename='data/' + filename + '.json', parameters=parameters)

# filename = 'bns_example_data0_1126259642-413_analysis_H1L1V1_result'
filename = 'bns_zero_spin_example_data0_1126259642-413_analysis_H1L1V1_result'
data = DataLoaderH5(filename='data/' + filename + '.hdf5', parameters=parameters)


plotter = PlotPosterior(data.posteriors_dict[parameters[0]], data.posteriors_dict[parameters[1]], data.injection_dict[parameters[0]], data.injection_dict[parameters[1]])

plotter.plot(save=True, show=False, xlabel=parameters[0], ylabel=parameters[1], title=filename)
