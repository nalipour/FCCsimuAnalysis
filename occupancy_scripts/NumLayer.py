# Calculate the number of layers as a function of phi

from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
import os.path
import numpy as np

gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gStyle.SetPadRightMargin(0.17)
gROOT.ForceStyle()


histNbLayers = TH2F("nb. of layers", "; #phi [deg]; Number of wires", 1440, -180, 180, 5, 0, 5)
hist = TH1F("nb. of layers", "; #phi [deg]; Number of wires", 180, -180, 180)

filename = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/angleScan_layer1.root"
store = EventStore([filename])

pos = {}

for event in store:
    hits = event.get("positionedHits")
    
    phi = []
    nb = hits.size()
    #print "hit: ", hits.size()
    for i in range (0, hits.size()):
        xpos=hits[i].position().x
        ypos=hits[i].position().y
        cellID = hits[i].core().cellId
        
        pos[cellId].append((x,y,z))
        angle = TMath.ATan2(ypos, xpos)*180/TMath.Pi()
        phi.append(angle)

    
    histNbLayers.Fill(np.mean(phi), nb)
    hist.Fill(np.mean(phi))

hist.Scale(1/10000.)
canv1=TCanvas("canv1", "canv1")
histNbLayers.Draw("colz")

canv2=TCanvas("canv2", "canv2")
hist.Draw()
bla = raw_input()
    
