import PySimpleGUI as sg
import os
import configuration as config 
import validatedata as datalyze
import pathlib
import fastnumbers
import traceback
import configparser
import matplotlib.pyplot as plt
import numpy as np
sg.theme('Default1')  
# These are the constants used for th GUI. 
FILE_PATH_KEY = 'FILE_PATH'
EXPECTED_VAL_KEY = 'EXPECTED_VAL'
OUTPUT_TEXT_KEY = 'OUTPUT_TEXT'
VALIDATE_BUTTON_KEY = 'VALIDATE_BUTTON'
EXIT_BUTTON_KEY = 'Exit'
FOLDER_BROWSE_KEY = 'FOLDER_BROWSE'
MIN_VOL_VALUE_KEY = 'MINIMUM_VOLUME_VALUE'
MAX_VOL_VALUE_KEY = 'MAXIMUM_VOLUME_VALUE'
M_VALUE_KEY = 'M_VALUE'
B_VALUE_KEY = 'B_VALUE'

# Now lets load our configuration file. 
currentConfig = config.loadConfigurationFile()
loadedValues = currentConfig['Default']
default_folder_path = loadedValues.get('test_folder_path',pathlib.Path().absolute())
mLoadedValue = loadedValues.get('m_value','-0.36')
bLoadedValue = loadedValues.get('b_value','300')
minLoadedValue = loadedValues.get('min_volume','300')
maxLoadedValue = loadedValues.get('max_volume','400')

def filterArrayOfValues(values, names):
    """Retuns an array that match the keys from the values list"""
    try:
        filteredArray = []
        for name in names:
            filteredArray.append(values[name])
        return filteredArray
    except:
        traceback.print_exc()
        print('There was an issue getting the values from the GUI.')


def checkIfValuesAreNumbers(values):
    """Checks to see if the numbers are all valid numbers."""
    try:
        for value in values:
            if fastnumbers.isfloat(value)==0:
                return False
        return True
    except:
        traceback.print_exc()
        print('There was an issue checking the inputs.')
        return False


def draw_plot(plotPoints, mValue, bValue, minVolume, maxVolume):
    try:
        plt.clf()
        font = {'weight': 'normal','size': 14}
        plt.title('Volume vs Pressure')
        plt.xlabel('Pressure [psig]',fontdict=font)
        plt.ylabel('Volume [mL]',fontdict=font)
        # Data for plotting
        plt.grid(True)
        t = np.array(plotPoints)
    
        s = bValue + (mValue * t)
        s2 = np.arange(minVolume,maxVolume,0.01)
        xValues = []
        for value in s2:
            xFound = round(((value-bValue)/mValue),4)
            xValues.append(xFound)
        ptsLabel = 'y='+str(mValue)+'x+'+str(bValue)
        plt.plot(xValues, s2, linestyle='solid')
        plt.plot(t,s, 'bs', label=ptsLabel)
        
        plt.legend(loc='upper right')
        plt.show(block=False)
    except:
        traceback.print_exc()
        print('There was an issue plotting the graph for this.')


# Now lets create the layout for the GUI. 
layout = [
    [sg.Text('File'), sg.InputText(default_text=default_folder_path, key=FILE_PATH_KEY), sg.FolderBrowse(key=FOLDER_BROWSE_KEY)
     ],
    [sg.Text('Min Volume (mL)'), sg.InputText(default_text=minLoadedValue,size=(12,48), key=MIN_VOL_VALUE_KEY),sg.Text('Max Volume (mL)'), sg.InputText(default_text=maxLoadedValue, size=(12,48),key=MAX_VOL_VALUE_KEY) ],
    [sg.Text('y ='),sg.InputText(default_text=mLoadedValue, size=(6,48), key=M_VALUE_KEY),sg.Text('x +'),sg.InputText(default_text=bLoadedValue, size=(6,48), key=B_VALUE_KEY)],
    [sg.Output(size=(88, 20), background_color='#000',
               text_color='#ffffff', key=OUTPUT_TEXT_KEY)],
    [sg.Submit(button_text='Validate', key=VALIDATE_BUTTON_KEY),
     sg.Cancel(button_text=EXIT_BUTTON_KEY)]
]

# Create the window that we will show. 
window = sg.Window('Validate Volume', layout)
while True:                             
    # The Event Loop
    event, values = window.read()
    if event in (None, 'Exit', 'Cancel'):
        minimumVolValue = datalyze.convertToNumber(values[MIN_VOL_VALUE_KEY], minLoadedValue)
        maximumVolValue = datalyze.convertToNumber(values[MAX_VOL_VALUE_KEY], maxLoadedValue)
        mValue = datalyze.convertToNumber(values[M_VALUE_KEY], mLoadedValue)
        bValue = datalyze.convertToNumber(values[B_VALUE_KEY], bLoadedValue)
        filePath = values[FILE_PATH_KEY]
        # Lets save our current config before exiting.
        config.saveConfiguationFile(minimumVolValue, maximumVolValue, mValue, bValue,str(filePath))
        break
  
    if event in ('VALIDATE_BUTTON'):

        filePathSelected = values[FOLDER_BROWSE_KEY]
        if filePathSelected == '':
            filePathSelected = str(default_folder_path)
        # Here are the string values that we are going to check 
        listOfValuesToCheck = [MIN_VOL_VALUE_KEY, MAX_VOL_VALUE_KEY, M_VALUE_KEY, B_VALUE_KEY]
        arrayOfInputValues = filterArrayOfValues(values, listOfValuesToCheck)
        if checkIfValuesAreNumbers(arrayOfInputValues)==False:
            print('Error: Please check your input values')
        else:
            minimumVolValue = datalyze.convertToNumber(values[MIN_VOL_VALUE_KEY])
            maximumVolValue = datalyze.convertToNumber(values[MAX_VOL_VALUE_KEY])
            mValue = datalyze.convertToNumber(values[M_VALUE_KEY])
            bValue = datalyze.convertToNumber(values[B_VALUE_KEY])

            
            print('Current Path: '+filePathSelected)
            # Get a list of txt files in the folder selected
            successfulTotal = 0 
            failedTotal = 0 
            # This list will keep track of the file names that failed validation. 
            failedList = []
            window[OUTPUT_TEXT_KEY].Update('')
            arr = [x for x in os.listdir(filePathSelected) if x.endswith(
                ".txt") or x.endswith(".TXT")]
            listOfAveragesFound = []

            # Now validate every file individually.
            for fileName in arr:
                print(f'\nFilename: {fileName}')
                # Create the full file path for the file. 
                filePath = filePathSelected+'/'+fileName
                averageFound = datalyze.getAverageFromFile(filePath)
                listOfAveragesFound.append(averageFound)
                if datalyze.validateFile(filePath, minimumVolValue, maximumVolValue, mValue, bValue) == True: 
                    successfulTotal+= 1
                else:
                    failedTotal+= 1 
                    failedList.append(fileName)
            # Now lets print out the results. 
            print(f'\nTests Succeeded: {successfulTotal}')
            print(f'Tests Failed: {failedTotal}')
            for failedFile in failedList:
                print(f'FAILED: {failedFile}')
            # Draw the plot for the files. 
            draw_plot(listOfAveragesFound, mValue,bValue, minimumVolValue, maximumVolValue)
            window.Refresh()
