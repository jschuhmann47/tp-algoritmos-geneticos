import random;
from fixture import equipos, dias;

def generar_cromosoma():
    cromosoma = []
    for _ in range(19):  # 19 fechas
        fecha = []
        for _ in range(10):  # 10 partidos por fecha
            equipo_local = random.choice(equipos.values())
            equipo_visitante = random.choice(equipos.values())
            dia_partido = random.randint(0, 3)  # Se elige aleatoriamente el día del partido
            partido = (equipo_local, equipo_visitante, dia_partido)
            fecha.append(partido)
        cromosoma.append(fecha)
    return cromosoma

def decodificar_cromosoma(cromosoma):
    fixture = []
    for fecha in cromosoma:
        partidos_fecha = []
        for partido in fecha:
            equipo_local = [equipo for equipo, indice in equipos.items() if indice == equipos[partido[0]]][0]
            equipo_visitante = [equipo for equipo, indice in equipos.items() if indice == equipos[partido[1]]][0]
            dia_partido = [dia for dia, indice in dias.items() if indice == partido[2]][0]
            partidos_fecha.append((equipo_local, equipo_visitante, dia_partido))
        fixture.append(partidos_fecha)
    return fixture
