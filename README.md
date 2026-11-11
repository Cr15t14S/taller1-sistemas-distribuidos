# Taller 1 — Coordinación y Datos del Sistema

**Universidad Distrital Francisco José de Caldas**  
**Facultad Tecnológica — Ingeniería en Telemática**  
**Asignatura:** Sistemas Distribuidos Modernos  
**Docente:** Msc. Ing. Óscar Gabriel Espejo Mojica  

## Integrantes del Equipo
* **Cristian Mauricio Salgado Romero** - 20262678041 (Nodo 1: 100.124.175.89)
* **Valentina Murcia Tapias** - 20262678026
* **Cristian Daniel Feo Patarroyo** - 20262678071 (Nodo 2: 100.118.94.6)
* **Natalia Herrera Gómez** - 20262678006 (Nodo 3: 100.98.174.25)
* **Ana Marcela Sánchez Escobar** - 20262678098 (Nodo 4: 100.72.188.70)

---

## 1. Arquitectura y Decisiones de Diseño

1. **Red Privada y Seguridad (E3):** Malla VPN sobre **Tailscale** conectando máquinas virtuales Ubuntu Server 26.04.1 LTS sin entorno gráfico. Autenticación SSH exclusivamente mediante clave pública (PasswordAuthentication no).
2. **Coordinación y Elección de Líder (E4):** Se seleccionó el **Algoritmo del Matón (Bully Algorithm - Garcia-Molina, 1982)** para la capa de coordinación por su convergencia determinista basada en IDs de nodo, complementado con el consenso nativo de MongoDB Replica Set para la alta disponibilidad de datos.
3. **Inventario Replicado y Modelo de Consistencia:** Clúster **MongoDB 7.0 (s-taller)** configurado como un Replica Set de 3 miembros votantes (Nodos 1, 3 y 4). Las lecturas y escrituras se dirigen al nodo PRIMARY exigiendo confirmación mayoritaria (Write Concern: majority).
4. **Detección y Resolución de Conflictos:** Uso de **Relojes Lógicos de Lamport**. Ante escrituras concurrentes durante una partición, gana la operación con mayor marca de tiempo (	imestamp) de Lamport; en caso de empate exacto, prevalece el nodo con el identificador numérico menor (
ode_id).

---

## 2. Estructura del Repositorio

\\\	ext
├── config/
│   ├── mongod_nodo1.conf              # Configuración de red Tailscale y replicación (Nodo 1)
│   ├── mongod_nodo3.conf              # Configuración de red Tailscale y replicación (Nodo 3)
│   └── mongod_nodo4.conf              # Configuración de red Tailscale y replicación (Nodo 4)
├── scripts/
│   ├── init_replicaset.js             # Inicialización del Replica Set rs-taller (3 miembros)
│   ├── aislar_nodo.sh                 # Simulación de partición de red con iptables (DROP en tailscale0)
│   └── reconectar_nodo.sh             # Restablecimiento de tráfico en interfaz tailscale0
├── logs/
│   ├── 01_eleccion_inicial_status.json # Registro E4: Nodo 1 elegido como PRIMARY inicial
│   ├── 02_particion_caida_lider.json   # Registro E4/E5: Caída de Nodo 1 y elección de Nodo 4 como PRIMARY
│   └── 03_reconexion_convergencia.json # Registro E5: Reintegración de Nodo 1 como SECONDARY (Convergencia)
├── .gitignore                         # Exclusión de llaves privadas (*.pem, *.key, .ssh/)
└── README.md                          # Documentación general del proyecto
\\\

---

## 3. Ejecución del Experimento de Partición (E5)

### Paso 1: Inicialización del Clúster
En el Nodo 1, ingresar a mongosh y ejecutar el script de configuración:
\\\ash
mongosh --file scripts/init_replicaset.js
\\\

### Paso 2: Provocar la Partición de Red (Aislar al Líder)
Ejecutar en el líder actual (Nodo 1) desde terminal local para bloquear paquetes entrantes y salientes por la interfaz 	ailscale0:
\\\ash
chmod +x scripts/aislar_nodo.sh
./scripts/aislar_nodo.sh
\\\
*Resultado:* El grupo mayoritario (Nodos 3 y 4) detecta la caída tras el electionTimeoutMillis (10s) y promueve automáticamente al **Nodo 4** como nuevo PRIMARY. El Nodo 1 aislado rechaza escrituras (WriteConcernFailed), priorizando **Consistencia (C)** sobre **Disponibilidad (A)** (Teorema CAP).

### Paso 3: Reconexión y Verificación de Convergencia
Restablecer la conectividad en el Nodo 1:
\\\ash
chmod +x scripts/reconectar_nodo.sh
./scripts/reconectar_nodo.sh
\\\
*Resultado:* El Nodo 1 detecta el término de elección superior (	erm: 2), cede su rol anterior y converge automáticamente al estado SECONDARY sincronizándose desde el Nodo 4 (100.72.188.70:27017).

---

## 4. Referencias y Bibliografía
* Garcia-Molina, H. (1982). *Elections in a Distributed Computing System*. IEEE Transactions on Computers, C-31(1).
* Fidge, C. J. (1988). *Timestamps in Message-Passing Systems That Preserve the Partial Ordering*.
* Mattern, F. (1989). *Virtual Time and Global States of Distributed Systems*.
* MongoDB Official Documentation v7.0 — *Replica Set Elections and Read/Write Concern*.
