"""
This script separates FCC vertices in start and end, (and primary and secondary, if information available)
and writes them to separate branches in a new files, creating graphs for the positions.
"""


from EventStore import EventStore
import argparse
import ROOT
from ROOT import fcc, std
from ROOT import *
import numpy as np

gROOT.ProcessLine(".L ~/CLICdpStyle/rootstyle/CLICdpStyle.C")
CLICdpStyle()
gStyle.SetOptStat(0)
gROOT.ForceStyle()
gStyle.SetPadRightMargin(0.17)

# command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("filename", help="edm file to read")
parser.add_argument("--nevents", help="max events to process (takes length of input root file by default)", type=int, default=-1)
parser.add_argument('--output', type=str, help="name of rootfile to write", default="simVertices.root")
args = parser.parse_args()

#args.filename="/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/shielding/incoherent_pairs_0.root"


primaryStartVertexVector = std.vector(fcc.GenVertexData)()
primaryEndVertexVector = std.vector(fcc.GenVertexData)()
secondaryStartVertexVector = std.vector(fcc.GenVertexData)()
secondaryEndVertexVector = std.vector(fcc.GenVertexData)()

print "creating root file and trees ..."

events = EventStore([args.filename])
if args.nevents == -1:
  args.nevents=len(events)
print len(events), " events in rootfile ", args.filename

j = 0
k = 0

hist1_start=ROOT.TH2D("hist", "Primary vertex: start; z [mm]; R [mm]; ", 1700, -8500, 8500, 900, 0, 9000)
hist1_end=ROOT.TH2D("hist", "Primary vertex: end; z [mm]; R [mm]; ", 1700, -8500, 8500, 900, 0, 9000)

hist2_start=ROOT.TH2D("hist", "Secondary vertex: start; z [mm]; R [mm]; ", 1700, -8500, 8500, 900, 0, 9000)
hist2_end=ROOT.TH2D("hist", "Secondary vertex: end; z [mm]; R [mm]; ", 1700, -8500, 8500, 900, 0, 9000)

test_index=0
print ""
for i, store in enumerate(events):
  print ".",
  if i > args.nevents: 
    break
  simparticles = store.get("simParticles")
  for p in simparticles:
    svertex = p.startVertex()
    evertex = p.endVertex()
    StartVertex = fcc.GenVertexData()
    StartVertex.position = svertex.position()
    StartVertex.ctau = svertex.ctau()
    EndVertex = fcc.GenVertexData()
    EndVertex.position = evertex.position()
    EndVertex.ctau = evertex.ctau()

    x_start=StartVertex.position.x
    y_start=StartVertex.position.y
    z_start=StartVertex.position.z
    r_start=np.sqrt(x_start**2+y_start**2)

    x_end=EndVertex.position.x
    y_end=EndVertex.position.y
    z_end=EndVertex.position.z
    r_end=np.sqrt(x_end**2+y_end**2)

    if p.status() == 201: # secondary
      hist2_start.Fill(z_start, r_start)
      hist2_end.Fill(z_end, r_end)

    else: # primary
      hist1_start.Fill(z_start, r_start)
      hist1_end.Fill(z_end, r_end)

    test_index += 1
    """    
    if test_index > 10000:
      break
      """
print "... drawing stuff "
canv1=ROOT.TCanvas("start 1", "start 1")
hist1_start.Draw("colz")

canv1.Print("start1.pdf")

canv2=ROOT.TCanvas("end 1", "end 1")
hist1_end.Draw("colz")
canv2.Print("end1.pdf")

canv3=ROOT.TCanvas("start 2", "start 2")
hist2_start.Draw("colz")
canv3.Print("start2.pdf")

canv4=ROOT.TCanvas("end 2", "end 2")
hist2_end.Draw("colz")
canv4.Print("end2.pdf")

bla=raw_input()
