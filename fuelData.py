#calculates gas consumption, prices and carbon footprint 
import pandas as pd
import datetime
import calendar

carEff = 9.78 #Kilometres/Litre for a 2011 ford escape 4 cyl, auto 6 speed from fuelexonomy.gov
planeEff = 3.2 #industry average of litres per km per passenger 
vehCarbEff = 2.35 #average kg of carbon dioxide per litre of gas consumed 
planeCarbEff = 3.15 #average kg of CO2 per litre of jet fuel consumed

def fuelUsed(disTotal): #finds litres of gas used in a car that month
    carLitres = disTotal/carEff
    return carLitres

def planeFuelUsed(planeTotal): #finds litres of gas used in a plane that month
    planeLitres = planeEff*planeTotal
    return planeLitres

def carbonUsed(vehLitres, planeLitres): #finds total carbon output that month
    vehCarb = vehCarbEff*vehLitres 
    planeCarb = planeCarbEff*planeLitres
    totalCarb = vehCarb + planeCarb
    return totalCarb

#returns cost of gas for selected month based on approximate gas used  and average gas price for that month in Vancvouer, BC
def gasPrices(month, year, vehLitres):
    month = month.capitalize()
    month = month[:3] #taking first three chars of the motnh to match the monthDic

    gasPriceDic = dict()
    monthDic = {month: index for index, month in enumerate(calendar.month_abbr) if month} #creats a dictionary with months as keys, numbers as values
    argDateKey = year + '-' + str(monthDic[month]) #key to be used is gasPriceDic. matches dateKey

    #excel sheet import
    data = pd.read_excel(r'C:\Users\fitcr\MyPythonScripts\py4e\GoogleMaps API\gasPricesVan.xlsx')
    df = pd.DataFrame(data, columns=['Month', 'Price']) #create data frame

    #creats a dictionary with year-month as keys and prices as values
    for row in df.itertuples(): #iterates through each row of the dataframe
        exMonth = row.Month
        price = row.Price
        datee = datetime.datetime.strptime(str(exMonth), '%Y-%m-%d %H:%M:%S') #converts to easier to use datetime
        dateKey = str(datee.year) + '-' + str(datee.month) #creates year-month key for dictionary
        gasPriceDic[dateKey] = (price/100) #adds to dic

    gasPrice = gasPriceDic[argDateKey]
    totalCost = gasPrice*vehLitres
    return totalCost



