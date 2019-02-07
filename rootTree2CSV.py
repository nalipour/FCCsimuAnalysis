from ROOT import gSystem
from ROOT import *
import os.path
import csv


filename = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/mergedHits.root"
filename_csv = "mergedHits.csv"

file = TFile(filename)
tree=file.Get("analysis")

with open(filename_csv, 'w') as csvfile:
    csv_writer=csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(["MCx", "MCy" , "MCz"])

    for entry in tree:
        MCx = tree.MC_x
        MCy = tree.MC_y
        MCz = tree.MC_z

        csv_writer.writerow([MCx, MCy, MCz])


