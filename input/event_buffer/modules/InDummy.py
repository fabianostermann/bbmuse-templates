PROVIDES = [ "MidiInEvents" ]

import time

def _update(bb):
    bb.MidiInEvents.event_list += [ 99 ]
    time.sleep(1.0)
