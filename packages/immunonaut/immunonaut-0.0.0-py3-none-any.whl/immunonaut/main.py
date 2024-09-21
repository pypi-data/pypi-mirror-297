# src/immunonaut/main.py
import os
import sys

from appdirs import user_config_dir, user_data_dir, user_cache_dir
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Protocol, Tuple, TypeAlias, Union

from mapping import IMMUNOMAP

# Application metadata/support directories
APP_AUTHOR = "kosmolebryce"
APP_NAME = "immunonaut"
APP_DATA_DIR = user_data_dir(APP_AUTHOR, APP_NAME)
APP_CONFIG_DIR = user_config_dir(APP_AUTHOR, APP_NAME)
APP_CACHE_DIR = user_cache_dir(APP_AUTHOR, APP_NAME)
HOME = Path.home()

# Custom typing
Abundance: TypeAlias = Union[int, float, Tuple[Union[int, float], Union[int, float]]]
Cell: TypeAlias = Tuple[str, Abundance]
Lineage: TypeAlias = Dict[str, Cell | List[Cell]]

class ImmuneSystem(Protocol):
    def __init__(self):
        self.species: str = "human"
        self.competence: bool = True
        self.cell_lineages: Lineage = {}
        self.abundances: List[Dict[str, Abundance]] = []

    def characterize(self):
        return {
            "species": self.species,
            "competence": self.competence,
            "cell_lineages": self.cell_lineages,
        }

@dataclass
class Human(ImmuneSystem):
    species: str = "human"
    competence: bool = True
    cell_lineages: Lineage = field(default_factory=lambda: {
        "granulocytes": [
            ("basophil", (0.005, 0.01)),
            ("eosinophil", (0.01, 0.04)),
            ("neutrophil", (0.40, 0.60))
            ],
        "monocyte": [
            ("dendritic", (0.16, 0.68)),
            ("macrophage", (0.2, 0.8))
        ]
    }
                                   )
    abundances: List[Dict[str, Abundance]] = field(default_factory=lambda: [])

def main():
    print()
    print("Starting Immunonaut...\n")
    print(f"Your current working directory is: `{os.getcwd()}`.")
    print("Your `PATH` environment variable is set to include: ")
    print()

    for i in sys.path:
        print(f">   {i}")

    print()

    human = Human()

    characteristics = human.characterize()

    for key, value in characteristics.items():
        if key == "cell_lineages":
            print(f"{key}:")

            for l in value:
                print("   ", l)
        else:
            print(f"{key}:")
            print(f"    {value}")

    for lineage, details in human.cell_lineages.items():
        for cell_type, freq in details:
            human.abundances.append({str(cell_type): freq})

    return

if __name__ == "__main__":
    main()