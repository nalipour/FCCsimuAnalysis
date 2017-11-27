import matplotlib.pyplot as plt


def plotHisto(file, var, unit, nbins=100):
    """Takes a file and plots histograms. Saves the plots as .pdf files"""
    f = plt.figure()
    file[var].plot.hist(bins=nbins)
    plt.xlabel(var+' ['+unit+']')
    plt.ylabel('Events')
    plt.show()
    f.savefig('figures/'+var+'.pdf')
