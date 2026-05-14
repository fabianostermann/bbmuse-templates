REQUIRES = [ "MidiInEvents" ]
PROVIDES = [ "DelayEvents" ]

import random
import mido

cfg = { "ch": 1, "time": 1.5, "chance": 0.5, "oct": +1 }

def _update(bb):
    in_list = bb.MidiInEvents.event_list
    out_list = bb.DelayEvents.event_list

    for msg in in_list:

        if random.random() < cfg["chance"]:
            delay_msg = msg.copy()

            new_note = delay_msg.note + cfg["oct"]*12
            while new_note < 0:
                new_note += 12
            while new_note >= 128:
                new_note -= 12
            delay_msg.note = new_note

            delay_msg.time += cfg["time"]
            delay_msg.channel = cfg["ch"]
            delay_msg.velocity = delay_msg.velocity #*60 //100 TODO: add velocity factor

            print("Sending:", delay_msg)
            out_list.append(delay_msg)
