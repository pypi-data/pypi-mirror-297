# src/immunonaut/mapping.py
from dataclasses import dataclass, field
from typing import List, TypeAlias

from .cell_types import (Granulocyte, Lymphocyte, Monocyte)

from .targets import Receptor

# Custom types
Species: TypeAlias = str

@dataclass
class HUMAN:
    species: Species = "human"
    NODs: List[Receptor.NodLikeReceptor.NOD] = field(default_factory=lambda: [
        Receptor.NodLikeReceptor.NOD.NOD1,
        Receptor.NodLikeReceptor.NOD.NOD2,
        Receptor.NodLikeReceptor.NOD.NOD3,
        Receptor.NodLikeReceptor.NOD.NOD4,
        Receptor.NodLikeReceptor.NOD.NOD5
    ]
                                                     )
    NLRPs: List[Receptor.NodLikeReceptor.NLRP] = field(default_factory=lambda: [
        Receptor.NodLikeReceptor.NLRP.NLRP1,
        Receptor.NodLikeReceptor.NLRP.NLRP2,
        Receptor.NodLikeReceptor.NLRP.NLRP3,
        Receptor.NodLikeReceptor.NLRP.NLRP4,
        Receptor.NodLikeReceptor.NLRP.NLRP5,
        Receptor.NodLikeReceptor.NLRP.NLRP6
    ]
                                                       )
    TLRs: List[Receptor.TollLikeReceptor] = field(default_factory=lambda: [
        Receptor.TollLikeReceptor.TLR1,
        Receptor.TollLikeReceptor.TLR2,
        Receptor.TollLikeReceptor.TLR3,
        Receptor.TollLikeReceptor.TLR4,
        Receptor.TollLikeReceptor.TLR5,
        Receptor.TollLikeReceptor.TLR6,
        Receptor.TollLikeReceptor.TLR7,
        Receptor.TollLikeReceptor.TLR8,
        Receptor.TollLikeReceptor.TLR9,
        Receptor.TollLikeReceptor.TLR10,
        Receptor.TollLikeReceptor.TLR11,
        Receptor.TollLikeReceptor.TLR12,
        Receptor.TollLikeReceptor.TLR13,
        Receptor.TollLikeReceptor.TLR14
        ]
                                                  )

    CELL_TYPES = (
        Granulocyte.Basophil,
        Monocyte.Dendritic,
        Granulocyte.Eosinophil,
        Monocyte.Macrophage,
        Monocyte,
        Granulocyte.Neutrophil,
        Lymphocyte,
        Lymphocyte.T,
        Lymphocyte.B,
        Lymphocyte.T.Helper,
        Lymphocyte.T.Killer,
        Lymphocyte.B.Effector,
        Lymphocyte.B.Memory
    )