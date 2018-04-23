#!/usr/bin/env python
import sys, imp
import os
from string import *
import commands
from os import listdir
import math

from ROOT import TFile,TH1F,TH2F,TTree, TCanvas, gPad
from ROOT import gDirectory
from array import array

import numpy as np

   # take the partciles from the pair-prod background
   # propagate the trajectory (helix)
   # show R vs z

        #
        # Note : to be able to run, need to define a CMSSW environment...
        # after having run ilc_env...
        #


from optparse import OptionParser
parser = OptionParser(usage="usage: %prog [options] ")
parser.add_option("--file", dest="file", help="file name of photons.dat", metavar="FILENAME")
parser.add_option("--angle",dest="angle", help="half crossing angle in mrad",metavar="ANGLE")
parser.add_option("--directory",dest="directory",help="path to files eg FCCH",metavar="PATH")
(options, args) = parser.parse_args()


def ReadOneFile(PairsDat, alpha, h2d ) :

   hist_px = TH1F("px", "; p_{x} [MeV]; Entries", 120, -20, 100)
   hist_py=TH1F("py", "; p_{y} [MeV]; Entries", 200, -10, 10)
   hist_pz=TH1F("pz", "; p_{z} [MeV]; Entries", 200, -1000, 1000)

   with open(PairsDat,"r") as fp:  
      lines = fp.readlines()
      for line in lines:
         if len(line.split())<2:
            continue
         pdgCode=float(line.split()[1])
         sign=np.sign(pdgCode)
         e = 1 #float(line.split()[9])
         charge = -sign
         px=float(line.split()[6])*e
         py=float(line.split()[7])*e
         pz=float(line.split()[8])*e
         hist_px.Fill(px*1000)
         hist_py.Fill(py*1000)
         hist_pz.Fill(pz*1000)


   canvx=TCanvas("px", "px")
   hist_px.Draw()
   gPad.SetLogy()
   gPad.Update()
   gPad.Modified()
   
   canvy=TCanvas("py", "py")
   hist_py.Draw()
   gPad.SetLogy()
   gPad.Update()
   gPad.Modified()
   
   canvz=TCanvas("pz", "pz")
   hist_pz.Draw()
   gPad.SetLogy()
   gPad.Update()
   gPad.Modified()

   bla=raw_input()

         

if __name__ == "__main__":

   if options.file is None and options.directory is None:
        print "Error, should specify either --file or --directory"
        sys.exit(1)

   if not options.file is None and not options.directory is None:
        print "Error, shoudl specify either --file or --directory"
        sys.exit(1)


   alpha = 0.
   if not options.angle is None:
        alpha = float(options.angle) / 1000.

   fhisto = TFile('histos_helix_test.root', 'recreate' )

   # the histograms :
   #nbins = 1000
   nbins = 500
   h2 = TH2F("h2d",";z (mm); R (mm); a.u.",nbins,0., 2250, nbins, 0., 2000. )

   if not options.file is None:
        ReadOneFile( options.file, alpha, h2 )

   if not options.directory is None:
	FMAX = 10    # limit to 10 files, as that's quite slow
        thePath = options.directory
        thedirectory = [ d for d in listdir(thePath) ]
    	ifile = 0
        for d in thedirectory:
           theFile=thePath+"/"+d
	   print "... process file : ",theFile
           ReadOneFile( theFile, alpha, h2)
	   ifile = ifile + 1
	   if ifile > FMAX :
		break

   fhisto.Write()
   fhisto.Close()





