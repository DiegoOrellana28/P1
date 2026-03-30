import sys
from typing import List, Tuple, Dict


Tarea = Tuple[str, int, str]
Asignacion = Tuple[str, str, int, int]


def leer_tareas() -> List[Tarea]:
    tareas: List[Tarea] = []

    with open("tareas.txt", "r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            partes = linea.split(",")

            id_tarea = partes[0]
            duracion = int(partes[1])
            categoria = partes[2]

            tarea: Tarea = (id_tarea, duracion, categoria)
            tareas.append(tarea)

    return tareas


def leer_recursos() -> Dict[str, List[str]]:
    recursos: Dict[str, List[str]] = {}

    with open("recursos.txt", "r") as archivo:
        for linea in archivo:
            linea = linea.strip()
            partes = linea.split(",")

            id_recurso = partes[0]
            categorias: List[str] = []

            i = 1
            while i < len(partes):
                categorias.append(partes[i])
                i += 1

            recursos[id_recurso] = categorias

    return recursos


def construir_indice_categoria_recurso(recursos: Dict[str, List[str]] ) -> Dict[str, List[str]]:
    indice: Dict[str, List[str]] = {}

    for id_recurso in recursos:
        for categoria in recursos[id_recurso]:
            if categoria not in indice:
                indice[categoria] = []

            indice[categoria].append(id_recurso)

    return indice


def calcular_score_tarea(tarea: Tarea,indice_categoria: Dict[str, List[str]]) -> float:
    _, duracion, categoria = tarea

    compatibles = indice_categoria[categoria]
    cantidad = len(compatibles)

    return duracion / cantidad


def ordenar_tareas(tareas: List[Tarea],indice_categoria: Dict[str, List[str]]) -> List[Tarea]:

    def clave_ordenamiento(tarea: Tarea):

        score = calcular_score_tarea(tarea, indice_categoria)
        duracion = tarea[1]
        id_tarea = tarea[0]

        return (-score, -duracion, id_tarea)

    tareas_ordenadas = sorted(tareas, key=clave_ordenamiento)

    return tareas_ordenadas


def buscar_recursos_compatibles(categoria: str, indice_categoria: Dict[str, List[str]]) -> List[str]:
    return indice_categoria[categoria]


def buscar_mejor_recurso(
    compatibles: List[str],
    tiempo_libre: Dict[str, int],
    recursos: Dict[str, List[str]],
    duracion: int
    ) -> str:

    mejor_recurso = compatibles[0]
    mejor_fin = tiempo_libre[mejor_recurso] + duracion

    for id_recurso in compatibles:
        fin_actual = tiempo_libre[id_recurso] + duracion

        if fin_actual < mejor_fin:
            mejor_fin = fin_actual
            mejor_recurso = id_recurso

        elif fin_actual == mejor_fin:
            if len(recursos[id_recurso]) < len(recursos[mejor_recurso]):
                mejor_recurso = id_recurso

    return mejor_recurso


def planificar_tareas(tareas: List[Tarea], recursos: Dict[str, List[str]]) -> List[Asignacion]:
    indice_categoria = construir_indice_categoria_recurso(recursos)
    tareas_ordenadas = ordenar_tareas(tareas, indice_categoria)

    tiempo_libre: Dict[str, int] = {}

    for id_recurso in recursos:
        tiempo_libre[id_recurso] = 0

    cronograma: List[Asignacion] = []

    for tarea in tareas_ordenadas:
        id_tarea = tarea[0]
        duracion = tarea[1]
        categoria = tarea[2]

        compatibles = buscar_recursos_compatibles(categoria, indice_categoria)
        mejor_recurso = buscar_mejor_recurso(compatibles,tiempo_libre,recursos,duracion)

        inicio = tiempo_libre[mejor_recurso]
        fin = inicio + duracion

        asignacion: Asignacion = (id_tarea, mejor_recurso, inicio, fin)
        cronograma.append(asignacion)

        tiempo_libre[mejor_recurso] = fin

    return cronograma


def escribir_output(cronograma: List[Asignacion]) -> None:
    with open("output.txt", "w") as archivo:
        for asignacion in cronograma:
            id_tarea = asignacion[0]
            id_recurso = asignacion[1]
            inicio = asignacion[2]
            fin = asignacion[3]

            linea = id_tarea + "," + id_recurso + "," + str(inicio) + "," + str(fin)
            archivo.write(linea + "\n")


def calcular_makespan(cronograma: List[Asignacion]) -> int:
    makespan = 0

    for asignacion in cronograma:
        fin = asignacion[3]

        if fin > makespan:
            makespan = fin

    return makespan


def main() -> None:
    
    if len(sys.argv) >= 2:
        makespan_objetivo = int(sys.argv[1])

    else:
        makespan_objetivo = None
        print("No se ingresó makespan objetivo")

    tareas = leer_tareas()
    recursos = leer_recursos()

    cronograma = planificar_tareas(tareas, recursos)

    escribir_output(cronograma)

    makespan = calcular_makespan(cronograma)
    print("Makespan obtenido:", makespan)

    if makespan_objetivo is not None:
        print("Makespan objetivo:", makespan_objetivo)

        if makespan <= makespan_objetivo:
            print("La solución cumple el objetivo.")
        else:
            print("La solución no cumple el objetivo.")


if __name__ == "__main__":
    main()
