#calculates gas consumption, prices and carbon footprint

carEff = 9.78 #Kilometres/Litre for a 2011 ford escape 4 cyl, auto 6 speed from fuelexonomy.gov
planeEff = 3.2 #industry average of litres per km per passenger 

def fuelUsed(disTotal):
    carLitres = disTotal/carEff
    return carLitres

def planeFuelUsed(planeTotal):
    planeLitres = planeEff*planeTotal
    return planeLitres
