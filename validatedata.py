import io
import csv


def checkFileExists(fn):
    try:
        open(fn, "r")
        return 1
    except IOError:
        print("Error: File does not appear to exist.")
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
        # Read in the file with the columns and row accessible 
        csv_reader = csv.DictReader(csv_file, delimiter='\t')
        line_count = 0
        print(csv_reader.fieldnames)
        for row in csv_reader:
            if line_count == 1:
                print(f'Column names are {row}')
                line_count += 1
            else:
                # print(f'\t{row[0]}')
                line_count += 1


main()
