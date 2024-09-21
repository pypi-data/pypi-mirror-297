# src/immunonaut/pathways.py
from typing import Dict, List, Protocol, Tuple, TypeAlias

# Custom typing
Signal: TypeAlias = str
SignalingPathway: TypeAlias = Dict[Signal, List[Signal]]

class Pathway(Protocol):
    call: Signal
    response: Signal
    target: SignalingPathway

class Adaptive(Pathway):
    def __init__(self, call, response, target) -> None:
        self.call = call
        self.response = response
        self.target = target

class Complement(Pathway):
    def __init__(self, call, response, target) -> None:
        self.call = call
        self.response = response
        self.target = target

class Innate(Pathway):
    def __init__(self, call, response, target) -> None:
        self.call = call
        self.response = response
        self.target = target