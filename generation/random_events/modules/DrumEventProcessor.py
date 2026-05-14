REQUIRES = []
PROVIDES = [ "DrumOutEvents" ]

from time import sleep, time
import random

import mido

target_time = None

def _update(bb):
    global target_time
    if target_time is None:
        target_time = future()
    
    if target_time <= time():
        event_list = bb.DrumOutEvents.event_list

        # decide channel
        ch = 9

        new_msg = mido.Message(
            'note_on',
            note=random.randint(37,48),
            velocity=random.randint(10,40),
            channel=ch,
        )
        event_list.append(new_msg)

        target_time = future()

def future():
    return time() + random.uniform(0.05, 4.0)**2