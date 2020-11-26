import json
import datetime
#import os
#os.chdir('C:\\Users\\fitcr\\MyPythonScripts\\py4e')

#currentYear = datetime.datetime.now().year
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
x = 1

while True:
    try:
#file path specific to my files and Google takeout. Loads into readable json file
        fileName = 'GoogleMaps API/MapsTakeoutNov2020/Takeout/Location History/Semantic Location History/' + year + '/' + year + '_' + month + '.json'
        with open(fileName,'r', encoding='utf8') as file:
            data = file.read()
        obj = json.loads(data)

        #goes throuhg each activity in timeline. either acticitySegment or placeVisit
        for items in obj['timelineObjects']:
            #for activity segments finds total distance, duration, longest distnce, duration
            if 'activitySegment'  in items:
                try:
                    distance = items['activitySegment']['distance']
                    disRes = float(distance/1000)
        
                    startTime = int(items['activitySegment']['duration']['startTimestampMs'])
                    endTime = int(items['activitySegment']['duration']['endTimestampMs'])
                    durMin = float((((endTime - startTime)/1000)/60))

                    #eliminates any non flying activities over 8 hours long because they are probably a glitch
                    if items['activitySegment']['activityType'] != 'FLYING' and durMin > 480:
                        continue
                    
                    #eliminates any walk segments over 1 hour because I was golfing or hiking, not travelling
                    if items['activitySegment']['activityType'] == 'WALKING' and durMin > 60:
                        continue
                    else: #adds duration and distance to total count
                        durTotal = durTotal + durMin
                        disTotal = disTotal + disRes
                        disTotal = round(disTotal, 1)
                    
                    if durMin > durBig: #finds duration and date of longest trip
                        durBig = durMin
                        startDateDur = datetime.datetime.fromtimestamp(startTime/1000, tz=None)
                    
                    if disRes > disBig: #finds distance and date of furthest trip
                        disBig = disRes
                        startDateDis = datetime.datetime.fromtimestamp(startTime/1000, tz=None)
                except KeyError:
                    continue
        break
    except:
        print('Month or year unavailable or typed incorrectly')
        print('\n')
        year = input('Select a year ')
        month = input('Select a year ')
        continue
      
durRes = str(datetime.timedelta(minutes=durTotal))
durBigRes = str(datetime.timedelta(minutes=durBig))

#end = datetime.datetime.fromtimestamp(endTime/1000, tz=None) 

print('\033[1m' + month.capitalize() + year + ' Stats' + '\033[0m')
print('Distance Travelled:', round(disTotal, 1),'km') 
print('Furthest trip:', round(disBig, 1),'km ---> on', startDateDis)
print('\n')
print('Total Time Travelling:',  durRes, 'Hours')
print('Longest Trip: ', durBigRes, 'Hours ---> on', startDateDur)


