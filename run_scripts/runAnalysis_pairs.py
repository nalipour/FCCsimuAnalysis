import os

#outDirectory = "world"
outDirectory = "shielding"

filenum =  [a for a in range(0, 100)]
filenum.pop(28)

filenum = [a for a in range(0, 5)]

for i in filenum:


    inputFile = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/incoherent_pairs_"+str(i)+".root"
    outputFile = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/Analysis/incoherent_pairs_"+str(i)+".root"
    os.system("./run fccrun.py Examples/options/mergeHits.py --input="+inputFile+" --outputfile="+outputFile)

