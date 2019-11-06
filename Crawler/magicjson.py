import requests
import pandas as pd
from urllib.parse import urljoin
from multiprocessing import Pool

#get all sets in json format
def all_sets(root_path):
    return requests.get(root_path).json()
    

# convert to dict
def convert_dict(set_magic):
    new_format = dict()
    new_format["baseSetSize"] = set_magic["baseSetSize"]
    new_format["baseSetSize"] = set_magic["baseSetSize"]
    new_format["parentCode"] = set_magic["code"]
    new_format["link"] = urljoin("https://www.mtgjson.com/json/", set_magic["code"]) + ".json"
    new_format["totalSetSize"] = set_magic["totalSetSize"]
    new_format["type"] = set_magic["type"]
    new_format["name"] = set_magic["name"]
    return new_format

#make pepileine
def pipeline(root_path):
    sets = all_sets(root_path)
    thread = Pool(3)
    sets_dict = thread.map(convert_dict,sets)
    df = pd.DataFrame(sets_dict)
    df.to_csv("link_sets.csv")
    return df

root_path = "https://mtgjson.com/json/SetList.json"
df = pipeline(root_path)
df.to_csv("all_sets.csv")