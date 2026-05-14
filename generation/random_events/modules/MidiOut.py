GROUP = "output"
REQUIRES = [ "MidiOutEvents", "DrumOutEvents" ]
PROVIDES = []

from time import sleep, perf_counter as timestamp
import sys, os, subprocess, signal
import mido
def _update(bb):
    """Sendet alle MIDI-Nachrichten, die im Blackboard-Queue stehen."""

    for event_list in [
        bb.MidiOutEvents.event_list,
        bb.DrumOutEvents.event_list,
    ]:
        for msg in event_list:
            if msg.time < timestamp():
                print("Sending:", msg)
                #MIDI_OUT.send(msg)

                if msg.time > 0:
                    latency_ms = (timestamp() - msg.time)*1000
                    if latency_ms >= 0.5:
                        latency_ms = round(latency_ms, 2)
                        print("WARNING: Sending msg to MIDI_OUT with latency of", latency_ms, "ms")

                event_list.remove(msg)

