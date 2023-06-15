from data_loader_json import DataLoaderJSON
from plot_posterior import PlotPosterior

filename = 'bns_example_result'
# filename = 'bns_fixed_m_example_result'

# parameters = ['symmetric_mass_ratio', 'lambda_tilde']
parameters = ['lambda_1', 'lambda_2']

data = DataLoaderJSON(filename=filename + '.json', parameters=parameters)

plotter = PlotPosterior(data.posteriors_dict[parameters[0]], data.posteriors_dict[parameters[1]], data.injection_dict[parameters[0]], data.injection_dict[parameters[1]])

plotter.plot(save=True, show=False, xlabel=parameters[0], ylabel=parameters[1], title=filename)
