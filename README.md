# ProyectCheckers
Proyecto de damas, donde consiste en dos jugadores
1. Piezas blancas
2. Piezas Rojas
El objetivo es capturar todas las piezas del oponente o bloquearlas para que no puedan realizar movimientos,
el jugador ganador es aquel que logre comer todas las piezas de nuestro enemigo.

Requerimientos del juego:
    instalar pygame -pip install pygame

Funcionamiento principal del codigo:
    Board : gestiona la configuración del tablero de juego, que incluye las piezas en sus posiciones iniciales y la visualización del tablero, también se encarga de atualizar los movimientos en el tablero

    Game: controla la lógica del juego, el manejo de turnos entre los jugadores y la determinación de cuándo termina el juego. Este componente utiliza el Singleton para asegurar que solo existe una instancia del juego en ejecución.

    Piece: define las características de las piezas, las posiciones en el tablero y si una pieza ha sido coronada como rey.

    MoveManager: función para los movimientos de piezas, validando los movimientos legales y ejecutando los movimientos en el tablero. 

    King Decorator: modifica las piezas regulares a reyes, en su caso dando capacidades de movimiento diferentes. Este patrón de diseño permite añadir dinámicamente nuevas funcionalidades.


    