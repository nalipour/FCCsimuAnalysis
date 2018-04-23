from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
from array import array

import numpy as np

if __name__ == '__main__':

    gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
    CLICdpStyle()
    gStyle.SetOptStat(0)


    hist_px=TH1F("px", "; p_{x} [MeV]; Entries", 200, -20, 100)
    hist_py=TH1F("py", "; p_{y} [MeV]; Entries", 200, -10, 10)
    hist_pz=TH1F("pz", "; p_{z} [MeV]; Entries", 200, -1000, 1000)
    hist_pT=TH1F("pT", "; p_{T} [MeV]; Entries", 200, 0, 200)

    gSystem.Load("libdatamodelDict")
    filename="../SimuOutput/Pairs_EdepCut1keV/incoherent_pairs_0.root"

    store=EventStore([filename])
    for event in store:
        particles = event.get("allGenParticles")

        for i in range (0, particles.size()):
            px=particles[i].core().p4.px*1000
            py=particles[i].core().p4.py*1000
            pz=particles[i].core().p4.pz*1000
            pT=np.sqrt(px**2+py**2) # MeV

            hist_px.Fill(px)
            hist_py.Fill(py)
            hist_pz.Fill(pz)
            hist_pT.Fill(pT)



    canvx=TCanvas("px", "px")
    hist_px.Draw()
    gPad.SetLogy()
    gPad.Update()
    gPad.Modified()
    canvx.Print("plots/incoherentPairs_px.pdf")

    canvy=TCanvas("py", "py")
    hist_py.Draw()
    gPad.SetLogy()
    gPad.Update()
    gPad.Modified()
    canvy.Print("plots/incoherentPairs_py.pdf")

    canvz=TCanvas("pz", "pz")
    hist_pz.Draw()
    gPad.SetLogy()
    gPad.Update()
    gPad.Modified()
    canvz.Print("plots/incoherentPairs_pz.pdf")

    canvT = TCanvas("pT", "pT")
    hist_pT.Draw()
    gPad.SetLogy()
    gPad.Update()
    gPad.Modified()
    canvT.Print("plots/incoherentPairs_pT.pdf")

    bla=raw_input()
