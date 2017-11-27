import matplotlib.pyplot as plt
import pandas as pd


def plotHisto(file, var, nbins=100):
    plt.figure()
    file[var].plot.hist(bins=nbins)
    plt.show()
    plt.figure()


file = pd.read_csv("data/bcp_output.csv")
plotHisto(file, 'x', 100)
plotHisto(file, 'time')
