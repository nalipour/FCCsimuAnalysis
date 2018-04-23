#!/usr/bin/env python
import sys, imp
import os
from string import *
import commands
from os import listdir
import math

from ROOT import TFile,TH1F,TH2F,TTree
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

   #Radius = 11
   #ZMAX = 47   # for FCC, 2T

   #Radius = 15
   #ZMAX = 85

   Radius = 37
   ZMAX = 125

   #Radius = 16
   #ZMAX = 62.5
   # to see the beam pipe:
   #Radius = 109
   #ZMAX = 1290

   #BField = 3.5
   #BField = 2.0   #  23 Feb 2016

   BField = 2.0 
   
   radius_pos = array( 'f', [ 0.0 ] )
   z_pos = array( 'f', [ 0.0 ] )

   fileTree = TFile( 'tree_pairs.root', 'recreate' )
   treeTree = TTree( 'tree', 'tree with histos' )
   treeTree.Branch( 'R', radius_pos, 'R/F' )
   treeTree.Branch( 'Z', z_pos, 'Z/F' )

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
         
         pt_star = math.sqrt( px*px + py*py )
         theta_star = math.atan2( pt_star, math.fabs(pz)  )

         # Now boost from com frame to lab frame
         ta = math.tan( alpha )
         e_prime = e * math.sqrt( 1 + ta*ta ) + px * ta
         px_prime = px * math.sqrt( 1 + ta*ta ) + e * ta
         py_prime = py
         pz_prime = pz
         
         pt = math.sqrt( px_prime*px_prime + py_prime*py_prime )
         theta = math.atan2( pt, math.fabs( pz_prime) )

         # Does this particle cross the VTX layer ?
         Cross = 0.
         
         tanLambda = pz_prime / pt 
         cos2Lambda = 1./ (1. + tanLambda*tanLambda)
         cosLambda = math.sqrt( cos2Lambda )
         sinLambda = math.sqrt( 1. - cos2Lambda )
         if pz_prime < 0:
            sinLambda = -sinLambda
         rho = pt / (0.3 * BField )    # rho in meters
         rho = rho * 1000.
         Alpha = math.atan2( px_prime, py_prime )
         Phi0 = math.pi - Alpha

         # do the helix :
         nstep = 10000
         delta = 1
         h = charge
         for istep in range(1,nstep):
            s = istep + 0.5
            x = rho * ( math.cos( Phi0 + h * s * cosLambda / rho ) - math.cos( Phi0 ) )
            y = rho * ( math.sin( Phi0 + h * s * cosLambda / rho ) - math.sin( Phi0 ) )
            z = s * sinLambda
            r = math.sqrt(x*x + y*y )


            
            if r > 10 :
               h2d.Fill( math.fabs(z), r )
               z_pos[0] = z
               radius_pos[0] = r
               # print "z_pos=", z_pos, ", radius=", radius_pos
               treeTree.Fill()

      fileTree.Write()
   fileTree.Close()

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

   fhisto = TFile('histos_helix.root', 'recreate' )

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





