REQUIRES = [ "MidiInEvents" ]
PROVIDES = [ "NewInEvents" ]

READ_OFFSET = 0

def _update(bb):

    in_list = bb.MidiInEvents.event_list

    bb.NewInEvents.former_note_on_events += bb.NewInEvents.new_note_on_events
    bb.NewInEvents.former_note_on_events = bb.NewInEvents.former_note_on_events[-50:]

    new_events = []

    global READ_OFFSET
    print(READ_OFFSET)
    print(len(in_list))
    while READ_OFFSET < len(in_list):
        msg = in_list[READ_OFFSET]
        READ_OFFSET += 1

        #if <CONDITION>: # <-- optional event filter
        new_events.append(msg)
        
    print("New events:", new_events)

    bb.NewInEvents.new_note_on_events = new_events

