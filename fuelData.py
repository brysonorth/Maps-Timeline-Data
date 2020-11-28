#calculates gas consumption, prices and carbon footprint 

carEff = 9.78 #Kilometres/Litre for a 2011 ford escape 4 cyl, auto 6 speed from fuelexonomy.gov
planeEff = 3.2 #industry average of litres per km per passenger 
vehCarbEff = 2.35 #average kg of carbon dioxide per litre of gas consumed 
planeCarbEff = 3.15 #average kg of CO2 per litre of jet fue consumed

def fuelUsed(disTotal):
    carLitres = disTotal/carEff
    return carLitres

def planeFuelUsed(planeTotal):
    planeLitres = planeEff*planeTotal
    return planeLitres

def carbonUsed(vehLitres, planeLitres):
    vehCarb = vehCarbEff*vehLitres 
    planeCarb = planeCarbEff*planeLitres
    totalCarb = vehCarb + planeCarb
    return totalCarb