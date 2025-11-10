from abc import ABC, abstractmethod
from typing import List, Dict
from src.domain.entities import Gasto

class AnalisisStrategy(ABC):
    @abstractmethod
    def analizar(self, gastos: List[Gasto]) -> Dict:
        pass