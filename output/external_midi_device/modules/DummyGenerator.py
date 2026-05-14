REQUIRES = []
PROVIDES = [ "OutEvents" ]

import time
import mido

def _update(bb):
    bb.OutEvents.event_list.append(
        mido.Message('note_on', note=60, channel=0)
    )
    time.sleep(0.5)
