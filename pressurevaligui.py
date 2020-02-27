import PySimpleGUI as sg
import os
import validatedata as datalyze
import pathlib
import fastnumbers
sg.theme('Default1')  
FILE_PATH_KEY = 'FILE_PATH'
EXPECTED_VAL_KEY = 'EXPECTED_VAL'
TOLERANCE_VAL_KEY = 'TOL_VAL'
OUTPUT_TEXT_KEY = 'OUTPUT_TEXT'
VALIDATE_BUTTON_KEY = 'VALIDATE_BUTTON'
EXIT_BUTTON_KEY = 'Exit'
FOLDER_BROWSE_KEY = 'FOLDER_BROWSE'
MIN_VOL_VALUE_KEY = 'MINIMUM_VOLUME_VALUE'
MAX_VOL_VALUE_KEY = 'MAXIMUM_VOLUME_VALUE'
default_folder_path = pathlib.Path().absolute()

layout = [
    [sg.Text('File'), sg.InputText(default_text=default_folder_path, key=FILE_PATH_KEY), sg.FolderBrowse(key=FOLDER_BROWSE_KEY)
     ],
    [sg.Text('Expected Value'), sg.InputText(size=(12, 48),
                                             default_text='120.00', key=EXPECTED_VAL_KEY)],
    [sg.Text('Min Volume (ex: 12.2)'), sg.InputText(size=(12,48), key=MIN_VOL_VALUE_KEY),sg.Text('Max Volume'), sg.InputText(size=(12,48),key=MAX_VOL_VALUE_KEY) ],
    [sg.Text('y ='),sg.InputText(size=(6,48)),sg.Text('x +'),sg.InputText(size=(6,48))],
    [sg.Text('Tolerance (ex: 0.01 for 1%)'), sg.InputText(
        size=(12, 48), default_text='0.1', key=TOLERANCE_VAL_KEY)],
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
        expectedVal = round(float(values[EXPECTED_VAL_KEY]),4)
        toleranceVal = round(float(values[TOLERANCE_VAL_KEY]),4)
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
            if datalyze.validateFile(fileName, expectedVal, toleranceVal) == 1:
                successfulTotal+= 1
            else:
                failedTotal+= 1 
                failedList.append(fileName)
        print(f'\nTests Succeeded: {successfulTotal}')
        print(f'Tests Failed: {failedTotal}')
        for failedFile in failedList:
            print(f'FAILED: {failedFile}')
        window.Refresh()
