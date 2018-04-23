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
gStyle.SetPadRightMargin(0.17)

subdet = "DCH"
readout = "positionedHits_"+subdet

arr_x=[]
arr_y =[]
arr_z =[]
arr_R=[]

vx = []
vy = []
vz = []
v_R = []

#outDirectory = "world"
outDirectory = "shielding"
filenb = 0

histV=TH2D("hist", "; z [mm]; R [mm]; ", 1400, -7000, 7000, 900, 0, 9000) 

fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/incoherent_pairs_"+str(filenb)+".root"
#fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/allEvents.root"
print fcc_file_name
store = EventStore([fcc_file_name])

for event in store:
    #    hits = event.get(readout)
    vertices = event.get("simVertices")

    
    for v in vertices:
        vxpos = v.position().x
        vypos = v.position().y
        vzpos = v.position().z
        vRpos = TMath.Sqrt(vxpos**2+vypos**2)

        if ((vRpos<=330 and vRpos>=325) or (vRpos>=2000 and vRpos<=2005)):
            print "no"
        else:

            vx.append(vxpos)
            vy.append(vypos)
            vz.append(vzpos)
            v_R.append(vRpos)
            
            histV.Fill(vzpos, vRpos)


histV.Scale(1/histV.Integral())
canvV = TCanvas("vertices", "vertices")
gr = TGraph2D(len(vx), array('f', vx), array('f', vy), array('f', vz))
gr.SetLineColor(kBlue)
gStyle.SetPalette(1);
gr.SetMarkerStyle(20);
gr.Draw("pcol")
gr.GetXaxis().SetTitle("x [mm]")
gr.GetYaxis().SetTitle("y [mm]")
gr.GetZaxis().SetTitle("z [mm]")

canvR = TCanvas("R", "R")
gr = TGraph(len(v_R), array('f', vz), array('f', v_R))
gr.SetLineColor(kBlue)
gStyle.SetPalette(1);
gr.SetMarkerStyle(20);
gr.Draw("AP")
gr.GetXaxis().SetTitle("z [mm]")
gr.GetYaxis().SetTitle("R [mm]")

gPad.Update()
gPad.Modified()



canvHist = TCanvas("canvHist", "canvHist")
histV.Draw("colz")

"""
    for i in range (0, hits.size()):
        cellid=hits[i].core().cellId
        time = hits[i].core().time
        xpos=hits[i].position().x
        ypos=hits[i].position().y
        zpos=hits[i].position().z
        
        arr_x.append(xpos)
        arr_y.append(ypos)
        arr_z.append(zpos)
        arr_R.append(TMath.Sqrt(xpos**2+ypos**2))


canv2 = TCanvas("wires", "wires")
gr = TGraph2D(len(arr_x), array('f', arr_x), array('f', arr_y), array('f', arr_z))
gr.SetLineColor(kBlue)
gStyle.SetPalette(1);
gr.SetMarkerStyle(20);
gr.Draw("pcol")
gr.GetXaxis().SetTitle("x [mm]")
gr.GetYaxis().SetTitle("y [mm]")
gr.GetZaxis().SetTitle("z [mm]")


gPad.Update()
gPad.Modified()

canv2.Print("plots/noDriftChamper.pdf")

canvR = TCanvas("R", "R")
gr = TGraph(len(arr_R), array('f', arr_z), array('f', arr_R))
gr.SetLineColor(kBlue)
gStyle.SetPalette(1);
gr.SetMarkerStyle(20);
gr.Draw("AP")
gr.GetXaxis().SetTitle("z [mm]")
gr.GetYaxis().SetTitle("R [mm]")

gPad.Update()
gPad.Modified()
canvR.Print("plots/noDriftChamper_R.pdf")
"""
bla=raw_input()
