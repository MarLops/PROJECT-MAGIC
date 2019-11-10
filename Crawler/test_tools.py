##unitest
import unittest
import tools_get_cards as tcard
import requests


class TestToolsMagic(unittest.TestCase):

    def test_new_format(self):
        cards = requests.get(url="https://www.mtgjson.com/json/P15A.json").json()['cards']
        card = cards[0]
        new_format = tcard.new_format(card)
        self.assertEqual(new_format['artist'],"Dave Dorman")
        self.assertEqual(new_format['colorIdentity'],"R")
        self.assertEqual(new_format['convertedManaCost'],3.0)
        self.assertEqual(new_format['rarity'],"rare")

    def test_arry_format_to_string(self):
        cards = requests.get(url="https://www.mtgjson.com/json/P15A.json").json()['cards']
        card = cards[0]
        new_format =  tcard.new_format(card)
        commander_legalities = new_format["legalities"].split("<legalities>")[1]
        legacy_legalities = new_format['legalities'].split("<legalities>")[5]
        self.assertEqual(commander_legalities,"commander=Legal")
        self.assertEqual(legacy_legalities,"legacy=Legal")


if __name__ == "__main__":
    unittest.main()