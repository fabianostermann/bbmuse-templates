REQUIRES = []
PROVIDES = [ "MidiOutEvents" ]

from time import sleep, time
import random

import mido

target_time = None

def _update(bb):
    global target_time
    if target_time is None:
        target_time = future()

    if target_time <= time(): 
        event_list = bb.MidiOutEvents.event_list

        # decide channel (all but drum channel)
        chs = list(range(16))
        chs.remove(9) # -> drum event channel
        ch = random.choice(chs)

        # Panning left to right
        pan = random.randint(0,120)
        event_list.append(mido.Message('control_change', control=10, value=pan, channel=ch)) # pan

        # Instrument change
        prog = random.randint(0,10)
        event_list.append(mido.Message('program_change', program=prog, channel=ch))

        new_msg = mido.Message(
            'note_on',
            note=random.randint(0,40),
            velocity=random.randint(10,120),
            channel=ch,
        )
        event_list.append(new_msg)

        target_time = future()

def future():
    return time() + random.uniform(0.05, 3.0)**2
