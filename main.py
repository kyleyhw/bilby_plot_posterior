from data_loader_json import DataLoaderJSON
from plot_posterior import PlotPosterior

filename = 'bns_example_result.json'
parameters = ['lambda_1', 'lambda_2']

data = DataLoaderJSON(filename=filename, parameters=parameters)

plotter = PlotPosterior(data.posteriors_dict['lambda_1'], data.posteriors_dict['lambda_2'])

plotter.plot(save=True, show=True, xlabel=r'\lambda_1', ylabel=r'\lambda_2')
