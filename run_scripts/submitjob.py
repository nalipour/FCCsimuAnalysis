import os


queue = "1nd"

for nb in range(5, 100):
    outDirectory="world"
    inputFile = "/afs/cern.ch/user/v/voutsina/public/data_top_hepevet_boosted/pairs_boosted"+str(nb)+".hepevt"
    outputFile = "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/SimuOutput/"+outDirectory+"/incoherent_pairs_"+str(nb)+".root"
    batch_folder= "/afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/"
    batch_script=batch_folder+"batchscripts/script_"+str(nb)+".sh"

    f=open(batch_script, 'w')
    f.write("source /afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW/init.sh \n")
    f.write("cd /afs/cern.ch/work/n/nali/Fellow/SoftwareFCC/FCCSW \n")
    f.write("./run fccrun.py Examples/options/geant_fullsim_fccee_hepevt.py --input="+inputFile+" --outputfile="+outputFile+" \n")

    f.close()
    
    os.system("chmod u+rwx %s"%batch_script)
    os.system("bsub -o %s/STDOUT -q %s %s"%(batch_folder+"batchscripts/log", queue, batch_script))
