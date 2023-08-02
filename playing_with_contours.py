import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

np.random.seed(seed=1)
data = np.random.multivariate_normal(mean=(0, 0), cov=np.identity(2), size=1000)
data = data.T
x = data[0]
y = data[1]


def cut_contour_at_axes(path):
    contour_x = path.vertices.T[0]
    contour_y = path.vertices.T[1]

    filter = np.intersect1d(np.where(contour_x > 0), np.where(contour_y > 0))

    print(path.vertices)

    path.vertices = path.vertices[filter]

    contour_x = path.vertices.T[0]
    contour_y = path.vertices.T[1]

    extended_contour_x = np.zeros(shape=(len(contour_x) + 2,))
    extended_contour_y = np.zeros(shape=(len(contour_y) + 2,))

    extended_contour_x[1: -1] = contour_x
    extended_contour_y[1: -1] = contour_y

    return extended_contour_x, extended_contour_y

def cut_contour_at_diagonal(path):
    contour_x = path.vertices.T[0]
    contour_y = path.vertices.T[1]

    filter = np.where(contour_y > contour_x)

    print(path.vertices)

    path.vertices = path.vertices[filter]

    contour_x = path.vertices.T[0]
    contour_y = path.vertices.T[1]

    extended_contour_x = np.zeros(shape=(len(contour_x) + 1,))
    extended_contour_y = np.zeros(shape=(len(contour_y) + 1,))

    extended_contour_x[0: -1] = contour_x
    extended_contour_y[0: -1] = contour_y

    extended_contour_x[-1] = contour_x[0]
    extended_contour_y[-1] = contour_y[0]

    return extended_contour_x, extended_contour_y



ax = sns.kdeplot(x=x, y=y, levels=[0.1, 0.5])
path = ax.collections[-1].get_paths()[0]
# print(path)
contour_x, contour_y = cut_contour_at_diagonal(path)
# path.codes = None

plt.figure()

plt.scatter(x, y, alpha=0.1)
plt.plot(contour_x, contour_y)
# sns.kdeplot(x=x, y=y, levels=[0.1])

plt.savefig('contour_test.png')
# plt.show()