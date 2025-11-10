from abc import ABC, abstractmethod
from src.domain.entities import TipoAlerta, Usuario

class Notificable(ABC):
    @abstractmethod
    def enviar_alerta(self, tipo: TipoAlerta, mensaje: str, usuario: Usuario) -> None:
        pass