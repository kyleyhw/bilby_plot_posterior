import matplotlib.pyplot as plt
import seaborn as sns

class PlotPosterior:
    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2

    def scatter_hist(self, x, y, ax, ax_histx, ax_histy):
        ax_histx.tick_params(axis="x", labelbottom=False)
        ax_histy.tick_params(axis="y", labelleft=False)

        sns.kdeplot(x=x, y=y, ax=ax)

        sns.kdeplot(x=x, ax=ax_histx)
        sns.kdeplot(y=y, ax=ax_histy)

        # ax_histx.hist(x)
        # ax_histy.hist(y, orientation='horizontal')


    def plot(self, save=False, show=False, xlabel='', ylabel=''):
        fig = plt.figure(figsize=(8, 8))
        ax = fig.add_gridspec(top=0.75, right=0.75).subplots()
        ax.set(box_aspect=1)

        ax_histx = ax.inset_axes([0, 1.05, 1, 0.25], sharex=ax)
        ax_histy = ax.inset_axes([1.05, 0, 0.25, 1], sharey=ax)

        self.scatter_hist(x=self.data1, y=self.data2, ax=ax, ax_histx=ax_histx, ax_histy=ax_histy)

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        if save:
            plt.savefig('plot.png')
        if show:
            plt.show()