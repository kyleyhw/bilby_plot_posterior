import json

class DataLoaderJSON:
    def __init__(self, filename, parameters):
        with open(filename) as file:
            data = json.load(file)

        posteriors = data['posterior']['content']

        self.posteriors_dict = {}

        for parameter in parameters:
            self.posteriors_dict[parameter] = posteriors[parameter]