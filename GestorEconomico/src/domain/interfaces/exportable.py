from abc import ABC, abstractmethod
from typing import List
from src.domain.entities import Gasto

class Exportable(ABC):
    @abstractmethod
    def exportar(self, gastos: List[Gasto]) -> str:
        pass