# src/immunonaut/models/human.py
from random import uniform
from typing import List, Protocol, TypeAlias, Tuple, Union

from immunonaut.cell_types import (Abundance, CellType, Granulocyte,
                                   Lymphocyte, Monocyte)

from immunonaut.mapping import HUMAN

class ImmuneSystem:
    def __init__(
            self,
            basophils: (List[Granulocyte.Basophil], Abundance) = ([],(0.005, 0.01)),
            cell_count: int = 1000,
            dendritic_cells: (List[Monocyte.Dendritic], Abundance) = (
                    [], (0.0016, 0.0068)
            ),
            eosinophils: (List[Granulocyte.Eosinophil], Abundance) = ([], (0.01, 0.04)),
            macrophages: (List[Monocyte.Macrophage], Abundance) = ([], (0.0, 0.0)),
            monocytes: (List[Monocyte], Abundance) = ([], (0.02, 0.08)),
            neutrophils: (List[Granulocyte.Neutrophil], Abundance) = ([], (0.4, 0.6)),
            immunocompetent: bool = True
    ) -> None:
        self.basophils = basophils
        self.cell_count = cell_count
        self.dendritic_cells = dendritic_cells
        self.eosinophils = eosinophils
        self.macrophages = macrophages
        self.monocytes = monocytes
        self.neutrophils = neutrophils
        self.immunocompetent = immunocompetent

        # Determining initial WBC counts
        self.basophil_population = self.basophils[0]
        self.basophil_range = (self.basophils[1][0], self.basophils[1][1])
        self.basophil_abundance = uniform(self.basophil_range[0], self.basophil_range[1])
        self.basophils_absolute = int(self.basophil_abundance * self.cell_count)

        self.dendritic_cell_population = self.dendritic_cells[0]
        self.dendritic_cell_range = (self.dendritic_cells[1][0], self.dendritic_cells[1][1])
        self.dendritic_cell_abundance = uniform(self.dendritic_cell_range[0], self.dendritic_cell_range[1])
        self.dendritic_cell_absolute = int(self.dendritic_cell_abundance * self.cell_count)

        self.eosinophil_population = self.eosinophils[0]
        self.eosinophil_range = (self.eosinophils[1][0], self.eosinophils[1][1])
        self.eosinophil_abundance = uniform(self.eosinophil_range[0], self.eosinophil_range[1])
        self.eosinophils_absolute = int(self.eosinophil_abundance * self.cell_count)

        self.macrophage_population = self.macrophages[0]
        self.macrophage_range = (self.macrophages[1][0], self.macrophages[1][1])
        self.macrophage_abundance = uniform(self.macrophage_range[0], self.macrophage_range[1])
        self.macrophages_absolute = int(self.macrophage_abundance * self.cell_count)

        self.monocyte_population = self.monocytes[0]
        self.monocyte_range = (self.monocytes[1][0], self.monocytes[1][1])
        self.monocyte_abundance = uniform(self.monocyte_range[0], self.monocyte_range[1]) - self.macrophage_abundance
        self.monocytes_absolute = int(self.monocyte_abundance * self.cell_count)

        self.neutrophil_population = self.neutrophils[0]
        self.neutrophil_range = (self.neutrophils[1][0], self.neutrophils[1][1])
        self.neutrophil_abundance = uniform(self.neutrophil_range[0], self.neutrophil_range[1])
        self.neutrophils_absolute = int(self.neutrophil_abundance * self.cell_count)

        # Initializing WBC populations
        if self.immunocompetent:
            try:
                self.basophil_population.append([Granulocyte.Basophil() for i in range(self.basophils_absolute)])
                self.dendritic_cell_population.append([Monocyte.Dendritic() for i in range(self.dendritic_cell_absolute)])
                self.eosinophil_population.append([Granulocyte.Eosinophil() for i in range(self.eosinophils_absolute)])
                self.macrophage_population.append([Monocyte.Macrophage() for i in range(self.macrophages_absolute)])
                self.monocyte_population.append([Monocyte() for i in range(self.monocytes_absolute)])
                self.neutrophil_population.append([Granulocyte.Neutrophil() for i in range(self.neutrophils_absolute)])
            except ValueError as e:
                print("Error: ", e)
            except Exception as e:
                print("Error: ", e)

def main() -> ImmuneSystem:
    immune_system = ImmuneSystem()
    return immune_system

if __name__ == '__main__':
    main()