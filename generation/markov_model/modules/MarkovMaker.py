REQUIRES = [ "MidiInEvents" ]
PROVIDES = [ "MarkovModel" ]

from collections import defaultdict

def build_markov_model(seq, n=1):
    """
    Build an n-th order Markov model from a sequence.

    Parameters
    ----------
    seq : sequence
        Input sequence (e.g., list of symbols, notes, tokens).
    n : int
        Order of the Markov model (n >= 1).

    Returns
    -------
    dict
        Mapping from n-gram (tuple of length n) to list of possible next symbols.
    """
    if n < 1:
        raise ValueError("n must be >= 1")

    model = defaultdict(list)

    for i in range(len(seq) - n):
        state = tuple(seq[i:i+n])
        next_symbol = seq[i+n]
        model[state].append(next_symbol)

    return dict(model)

MAX_NUM_OF_PAST_EVENTS = 1000

def _update(bb):
    pitches = [ msg.note for msg in bb.MidiInEvents.event_list if msg.type == 'note_on' ]

    for past_symbols in [ 1, 2, 4, 8 ]:
        print(f"Make {past_symbols}-order Markov model..")
        model = build_markov_model(pitches[-MAX_NUM_OF_PAST_EVENTS:], n=past_symbols)
        
        print(model)
        bb.MarkovModel.pitch_models[past_symbols] = model
        
        
