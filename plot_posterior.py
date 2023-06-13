import matplotlib.pyplot as plt
import seaborn as sns

class PlotPosterior:
    def __init__(self, data1, data2):
        self.data1 = data1
        self.data2 = data2

    def plot(self):
        fig, ax = plt.subplots(1, 1)