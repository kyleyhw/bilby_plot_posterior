import numpy as np
from data_loaders import DataLoaderJSON, DataLoaderH5
def delta_Lambda_tilde(eta, lambda_1, lambda_2):
    first_term = np.sqrt(1 - 4*eta) * (1 - (13272 / 1319)*eta + (8944/1319)*eta**2)*(lambda_1 + lambda_2)
    second_term = (1 - (15910/1319)*eta + (32850/1319)*eta**2 + (3380/1319)*eta**3)*(lambda_1 - lambda_2)

    return 0.5 * (first_term + second_term)

def Lambda_tilde(q, lambda_1, lambda_2):
    numerator = 16 * ((12 * q + 1) * lambda_1 + (12 + q) * q**4 * lambda_2)
    denominator = 13 * (1 + q)**5

    return numerator / denominator

parameters = ['lambda_1', 'lambda_2', 'symmetric_mass_ratio', 'mass_ratio']

# filename = 'bns_example_result'
# filename = 'bns_fixed_m_example_result'
# data = DataLoaderJSON(filename=filename + '.json', parameters=parameters)

filename = 'bns_example_data0_1126259642-413_analysis_H1L1V1_result'
data = DataLoaderH5(filename='data/' + filename + '.hdf5', parameters=parameters)

eta = data.injection_dict['symmetric_mass_ratio']
q = data.injection_dict['mass_ratio']
lambda_1 = data.injection_dict['lambda_1']
lambda_2 = data.injection_dict['lambda_2']

dLt = delta_Lambda_tilde(eta, lambda_1, lambda_2)
Lt = Lambda_tilde(q, lambda_1, lambda_2)

print('injected lambda_1', lambda_1)
print('injected lambda_2', lambda_2)

print('delta_Lambda_tilde from injected L1L2 =', dLt)
print('Lambda_tilde from injected L1L2 =', Lt)

print()

estimated_lambda_1 = 600
estimated_lambda_2 = 1250

estimated_dLt = delta_Lambda_tilde(eta, estimated_lambda_1, estimated_lambda_2)
estimated_Lt = Lambda_tilde(q, estimated_lambda_1, estimated_lambda_2)

# print('delta_Lambda_tilde from recovered L1L2 =', estimated_dLt)
# print('Lambda_tilde from recovered L1L2 =', estimated_Lt)