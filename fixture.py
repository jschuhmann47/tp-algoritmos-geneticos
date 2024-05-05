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

dias = {"viernes": 0, "sábado": 1, "domingo": 2, "lunes": 3}

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


def calcular_aptitud(fixture):
    aptitud = 0

    # Restricción: Todos los equipos deben jugar como mínimo y máximo 1 partido por fecha
    # Restricción: Un equipo nunca puede jugar contra sí mismo
    for fecha in fixture:
        equipos_fecha = []
        for partido in fecha:
            equipos_fecha.extend(partido[:2])
        for equipo in equipos.keys():
            if equipos_fecha.count(equipo) != 1:
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
    equipos_local = []
    equipos_visitante = []
    for fecha in fixture:
        for partido in fecha:
            equipos_local.append(partido[0])
            equipos_visitante.append(partido[1])
    for equipo in equipos.keys():
        if equipos_local.count(equipo) != equipos_visitante.count(equipo):
            aptitud += 1

    for equipo in equipos.keys():
        partidos_de_local = 0
        partidos_de_visitante = 0
        for fecha in fixture:
            partidos_de_local += len(filter(lambda partido: partido[0] == equipo, fecha))
            partidos_de_visitante += len(filter(lambda partido: partido[1] == equipo, fecha))
        if not (partidos_de_local == 10 and partidos_de_visitante == 9 or partidos_de_local == 9 and partidos_de_visitante == 10):
            aptitud += 1

    # Restricción: Los equipos deben alternar de localía fecha tras fecha
    # AGREGAR ITERAR PARTIDOS DE LA FECHA
    for i in range(len(fixture) - 1):
        for equipo in equipos.keys():
            if (fixture[i][0][0] == equipo and fixture[i + 1][0][0] == equipo) or (
                fixture[i][0][1] == equipo and fixture[i + 1][0][1] == equipo
            ):
                aptitud += 1

    # Restricción: Por cada fecha debe haber 2 partidos el viernes, 3 el sábado, 3 el domingo y 2 el lunes
    conteo_dias = {"viernes": 0, "sábado": 0, "domingo": 0, "lunes": 0}
    for fecha in fixture:
        for partido in fecha:
            dia = [dia for dia, indice in dias.items() if indice == partido[2]][0]
            conteo_dias[dia] += 1
        if (
            conteo_dias["viernes"] != 2
            or conteo_dias["sábado"] != 3
            or conteo_dias["domingo"] != 3
            or conteo_dias["lunes"] != 2
        ):
            aptitud += 1

    # Restricción: River y Boca deben jugar todos sus partidos los días domingo
    for fecha in fixture:
        for partido in fecha:
            if partido[0] in ["river", "boca"] or partido[1] in ["river", "boca"]:
                if partido[2] != dias["domingo"]:
                    aptitud += 1

    # Restricción: El partido entre River y Boca se debe jugar en la fecha 10
    # NO ES NECESARIO QUE SEA EL 1RO DE LA FECHA
    if fixture[9][0][0] not in ["river", "boca"] or fixture[9][0][1] not in [
        "river",
        "boca",
    ]:
        aptitud += 1

    # Restricción: Los equipos que son clásicos no pueden jugar de local el mismo día
    # REHACER
    for fecha in fixture:
        for partido in fecha:
            if (partido[0], partido[1]) in partidos_clasicos or (
                partido[1],
                partido[0],
            ) in partidos_clasicos:
                if partido[0] in equipos_grandes and partido[1] in equipos_grandes:
                    if partido[2] == dias["domingo"]:
                        aptitud += 1

    # Restricción: Por cada fecha, el día sábado debe haber, como mínimo, un partido que involucre a un equipo grande
    equipos_sabado = []
    for fecha in fixture:
        for partido in fecha:
            if partido[2] == dias["sábado"]:
                equipos_sabado.extend(partido[:2])
        if not any(equipo in equipos_grandes for equipo in equipos_sabado):
            aptitud += 1

    # Restricción: Por cada fecha, el día domingo debe haber, como mínimo, dos partidos que involucren a un equipo grande
    # HAY MÁS EQUIPOS GRANDES
    equipos_domingo = []
    for fecha in fixture:
        for partido in fecha:
            if partido[2] == dias["domingo"]:
                equipos_domingo.extend(partido[:2])
    if equipos_domingo.count("river") + equipos_domingo.count("boca") < 2:
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
