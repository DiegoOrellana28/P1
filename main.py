from typing import List, Tuple, Dict

# Tarea: (id, duracion, categoria)
def leer_tareas() -> List[Tuple[str, int, str]]:
    tareas = []
    with open("tareas.txt", "r") as f:
        for linea in f:
            partes = linea.strip().split(",")
            tarea_id = partes[0]
            duracion = int(partes[1])
            categoria = partes[2]
            tareas.append((tarea_id, duracion, categoria))
    return tareas


# Recursos: {id: [categorias]}
def leer_recursos() -> Dict[str, List[str]]:
    recursos = {}
    with open("recursos.txt", "r") as f:
        for linea in f:
            partes = linea.strip().split(",")
            recurso_id = partes[0]
            categorias = partes[1:]
            recursos[recurso_id] = categorias
    return recursos

if __name__ == "__main__":
    tareas = leer_tareas()
    recursos = leer_recursos()

    print("Tareas:", tareas)
    print("Recursos:", recursos)