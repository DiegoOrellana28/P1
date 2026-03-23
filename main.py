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

def ordenar_tareas(tareas: List[Tarea]) -> List[Tarea]:
    tareas_ordenadas = sorted(tareas, key=lambda tarea: tarea[1], reverse=True)
    return tareas_ordenadas

def buscar_recursos_compatibles(
    categoria: str, recursos: Dict[str, List[str]]
) -> List[str]:
    compatibles: List[str] = []

    for id_recurso in recursos:
        categorias = recursos[id_recurso]

        if categoria in categorias:
            compatibles.append(id_recurso)

    return compatibles

def main() -> None:
    tareas = leer_tareas()
    recursos = leer_recursos()

    print("Tareas leídas:")
    print(tareas)

    print("Recursos leídos:")
    print(recursos)

    tareas_ordenadas = ordenar_tareas(tareas)

    print("Tareas ordenadas:")
    print(tareas_ordenadas)

    primera_tarea = tareas_ordenadas[0]
    categoria = primera_tarea[2]

    compatibles = buscar_recursos_compatibles(categoria, recursos)

    print("Recursos compatibles para la primera tarea:")
    print(compatibles)


if __name__ == "__main__":
    main()
