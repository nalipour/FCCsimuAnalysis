import os
"""
inputFile = "/afs/cern.ch/user/v/voutsina/public/test.hepevt"
outputFile = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/test.root"
os.system("./run fccrun.py Examples/options/geant_fullsim_fccee_hepevt.py --input="+inputFile+" --outputfile="+outputFile)

bla = raw_input()
"""

#outDirectory = "world"
outDirectory = "shielding"

for i in range(3, 100):

    inputFile = "/afs/cern.ch/user/v/voutsina/public/data_top_hepevet_boosted/pairs_boosted"+str(i)+".hepevt"
    outputFile = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/incoherent_pairs_"+str(i)+".root"
    os.system("./run fccrun.py Examples/options/geant_fullsim_fccee_hepevt.py --input="+inputFile+" --outputfile="+outputFile)

"""
originalFile="Examples/options/geant_fullsim_fccee_hepevt.py"

for i in range(0, 100):
    newFile="Examples/options/simuFiles_FCCee/geant_fullsim_pairs"+str(i)+".py"

    file=open(originalFile, "r")
    file_new=open(newFile, "w")

    stringReplace="str("+str(i)+")"
    for line in file:
        file_new.write(line.replace("FILENUM", stringReplace))

    file.close()
    file_new.close()


    os.system("./run fccrun.py "+newFile)
    print "**********nalipourTest: finished event: ", i
"/afs/cern.ch/user/v/voutsina/public/data_top_hepevet_boosted/pairs_boosted"+FILENUM+".hepevt"

"""
