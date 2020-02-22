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
    filename = input('What is the file name?')
    # Lets see if the file exists first
    if checkFileExists(filename) != 1:
        return
  
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 1:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                print(
                    f'\t{row[0]}')
                line_count += 1


main()
