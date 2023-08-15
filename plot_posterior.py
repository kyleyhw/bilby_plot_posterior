import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class PlotPosterior:
    def __init__(self, data1, data2, injected_1, injected_2, limit_at_axes=False, limit_at_diagonal=False):
        self.data1 = data1
        self.data2 = data2
        self.injected_1 = injected_1
        self.injected_2 = injected_2

        self.limit_at_axes = limit_at_axes
        self.limit_at_diagonal = limit_at_diagonal

        self.clip = None

        self.bin_widths = self.hist_bin_sizes()

    def scotts_rule(self, n, d):
        result = n ** (-1. / (d + 4))
        return result

    def hist_bin_sizes(self):
        x_bin_size = (np.max(self.data1) - np.min(self.data1)) / np.sqrt(len(self.data1))
        y_bin_size = (np.max(self.data2) - np.min(self.data2)) / np.sqrt(len(self.data2))

        return x_bin_size, y_bin_size

    def extend_data_for_axis_limit(self, data1, data2, bin_widths):
        coords = np.column_stack((data1, data2))
        x_bin_width, y_bin_width = bin_widths

        first_quadrant_filter = np.intersect1d(np.where(coords[:, 0] > 0)[0], np.where(coords[:, 1] > 0)[0])
        coords = coords[first_quadrant_filter]

        x_extend_filter = np.where(coords[:, 0] < x_bin_width)[0]
        y_extend_filter = np.where(coords[:, 1] < y_bin_width)[0]

        x_extend_length = len(x_extend_filter)
        y_extend_length = len(y_extend_filter)

        extend_length = x_extend_length + y_extend_length # if zero, then cannot broadcast coords into coords_extended[x_extend_length:-y_extend_length]

        flip_x_matrix = np.zeros(shape=(2, 2))
        flip_x_matrix[0, 0] = -1
        flip_x_matrix[1, 1] = 1

        flip_y_matrix = np.zeros(shape=(2, 2))
        flip_y_matrix[0, 0] = 1
        flip_y_matrix[1, 1] = -1

        coords_extended = np.zeros(shape=(x_extend_length + len(coords) + y_extend_length, 2))
        if extend_length != 0:
            coords_extended[x_extend_length:-y_extend_length] = coords
            for i in range(x_extend_length):
                coords_extended[i] = coords[x_extend_filter][i] @ flip_x_matrix
            for i in range(y_extend_length):
                coords_extended[-i - 1] = coords[y_extend_filter][i] @ flip_y_matrix
        else:
            coords_extended = coords

        extended_data1, extended_data2 = zip(*coords_extended)

        return extended_data1, extended_data2

    def rotate_data(self, data1, data2, angle): # angle in degrees
        angle = angle * np.pi / 180

        coords = np.column_stack((data1, data2))

        rotation_matrix = np.zeros(shape=(2, 2))
        rotation_matrix[0, 0] = np.cos(angle)
        rotation_matrix[0, 1] = -np.sin(angle)
        rotation_matrix[1, 0] = np.sin(angle)
        rotation_matrix[1, 1] = np.cos(angle)

        rotated_coords = np.zeros_like(coords)
        for i, coord in enumerate(coords):
            rotated_coords[i] = coord @ rotation_matrix

        rotated_data1, rotated_data2 = zip(*rotated_coords)

        return rotated_data1, rotated_data2

    def get_xy_from_contour(self, contour):
        path = contour.collections[-1].get_paths()[0]

        contour_x = path.vertices.T[0]
        contour_y = path.vertices.T[1]

        return contour_x, contour_y

    def cut_contour_at_axes(self, contour):
        path = contour.collections[-1].get_paths()[0]

        contour_x = path.vertices.T[0]
        contour_y = path.vertices.T[1]

        filter = np.intersect1d(np.where(contour_x > 0), np.where(contour_y > 0))

        path.vertices = path.vertices[filter]

        contour_x = path.vertices.T[0]
        contour_y = path.vertices.T[1]

        extended_contour_x = np.zeros(shape=(len(contour_x) + 2,))
        extended_contour_y = np.zeros(shape=(len(contour_y) + 2,))

        extended_contour_x[1: -1] = contour_x
        extended_contour_y[1: -1] = contour_y

        return extended_contour_x, extended_contour_y


    def cut_contour_at_diagonal(self, contour):
        path = contour.collections[-1].get_paths()[0]

        contour_x = path.vertices.T[0]
        contour_y = path.vertices.T[1]

        filter = np.where(contour_y > contour_x)

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


    def scatter_hist(self, x, y, ax, injected_x, injected_y, ax_histx, ax_histy, scatter_color='blue', **kwargs):
        clip = None

        kde_x = x.copy()
        kde_y = y.copy()

        if self.limit_at_axes:
            kde_x, kde_y = self.extend_data_for_axis_limit(x, y, bin_widths=self.bin_widths)

            x_clip = (0, 99999)
            y_clip = (0, 99999)
            clip = (x_clip, y_clip)

        if self.limit_at_diagonal:
            kde_x, kde_y = self.rotate_data(kde_x, kde_y, 45) # rotating clockwise, why is it 45 and not -45?
            kde_x, kde_y = self.extend_data_for_axis_limit(kde_x, kde_y, bin_widths=self.bin_widths)
            kde_x, kde_y = self.rotate_data(kde_x, kde_y, -45)

        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        main_ninety_contour = sns.kdeplot(x=kde_x, y=kde_y, levels=[0.1], clip=clip, **kwargs)
        main_fifty_contour = sns.kdeplot(x=kde_x, y=kde_y, levels=[0.5], clip=clip, **kwargs)

        main_ninety_x, main_ninety_y = self.get_xy_from_contour(main_ninety_contour)
        main_fifty_x, main_fifty_y = self.get_xy_from_contour(main_fifty_contour)

        if self.limit_at_axes:
            main_ninety_x, main_ninety_y = self.cut_contour_at_axes(main_ninety_contour)
            main_fifty_x, main_fifty_y = self.cut_contour_at_axes(main_fifty_contour)
        if self.limit_at_diagonal:
            main_ninety_x, main_ninety_y = self.cut_contour_at_diagonal(main_ninety_contour)
            main_fifty_x, main_fifty_y = self.cut_contour_at_diagonal(main_fifty_contour)

        ax.scatter(x, y, alpha=0.07, color=scatter_color)
        ax.plot(main_ninety_x, main_ninety_y, **kwargs)
        ax.plot(main_fifty_x, main_fifty_y, **kwargs)

        sns.kdeplot(x=kde_x, ax=ax_histx, **kwargs)
        sns.kdeplot(y=kde_y, ax=ax_histy, **kwargs)

        ax.axvline(injected_x, color='black')
        ax.axhline(injected_y, color='black')
        ax.scatter([injected_x], [injected_y], color='black', marker='o', label='injected value')

        # ax.axvline(0, color='red')
        # ax.axhline(0, color='red')

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