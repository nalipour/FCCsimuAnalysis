from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
import os.path

gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gROOT.ForceStyle()


subdet = "DCH"
readout = "positionedHits_"+subdet


histR = TH1F("FCCee", "; Radius [mm]; Occupancy", 140, 0, 1400)


index = 30

fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/Pairs_EdepCut1keV/allEvents.root"

store = EventStore([fcc_file_name])


for event in store:
    hits = event.get(readout)
    
    for i in range (0, hits.size()):
        energy=hits[i].core().energy*1e6
        cellid=hits[i].core().cellId
        zpos=hits[i].position().z
        xpos=hits[i].position().x
        ypos=hits[i].position().y
        
        radius = TMath.Sqrt(xpos**2+ypos**2)
        histR.Fill(radius)
        

histR.Scale(1/float(index))

canv1 = TCanvas("R", "R")
histR.Draw()

gPad.Update()
gPad.Modified()


bla = raw_input()
