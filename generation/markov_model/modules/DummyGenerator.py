REQUIRES = []
PROVIDES = [ "MidiInEvents" ]

import time
import random
import mido

def _update(bb):
    pitch = random.choice(list(range(60,72)))
    bb.MidiInEvents.event_list.append(
        mido.Message('note_on', note=pitch, channel=0, time=time.perf_counter())
    )
    time.sleep(0.5)

