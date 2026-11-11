# -*- coding: utf-8 -*-
"""
Taller 1 - Sistemas Distribuidos Modernos
Implementacion de Capa de Coordinacion (Algoritmo del Maton / Bully)
y Resolucion de Conflictos con Relojes Logicos de Lamport y Vectores de Version.
"""

NODOS = {
    1: "100.124.175.89",
    2: "100.118.94.6",
    3: "100.98.174.25",
    4: "100.72.188.70"
}

class RelojLamport:
    def __init__(self, node_id):
        self.node_id = node_id
        self.timestamp = 0
        self.vector = {n: 0 for n in NODOS}

    def tick(self):
        self.timestamp += 1
        self.vector[self.node_id] += 1
        return self.timestamp, dict(self.vector)

    def actualizar(self, otro_ts, otro_vector):
        self.timestamp = max(self.timestamp, otro_ts) + 1
        for k, v in otro_vector.items():
            self.vector[k] = max(self.vector.get(k, 0), v)
        self.vector[self.node_id] += 1

def son_concurrentes(v1, v2):
    menor_o_igual_1 = all(v1[k] <= v2[k] for k in v1)
    menor_o_igual_2 = all(v2[k] <= v1[k] for k in v1)
    return not (menor_o_igual_1 or menor_o_igual_2)

def resolver_conflicto_lamport(escritura_a, escritura_b):
    """
    Regla documentada (Seccion 1): Gana la escritura con mayor marca de Lamport.
    En caso de empate exacto, gana el nodo con identificador numerico menor.
    """
    if escritura_a["lamport_ts"] != escritura_b["lamport_ts"]:
        ganador = escritura_a if escritura_a["lamport_ts"] > escritura_b["lamport_ts"] else escritura_b
    else:
        ganador = escritura_a if escritura_a["node_id"] < escritura_b["node_id"] else escritura_b
    return ganador

class NodoBully:
    def __init__(self, node_id, nodos_activos):
        self.node_id = node_id
        self.nodos_activos = nodos_activos
        self.estado = "SEGUIDOR"
        self.lider_actual = None
        self.reloj = RelojLamport(node_id)

    def iniciar_eleccion(self):
        self.estado = "CANDIDATO"
        superiores = [n for n in self.nodos_activos if n > self.node_id]
        if not superiores:
            self.estado = "LIDER"
            self.lider_actual = self.node_id
            return self.node_id
        else:
            nuevo_lider = max(superiores)
            self.estado = "SEGUIDOR"
            self.lider_actual = nuevo_lider
            return nuevo_lider

if __name__ == "__main__":
    # Simulacion de verificacion de eleccion y resolucion de colision durante particion
    nodo1 = NodoBully(1, [1, 3, 4])
    nodo4 = NodoBully(4, [3, 4]) # Nodo 1 aislado
    print(f"[Bully] Lider elegido tras aislar Nodo 1: Nodo {nodo4.iniciar_eleccion()} ({NODOS[4]})")

    ts1, vec1 = nodo1.reloj.tick()
    ts4, vec4 = nodo4.reloj.tick()
    op_aislada = {"node_id": 1, "lamport_ts": ts1, "vector": vec1, "cpu": 1.4, "mem_mb": 382}
    op_mayoria = {"node_id": 4, "lamport_ts": ts4, "vector": vec4, "cpu": 2.7, "mem_mb": 524}

    if son_concurrentes(op_aislada["vector"], op_mayoria["vector"]):
        ganadora = resolver_conflicto_lamport(op_aislada, op_mayoria)
        print(f"[Conflicto Detectado] Concurrencia en vectores. Gana operacion del Nodo {ganadora['node_id']} con Lamport={ganadora['lamport_ts']}")
