# Spaceship Python Game

## Desenvolupadors

- [Marco Fernández](https://github.com/Treep035)
- [Joaquin Guzmán](https://github.com/joacoguzmanz)

### Demo
- [Enllaç a la demostració del joc](https://www.loom.com/share/9167af033edd4d52ac262dc66fbe676a?sid=03845b49-ab7e-420b-a675-03683feb1a63)

---

## Ampliacions

### 1. Sistema de Puntuació
Hem implementat un sistema de puntuació incrementant la puntuació del jugador cada vegada que esquiva o destrueix un obstacle. En el codi, la variable `score` s'incrementa:
- A la classe `Obstacle`, quan un obstacle es mou fora del costat esquerre de la pantalla.
- Quan una bala col·lideix amb un obstacle (utilitzant la detecció de col·lisions amb `pygame.sprite.groupcollide`).

### 2. Dificultat Incremental
Per augmentar progressivament el repte, el joc incrementa el `difficulty_level` cada 15 segons. Això afecta el joc de la següent manera:
- Augmentant la velocitat dels obstacles (utilitzant `random.randint(3 + difficulty_level, 7 + difficulty_level)` a la classe `Obstacle`).
- Reduint l'interval d'aparició dels obstacles (`spawn_interval` es redueix), de manera que apareixen més sovint a mesura que avança el temps.

### 3. Sistema de Vides
El sistema de vides permet que el jugador pugui rebre diversos impactes abans que el joc acabi. La implementació inclou:
- Inicialitzar una variable `lives` (configurada a 3).
- Reduir `lives` en un cada vegada que el jugador col·lisiona amb un obstacle.
- Restablir la posició del jugador (i eliminar obstacles) si li queden vides; en cas contrari, el joc entra en estat de Game Over.

### 4. Menú d'Inici i Reinici
El joc disposa d'un menú d'inici i una pantalla de Game Over:
- **Menú d'Inici:** La funció `show_menu()` mostra una pantalla d'introducció i espera que el jugador premi la barra d'espai per començar.
- **Pantalla de Game Over:** La funció `show_game_over()` mostra la puntuació final i la puntuació més alta, i espera que es premi una tecla per reiniciar el joc.

### 5. Efectes de So i Música de Fons
Per millorar l'experiència del joc, s'han afegit elements d'àudio:
- **Música de fons:** Es carrega amb `pygame.mixer.music.load` i es reprodueix en bucle, establint un ambient sonor continu.
- **Efectes de so:** Sons específics per als trets (`SHOOT_SOUND`) i explosions (`EXPLODE_SOUND`) es reprodueixen durant esdeveniments del joc, com disparar o col·lidir amb obstacles.

### 8. Pantalla de Pausa
S'ha afegit una funció de pausa que permet aturar temporalment el joc:
- Prement la tecla ESC, es commuta l'estat de pausa.
- Quan el joc està en pausa, es mostra un missatge ("PAUSA" amb instruccions per prémer ESC per continuar), i el joc no es reprèn fins que es prem ESC de nou.

### 9. Marcador de Rècords (High Scores)
Un sistema de puntuació màxima permet fer un seguiment i mostrar la millor puntuació aconseguida:
- El joc llegeix la puntuació més alta d'un fitxer (`highscore.txt`) en iniciar-se.
- Després de cada partida, si la puntuació actual supera la puntuació màxima emmagatzemada, el fitxer s'actualitza.
- La puntuació més alta es mostra a la pantalla durant el joc.

### 12. Sistema de Disparos
El sistema de trets afegeix un element d'acció extra al joc:
- S'ha implementat una classe `Bullet` per representar els projectils.
- Quan el jugador prem la barra d'espai (i el joc no està en pausa), es crea una bala a la posició actual del jugador.
- Les bales es desplacen per la pantalla i s'eliminen si surten dels límits, i també destrueixen obstacles quan col·lideixen amb ells.

