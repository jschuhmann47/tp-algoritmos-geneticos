equipos = {
    "river": 0,
    "boca": 1,
    "racing": 2,
    "independiente": 3,
    "san_lorenzo": 4,
    "huracan": 5,
    "velez": 6,
    "argentinos_juniors": 7,
    "banfield": 8,
    "lanus": 9,
    "gimnasia": 10,
    "estudiantes": 11,
    "rosario_central": 12,
    "newells": 13,
    "talleres": 14,
    "belgrano": 15,
    "colon": 16,
    "union": 17,
    "godoy_cruz": 18,
    "atletico_tucuman": 19,
}

equipos_grandes = [
    "river",
    "boca",
    "racing",
    "independiente",
    "san_lorenzo",
    "velez",
    "estudiantes",
]

equipos_chicos = [equipo for equipo in equipos.keys() if equipo not in equipos_grandes]

partidos_clasicos = [
    ("river", "boca"),
    ("racing", "independiente"),
    ("san_lorenzo", "huracan"),
    ("banfield", "lanus"),
    ("gimnasia", "estudiantes"),
    ("rosario_central", "newells"),
    ("talleres", "belgrano"),
    ("colon", "union"),
    ("velez", "argentinos_juniors"),
    ("godoy_cruz", "atletico_tucuman"),
]

'''
fixture[i][j][k]:
i: fecha
j: partido
k: 0 y 1 son los equipos local y visitante
'''

def cuantos_cumplen(lista, f):
    return len(list(filter(f, lista)))

def dia_del_indice(i):
    if i < 2:
        return 0 # vie
    if i < 6:
        return 1 # sab
    if i < 9:
        return 2 # dom
    return 3 # lun

def calcular_aptitud(fixture):
    aptitud = 0

    # Restricción: Todos los equipos deben jugar como mínimo y máximo 1 partido por fecha
    for fecha in fixture:
        equipos_fecha = []
        for partido in fecha:
            equipos_fecha.append(partido[0])
            equipos_fecha.append(partido[1])
        if any(equipo for equipo in equipos.keys() if equipos_fecha.count(equipo) != 1):
            aptitud += 2
    
    # Restricción: Un equipo nunca puede jugar contra sí mismo
    for fecha in fixture:
        for partido in fecha:
            if partido[0] == partido[1]:
                aptitud += 1

    # Restricción: Todos los equipos deben jugar entre ellos
    for equipo in equipos.keys():
        todos_los_equipos_contra_los_que_jugo = set()
        for fecha in fixture:
            partidos_del_equipo = filter(lambda partido: partido[0] == equipo or partido[1] == equipo, fecha)
            equipos_contra_los_que_jugo = map(lambda partido: partido[0] if partido[1] == equipo else partido[1], partidos_del_equipo)
            todos_los_equipos_contra_los_que_jugo = todos_los_equipos_contra_los_que_jugo.union(set(equipos_contra_los_que_jugo))
        todos_los_equipos_contra_los_que_jugo.add(equipo)
        if len(todos_los_equipos_contra_los_que_jugo) != len(equipos):
            aptitud += 1

    # Restricción: La mitad de los equipos deben jugar 10 partidos de local y 9 de visitante, y viceversa
    for equipo in equipos.keys():
        partidos_de_local = 0
        partidos_de_visitante = 0
        for fecha in fixture:
            partidos_de_local += cuantos_cumplen(fecha, lambda partido: partido[0] == equipo)
            partidos_de_visitante += cuantos_cumplen(fecha, lambda partido: partido[1] == equipo)
        if not (partidos_de_local == 10 and partidos_de_visitante == 9 or partidos_de_local == 9 and partidos_de_visitante == 10):
            aptitud += 1

    # Restricción: Los equipos deben alternar de localía fecha tras fecha
    for equipo in equipos.keys():
        for i in range(len(fixture) - 1):
            partidos_de_local = cuantos_cumplen(fixture[i], lambda partido: partido[0] == equipo)
            partidos_de_visitante = cuantos_cumplen(fixture[i], lambda partido: partido[1] == equipo)
            partidos_de_local_en_la_siguiente = cuantos_cumplen(fixture[i + 1], lambda partido: partido[0] == equipo)           
            partidos_de_visitante_en_la_siguiente = cuantos_cumplen(fixture[i + 1], lambda partido: partido[1] == equipo)
            if (partidos_de_local > 0 and partidos_de_local_en_la_siguiente > 0 or partidos_de_visitante > 0 and partidos_de_visitante_en_la_siguiente > 0):
                aptitud += 1
                break

    # Restricción: River y Boca deben jugar todos sus partidos los días domingo
    # [vie, vie, sab, sab, sab, dom, dom, dom, lun, lun]
    for fecha in fixture:
        for indice_partido in range(len(fecha)):
            if fecha[indice_partido][0] in ["river", "boca"] or fecha[indice_partido][1] in ["river", "boca"]:
                if indice_partido < 5 or indice_partido > 7:
                    aptitud += 1
                    break

    # Restricción: El partido entre River y Boca se debe jugar en la fecha 10
    hay_partido_de_river_boca = False
    for partido in fixture[9]:
        if partido[0] in ["river", "boca"] and partido[1] in [
            "river",
            "boca",
        ]:
            hay_partido_de_river_boca = True
            break
    if not hay_partido_de_river_boca:
        aptitud += 1

    # Restricción: Los equipos con sus rivales clásicos no pueden jugar de local el mismo día
    for fecha in fixture:
        locales = [[], [], [], []]
        for i in range(len(fecha)):
            locales[dia_del_indice(i)].append(fecha[i][0])
        for locales_dia in locales:
            for i in range(len(locales_dia)):
                for j in range(len(locales_dia[i + 1:])):
                    if (i, j) in partidos_clasicos or (j, i) in partidos_clasicos:
                        aptitud += 1

    # Restricción: Por cada fecha, el día sábado debe haber, como mínimo, un partido que involucre a un equipo grande
    equipos_sabado = []
    for fecha in fixture:
        for partido in fecha[2:5]:
            equipos_sabado.extend(partido)
        if not any(equipo in equipos_grandes for equipo in equipos_sabado):
            aptitud += 1

    # Restricción: Por cada fecha, el día domingo debe haber, como mínimo, dos partidos que involucren a un equipo grande
    equipos_domingo = []
    for fecha in fixture:
        for partido in fecha[5:8]:
            equipos_domingo.extend(partido)
        if cuantos_cumplen(equipos_domingo, lambda equipo: equipo in equipos_grandes) < 2:
            aptitud += 1

    # Restricción: Solo puede haber un partido entre equipos clásicos por fecha
    for fecha in fixture:
        partidos_clasicos_fecha = [
            (partido[0], partido[1])
            for partido in fecha
            if (partido[0], partido[1]) in partidos_clasicos
            or (partido[1], partido[0]) in partidos_clasicos
        ]
        if len(partidos_clasicos_fecha) > 1:
            aptitud += 1

    return aptitud
