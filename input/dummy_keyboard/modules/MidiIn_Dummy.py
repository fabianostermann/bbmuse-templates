REQUIRES = []
PROVIDES = ["MidiInEvents"]

import sys
import termios
import tty
import fcntl
import os
import mido
from time import perf_counter as timestamp

DUMMY_NOTE_BASE = 60

# stored original terminal mode
_ORIG_ATTRS = None


def _init():
    global _ORIG_ATTRS

    # store original terminal attributes
    _ORIG_ATTRS = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    # make stdin non-blocking
    flags = fcntl.fcntl(sys.stdin.fileno(), fcntl.F_GETFL)
    fcntl.fcntl(sys.stdin.fileno(), fcntl.F_SETFL, flags | os.O_NONBLOCK)

    print("Keyboard MIDI active (terminal backend). Press digits 0–9.")


def _update(bb):

    try:
        data = sys.stdin.read()
        if data is None:
            data = ""
    except (IOError, OSError, TypeError):
        data = ""

    # If bytes -> decode
    if isinstance(data, bytes):
        try:
            data = data.decode()
        except Exception:
            data = ""
            
    if data is None or data == "":
        return

    print("data:", data)

    # Only keep 0–9
    pressed_now = set(d for d in data if d in "0123456789")
    print("Pressed:", pressed_now)

    for d in pressed_now:
        note = DUMMY_NOTE_BASE + int(d)
        msg = mido.Message("note_on", note=note, velocity=100)
        msg.time = timestamp()
        bb.MidiInEvents.event_list.append(msg)



def _close():
    global _ORIG_ATTRS
    if _ORIG_ATTRS:
        # restore terminal mode
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, _ORIG_ATTRS)
    print("Keyboard MIDI stopped.")

