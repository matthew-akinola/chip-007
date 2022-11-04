import json
import csv
import os
from chip007_lib import dict_hash, convert_to_dict, get_filename 




def csv_converter():
    filepath = input("Enter the file path of filename(if file is in current dir): ")
    data = []
    try:
        with open(filepath, encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)

            for row in csv_reader:

                # Convert keys to lowercase
                row = {key.lower(): val for key, val in row.items()}
                value = row['filename']+'.json'
                row['hash'] = dict_hash(value)
                row['format'] = "CHIP-0007"
                row['sensitive_content'] = False

                attributes = row['attributes']
                row['attributes'] = convert_to_dict(row['attributes'])

                try:
                    # attempt to cast to int
                    row['series number'] = int(row['series number'])

                except:  
                    continue

                # first create a folder to store the json files
                if not os.path.isdir('jsonfiles'):
                    os.mkdir('jsonfiles')

                # converts each row entry to a json
                with open(os.path.join('jsonfiles', row['filename']+'.json'), 'w', encoding='utf-8') as jsonfile:
                    jsonfile.write(json.dumps(row, indent=4))

                # delete unneeded attributes or data from the loop before appending to the data list.
                row['attributes'] = attributes
                del row['format']
                del row['sensitive_content']

                data.append(row)

        # Get the list of fieldnames/keys/columns
        fields = data[0].keys()
        filename = get_filename(filepath)
        # create an Output folder for the output csv file
        if not os.path.isdir('Output'):
            os.mkdir('Output')
        with open(os.path.join( 'Output', filename +'.output.csv'), 'w', encoding='UTF8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)

    except PermissionError:
        print("\Error: Kindly close the former csv file so the new one can be saved.\n")
        exit()

    except FileNotFoundError:
        print("\nerror: Please confirm that the file path or file name is correct")

        exit()



# kick start the application
csv_converter()