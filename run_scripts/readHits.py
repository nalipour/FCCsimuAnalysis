from ROOT import gSystem
from EventStore import EventStore
import csv

gSystem.Load("libdatamodelDict")

filename="test"
store = EventStore([filename+".root"])

with open(filename+'.csv', 'w') as csvfile:
    csv_writer=csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(["x", "y" , "z", "cellId", "energy", "time"])
    for event in store:
        hits = event.get("positionedHits")

        print  "====================", hits.size()
        for i in range (0, hits.size()):
            print "x=", hits[i].position().x
            print "y=", hits[i].position().y
            print "z=", hits[i].position().z
            cellid=hits[i].core().cellId
            print "system=", cellid % 16
            #csv_writer.writerow([hits[i].position().x, hits[i].position().y, hits[i].position().z, hits[i].core().cellId, hits[i].core().energy, hits[i].core().time])

        bla = raw_input()
