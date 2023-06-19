import numpy as np
from data_loader import DataLoaderJSON
def delta_Lambda_tilde(eta, lambda_1, lambda_2):
    first_term = np.sqrt(1 - 4*eta) * (1 - (13272 / 1319)*eta + (8944/1319)*eta**2)*(lambda_1 + lambda_2)
    second_term = (1 - (15910/1319)*eta + (32850/1319)*eta**2 + (3380/1319)*eta**3)*(lambda_1 - lambda_2)

    return 0.5 * (first_term + second_term)

filename = 'bns_example_result'
# filename = 'bns_fixed_m_example_result'

parameters = ['lambda_1', 'lambda_2', 'symmetric_mass_ratio']

data = DataLoaderJSON(filename=filename + '.json', parameters=parameters)

eta = data.injection_dict['symmetric_mass_ratio']
lambda_1 = data.injection_dict['lambda_1']
lambda_2 = data.injection_dict['lambda_2']

result = delta_Lambda_tilde(eta, lambda_1, lambda_2)

print(result)