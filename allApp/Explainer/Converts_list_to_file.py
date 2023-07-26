import json

def Converts_list_to_JSON_file(lst:list):
    """
    Converts a list to the requested file
    """
    jsonString = json.dumps(lst)
    return jsonString

