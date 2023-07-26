import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PlotPosterior:
    def __init__(self, data1, data2, injected_1, injected_2, limit_at_axes=True, limit_at_diagonal=False):
        self.data1 = data1
        self.data2 = data2
        self.injected_1 = injected_1
        self.injected_2 = injected_2

        self.limit_at_axes = limit_at_axes
        self.limit_at_diagonal = limit_at_diagonal

        self.clip = None

        self.bin_width = 200

    def extend_data_for_hard_limit(self, data1, data2, bin_width):
        coords = np.column_stack((data1, data2))

        extend_length = int(np.ceil(bin_width))

        x_sort_indices = np.lexsort((coords[:,1], coords[:,0]))
        y_sort_indices = np.lexsort((coords[:,0], coords[:,1]))

        flip_x_matrix = np.zeros(shape=(2, 2))
        flip_x_matrix[0, 0] = -1
        flip_x_matrix[1, 1] = 1

        flip_y_matrix = np.zeros(shape=(2, 2))
        flip_y_matrix[0, 0] = 1
        flip_y_matrix[1, 1] = -1

        coords_extended = np.zeros(shape=(extend_length + len(coords) + extend_length, 2))
        coords_extended[extend_length:-extend_length] = coords

        for i in range(extend_length):
            coords_extended[i] = coords[x_sort_indices][i] @ flip_x_matrix
            coords_extended[-i] = coords[y_sort_indices][i] @ flip_y_matrix

            coords_extended[2*i] = coords[x_sort_indices][i]
            coords_extended[2*-i] = coords[y_sort_indices][i]

        extended_data1, extended_data2 = zip(*coords_extended)

        return extended_data1, extended_data2

    def scatter_hist(self, x, y, ax, injected_x, injected_y, ax_histx, ax_histy, scatter_color='blue', **kwargs):
        clip = None

        if self.limit_at_axes:
            x_clip = (0, 99999)
            y_clip = (0, 99999)
            clip = (x_clip, y_clip)

            x, y = self.extend_data_for_hard_limit(x, y, bin_width=self.bin_width)

        if self.limit_at_diagonal:
            pass

        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)



        sns.kdeplot(x=x, y=y, ax=ax, levels=[0.1, 0.5], clip=clip, **kwargs)
        ax.scatter(x, y, alpha=0.07, color=scatter_color)

        sns.kdeplot(x=x, ax=ax_histx, **kwargs)
        sns.kdeplot(y=y, ax=ax_histy, **kwargs)

        ax.axvline(injected_x, color='black')
        ax.axhline(injected_y, color='black')
        ax.scatter([injected_x], [injected_y], color='black', marker='o', label='injected value')

    def plot(self, save=False, show=False, xlabel='', ylabel='', title='', **kwargs):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
        ax.set(box_aspect=1)

        ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
        ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)

        self.scatter_hist(x=self.data1, y=self.data2, ax=ax, injected_x=self.injected_1, injected_y=self.injected_2, ax_histx=ax_histx, ax_histy=ax_histy, **kwargs)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        plt.title(title)
        plt.legend()

        if save:
            plt.savefig('plots/' + title + '_plot.png')
        if show:
            plt.show()