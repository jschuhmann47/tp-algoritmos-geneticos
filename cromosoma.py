import random;
from fixture import equipos;

def generar_cromosoma():
    cromosoma = []
    for _ in range(19):  # 19 fechas
        # Dentro de una fecha, no hay repetidos (en la población inicial)
        fecha = list(range(20))
        random.shuffle(fecha)
        cromosoma.append(fecha)
    return sum(cromosoma, []) # Se concatenan los resultados para pasárselos a la lib

def decodificar_cromosoma(cromosoma):
    fixture = []
    for i in range(19):
        fecha = cromosoma[i * 20 : (i + 1) * 20]
        partidos_fecha = []
        for j in range(10):
            partido = fecha[j * 2 : (j + 1) * 2]
            equipo_local = [equipo for equipo, indice in equipos.items() if indice == partido[0]][0]
            equipo_visitante = [equipo for equipo, indice in equipos.items() if indice == partido[1]][0]
            partidos_fecha.append((equipo_local, equipo_visitante))
        fixture.append(partidos_fecha)
    return fixture
