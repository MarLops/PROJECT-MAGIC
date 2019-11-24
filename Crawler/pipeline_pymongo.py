'''
Save the cards in mongodb, using threads
'''

import tools_get_cards as tcard
from threading import Event, Thread
from queue import Queue
import pandas as pd
from time import sleep
import pymongo
#create the Event
event = Event()
# create Queue with links
df = pd.read_csv("link_sets.csv")
total_set = len(df)
#Get maxsize to avoid trouble
fila = Queue(maxsize=total_set + 2)
[fila.put(set_cards) for set_cards in list(df["link"])[:20]]
# Put kill to finish the worker
fila.put("Kill")

# Construto Worker, using Thread class
class Worker(Thread):
    def __init__(self, target, queue, *, name='Worker'):
        super().__init__()
        #rewrite target and queue
        self.name = name
        self.queue = queue
        self._target = target
        self._stoped = False
        #print(self.name, 'started')

    def run(self):
        #wait event.set()
        #event.wait()
        while not self.queue.empty():
            set_cards = self.queue.get()
            print(self.name, set_cards)
            #when get Kill from queue
            if set_cards == 'Kill':
                #Put kill again to queue to another worker see it
                self.queue.put(set_cards)
                #Change stoped to True, to go in .join()
                self._stoped = True
                break
            #Do the function in queue
            self._target(set_cards)

    def join(self):
        while not self._stoped:
            sleep(0.1)

def pipeline(set_cards):
    #read dataframe
    name_set =set_cards.split("/")[-1].split(".")[0] + "_set"
    print (f'read the set {name_set}')
    set_json = tcard.read_of_set(set_cards)
    cards = list()
    for card in set_json['cards']:
        cards.append(tcard.new_format(card))
    
    # database
    client = pymongo.MongoClient()
    db = client['test_card']
    collection = db['test_card']
   
    for card in cards:
        try:
           collection.insert_one(card)
        except Exception as e:
            print ("ERRO")
            print (card)
            print (e)
    client.close()
    
def get_pool(n_th: int):
    """Retorna um número n de Threads."""
    return [Worker(target=pipeline, queue=fila, name=f'Worker{n}')
            for n in range(n_th)]



#Start the project
print(fila.queue)
thrs = get_pool(3)
print ('start')
print(thrs[0].queue)
[th.start() for th in thrs]
print ('joins')
[th.join() for th in thrs]
event.set()
