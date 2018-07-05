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

nRings = 8
nSuperLayer = 14


def occupancy_1BX(filename, hist_layer_percentage, hist_SL):
    file = TFile(filename)
    tree=file.Get("analysis")
    n_BX=1

    hist = TH2D("hist", "; #phi [deg]; Layer radius [mm]; Entries", 360, 0, 360, 112, 345, 1689)#112, 0, 112)
    hist_layer = TH1D("layerHist", " ; Layer radius [mm]; # Wires hit", 112, 345, 1689)


    count_occupancy={}
    
    for entry in tree:
        layerid=tree.layerId
        wireid=tree.wireId

        if layerid not in count_occupancy:
            count_occupancy[layerid]=0
    
    
        superLayer = int(layerid/nRings)
        ring = layerid % nRings

        nWires = 192 + superLayer * 48
        delta_phi = 360./nWires 

        phi = delta_phi*wireid


        layer_R = 345+layerid*12
        hist.Fill(phi, layer_R)
        hist_layer.Fill(layer_R)
        hist_SL.Fill(superLayer)

    for superlayer in range(0, nSuperLayer):
        nWires = 192 + superlayer * 48
        wiresSL=0

        for ring in range(0, nRings):
            layerid = superlayer*nRings+ring
            # layerR=hist_layer.GetBinCenter(layerid+1)

            wires = hist_layer.GetBinContent(layerid+1)
            hist_layer_percentage.SetBinContent(layerid+1, wires/float(nWires)*100)
            wiresSL+=wires
        hist_SL.SetBinContent(superlayer+1, wiresSL/float(nWires*nRings)*100)
        # print "superlayer: ", superlayer, ", wires: ", wiresSL/float(nWires*nRings)*100

    
    return hist_layer_percentage, hist_SL


pathFolder = "/eos/user/n/nali/incoherentPairs/"
outDirectory = "Z_2/"
analysisDirectory = "Analysis"
#outDirectory = "out_4_06_2018/"
#analysisDirectory = "Analysis_DCA8mm_E100eV"


# BXNUM = 0
histSum = TH1D("layerHistpercentage", " ; Layer radius [mm]; Wires hit [%]", 112, 345, 1689)
histSumSL = TH1D("layerHistpercentage", " ; Layers; Wires hit [%]", nSuperLayer, 0, nSuperLayer*8)

totBX = 1000
#totBX = 101
countIndex = 0
for BXNUM in range(0, totBX):
    filename = pathFolder+outDirectory+analysisDirectory+"/incoherent_pairs_"+str(BXNUM)+".root"

    if (not os.path.isfile(filename)):
        continue
    hist_layer_percentage = TH1D("layerHistpercentage", " ; Layer radius [mm]; Wires hit [%]", 112, 345, 1689)
    hist_SL = TH1D("SLHist", " ; Layers; # Wires hit", nSuperLayer, 0, nSuperLayer)
    hist_layer_percentage, hist_SL = occupancy_1BX(filename, hist_layer_percentage, hist_SL)
    histSum.Add(hist_layer_percentage)
    histSumSL.Add(hist_SL)
    countIndex+=1


print "countIndex=", countIndex
#print "Nums: ", countIndex*20/400 

#scaleNum=totBX
scaleNum=totBX/4.
print "scaleNum=", scaleNum

canvSum = TCanvas("Sum", "Sum")
histSum.Scale(1/float(scaleNum))
histSum.Draw()
#histSum.GetYaxis().SetRangeUser(0, 2)
gPad.Update()
gPad.Modified()
canvSum.Print("plots/"+analysisDirectory+".pdf")

canvSumSL = TCanvas("SumSL", "SumSL")
histSumSL.Scale(1/float(scaleNum))
histSumSL.Draw()
histSumSL.GetXaxis().SetRangeUser(0, 112)
histSumSL.GetYaxis().SetRangeUser(0, 6)
#histSumSL.GetYaxis().SetRangeUser(0, 2)
gPad.Update()
gPad.Modified()
canvSumSL.Print("plots/"+analysisDirectory+"_SL.pdf")

bla = raw_input()
