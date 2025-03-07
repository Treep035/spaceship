import pygame
import random
import sys

# ========================
# Configuració inicial
# ========================
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)

# Inicialitzar Pygame i la finestra
pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("resources/sounds/main.mp3")  # Cambia la ruta si es necesario
pygame.mixer.music.set_volume(0.5)  # Ajusta el volumen de la música (0.0 a 1.0)
pygame.mixer.music.play(-1, 0.0)

EXPLOSION_IMAGE = pygame.image.load("resources/images/explode.png")  # Asegúrate de que esta imagen esté en la carpeta
EXPLOSION_IMAGE = pygame.transform.scale(EXPLOSION_IMAGE, (50, 50))

SHOOT_SOUND = pygame.mixer.Sound("resources/sounds/shoot.mp3")
EXPLODE_SOUND = pygame.mixer.Sound("resources/sounds/explode.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SpaceShip Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# ========================
# Variables Globals del Joc
# ========================
score = 0
difficulty_level = 1
lives = 3
last_difficulty_update_time = pygame.time.get_ticks()
spawn_interval = 1500
ADD_OBSTACLE = pygame.USEREVENT + 1

# ========================
# High Score Functions
# ========================
def load_high_score():
    try:
        with open("highscore.txt", "r") as f:
            return int(f.read().strip())
    except:
        return 0

def save_high_score(score_value):
    with open("highscore.txt", "w") as f:
        f.write(str(score_value))

high_score = load_high_score()

# ========================
# Funcions Auxiliars
# ========================

def draw_text(surface, text, font, color, x, y):
    """Dibuixa un text a la pantalla."""
    text_obj = font.render(text, True, color)
    surface.blit(text_obj, (x, y))

# ========================
# Classes del Joc
# ========================

class Player(pygame.sprite.Sprite):
    """Classe per al jugador."""
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("resources/images/spaceship.png")  # Imagen original de la nave
        self.image = pygame.transform.scale(self.image, (50, 50))  # Ajusta el tamaño si es necesario
        self.rect = self.image.get_rect()
        self.rect.center = (100, HEIGHT // 2)
        self.speed = 5

    def update(self):
        """Actualitza la posició del jugador segons les tecles premudes (WASD)."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed

        # Evitar que el jugador surti de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

    def trigger_explosion(self):
        """Crear la explosió a la posició de la nau."""
        explosion = Explosion(self.rect.center)  # Posicionar la explosión en el centro de la nave
        all_sprites.add(explosion)  # Añadir la explosión al grupo de sprites


class Obstacle(pygame.sprite.Sprite):
    """Classe per als obstacles."""
    def __init__(self):
        super().__init__()
        # Crear un obstacle amb dimensions aleatòries
        self.image = pygame.image.load("resources/images/meteorite.png")  # Cambia "obstaculo_imagen.png" por el nombre de tu archivo de imagen
        self.image = pygame.transform.scale(self.image, (random.randint(20, 100), random.randint(20, 100)))  # Ajusta el tamaño aleatorio
        self.rect = self.image.get_rect()
        # Posició inicial: fora de la pantalla per la dreta
        self.rect.x = WIDTH + random.randint(10, 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = random.randint(3 + difficulty_level, 7 + difficulty_level)

    def update(self):
        """Mou l'obstacle cap a l'esquerra i, si surt de la pantalla, s'incrementa la puntuació i s'elimina."""
        global score
        self.rect.x -= self.speed
        if self.rect.right < 0:
            score += 1
            self.kill()

class Bullet(pygame.sprite.Sprite):
    """Classe per als projectils disparats pel jugador."""
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((10, 4))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.speed = 10

    def update(self):
        """Mou el projectil cap a la dreta i el destrueix si surt de la pantalla."""
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    """Classe per a la explosió."""
    def __init__(self, pos):
        super().__init__()
        self.image = EXPLOSION_IMAGE  # Imagen de la explosión
        self.rect = self.image.get_rect(center=pos)  # Centrar la explosión en la posición
        self.time_created = pygame.time.get_ticks()  # Almacenamos el tiempo de creación

    def update(self):
        """Destruir la explosión después de 0.5 segundos."""
        if pygame.time.get_ticks() - self.time_created > 500:  # 500 ms = 0.5 segundos
            self.kill()  # Eliminar la explosión del grupo de sprites


# ========================
# Funció per reinicialitzar el Joc
# ========================

def new_game():
    """Reinicialitza totes les variables i grups per començar una nova partida."""
    global score, difficulty_level, lives, last_difficulty_update_time, spawn_interval
    global all_sprites, obstacles, bullets, player
    score = 0
    difficulty_level = 1
    lives = 3
    last_difficulty_update_time = pygame.time.get_ticks()
    spawn_interval = 1500
    pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    player = Player()
    all_sprites.add(player)

# ========================
# Funció per mostrar el menú principal
# ========================

def show_menu():
    """Mostra la pantalla de menú d'inici i espera que l'usuari premi alguna tecla per començar."""
    # Cargar la imagen de fondo
    background = pygame.image.load("resources/images/background.jpg")  # Cambia la ruta si es necesario
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))  # Ajustar el tamaño

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Solo iniciar el juego si se presiona SPACE
                    waiting = False

        # Dibuixar el fondo
        screen.blit(background, (0, 0))  # Dibuja el fondo en la pantalla

        # Dibuixar el text del menú
        draw_text(screen, "SpaceShip", font, WHITE, 325, 200)
        draw_text(screen, "Press", font, WHITE, 270, 250)
        draw_text(screen, "SPACE", font, RED, 345, 250)
        draw_text(screen, "to start", font, WHITE, 440, 250)

        draw_text(screen, "TO MOVE USE", font, WHITE, 100, 300)
        draw_text(screen, "TO PAUSE", font, WHITE, 350, 300)
        draw_text(screen, "TO SHOOT", font, WHITE, 600, 300)
        draw_text(screen, "   W", font, WHITE, 100, 330)
        draw_text(screen, "        ESC", font, WHITE, 350, 330)
        draw_text(screen, "      SPACE", font, WHITE, 600, 330)
        draw_text(screen, "A   S   D", font, WHITE, 100, 360)

        pygame.display.flip()

# Variable para gestionar la pausa
paused = False

# ========================
# Funció per mostrar la pantalla de Pausa
# ========================
def show_pause():
    """Mostra la pantalla de pausa fins que el jugador premi l'ESCAPE."""
    background = pygame.Surface((WIDTH, HEIGHT))
    background.fill(WHITE)  # Fondo blanco

    draw_text(screen, "PAUSA", font, WHITE, WIDTH // 2 - 60, HEIGHT // 2 - 30)
    draw_text(screen, "Press ESC to continue", font, WHITE, WIDTH // 2 - 130, HEIGHT // 2 + 10)
    pygame.display.flip()

    # Esperar que el jugador presione ESCAPE para continuar
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

# ========================
# Funció per executar la partida
# ========================

def game_loop():
    """Executa el bucle principal de la partida."""
    global score, difficulty_level, last_difficulty_update_time, spawn_interval, lives
    new_game()
    game_state = "playing"
    running = True
    paused = False  # Variable para controlar la pausa

    background = pygame.image.load("resources/images/background.jpg")  # Cambia la ruta si es necesario
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    while running and game_state == "playing":
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == ADD_OBSTACLE:
                obstacle = Obstacle()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    paused = not paused  # Alterna el estado de pausa
                if event.key == pygame.K_SPACE and not paused:
                    # Crear i afegir un projectil a partir de la posició del jugador
                    bullet = Bullet(player.rect.center)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    SHOOT_SOUND.play()

        # Si el juego está en pausa, mostrar la pantalla de pausa y no actualizar nada más
        if paused:
            draw_text(screen, "PAUSE", font, WHITE, WIDTH // 2 - 60, HEIGHT // 2 - 30)
            draw_text(screen, "Press ESC to continue", font, WHITE, WIDTH // 2 - 130, HEIGHT // 2 + 10)
            pygame.display.flip()
            continue

        # Incrementar la dificultat cada 15 segons
        current_time = pygame.time.get_ticks()
        if current_time - last_difficulty_update_time >= 15000:
            difficulty_level += 1
            last_difficulty_update_time = current_time
            spawn_interval = max(500, 1500 - difficulty_level * 100)
            pygame.time.set_timer(ADD_OBSTACLE, spawn_interval)

        # Actualitzar els sprites
        all_sprites.update()

        # Comprovar col·lisions entre projectils i obstacles
        hits = pygame.sprite.groupcollide(bullets, obstacles, True, True)
        for hit in hits:
            score += 1

        # Comprovar col·lisions entre el jugador i els obstacles
        if pygame.sprite.spritecollideany(player, obstacles):
            lives -= 1
            EXPLODE_SOUND.play()
            player.trigger_explosion()  # Crear l'explosió en la posició de la nau
            if lives > 0:
                # Reinicialitzar la posició del jugador i esborrar els obstacles
                player.rect.center = (100, HEIGHT // 2)
                for obs in obstacles:
                    obs.kill()
            else:
                game_state = "game_over"

        # Dibuixar la escena
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        score_text = font.render("Punctuation: " + str(score), True, WHITE)
        difficulty_text = font.render("Difficulty: " + str(difficulty_level), True, WHITE)
        lives_text = font.render("Lives: " + str(lives), True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(difficulty_text, (10, 40))
        screen.blit(lives_text, (10, 70))
        pygame.display.flip()
    return score


# ========================
# Funció per mostrar la pantalla de Game Over
# ========================

def show_game_over(final_score):
    """Mostra la pantalla de Game Over amb la puntuació final i espera per reiniciar."""
    global high_score
    if final_score > high_score:
        high_score = final_score
        save_high_score(high_score)

    background = pygame.image.load("resources/images/background.jpg")  # Cambia la ruta si es necesario
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))

    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                waiting = False
        screen.blit(background, (0, 0))
        draw_text(screen, "Game Over!", font, RED, 350, 200)
        draw_text(screen, "Final score: " + str(final_score) + " points", font, WHITE, 320, 250)
        draw_text(screen, "High score: " + str(final_score) + " points", font, WHITE, 320, 280)
        draw_text(screen, "Press any key to restart", font, WHITE, 300, 300)
        pygame.display.flip()

# ========================
# Bucle principal del programa
# ========================

while True:
    show_menu()                   # Mostrar menú d'inici
    final_score = game_loop()       # Executar la partida
    show_game_over(final_score)     # Mostrar pantalla de Game Over i esperar reinici
