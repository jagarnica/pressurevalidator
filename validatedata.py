import io
import csv
import traceback

def checkFileExists(fn):
    try:
        open(fn, "r")
        return 1
    except IOError:
        print("Error: File does not appear to exist.")
        return 0
# This returns the avg for a total number and the number of items 
def getAvg(numList):
    try: 
        avg = sum(numList)/len(numList)
        return avg
    except:
        traceback.print_exc()
        print('ERROR: There was an issue getting the average')
        return 0
def checkIfInRange(num, expected, tolerance):
    # TODO Add range checking
    # This is the minimum value, for example a tolerance of 0.1 would be expected * 0.9
    minVal = expected * (1-tolerance)
    maxVal = expected * (1+tolerance)
    if num >= minVal and num <=maxVal: 
        print('PUMPS PASSES TOLERANCE TEST')
        return 1 
    print('FAIL: PUMP DOES NOT PASS TOLERANCE TEST')
    return 0 
    
def main():
    print('About to try to read in file...')
    # filename = input('What is the file name?')
    # This is temporary for debugging 
    filename = '12_25_35.TXT'
    # Lets see if the file exists first
    if checkFileExists(filename) != 1:
        return
  
    with open(filename) as csv_file:
        # first lets read in the file 
        # This is used to skip the first line because of the headers. 
        next(csv_file)
        # total of all the pressure in the data. 
        pressureDataList = []
        pressureHeaderName = "Pressure(psig)"
        timeHeaderName = "Time(ms)"
        # Read in the file with the columns and row accessible 
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        line_count = 0
        
        for row in csv_reader:
            if line_count == 1:
                # print(f'Column names are {row}')
                line_count += 1
            else:
                # print(f'\t{row[0]}')
                currentTime = float(row[timeHeaderName])
                if currentTime >= 2000 and currentTime <= 8000:
                    pressureDataList.append(float(row[pressureHeaderName]))
                    # print(f'\t Time: {row["Time(ms)"]} Pressure: {row["Pressure(psig)"]}')
                line_count += 1
        averageCalculated = round(getAvg(pressureDataList),2)
        print(f'\nHere is the average found {round(getAvg(pressureDataList),2)}')
        toleranceValue = 0.05
        expectedValue = 120.0 
        checkIfInRange(averageCalculated, expectedValue, toleranceValue)

main()
