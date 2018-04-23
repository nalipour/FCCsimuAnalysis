from ROOT import gSystem
from ROOT import *
import os.path
import numpy as np
from array import array


gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gStyle.SetPadRightMargin(0.17)
gROOT.ForceStyle()

"""
path="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/Pairs_EdepCut1keV/Analysis/"
filename = "allEvents.root"

path = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/out1/Analysis/"
filename = "incoherent_pairs_2.root"
"""
"""
path="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/out1/Analysis/"
filename = "incoherent_pairs_0.root"
"""
#outDirectory = "world"
outDirectory = "shielding"
filenum=[47, 70, 66]
i = 0
filename="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/Analysis/incoherent_pairs_"+str(i)+".root"

file = TFile(filename)
tree=file.Get("analysis")
n_BX=1

nRings = 8
nSuperLayer = 14


hist = TH2D("hist", "; #phi [deg]; Layer radius [mm]; Entries", 360, 0, 360, 112, 345, 1689)#112, 0, 112)
hist_hits = TH2D("hist", "; R [mm]; nb hits", 56, 345, 1689, 180, 0, 360)
hist_layer = TH1D("layerHist", " ; Layer radius [mm]; # Wires hit", 112, 345, 1689)
hist_layer_percentage = TH1D("layerHistpercentage", " ; Layer radius [mm]; Wires hit [%]", 112, 345, 1689)

count_occupancy={}

for entry in tree:
    layerid=tree.layerId
    wireid=tree.wireId
    nbWiresHit=tree.wireXhit

    if layerid not in count_occupancy:
        count_occupancy[layerid]=0
    
    count_occupancy[layerid]+=nbWiresHit

    
    superLayer = int(layerid/nRings)
    ring = layerid % nRings

    nWires = 192 + superLayer * 48
    delta_phi = 360./nWires 

    phi = delta_phi*wireid


    #hist.Fill(phi, layerid)
    #print "layerid=", layerid
    layer_R = 345+layerid*12
    hist.Fill(phi, layer_R)
    hist_layer.Fill(layer_R)
    hist_hits.Fill(layer_R, nbWiresHit)

print count_occupancy


for i in range(0, 112):
    layerR=hist_layer.GetBinCenter(i)
    wires = hist_layer.GetBinContent(i)

    layerid=i
    superLayer = int(layerid/nRings)

    nWires = 192 + superLayer * 48
    hist_layer_percentage    
    print "layerR", layerR, "nWires=", nWires, ", wiresHit=", wires
    hist_layer_percentage.SetBinContent(i, wires/float(nWires)*100)
    

canv1 = TCanvas("canv1", "canv1")
hist.Draw("colz")
canv1.Print("plots/layerR_vs_phi.pdf")

canv2 = TCanvas("canv2", "canv2")
#hist_layer.Scale(1./n_BX)
hist_layer.Draw()
canv2.Print("plots/layerR_vs_wires.pdf")

canv2percent = TCanvas("canv2percent", "canv2percent")
#hist_layer.Scale(1./n_BX)
hist_layer_percentage.Draw()
canv2percent.Print("plots/layerR_vs_wires_percent.pdf")


canv3 = TCanvas("canv3", "canv3")
hist_hits.Draw("colz")

canv4 = TCanvas("canv4", "canv4")
gr=TGraph(len(count_occupancy), array('f', count_occupancy.keys()), array('f', count_occupancy.values()))
gr.Draw("ALP")

bla=raw_input()
