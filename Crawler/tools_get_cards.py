#creat tools to get all cards
import requests

def read_of_set(url_set):
    return requests.get(url_set).json()

def new_format(card):
    """
    Return card in new format
    card = dict 
    """
    #12 metadada
    new_format = dict()
    all_metatada_single = ["artist","flavorText","manaCost","name","text","type","convertedManaCost","rarity"]
    all_metadada_array = ["colorIdentity","colors","types"]
    all_metadada_dict = ["legalities"]

    for metadata in all_metatada_single:
        new_format[metadata] = check_exist(card,metadata)

    for metadata in all_metadada_array:
        try:
            if check_exist(card,metadata) == []:
                new_format[metadata] = "Null"
            else:
                new_format[metadata] = "|".join([i for i in check_exist(card,metadata)])
        except:
            new_format[metadata] = "Null"

    for metadata in all_metadada_dict:
        try:
            if check_exist(card,metadata) == "Null":
                new_format[metadata] = "Null"
            else:
                new_format[metadata] = Arry_format_to_string(check_exist(card,metadata),metadata)
        except:
            new_format[metadata] = "Null"
    
    return new_format
  
def Arry_format_to_string(format_array,metadata):
    new_format = ""
    for key in format_array.keys():
        new_format = new_format + f'<{metadata}>' + str(key) + "=" + str(format_array[key]) + f'<{metadata}> '
    return new_format

def check_exist(card,key):
    if key not in card.keys():
        return "Null"
    else:
        if card[key] != None:
            return card[key]
        return "Null"

def cards_of_set(url_set):
    return requests.get(url_set).json()

