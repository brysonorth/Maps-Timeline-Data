import json
import datetime
import fuelData

year = input('Select a year ')
#year = '2020'
month = input('Select a month ')
#month = 'april'
print('\n')
month = month.upper()
disTotal = 0
durTotal = 0
disBig = 0
durBig = 0
vehTotal = 0
x = 1
planeTotal = 0
activities = {"IN_PASSENGER_VEHICLE":'car',
"WALKING": 'walking',
"CYCLING": 'cycling',
"IN_BUS": 'bus',
"FLYING": 'flying',
"IN_SUBWAY": 'skytrain'}

while True:
    if year == '2018' and month == 'AUGUST':
        print('\n')
        print('Data not available for that month')
        year = input('Select a year ')
        month = input('Select a month ')
        month = month.upper()
        continue
    try:
        #file path specific to my files and Google takeout. Loads into readable json file
        fileName = 'GoogleMaps API/MapsTakeoutNov2020/Takeout/Location History/Semantic Location History/' + year + '/' + year + '_' + month + '.json'
        with open(fileName,'r', encoding='utf8') as file:
            data = file.read()
        obj = json.loads(data)

        #goes through each activity in timeline. either activitySegment or placeVisit
        for items in obj['timelineObjects']:
            #for activity segments finds total distance, total duration, longest distnce, longest duration
            if 'activitySegment'  in items:
                try:
                    distance = items['activitySegment']['distance'] #gives dita
                    disKm = float(distance/1000) #converts metres into kilometres
        
                    startTime = int(items['activitySegment']['duration']['startTimestampMs'])
                    endTime = int(items['activitySegment']['duration']['endTimestampMs'])
                    durMin = float((((endTime - startTime)/1000)/60)) #converts time into minutes

                    #eliminates any non flying activities over 8 hours long because they are probably a glitch
                    if items['activitySegment']['activityType'] != 'FLYING' and durMin > 480:
                        continue
                    
                    #eliminates any walk segments over 1 hour because I was golfing or hiking, not travelling
                    if items['activitySegment']['activityType'] == 'WALKING' and durMin > 60:
                        continue
                    #adds duration and distance to total count
                    durTotal = durTotal + durMin
                    disTotal = disTotal + disKm
                    disTotal = round(disTotal, 1)
                    
                    if durMin > durBig: #finds duration and date of longest trip
                        durBig = durMin
                        startDateDur = datetime.datetime.fromtimestamp(startTime/1000, tz=None)
                        activityTypeDur = items['activitySegment']['activityType']
                    
                    if disKm > disBig: #finds distance and date of furthest trip
                        disBig = disKm
                        startDateDis = datetime.datetime.fromtimestamp(startTime/1000, tz=None)
                        activityTypeDis = items['activitySegment']['activityType']
                    
                    #finds distance driven in passenger vehicles
                    if items['activitySegment']['activityType'] == 'IN_PASSENGER_VEHICLE':
                        vehTotal = vehTotal + disKm
                    
                    #finds total distance travelled by plane
                    if items['activitySegment']['activityType'] == 'FLYING':
                        planeTotal = planeTotal + disKm
                except KeyError:
                    continue
        break
    except:
        print('Month or year unavailable or typed incorrectly')
        print('\n')
        year = input('Select a year ')
        month = input('Select a month ')
        month = month.upper()
        continue
      
durRes = str(datetime.timedelta(minutes=durTotal)) #converts into easily readable datetime string
durBigRes = str(datetime.timedelta(minutes=durBig))
vehLitres = fuelData.fuelUsed(vehTotal)
planeLitres = fuelData.planeFuelUsed(planeTotal)
totalCarb = fuelData.carbonUsed(vehLitres,planeLitres)

#end = datetime.datetime.fromtimestamp(endTime/1000, tz=None) 

print('\033[1m' + month.capitalize() +' ' + year + ' Stats' + '\033[0m')
print('Distance Travelled:', round(disTotal, 1),'km') 
print('Furthest trip:', round(disBig, 1),'km ---> on', startDateDis, 'via', activities[activityTypeDis].lower())
print('\n')
print('Total Time Travelling:',  durRes, 'Hours')
print('Longest Trip:', durBigRes, 'Hours ---> on', startDateDur, 'via', activities[activityTypeDis].lower())
print('\n')
print('Approximate car fuel used:', round(vehLitres,1), 'Litres')
if planeTotal > 0:
    print('Approximate plane fuel used:', round(planeLitres, 1), 'Litres' )
print('Approximate carbon used:', round(totalCarb, 1), 'kg of CO2')

