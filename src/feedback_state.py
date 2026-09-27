"""Reference implementation for Feedback-Weighted State Adaptation.

'I' is a model state, not personal identity or consciousness.
"""
from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class Step:
    before: float
    feedback_delta: float
    weight: float
    raw_update: float
    applied_update: float
    memory_input: float
    after: float
    held: bool

def clip(x: float, limit: Optional[float]) -> float:
    if limit is None:return x
    if limit < 0:raise ValueError("limit must be nonnegative")
    return max(-limit,min(limit,x))

def update_state(state: float, feedback_delta: float, weight: float,
                 epsilon: float=0.0, max_update: Optional[float]=None,
                 memory_input: float=0.0, memory_gain: float=0.0) -> Step:
    if epsilon < 0:raise ValueError("epsilon must be nonnegative")
    held=abs(feedback_delta) <= epsilon
    raw=feedback_delta*weight
    applied=0.0 if held else clip(raw,max_update)
    after=state+applied+memory_gain*memory_input
    return Step(state,feedback_delta,weight,raw,applied,memory_input,after,held)

def trajectory(initial: float, deltas, weights, **kwargs):
    ds=list(deltas);ws=list(weights)
    if len(ds)!=len(ws):raise ValueError("deltas and weights must have equal length")
    out=[initial];state=initial
    for d,w in zip(ds,ws):
        step=update_state(state,d,w,**kwargs);state=step.after;out.append(state)
    return out
