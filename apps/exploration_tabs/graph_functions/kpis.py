import plotly.graph_objs as go

# TODO: add layout parameters


########## Helper functions ##########

def _base_graph(x, y, **params):
    raise NotImplementedError


## Similar to graphs2d, but might need
## three or more values in the tuple
graph_configs = {
    'baseline': (True, True),
 }


########## Graph functions ##########
## Functions below here implement the various graphs
## These should return plotly traces (i.e. lists of `go` objects)

def baseline(x, y):
    raise NotImplementedError
    return [_base_graph(x, y, mode="markers")]

def other_graph(x, y):
    raise NotImplementedError
    return [_base_graph(x, y, mode="markers")]
