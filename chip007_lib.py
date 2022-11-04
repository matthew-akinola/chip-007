import hashlib
import ntpath
import json


def convert_to_dict(value):

    split_list = value.split(';')

    new = [i.strip() for i in split_list]

    js = dict()

    for string in new:

        item = []
        item2 = []

        for i in string:
            if i == ':':
                break
            item.append(i)

        key = ''.join(item)

        for i in reversed(string):
            if i == ':':
                break
            item2.append(i)

        value = ''.join(item2)
        value = value.strip()[::-1]

        if value == 'none':
            value = None

        js[key] = value

    return js


def get_filename(path):

    key, value = ntpath.split(path)  # extract the filename from the path

    # remove the file extension

    if value:
        file_name = value.rsplit('.', 1)[0]

    else:
        file = ntpath.basename(key)
        file_name = file.rsplit('.', 1)[0]

    return file_name



def dict_hash(dictionary):
    # a function that hashes a dictionary
    encoded = json.dumps(dictionary).encode()
    return hashlib.sha256(encoded).hexdigest()