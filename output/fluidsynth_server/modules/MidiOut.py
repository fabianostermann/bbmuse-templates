REQUIRES = [ "OutEvents" ]
PROVIDES = []

from time import sleep, perf_counter as timestamp
import sys, os, subprocess, signal
import mido

FLUIDSYNTH_PROCESS = None
MIDI_OUT = None

FLUIDSYNTH_CONF = "fluidsynth.conf"

def open_matching_midi_out(match):
    """ Find a device, e.g. "UA-25", "Fluid", "Timidity", etc. """
    ports = mido.get_output_names()
    print("All avail. ports:", ports)

    matching = [p for p in ports if match.lower() in p.lower()]
    print("Matching ports:", matching)

    return mido.open_output(matching[0])

def create_fluidsynth_out(name="default"):
    global FLUIDSYNTH_PROCESS
    name = "bbmuse-"+name
    cmd = [ "fluidsynth",
            "-a", "pulseaudio",
            "-m", "alsa_seq",
            "-o", "midi.portname="+str(name),
        ]
    if os.path.isfile(FLUIDSYNTH_CONF):
        cmd += ["-f", FLUIDSYNTH_CONF]
    else:
        print(f"Fluidsynth config file '{FLUIDSYNTH_CONF}' not found. Falling back to default config (usually ~/.fluidsynth).")
    FLUIDSYNTH_PROCESS = subprocess.Popen(
        cmd,
        start_new_session=True,
        stdin=subprocess.PIPE,
        stdout=sys.stdout,
        stderr=sys.stdout,
    )
    sleep(1)

    return open_matching_midi_out(name)

def _init():
    global MIDI_OUT

    MIDI_OUT = create_fluidsynth_out()

    # load fluidsynth instruments to channels
    for ch, prog in zip(range(16), range(16)):
        MIDI_OUT.send(
            mido.Message('program_change', program=prog, channel=ch)
        )


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

    if FLUIDSYNTH_PROCESS:
        os.killpg(os.getpgid(FLUIDSYNTH_PROCESS.pid), signal.SIGTERM)
        
  
