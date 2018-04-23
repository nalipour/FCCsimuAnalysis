from ROOT import gSystem
from ROOT import *
from array import array

import numpy as np

if __name__ == '__main__':

    gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
    CLICdpStyle()
    gStyle.SetOptStat(0)
    gStyle.SetPadRightMargin(0.17)

    file = TFile("tree_pairs.root")
    tree=file.Get("tree")

    hist = TH2F("pairs", "; z [mm]; R [mm];", 2250, 0, 2250, 150, 0, 150)
    tree.Draw("R:Z>>pairs", "", "colz")

    line_VXD_Barrel =TLine(0, 17, 125, 17);
    line_VXD_Barrel.SetLineColor(kViolet)
    line_VXD_Barrel.Draw()

    line_VXD_Barrel_rout =TLine(0, 59, 125, 59);
    line_VXD_Barrel_rout.SetLineColor(kViolet)
    line_VXD_Barrel_rout.Draw()

    line_VXD_endcap_in =TLine(159, 24, 159, 102);
    line_VXD_endcap_in.SetLineColor(kViolet)
    line_VXD_endcap_in.Draw()

    line_VXD_endcap_out =TLine(301, 45, 301, 102);
    line_VXD_endcap_out.SetLineColor(kViolet)
    line_VXD_endcap_out.Draw()


    line_track_Barrel =TLine(0, 127, 2250, 127);
    line_track_Barrel.SetLineColor(kViolet)
    line_track_Barrel.Draw()

    gPad.Update()
    gPad.Modified()

    bla=raw_input()
    
