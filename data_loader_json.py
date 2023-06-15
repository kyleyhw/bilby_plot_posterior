import json

class DataLoaderJSON:
    def __init__(self, filename, parameters):
        with open(filename) as file:
            data = json.load(file)

        posteriors = data['posterior']['content']
        injection_parameters = data['injection_parameters']

        self.posteriors_dict = {}
        self.injection_dict = {}

        for parameter in parameters:
            self.posteriors_dict[parameter] = posteriors[parameter]
            self.injection_dict[parameter] = injection_parameters[parameter]