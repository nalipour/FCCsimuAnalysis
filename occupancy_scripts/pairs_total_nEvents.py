from ROOT import gSystem
from ROOT import *
from EventStore import EventStore
import os.path
import numpy as np

# Calculate total number of events (particles, hits in subdet)

gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gROOT.ForceStyle()


readouts = ["positionedHits_barrel", "positionedHits_endcap"]
sum_hits = {r:0 for r in readouts}
readout = "positionedHits_barrel"


nb_particles = []
nb_barrel = []
nb_endcap = []
nb_DCH = []


tot_nbFiles = 29
for filenb in range(0, tot_nbFiles):
    fcc_file_name="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/Pairs_EdepCut1keV/incoherent_pairs_"+str(filenb)+".root"

    store = EventStore([fcc_file_name])

    for event in store:

        nb_particles.append(event.get("allGenParticles").size())
        nb_barrel.append(event.get("positionedHits_barrel").size())
        nb_endcap.append(event.get("positionedHits_endcap").size())
        nb_DCH.append(event.get("positionedHits_DCH").size())



print "Nb. of pairs=", np.mean(nb_particles)
print "Nb. hits barrel=", np.mean(nb_barrel)
print "Nb. hits endcap=", np.mean(nb_endcap)
print "Nb. hits DCH=", np.mean(nb_DCH)
bla = raw_input()
    


