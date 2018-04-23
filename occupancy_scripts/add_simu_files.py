from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
from array import array
import os

if __name__ == '__main__':

    gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
    CLICdpStyle()
    gStyle.SetOptStat(0)

    directory = "shielding"
    #path = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/Pairs_EdepCut1keV/Analysis/"
    path = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+directory+"/"
    haddCommand="hadd -f "+path+"allEvents.root "

    index=0


    for i in range(0, 22):
        filename=path+"incoherent_pairs_"+str(i)+".root"
        if os.path.isfile(filename):
            haddCommand+=filename+" "
            index+=1


    print "index=", index
    os.system(haddCommand)
