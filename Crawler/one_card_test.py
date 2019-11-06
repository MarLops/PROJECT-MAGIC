### test the link of .csv
import requests
import pandas as pd
import json

def cards_of_set(url_set):
    return requests.get(url_set).json()

def save_card_as_json(card):
    file_name = card["name"] + ".json"
    with open (file_name,'w') as f:
        json.dump(card,f)

df = pd.read_csv("link_sets.csv")
set_test = df["link"].iloc[60]
print (f'Make a test with {set_test} set')
cards = cards_of_set(set_test)
one_card = cards['cards'][100]
card_name = one_card['name']
print (f'The {card_name} was return')
save_card_as_json(one_card)

