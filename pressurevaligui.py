import PySimpleGUI as sg
import os
import validatedata as datalyze
import pathlib
import fastnumbers
sg.theme('Default1')  
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
default_folder_path = pathlib.Path().absolute()
def checkIfValuesAreNumbers(valuesToCheck):
    for value in valuesToCheck:
        if fastnumbers.isfloat(value)==0:
            return 0
    return 1
layout = [
    [sg.Text('File'), sg.InputText(default_text=default_folder_path, key=FILE_PATH_KEY), sg.FolderBrowse(key=FOLDER_BROWSE_KEY)
     ],
    [sg.Text('Min Volume (ex: 12.2)'), sg.InputText(size=(12,48), key=MIN_VOL_VALUE_KEY),sg.Text('Max Volume'), sg.InputText(size=(12,48),key=MAX_VOL_VALUE_KEY) ],
    [sg.Text('y ='),sg.InputText(size=(6,48), key=M_VALUE_KEY),sg.Text('x +'),sg.InputText(size=(6,48), key=B_VALUE_KEY)],
    [sg.Output(size=(88, 20), background_color='#000',
               text_color='#ffffff', key=OUTPUT_TEXT_KEY)],
    [sg.Submit(button_text='Validate', key=VALIDATE_BUTTON_KEY),
     sg.Cancel(button_text=EXIT_BUTTON_KEY)]
]
window = sg.Window('Validate Pressure', layout)
while True:                             # The Event Loop
    event, values = window.read()
    # print(event, values) #debug
    if event in (None, 'Exit', 'Cancel'):
        break
    if event in ('VALIDATE_BUTTON'):

        filePathSelected = values[FOLDER_BROWSE_KEY]
        if filePathSelected == '':
            filePathSelected = str(default_folder_path)
        
        minimumVolValue = fastnumbers.fast_float(values[MIN_VOL_VALUE_KEY])
        maximumVolValue = fastnumbers.fast_float(values[MAX_VOL_VALUE_KEY])
        mValue = fastnumbers.fast_float(values[M_VALUE_KEY])
        bValue = fastnumbers.fast_float(values[B_VALUE_KEY])
        
        print('Current Path: '+filePathSelected)
        # Get a list of txt files in the folder selected
        successfulTotal = 0 
        failedTotal = 0 
        failedList = []
        window[OUTPUT_TEXT_KEY].Update('')
        arr = [x for x in os.listdir(filePathSelected) if x.endswith(
            ".txt") or x.endswith(".TXT")]
        for fileName in arr:
            print(f'\nFilename: {fileName}')
            if datalyze.validateFile(fileName, minimumVolValue, maximumVolValue, mValue, bValue) == 1:
                successfulTotal+= 1
            else:
                failedTotal+= 1 
                failedList.append(fileName)
        print(f'\nTests Succeeded: {successfulTotal}')
        print(f'Tests Failed: {failedTotal}')
        for failedFile in failedList:
            print(f'FAILED: {failedFile}')
        window.Refresh()
