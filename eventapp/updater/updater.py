from eventapp.models import *
from random import randrange

def create_save():
    SEvent = SaveEvent.objects.all()
    rand_num = randrange(100)

    try:
        SEvent.create(saved = rand_num)
    except:
        print("There was an error!")

