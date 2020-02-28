import io
import csv
import traceback
import fastnumbers


def checkFileExists(fn):
    try:
        open(fn, "r")
        return 1
    except IOError:
        print("Error: File does not appear to exist.")
        return 0
# This returns the avg for a total number and the number of items
def handleFailedNumConversion(x):
    print(f'ERROR: Please check your inputs are valid number values: {x}')

def getAvg(numList):
    try:
        avg = sum(numList)/len(numList)
        return avg
    except:
        traceback.print_exc()
        print('ERROR: There was an issue getting the average')
        return 0

def convertToNumber(stringNum):
    """Converts a string to a real number for python. The default value is 0."""
    return fastnumbers.fast_real(stringNum, default=0, coerce=False, on_fail=handleFailedNumConversion)

def checkIfInRange(num, expected, tolerance):
    # This is the minimum value, for example a tolerance of 0.1 would be expected * 0.9
    minVal = expected * (1-tolerance)
    maxVal = expected * (1+tolerance)
    if num >= minVal and num <= maxVal:
        print('SUCCESS: PUMPS PASSES TOLERANCE TEST')
        return 1
    print('FAIL: PUMP DOES NOT PASS TOLERANCE TEST')
    return 0

def checkIfInMinMax(numVal, minVal, maxVal):
    # This is to check if it falls between the min and max. 
    if numVal >= minVal and numVal <= maxVal:
        return 1
    else:
        return 0

def getValueFromFunction(mVal, xVal, bVal):
    try:
        valueCalculated = (mVal * xVal) + bVal
        return valueCalculated
    except:
        print('ERROR: There was an issue calculating the value using the formula. Check values')
        return -1
def validateFile(filename, minValue, maxValue, mValue, bValue):
    """This reads the file from the folder. Checks to see if it is between the min and max value after calculating the average and plugging into the linear function."""
    # filename = input('What is the file name?')
    # This is temporary for debugging
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
        try:
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
            averageCalculated = round(getAvg(pressureDataList), 2)
            calculatedYVal = round(getValueFromFunction(mValue, averageCalculated,bValue),4)
            print(f'Average Value: {round(getAvg(pressureDataList),2)}')
            print(f'Calculated Value: {calculatedYVal}')
            return checkIfInMinMax(calculatedYVal, minValue, maxValue)
        except:
            print(f'There was an error reading this file! {filename}')
            return 0
