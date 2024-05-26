import random;
from fixture import equipos, dias;

def generar_cromosoma():
    cromosoma = []
    for _ in range(19):  # 19 fechas
        fecha = []
        for _ in range(10):  # 10 partidos por fecha
            equipo_local = random.choice(list(equipos.values()))
            equipo_visitante = random.choice(list(equipos.values()))
            dia_partido = random.randint(0, 3)  # Se elige aleatoriamente el día del partido
            partido = (equipo_local, equipo_visitante, dia_partido)
            fecha.append(partido)
        cromosoma.append(fecha)
    return sum(sum(cromosoma, []), ()) # Se concatenan los resultados para pasárselos a la lib

def decodificar_cromosoma(cromosoma):
    fixture = []
    for i in range(19):
        fecha = cromosoma[i * 30 : (i + 1) * 30]
        partidos_fecha = []
        for j in range(10):
            partido = fecha[j * 3 : (j + 1) * 3]
            equipo_local = [equipo for equipo, indice in equipos.items() if indice == partido[0]][0]
            equipo_visitante = [equipo for equipo, indice in equipos.items() if indice == partido[1]][0]
            dia_partido = [dia for dia, indice in dias.items() if indice == partido[2]][0]
            partidos_fecha.append((equipo_local, equipo_visitante, dia_partido))
        fixture.append(partidos_fecha)
    return fixture
