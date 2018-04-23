from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
import os.path

gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gROOT.ForceStyle()

fcc_x=TH1F("fccX", "; x [mm]; Average # of hits/BX", 400, -2000, 2000)
fcc_y=TH1F("fccY", "; y [mm]; Average # of hits/BX", 400, -2000, 2000)
histEnergy=TH1F("Energy", "; E_{dep} [GeV]; Entries", 100, 0, 20)
histTime=TH1F("Time", "; time [ns]; Entries", 200, 0, 20)
histFCC = TH1F()
histR_2d = TH2F()
histR = TH1F()


subdet = "barrel"
#subdet = "endcap"
#subdet = "DCH"
readout = "positionedHits_"+subdet

if subdet == "barrel":
    histFCC=TH1F("FCCee", "; z [mm]; hits / cm^{2} / BX", 25, -125, 125)
    histR_2d = TH2F("FCCee", "; z [mm]; Radius [mm]", 25, -125, 125, 6, 0, 60)
    histR = TH1F("FCCee", "; Radius [mm]; Occupancy", 6, 0, 60)
elif subdet == "endcap":
    histFCC=TH1F("FCCee", "; z [mm]; Average # of hits/BX", 700, -350, 350)
    histR = TH1F("Endcap R", "; Radius [mm]; hits / cm^{2} / BX", 102, 0, 102)
elif subdet == "DCH":
    histFCC=TH1F("FCCee", "; z [mm]; Average # of hits/BX", 450, -2250, 2250)
    histR_2d = TH2F("FCCee", "; z [mm]; Radius [mm]", 450, -2250, 2250, 140, 0, 1400)
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
        print 'radius=', radius
        histR_2d.Fill(zpos, radius)
        histR.Fill(radius)
        
        # if energy>1:
        histFCC.Fill(zpos)
        histEnergy.Fill(energy)
        histTime.Fill(hits[i].core().time)
        # if (zpos<10 and zpos>0):
        fcc_x.Fill(xpos)
        fcc_y.Fill(ypos)

radius = 1
area_z = 2*TMath.Pi()*radius*histFCC.GetXaxis().GetBinWidth(1)*10
histFCC.Scale(1/float(index*area_z))
histEnergy.Scale(1/float(index))
fcc_x.Scale(1/float(index))
fcc_y.Scale(1/float(index))


histFCC.SetLineColor(kGreen+2)
histFCC.SetFillColor(kGreen+2)
histFCC.SetMarkerStyle(8)
histFCC.SetMarkerColor(kGreen+2)
#histFCC.SetLineWidth(6)
#histFCC.SetLineStyle(2)

print "======", histFCC.GetXaxis().GetBinWidth(9)
canv1 = TCanvas("zpos", "zpos")
histFCC.Draw("LP")
#histFCC.Sumw2()
gPad.Update()
gPad.Modified()

canv2 = TCanvas("xpos", "xpos")
fcc_x.Draw("L")

canv3 = TCanvas("ypos", "ypos")
fcc_y.Draw("L")

canv4 = TCanvas("Edep", "Edep")
histEnergy.Draw()
#histEnergy.Draw("lp hist")

canv5 = TCanvas("radius 2D", "radius 2D")
histR_2d.Draw("colz")

canv6 = TCanvas("radius", "radius")
histR.Draw("")
"""
canv1.Print("zpos.pdf")
canv2.Print("xpos.pdf")
canv3.Print("ypos.pdf")
canv4.Print("Edep.pdf")
"""

bla = raw_input()
