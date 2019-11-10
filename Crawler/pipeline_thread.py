### Second model to get all cards os magic - Using worker
import tools_get_cards as tcard
from threading import Event, Thread
from queue import Queue
import pandas as pd
from time import sleep

event = Event()
df = pd.read_csv("link_sets.csv")
total_set = len(df)
fila = Queue(maxsize=total_set + 2)
[fila.put(set_cards) for set_cards in list(df["link"])[:5]]
event.set()
fila.put("Kill")

class Worker(Thread):
    def __init__(self, target, queue, *, name='Worker'):
        super().__init__()
        self.name = name
        self.queue = queue
        self._target = target
        self._stoped = False
        #print(self.name, 'started')

    def run(self):
        event.wait()
        while not self.queue.empty():
            set_cards = self.queue.get()
            print(self.name, set_cards)
            if set_cards == 'Kill':
                self.queue.put(set_cards)
                self._stoped = True
                break
            self._target(set_cards)

    def join(self):
        while not self._stoped:
            sleep(0.1)

def pipeline(set_cards):
    set_json = tcard.read_of_set(set_cards)
    cards = list()
    for card in set_json['cards']:
        #name = card['name'] 
        #print (f'The card is {name}')
        cards.append(tcard.new_format(card))
    df = pd.DataFrame(cards)
    file_name =  set_cards.split("/")[-1].split(".")[0]+ ".csv"
    df.to_csv(file_name)

def get_pool(n_th: int):
    """Retorna um número n de Threads."""
    return [Worker(target=pipeline, queue=fila, name=f'Worker{n}')
            for n in range(n_th)]


print(fila.queue)

thrs = get_pool(2)
print ('start')
print(thrs[0].queue)

[th.start() for th in thrs]
print ('joins')
[th.join() for th in thrs]
