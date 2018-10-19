from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
import os.path
import numpy as np
from array import array


# Calculate total number of events (particles, hits in subdet)

gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gROOT.ForceStyle()

subdet = "DCH"
readout = "positionedHits_"+subdet

Different_wires_hit=[]



filesNum= [a for a in range(0, 101)]
#outDirectory = "trajectory_noCut"
outDirectory = "shielding_noCut" 

for filenb in filesNum:
    # fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/Pairs_EdepCut1keV/incoherent_pairs_"+str(filenb)+".root"
    fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/incoherent_pairs_"+str(filenb)+".root"

    nbHits_per_wire = {}
    time_per_wire = {}
    xpos_per_wire = {}
    ypos_per_wire = {}
    zpos_per_wire = {}

    store = EventStore([fcc_file_name])

    for event in store:
        hits = event.get(readout)
        for i in range (0, hits.size()):
            cellid=hits[i].core().cellId
            time = hits[i].core().time
            xpos=hits[i].position().x
            ypos=hits[i].position().y
            zpos=hits[i].position().z


            if cellid not in nbHits_per_wire:
                nbHits_per_wire[cellid]=0
                time_per_wire[cellid]=[]
                xpos_per_wire[cellid]=[]
                ypos_per_wire[cellid]=[]
                zpos_per_wire[cellid]=[]


            nbHits_per_wire[cellid]+=1
            time_per_wire[cellid].append(time)
            xpos_per_wire[cellid].append(xpos)
            ypos_per_wire[cellid].append(ypos)
            zpos_per_wire[cellid].append(zpos)



    nb =  sorted(nbHits_per_wire.values())
    keysWire=nbHits_per_wire.keys()
    print "wires hit=", len(keysWire)
    Different_wires_hit.append(len(keysWire))
    wire4hits = nbHits_per_wire.keys()[nbHits_per_wire.values().index(4)]
    time_4hits = time_per_wire[wire4hits]
    xpos_4hits = xpos_per_wire[wire4hits]
    ypos_4hits = ypos_per_wire[wire4hits]
    zpos_4hits = zpos_per_wire[wire4hits]
    """
    print "time_4hits: ", time_4hits
    print "xpos_4hits: ", xpos_4hits
    print "ypos_4hits: ", ypos_4hits
    print "zpos_4hits: ", zpos_4hits
    """
    # print wire
    # print time_per_wire[wire]

    
    maxval= 500
    minval = 0
    nbins = maxval - minval
    hist = TH1F("hist", "; Number of hits per wire (for BX0); Entries", nbins, minval, maxval)
    for i in range(0, len(nb)):
        hist.Fill(nb[i])


        
    """canv = TCanvas("canv", "canv")
    hist.SetLineColor(kGreen+2)
    hist.Draw("")
    #gPad.SetLogy()
    gPad.Update()
    gPad.Modified()"""
#    bla=raw_input()
    
    # canv.Print("plots/DCH/nbWires_BX"+str(filenb)+".pdf")

print Different_wires_hit
print "Average : different wires hit: ", np.mean(Different_wires_hit)
print "occupancy: ", np.mean(Different_wires_hit)/56448.*100., " [%]"
canv2 = TCanvas("wires", "wires")
gr = TGraph(len(Different_wires_hit), array('f', range(1, len(Different_wires_hit)+1)), array('f', Different_wires_hit))
gr.SetLineColor(kBlue)
gr.Draw("AL")
gr.GetXaxis().SetTitle("BX")
gr.GetYaxis().SetTitle("Nb. of wires hit")

#canv2.Print("hits_vs_BX.pdf")
gPad.Update()
gPad.Modified()

bla=raw_input()
