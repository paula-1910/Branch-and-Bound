from dataclasses import dataclass, field
from typing import List
import math

# Definición del estado

@dataclass
class Estado:
    semanas_restantes: int
    eda: str
    ecuaciones: str
    calculo: str
    geometria: str
    suspensos_inevitables: int
    estres: int = 0

    def asignaturas(self):
        return [self.eda, self.ecuaciones, self.calculo, self.geometria]


# Cálculo de la cota inferior

def cota_inferior(estado: Estado) -> int:
   
    if estado.eda == "Suspensa":
        return math.inf

    suspensos = estado.suspensos_inevitables
    for asignatura in estado.asignaturas():
        if asignatura == "Suspensa":
            suspensos += 1

    return suspensos

# Generación de decisiones

def expandir_estado(estado: Estado) -> List[Estado]:
  
    hijos = []

    if estado.semanas_restantes == 0:
        return hijos

    # D1: Priorizar EDA II
    hijos.append(Estado(
        estado.semanas_restantes - 1,
        "Aprobable",
        estado.ecuaciones,
        estado.calculo,
        estado.geometria,
        estado.suspensos_inevitables,
        estado.estres + 1
    ))

    # D2: Priorizar secundarias
    hijos.append(Estado(
        estado.semanas_restantes - 1,
        "Suspensa" if estado.semanas_restantes == 1 else estado.eda,
        "Aprobable",
        "Aprobable",
        estado.geometria,
        estado.suspensos_inevitables + (1 if estado.semanas_restantes == 1 else 0),
        estado.estres + 2
    ))

    # D3: Repartir esfuerzo
    hijos.append(Estado(
        estado.semanas_restantes - 1,
        estado.eda,
        estado.ecuaciones,
        estado.calculo,
        estado.geometria,
        estado.suspensos_inevitables,
        estado.estres + 3
    ))

    return hijos

# Algoritmo Branch and Bound

def branch_and_bound(estado_inicial: Estado):
    mejor_solucion = None
    mejor_cota = math.inf

    pila = [estado_inicial]

    while pila:
        estado = pila.pop()
        cota = cota_inferior(estado)

        # Poda
        if cota >= mejor_cota:
            continue

        # Nodo hoja
        if estado.semanas_restantes == 0:
            mejor_solucion = estado
            mejor_cota = cota
            continue

        # Expandir
        for hijo in expandir_estado(estado):
            pila.append(hijo)

    return mejor_solucion, mejor_cota


# Ejecución del modelo


if __name__ == "__main__":
    print("Configuración inicial del semestre")
    semanas = int(input("Introduce el número de semanas restantes (ej. 3): "))
    prioridad = input("¿Deseas priorizar EDA II desde el inicio? (s/n): ").lower()

    
    estado_inicial = Estado(
        semanas_restantes=3,
        eda="Dudosa",
        ecuaciones="Dudosa",
        calculo="Dudosa",
        geometria="Dudosa",
        suspensos_inevitables=0
    )

    solucion, suspensos = branch_and_bound(estado_inicial)

    print("Mejor solución encontrada:\n")
    print(f"EDA II: {solucion.eda}")
    print(f"Ecuaciones: {solucion.ecuaciones}")
    print(f"Cálculo: {solucion.calculo}")
    print(f"Geometría: {solucion.geometria}")
    print(f"Suspensos mínimos: {suspensos}")
    print(f"Estrés total: {solucion.estres}")
