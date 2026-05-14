REQUIRES = [ "OutEvents" ]
PROVIDES = []

DEVICE_NAME = "UA-25"

from time import sleep, perf_counter as timestamp
import sys, os, subprocess, signal
import mido

MIDI_OUT = None

def open_matching_midi_out(match):
    """ Find a device, e.g. "UA-25", "Fluid", "Timidity", etc. """
    ports = mido.get_output_names()
    print("All avail. ports:", ports)

    matching = [p for p in ports if match.lower() in p.lower()]
    print("Matching ports:", matching)

    assert len(matching) > 0, f"No port matching {DEVICE_NAME} found."

    return mido.open_output(matching[0])

def _init():
    global MIDI_OUT
    
    MIDI_OUT = open_matching_midi_out(DEVICE_NAME)

def _update(bb):
    """Sendet alle MIDI-Nachrichten, die im Blackboard-Queue stehen."""

    if MIDI_OUT is None:
        return

    event_list = bb.OutEvents.event_list

    for msg in event_list:
        if msg.time < timestamp():
            print("Sending:", msg)
            MIDI_OUT.send(msg)

            if msg.time > 0:
                latency_ms = (timestamp() - msg.time)*1000
                if latency_ms >= 0.5:
                    latency_ms = round(latency_ms, 2)
                    print("WARNING: Sending msg to MIDI_OUT with latency of", latency_ms, "ms")

            event_list.remove(msg)


def _close():
    global MIDI_OUT

    if MIDI_OUT is not None:
        # all notes off
        for ch in range(16):
            for pitch in range(128):
                MIDI_OUT.send(mido.Message('note_off', note=pitch, channel=ch))

        MIDI_OUT.close()
        MIDI_OUT = None
        print("MIDI OUT closed cleanly.")

