# Registro de Métricas de Recursos durante el Experimento de Partición (Entregable E5)

Mediciones obtenidas mediante htop en los 3 miembros del Replica Set (rs-taller) antes del aislamiento, durante la partición con iptables y tras la reconexión y convergencia.

| Nodo | Métrica | 1. Antes de aplicar iptables | 2. Durante el aislamiento | 3. Después de reconectar (Convergencia) |
| :--- | :--- | :---: | :---: | :---: |
| *Nodo 1 (100.124.175.89)* (Líder inicial / Aislado) | *CPU (%)* | 1.4% | 1.4% | 1.2% |
| *Nodo 1 (100.124.175.89)* | *Memoria (MB)* | 574 M | 382 M | 542 M |
| *Nodo 3 (100.98.174.25)* (Secundario) | *CPU (%)* | 12.6% | 4.1% | 2.0% |
| *Nodo 3 (100.98.174.25)* | *Memoria (MB)* | 357 M | 534 M | 536 M |
| *Nodo 4 (100.72.188.70)* (Nuevo Líder tras caída) | *CPU (%)* | 5.6% | 2.7% | 4.1% |
| *Nodo 4 (100.72.188.70)* | *Memoria (MB)* | 356 M | 524 M | 529 M |
