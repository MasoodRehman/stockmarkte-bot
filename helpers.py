import json

def getCompaniesFromJsonFile(filename):
    """
    JSON file reader
    ==========================================================
    This function will get the data from json file and convert into list.
    """
    fname = 'store/'+filename
    content = []
    with open(fname, 'r') as f:
        for line in f:
            content.append(json.loads(line))
    return content


def dict_factory(cursor, row):
    """
    Dictionary Factory
    ==========================================================
    This function will convert database result into dictionary.
    """
    d = dict()
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
