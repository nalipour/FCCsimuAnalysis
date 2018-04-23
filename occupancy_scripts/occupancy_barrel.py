from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
import os.path


gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gROOT.ForceStyle()

def calculateArea(radius, width):
    return  2*TMath.Pi()*radius*width*0.1


subdet = "barrel"
readout = "positionedHits_"+subdet


histFCC_1=TH1F("FCCee_1", "; z [mm]; hits / cm^{2} / BX", 25, -125, 125)
histFCC_2=TH1F("FCCee_2", "; z [mm]; hits / cm^{2} / BX", 25, -125, 125)
histFCC_3=TH1F("FCCee_3", "; z [mm]; hits / cm^{2} / BX", 25, -125, 125)
histFCC_4=TH1F("FCCee_4", "; z [mm]; hits / cm^{2} / BX", 25, -125, 125)
histFCC_5=TH1F("FCCee_5", "; z [mm]; hits / cm^{2} / BX", 25, -125, 125)
histFCC_6=TH1F("FCCee", "; z [mm]; hits / cm^{2} / BX", 25, -125, 125)
histR_2d = TH2F("FCCee", "; z [mm]; Radius [mm]", 25, -125, 125, 6, 0, 60)
histR = TH1F("FCCee", "; Radius [mm]; Occupancy", 6, 0, 60)


index = 22

directory="shielding"
fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+directory+"/allEvents.root"


store = EventStore([fcc_file_name])

radius_1 = 1 # cm
radius_2 = 1 # cm
radius_3 = 1 # cm
radius_4 = 1 # cm
radius_5 = 1 # cm
radius_6 = 1 # cm

for event in store:
    hits = event.get(readout)
    
    for i in range (0, hits.size()):
        energy=hits[i].core().energy*1e6
        cellid=hits[i].core().cellId
        zpos=hits[i].position().z
        xpos=hits[i].position().x
        ypos=hits[i].position().y
        
        radius = TMath.Sqrt(xpos**2+ypos**2)
        
        if radius<19:
            histFCC_1.Fill(zpos)
            radius_1 = 17/10.
        elif radius<30:
            histFCC_2.Fill(zpos)
            radius_2 = 19/10.
        elif radius<39:
            histFCC_3.Fill(zpos)
            radius_3 = 37/10.
        elif radius<50:
            histFCC_4.Fill(zpos)
            radius_4 = 39/10.
        elif radius<59:
            histFCC_5.Fill(zpos)
            radius_5 = 57/10.
        elif radius<70:
            histFCC_6.Fill(zpos)
            radius_6 = 59/10.




area1 = float(index)*calculateArea(radius_1, histFCC_1.GetXaxis().GetBinWidth(1)) # radius in cm, binWidth in mm
area2 = float(index)*calculateArea(radius_2, histFCC_2.GetXaxis().GetBinWidth(1)) # radius in cm, binWidth in mm
area3 = float(index)*calculateArea(radius_3, histFCC_3.GetXaxis().GetBinWidth(1)) # radius in cm, binWidth in mm
area4 = float(index)*calculateArea(radius_4, histFCC_4.GetXaxis().GetBinWidth(1)) # radius in cm, binWidth in mm
area5 = float(index)*calculateArea(radius_5, histFCC_5.GetXaxis().GetBinWidth(1)) # radius in cm, binWidth in mm
area6 = float(index)*calculateArea(radius_6, histFCC_6.GetXaxis().GetBinWidth(1)) # radius in cm, binWidth in mm

histFCC_1.Scale(1/area1)
histFCC_2.Scale(1/area2)
histFCC_3.Scale(1/area3)
histFCC_4.Scale(1/area4)
histFCC_5.Scale(1/area5)
histFCC_6.Scale(1/area6)

histFCC_1.SetLineColor(kRed+2)
histFCC_2.SetLineColor(kGreen+2)
histFCC_3.SetLineColor(kBlue)
histFCC_4.SetLineColor(kYellow)
histFCC_5.SetLineColor(kMagenta)
histFCC_6.SetLineColor(kAzure+10)

leg=TLegend(0.4, 0.6, 0.8, 0.9)
leg.SetFillStyle(0)

leg.AddEntry(histFCC_1, "VXD L1", "lp")
leg.AddEntry(histFCC_2, "VXD L2", "lp")
leg.AddEntry(histFCC_3, "VXD L3", "lp")
leg.AddEntry(histFCC_4, "VXD L4", "lp")
leg.AddEntry(histFCC_5, "VXD L5", "lp")
leg.AddEntry(histFCC_6, "VXD L6", "lp")

st = THStack("barrel", "; z [mm]; hits / cm^{2} / BX")
st.Add(histFCC_1)
st.Add(histFCC_2)
st.Add(histFCC_3)
st.Add(histFCC_4)
st.Add(histFCC_5)
st.Add(histFCC_6)


canv1 = TCanvas("zpos", "zpos")
st.Draw("nostack")
leg.Draw()
#histFCC.Sumw2()
gPad.Update()
gPad.Modified()

bla = raw_input()
