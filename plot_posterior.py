import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class PlotPosterior:
    def __init__(self, data1, data2, injected_1, injected_2, limit_at_axes=False, limit_at_diagonal=False):
        self.data1 = data1
        self.data2 = data2
        self.injected_1 = injected_1
        self.injected_2 = injected_2

        self.data1_reflected = np.flip(self.data1)
        self.data2_reflected = np.flip(self.data2)

        if limit_at_axes:


    def scatter_hist(self, x, y, ax, injected_x, injected_y, ax_histx, ax_histy, **kwargs):
        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        sns.kdeplot(x=x, y=y, ax=ax, levels=[0.1, 0.5], clip=(0, 3000), **kwargs)
        plt.scatter(x, y, alpha=0.1, color='blue')

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