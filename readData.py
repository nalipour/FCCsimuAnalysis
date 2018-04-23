import pandas as pd
import plot_functions as pf

file = pd.read_csv('data/gaussDigi_test.csv')
pf.plotHisto(file, 'x', 'mm', 100)
pf.plotHisto(file, 'y', 'mm', 100)
pf.plotHisto(file, 'z', 'mm', 100)
pf.plotHisto(file, 'time', 'ns')
