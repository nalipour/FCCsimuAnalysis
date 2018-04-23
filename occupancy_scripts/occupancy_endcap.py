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

def normaliseToArea(hist):
    for i in range(1, hist.GetNbinsX()+1):
        radius = hist.GetBinCenter(i)*0.1 # cm
        binWidth = hist.GetXaxis().GetBinWidth(1) # mm
        hits = hist.GetBinContent(i)
        area = calculateArea(radius, binWidth)*float(index)
        hist.SetBinContent(i, hits/area)


subdet = "endcap"
readout = "positionedHits_"+subdet


histFCC_1=TH1F("FCCee_1", "; R [mm]; hits / cm^{2} / BX", 51, 0, 102)
histFCC_2=TH1F("FCCee_2", "; R [mm]; hits / cm^{2} / BX", 51, 0, 102)
histFCC_3=TH1F("FCCee_3", "; R [mm]; hits / cm^{2} / BX", 51, 0, 102)
histFCC_4=TH1F("FCCee_4", "; R [mm]; hits / cm^{2} / BX", 51, 0, 102)
histFCC_5=TH1F("FCCee_5", "; R [mm]; hits / cm^{2} / BX", 51, 0, 102)
histFCC_6=TH1F("FCCee_6", "; R [mm]; hits / cm^{2} / BX", 51, 0, 102)


index = 99

#fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/Pairs_EdepCut1keV/allEvents.root"
fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/world/allEvents.root"
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

        if TMath.Abs(zpos)<161:
            histFCC_1.Fill(radius)
        elif TMath.Abs(zpos)<170:
            histFCC_2.Fill(radius)
        elif TMath.Abs(zpos)<231:
            histFCC_3.Fill(radius)
        elif TMath.Abs(zpos)<250:
            histFCC_4.Fill(radius)
        elif TMath.Abs(zpos)<301:
            histFCC_5.Fill(radius)
        elif TMath.Abs(zpos)<320:
            histFCC_6.Fill(radius)


"""
for i in range(1, histFCC_1.GetNbinsX()+1):
    radius = histFCC_1.GetBinCenter(i)*0.1 # cm
    binWidth = histFCC_1.GetXaxis().GetBinWidth(1) # mm
    hits = histFCC_1.GetBinContent(i)
    area = calculateArea(radius, binWidth)*float(index)
    histFCC_1.SetBinContent(i, hits/area)

    print "bin: ", i, ", center: ", hits
"""

normaliseToArea(histFCC_1)
normaliseToArea(histFCC_2)
normaliseToArea(histFCC_3)
normaliseToArea(histFCC_4)
normaliseToArea(histFCC_5)
normaliseToArea(histFCC_6)


histFCC_1.SetLineColor(kRed+2)
histFCC_2.SetLineColor(kGreen+2)
histFCC_3.SetLineColor(kBlue)
histFCC_4.SetLineColor(kYellow)
histFCC_5.SetLineColor(kMagenta)
histFCC_6.SetLineColor(kAzure+10)

leg=TLegend(0.6, 0.6, 0.8, 0.9)
leg.SetFillStyle(0)

leg.AddEntry(histFCC_1, "VXD D1", "lp")
leg.AddEntry(histFCC_2, "VXD D2", "lp")
leg.AddEntry(histFCC_3, "VXD D3", "lp")
leg.AddEntry(histFCC_4, "VXD D4", "lp")
leg.AddEntry(histFCC_5, "VXD D5", "lp")
leg.AddEntry(histFCC_6, "VXD D6", "lp")

st = THStack("barrel", "; R [mm]; hits / cm^{2} / BX")
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
canv1.Print("plots/occupancy_VXD_endcap.pdf")
bla = raw_input()
