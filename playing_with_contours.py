import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

np.random.seed(seed=1)
data = np.random.multivariate_normal(mean=(0, 0), cov=np.identity(2), size=1000)
data = data.T
x = data[0]
y = data[1]


ax = sns.kdeplot(x=x, y=y, levels=[0.1, 0.5])
print(ax.collections[-1].get_paths())

# for path in ax.collections[-1].get_paths():
#     print(path)

plt.figure()

plt.scatter(x, y, alpha=0.1)
plt.plot()

plt.savefig('contour_test.png')
# plt.show()