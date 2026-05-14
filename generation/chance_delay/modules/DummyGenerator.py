REQUIRES = []
PROVIDES = [ "MidiInEvents" ]

import time
import mido

def _update(bb):
    bb.MidiInEvents.event_list.append(
        mido.Message('note_on', note=60, channel=0, time=time.perf_counter())
    )
    time.sleep(0.5)
