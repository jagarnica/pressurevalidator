import json
import configparser
config = configparser.ConfigParser()
CONFIG_FILE_NAME = 'config.ini'
# These are our default values just in case the file does not exist. 
config['DEFAULT'] = {'Min_Volume': '300','Max_Volume': '400','M_Value': '-0.36','B_Value':'300'}
# this file is in charge of loading the configuration file. 
def checkFileExists(fn):
    try:
        open(fn, "r")
        return 1
    except IOError:
        print("Error: File does not appear to exist.")
        return 0
# This returns the avg for a total number and the number of items
def loadConfigurationFile():
    if checkFileExists(CONFIG_FILE_NAME)==False: 
        with open(CONFIG_FILE_NAME, 'w') as configfile:
            config.write(configfile)

    createdConfig = configparser.ConfigParser()
    createdConfig.read(CONFIG_FILE_NAME)
    return createdConfig 
print(f'Configuration: {loadConfigurationFile()}')