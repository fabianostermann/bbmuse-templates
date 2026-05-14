pitch_models = {}

def predict(state, order=None):

    if isinstance(state, list):
        state = tuple(state)
        
    if order is None:
        order = len(state)

    model = pitch_models[order]
    return model[state]

