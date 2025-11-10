from dataclasses import dataclass

@dataclass
class ComparacionGastos:
    diferencia_total: float
    porcentaje_cambio: float
    mes_actual_total: float
    mes_anterior_total: float
    
    def __str__(self) -> str:
        tendencia = "aumento" if self.diferencia_total >= 0 else "disminución"
        return (f"Comparación mensual: {tendencia} de ${abs(self.diferencia_total):.2f} "
                f"({self.porcentaje_cambio:+.1f}%)")