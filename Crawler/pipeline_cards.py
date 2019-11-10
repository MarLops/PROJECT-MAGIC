## First model to get all cards os magic

import tools_get_cards as tcard
import pandas as pd

df = pd.read_csv("link_sets.csv")
for set_cards,set_name in zip(list(df["link"]),list(df["name"])):
    cards = list()
    print(f'the set is {set_cards}')
    set_json = tcard.read_of_set(set_cards)
    for card in set_json['cards']:
        name = card['name'] 
        print (f'The card is {name}')
        cards.append(tcard.new_format(card))
    df = pd.DataFrame(cards)
    file_name = set_cards.split("/")[-1].split(".")[0] + ".csv"
    df.to_csv(file_name)
    break


