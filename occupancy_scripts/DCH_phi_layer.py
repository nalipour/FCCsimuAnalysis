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


def occupancy_1BX(filename, BXNUM, hist_layer_percentage):
    file = TFile(filename)
    tree=file.Get("analysis")
    n_BX=1

    nRings = 8
    nSuperLayer = 14


    hist = TH2D("hist", "; #phi [deg]; Layer radius [mm]; Entries", 360, 0, 360, 112, 345, 1689)#112, 0, 112)
    hist_hits = TH2D("hist", "; R [mm]; nb hits", 56, 345, 1689, 180, 0, 360)
    hist_layer = TH1D("layerHist", " ; Layer radius [mm]; # Wires hit", 112, 345, 1689)
    # hist_layer_percentage = TH1D("layerHistpercentage", " ; Layer radius [mm]; Wires hit [%]", 112, 345, 1689)

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


        layer_R = 345+layerid*12
        hist.Fill(phi, layer_R)
        hist_layer.Fill(layer_R)
        hist_hits.Fill(layer_R, nbWiresHit)

    print count_occupancy


    for i in range(0, nRings*nSuperLayer):
        layerR=hist_layer.GetBinCenter(i)
        wires = hist_layer.GetBinContent(i)

        layerid=i
        superLayer = int(layerid/nRings)
    
        nWires = 192 + superLayer * 48
        hist_layer_percentage    
        print "layerR", layerR, "nWires=", nWires, ", wiresHit=", wires
        hist_layer_percentage.SetBinContent(i, wires/float(nWires)*100)
    

    # canv1 = TCanvas("canv1", "canv1")
    # hist.Draw("colz")
    # canv1.Print("plots/"+outDirectory+"layerR_vs_phi.pdf")

    # canv2 = TCanvas("canv2", "canv2")
    # hist_layer.Scale(1./n_BX)
    # hist_layer.Draw()
    # canv2.Print("layerR_vs_wires.pdf")




    """
    canv3 = TCanvas("canv3", "canv3")
    hist_hits.Draw("colz")
    
    canv4 = TCanvas("canv4", "canv4")
    gr=TGraph(len(count_occupancy), array('f', count_occupancy.keys()), array('f', count_occupancy.values()))
    gr.Draw("ALP")
    """

    return hist_layer_percentage



outDirectory = "shielding_noCut"

# BXNUM = 0
histSum = TH1D("layerHistpercentage", " ; Layer radius [mm]; Wires hit [%]", 112, 345, 1689)
totBX = 101
for BXNUM in range(0, totBX):
    filename = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/Analysis/incoherent_pairs_"+str(BXNUM)+".root"
    hist_layer_percentage = TH1D("layerHistpercentage", " ; Layer radius [mm]; Wires hit [%]", 112, 345, 1689)
    hist_layer_percentage = occupancy_1BX(filename, BXNUM, hist_layer_percentage)
    canv2percent = TCanvas("canv2percent", "canv2percent")
    hist_layer_percentage.Draw()
    canv2percent.Print("plots/"+outDirectory+"_layerR_vs_wires_percent"+str(BXNUM)+".pdf")
    histSum.Add(hist_layer_percentage)

canvSum = TCanvas("Sum", "Sum")
histSum.Scale(1/float(totBX))
histSum.Draw()
canvSum.Print("plots/ocupancy_DCH_percentage.pdf")

bla = raw_input()
