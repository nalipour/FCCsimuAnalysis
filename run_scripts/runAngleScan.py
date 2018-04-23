import os
import numpy as np


for i in range(7, 10):
    theta = i*10
    if theta==0:
        theta+=0.0001
    theta = theta/180.*np.pi

    eta = -np.log(np.tan(theta/2.))
    filename = "theta_"+str(i*10)+".root"
    

    os.system("./run fccrun.py Examples/options/geant_fullsim_fccee_pgun.py --eta="+str(eta)+" --outputfile="+filename+" --nevents=5000")
    print "**********nalipourTest: finished event: ", theta, "***", eta, "*****", filename



#./run fccrun.py Examples/options/geant_fullsim_fccee_pgun.py --eta=1 --outputfile="eta1.root" --nevents=10000
