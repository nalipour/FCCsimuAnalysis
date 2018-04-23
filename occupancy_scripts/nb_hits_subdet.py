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
allHits = {r: [] for r in readouts}

angles=range(0, 100, 10)

meanHits_perAngle = {r: [] for r in readouts}


path="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/angleScan/"

for angle in angles:
    filename=path+"theta_"+str(angle)
    store = EventStore([filename+".root"])


    
    for event in store:
        for readout in readouts:
            allHits[readout].append(returnHitsReadout(readout, event))

    for readout in readouts:
        meanHits_perAngle[readout].append(np.median(allHits[readout]))

mg=TMultiGraph("mg", "; #theta [deg]; # layers hit")
leg=TLegend(0.2, 0.6, 0.5, 0.8)
leg.SetFillStyle(0)

##### Draw VXD
for i in range(0, len(readouts)-1):
    readout = readouts[i]
    vals = meanHits_perAngle[readout]
    gr = TGraph(len(angles), array('f', angles), array('f', vals))
    gr.SetLineColor(colors[i])
    gr.SetMarkerColor(colors[i])
    gr.SetMarkerStyle(8)
    mg.Add(gr)
    leg.AddEntry(gr, readoutName[i], 'lp')

canv_VXD = TCanvas("VXD", "VXD")
mg.Draw("ALP")
mg.GetXaxis().SetRangeUser(0, 90)
leg.Draw()

gPad.Update()
gPad.Modified()

canv_CDH = TCanvas("CDH", "CDH")
gr_CDH = TGraph(len(angles), array('f', angles), array('f', meanHits_perAngle[readouts[len(readouts)-1]]))
gr_CDH.SetLineColor(kRed+2)
gr_CDH.SetMarkerColor(kRed+2)
gr_CDH.SetMarkerStyle(8)

gr_CDH.Draw("ALP")
gr_CDH.GetXaxis().SetRangeUser(0, 90)
gr_CDH.GetXaxis().SetTitle("#theta [deg]")
gr_CDH.GetYaxis().SetTitle("# layers hit in DCH")

gPad.Update()
gPad.Modified()

bla = raw_input()
"""
hist_barrel = TH1F("Barrel", "; Nb. hits in VXD Barrel; Events", 20, 0, 20)
hist_endcap = TH1F("Endcap", "; Nb. hits in VXD Endcap; Events", 20, 0, 20)
hist_DCH = TH1F("DCH", "; Nb. hits in DCH; Events", 100, 100, 200)
hist_total = TH1F("Total", "; Total nb. hits; Events", 100, 100, 200)
"""




"""
        hits_barrel = event.get("positionedHits_barrel")
        hits_endcap = event.get("positionedHits_endcap")
        hits_DCH = event.get("positionedHits_DCH")
        
        nb_barrel = hits_barrel.size()
        nb_endcap = hits_endcap.size()
        nb_DCH = hits_DCH.size()
        nb_total = nb_barrel + nb_endcap + nb_DCH        

        hist_barrel.Fill(nb_barrel)
        hist_endcap.Fill(nb_endcap)
        hist_DCH.Fill(nb_DCH)
        hist_total.Fill(nb_total)

canv1 = TCanvas("Barrel", "Barrel")
hist_barrel.Draw()
canv1.Print("plots/Barrel_phiscan.pdf")
canv2 = TCanvas("Endcap", "Endcap")
hist_endcap.Draw()
canv2.Print("plots/Endcap_phiscan.pdf")
canv3 = TCanvas("DCH", "DCH")
hist_DCH.Draw()
canv3.Print("plots/DCH_phiscan.pdf")
canv4 = TCanvas("Total", "Total")
hist_total.Draw()
canv4.Print("plots/Total_phiscan.pdf")
"""

bla=raw_input()


    #evInfo=store.get("evtinfo")
    # print evInfo
    #assert(len(clusters) == 1)
