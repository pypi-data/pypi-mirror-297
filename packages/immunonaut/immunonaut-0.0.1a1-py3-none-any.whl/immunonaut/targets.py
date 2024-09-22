from dataclasses import dataclass
from typing import List, TypeAlias

# Custom typing
Symbol: TypeAlias = str | List[str]

@dataclass(frozen=True)
class Receptor:

    @dataclass(frozen=True)
    class TollLikeReceptor:
        TLR1: Symbol = "TLR1"
        TLR2: Symbol = "TLR2"
        TLR3: Symbol = "TLR3"
        TLR4: Symbol = "TLR4"
        TLR5: Symbol = "TLR5"
        TLR6: Symbol = "TLR6"
        TLR7: Symbol = "TLR7"
        TLR8: Symbol = "TLR8"
        TLR9: Symbol = "TLR9"
        TLR10: Symbol = "TLR10"
        TLR11: Symbol = "TLR11"
        TLR12: Symbol = "TLR12"
        TLR13: Symbol = "TLR13"
        TLR14: Symbol = "TLR14"

    @dataclass(frozen=True)
    class NodLikeReceptor:

        @dataclass(frozen=True)
        class NOD:
            NOD1: Symbol ="NOD1"
            NOD2: Symbol = "NOD2"
            NOD3: Symbol = "NOD3"
            NLRC3 = NOD3
            NOD4: Symbol = "NOD4"
            NLRC5 = NOD4
            NOD5: Symbol = "NOD5"
            NLRX1 = NOD5
            CIITA: Symbol = "CIITA"

        @dataclass(frozen=True)
        class NLRP:
            NLRP1: Symbol = "NLRP1"
            NLRP2: Symbol = "NLRP2"
            NLRP3: Symbol = "NLRP3"
            NLRP4: Symbol = "NLRP4"
            NLRP5: Symbol = "NLRP5"
            NLRP6: Symbol = "NLRP6"
            NLRP7: Symbol = "NLRP7"
            NLRP8: Symbol = "NLRP8"
            NLRP9: Symbol = "NLRP9"
            NLRP10: Symbol = "NLRP10"
            NLRP11: Symbol = "NLRP11"
            NLRP12: Symbol = "NLRP12"
            NLRP13: Symbol = "NLRP13"
            NLRP14: Symbol = "NLRP14"

    ...