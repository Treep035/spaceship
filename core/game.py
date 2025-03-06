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

SHOOT_SOUND = pygame.mixer.Sound("resources/sounds/shoot.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Joc Extensible - Ampliació 4: Menú, Reinici i Disparar")
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
        self.image = pygame.image.load("resources/images/spaceship.png")  # Cambia "jugador_imagen.png" por el nombre de tu archivo de imagen
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
                waiting = False

        # Dibuixar el fondo
        screen.blit(background, (0, 0))  # Dibuja el fondo en la pantalla

        # Dibuixar el text del menú
        draw_text(screen, "Joc Extensible", font, WHITE, 300, 200)
        draw_text(screen, "Prem qualsevol tecla per començar", font, WHITE, 220, 250)
        
        pygame.display.flip()


# ========================
# Funció per executar la partida
# ========================

def game_loop():
    """Executa el bucle principal de la partida."""
    global score, difficulty_level, last_difficulty_update_time, spawn_interval, lives
    new_game()
    game_state = "playing"
    running = True

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
                if event.key == pygame.K_SPACE:
                    # Crear i afegir un projectil a partir de la posició del jugador
                    bullet = Bullet(player.rect.center)
                    all_sprites.add(bullet)
                    bullets.add(bullet)

                    SHOOT_SOUND.play()
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
        score_text = font.render("Puntuació: " + str(score), True, WHITE)
        difficulty_text = font.render("Dificultat: " + str(difficulty_level), True, WHITE)
        lives_text = font.render("Vides: " + str(lives), True, WHITE)
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
        draw_text(screen, "Puntuació Final: " + str(final_score), font, BLACK, 320, 250)
        draw_text(screen, "Prem qualsevol tecla per reiniciar", font, BLACK, 250, 300)
        pygame.display.flip()

# ========================
# Bucle principal del programa
# ========================

while True:
    show_menu()                   # Mostrar menú d'inici
    final_score = game_loop()       # Executar la partida
    show_game_over(final_score)     # Mostrar pantalla de Game Over i esperar reinici
