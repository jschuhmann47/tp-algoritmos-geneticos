import random;
from fixture import equipos, dias_semana;

def generar_cromosoma():
    cromosoma = []
    for _ in range(190):  # 190 combinaciones posibles de equipos
        localia = random.randint(0, 1)
        dia_semana = random.randint(0, 3)
        nro_fecha = random.randint(0, 18)
        cromosoma.append(nro_fecha * 8 + dia_semana * 2 + localia)
    return cromosoma

def obtener_equipos_segun_indice(i):
    iteraciones = 0
    i = i - 19
    while i >= 0:
        iteraciones += 1
        i -= (19 - iteraciones)
    equipo_1 = iteraciones
    equipo_2 = iteraciones + (19 - iteraciones + i) + 1
    return [equipo_1, equipo_2]

def decodificar_cromosoma(cromosoma):
    fixture = [[] for _ in range(19)]
    for i in range(len(cromosoma)):
        partido = cromosoma[i]
        nro_fecha = partido // 8
        dia_semana = (partido % 8) // 2
        localia = partido // 2
        [equipo_1, equipo_2] = obtener_equipos_segun_indice(i)
        if localia == 1:
            equipo_2, equipo_1 = equipo_1, equipo_2
        fixture[nro_fecha].append([equipos[equipo_1], equipos[equipo_2], dias_semana[dia_semana]])
    return fixture
