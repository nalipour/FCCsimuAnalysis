from ROOT import gSystem
from EventStore import EventStore
import csv
# import DDRec

gSystem.Load("libdatamodelDict")

# filename="angleScan_layer2"
filename = "simu_test"
# filename = "angleScan_layer1_debug"
store = EventStore([filename+".root"])

with open(filename+'.csv', 'w') as csvfile:
    csv_writer=csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(["x", "y" , "z", "cellId", "energy", "time"])
    for event in store:
        hits = event.get("positionedHits_DCH")
        for i in range (0, hits.size()):
            csv_writer.writerow([hits[i].position().x, hits[i].position().y, hits[i].position().z, hits[i].core().cellId, hits[i].core().energy, hits[i].core().time])
        # print >> file, hits[i].position().x,",",hits[i].position().y,",", hits[i].position().z, ",", hits[i].core().cellId, ",", hits[i].core().energy, ",", hits[i].core().time
        



    #evInfo=store.get("evtinfo")
    # print evInfo
    #assert(len(clusters) == 1)
