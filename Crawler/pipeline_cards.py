import tools_get_cards as tcard
import pandas as pd

df = pd.read_csv("link_sets.csv")
cards = list()
for set_cards in list(df["link"])[:10]:
    print(f'the set is {set_cards}')
    set_json = tcard.read_of_set(set_cards)
    for card in set_json['cards']:
        name = card['name'] 
        print (f'The card is {name}')
        cards.append(tcard.new_format(card))


df = pd.DataFrame(cards)
df.to_csv("teste.csv")