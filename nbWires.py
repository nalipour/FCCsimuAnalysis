def fun(nRing):
    def nbWires(SL):
        sensWires = nRing * (192 + SL * 48)
        fieldWires = 5 * sensWires
        total = sensWires + fieldWires
        return sensWires, fieldWires, total
    return nbWires


wires = list(map(fun(8), range(14)))
nSens = sum([x[0] for x in wires])
nField = sum([x[1] for x in wires])
nTotal = sum([x[2] for x in wires])

nTotal + 384
