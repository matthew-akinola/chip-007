import json
import hashlib
import csv
import os
import ntpath


def dict_hash(dictionary: dict):
    # a function that hashes a dictionary
    encoded = json.dumps(dictionary).encode()
    return hashlib.sha256(encoded).hexdigest()



def converter():
    try:
        data = []
        filepath = input("Enter the file path of filename(if file is in current dir): ")
        csv_file = open(filepath, encoding='utf-8', mode='r+')
        csv_data = csv.DictReader(csv_file)
        for row in csv_data:   
            row = {key.lower(): val for key, val in row.items()}
            row["hash"] = dict_hash(row['filename']+'.json')
            data.append(row)
            row['format'] = "CHIP-0007"
            row['sensitive_content'] = False
            try:
                row['series number'] = int(row['series number'])

            except:  
                    continue
            # make a jsonfiles directory
            if not os.path.isdir('jsonfiles'):
                    os.mkdir('jsonfiles')

                    # converts each row entry to a json
            with open(os.path.join('jsonfiles', 'nft' +row['filename']+'.json'), 'w', encoding='utf-8') as jsonfile:
                    jsonfile.write(json.dumps(row, indent=4))

            fields = data[0].keys()           
            filename = get_filename(filepath)
            # create an Output folder for the output csv file
            if not os.path.isdir('Output'):
                    os.mkdir('Output')
            with open(os.path.join( 'Output', filename +'.output.csv'), 'w', encoding='UTF8', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fields)
                writer.writeheader()
                 # sends the updated data  into a new csv file
                writer.writerows(data)
    except FileNotFoundError:
        print("\nerror: Invalid file path")
        print("Please confirm that the file path or file name is correct")

        exit()




def get_filename(path):

    head, tail = ntpath.split(path)  # extract the filename from the path

    # remove the file extension

    if tail:
        file_name = tail.rsplit('.', 1)[0]

    else:
        file = ntpath.basename(head)
        file_name = file.rsplit('.', 1)[0]

    return file_name
converter()