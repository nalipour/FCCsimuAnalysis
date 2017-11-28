# Calculate the material in gas
# GasHe_90Isob_10

pressure = 1.0  # *CLHEP::atmosphere
temperature = 293.15  # *CLHEP::kelvin
frHe = 90.0

densityHe = 0.000166  # *CLHEP::g/CLHEP::cm3;
densityIsoB = 0.00249  # *CLHEP::g/CLHEP::cm3;
fractionHe = frHe / 100.  # *CLHEP::perCent;

density = fractionHe * densityHe + (1-fractionHe)*densityIsoB
density *= pressure/(1.0)  # *CLHEP::atmosphere);

atomicWeight_He = 4.002602  # g/mol
atomicWeight_C = 12.0107  # g/mol
atomicWeight_H = 1.00794  # g/mol

pwHe = fractionHe*atomicWeight_He
pwC = (1.0-fractionHe) * 4.0*atomicWeight_C
pwH = (1.0-fractionHe) * 10.0*atomicWeight_H
atomicWeightMix = pwHe + pwC + pwH

pwHe /= atomicWeightMix  # He
pwH /= atomicWeightMix  # H

f_He = pwHe
f_H = pwH
f_C = 1.0 - pwHe - pwH  # C

print('density: ', density)
print('fraction He: ', f_He)
print('fraction H: ', f_H)
print('fraction C: ', f_C)
print('fraction total: ', f_He + f_H + f_C)
