from ROOT import gSystem
from EventStore import EventStore
import numpy as np
from array import array


from ROOT import *
import os.path


gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gStyle.SetPadRightMargin(0.17)
gROOT.ForceStyle()

def returnHitsReadout(readout, event):
    hits = event.get(readout)
    return hits.size()



gSystem.Load("libdatamodelDict")



colors = [kBlue, kGreen+2, kRed+2]

readouts = ["positionedHits_barrel", "positionedHits_endcap", "positionedHits_DCH"]
readoutName = ["VXD Barrel", "VXD Endcap", "DCH"]
allHits = []

angles=range(0, 100, 10)




path="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/angleScan/"

angle = 10
filename=path+"theta_"+str(angle)
store = EventStore([filename+".root"])


readout = "positionedHits_endcap"
hist = TH1F(readout, "; Nb. hits in VXD Endcap; Events", 20, 0, 20)

for event in store:
    nb = returnHitsReadout(readout, event)
    hist.Fill(nb)



canv1 = TCanvas("Barrel", "Barrel")
hist.Draw()

bla = raw_input()
