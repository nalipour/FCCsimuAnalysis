import pandas as pd
import plot_functions as pf

file = pd.read_csv('data/bcp_output.csv')
pf.plotHisto(file, 'x', 'mm', 100)
pf.plotHisto(file, 'time', 'ns')
