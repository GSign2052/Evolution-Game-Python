import pygame
import random
import math
import logging

# ===============================
# KONSTANTEN UND EINSTELLUNGEN
# ===============================

# Fenstergröße
WINDOW_WIDTH = 1600
WINDOW_HEIGHT = 1000

# Spielparameter
FPS = 30

# Farben
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
ORANGE = ( 214, 151, 69)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)
TRANSPARENT_GRAY = (128, 128, 128, 150)

# Größe der Sprites
PLANT_SIZE = 20
PREY_SIZE = 38
PREDATOR_SIZE = 80
OBSTACLE_SIZE = 50

# Anzahl der Anfangsobjekte
NUM_PLANTS = 500
NUM_PREYS = 20
MIN_PREDATORS = 5
NUM_OBSTACLES = 30

# Maximale Anzahl an Pflanzen
MAX_PLANTS = 500

# Lebenszeiten in Millisekunden
PREY_LIFETIME = 100000
PREDATOR_LIFETIME = 200000

# Fortpflanzungsbedingungen

PLANTS_EATEN_TO_REPRODUCE = 8
PREYS_EATEN_TO_REPRODUCE = 5

# Sichtfeld
SIGHT_RANGE = 200

# Minimale Anzahl an Beute
MIN_PREYS = 1

# Wachstumsrate
PLANT_GROWTH_INTERVAL = 0.001  # Zeitintervall für das Wachstum in Millisekunden

# Bewegungsparameter
PREY_SPEED = 1.2
PREDATOR_SPEED = 1.4
RANDOM_MOVEMENT_INTERVAL = 2000

# Ausdauerparameter
SPRINT_SPEED_MULTIPLIER = 3
SPRINT_DURATION = 2000  # Dauer des Sprints in Millisekunden
COOLDOWN_DURATION = 6000  # Cooldown-Zeit in Millisekunden
# ===============================
# RESTART BUTTON
# ===============================
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 30
BUTTON_COLOR = WHITE
BUTTON_HOVER_COLOR = (200, 200, 200)
BUTTON_TEXT_COLOR = BLACK
BUTTON_FONT = 'Arial'

# ===============================
# LOGGING EINRICHTEN
# ===============================
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# ===============================
# SPIELKLASSEN
# ===============================

class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, size, sight_range, life_time, speed):
        super().__init__()
        self.image_path = image_path
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (size, size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.size = size
        self.sight_range = sight_range
        self.life_time = life_time
        self.base_speed = speed
        self.speed = speed
        self.timer = pygame.time.get_ticks()
        self.last_food_time = pygame.time.get_ticks()
        self.last_random_movement_time = pygame.time.get_ticks()
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()

        # Ausdauerparameter
        self.sprint_start_time = None
        self.cooldown_end_time = 0
        self.is_sprinting = False

    def update(self):
        if pygame.time.get_ticks() - self.timer > self.life_time:
            logging.info(f"{self.__class__.__name__} hat seine Lebenszeit überschritten und wird entfernt.")
            self.kill()

        self.handle_sprint()
        self.wrap_around_screen()
        self.random_movement()
        self.rotate_image()

    def handle_sprint(self):
        current_time = pygame.time.get_ticks()
        if self.is_sprinting:
            if current_time - self.sprint_start_time > SPRINT_DURATION:
                self.is_sprinting = False
                self.cooldown_end_time = current_time + COOLDOWN_DURATION
            self.speed = self.base_speed * SPRINT_SPEED_MULTIPLIER
        else:
            if current_time < self.cooldown_end_time:
                self.speed = self.base_speed
            else:
                self.speed = self.base_speed

    def start_sprint(self):
        if not self.is_sprinting and pygame.time.get_ticks() > self.cooldown_end_time:
            self.is_sprinting = True
            self.sprint_start_time = pygame.time.get_ticks()

    def detect_objects(self, objects):
        detected = []
        for obj in objects:
            if self.get_distance(obj) < self.sight_range:
                detected.append(obj)
        return detected

    def get_distance(self, obj):
        return math.hypot(self.rect.centerx - obj.rect.centerx, self.rect.centery - obj.rect.centery)

    def wrap_around_screen(self):
        if self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = WINDOW_HEIGHT

    def random_movement(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_random_movement_time > RANDOM_MOVEMENT_INTERVAL:
            self.last_random_movement_time = current_time
            self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def rotate_image(self):
        angle = self.direction.angle_to(pygame.Vector2(0, -1))
        self.image = pygame.transform.rotate(pygame.image.load(self.image_path).convert_alpha(), angle)
        self.image = pygame.transform.scale(self.image, (self.size, self.size))

class Prey(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, 'images/prey.png', PREY_SIZE, SIGHT_RANGE, PREY_LIFETIME, PREY_SPEED)
        self.plants_eaten = 0

    def update(self):
        super().update()
        self.move()
        self.search_for_food()
        self.avoid_obstacles()

    def move(self):
        predators_in_range = self.detect_objects(predators)
        if predators_in_range:
            self.start_sprint()  # Beginne Sprinten, wenn ein Jäger in der Nähe ist
            closest_predator = min(predators_in_range, key=lambda p: self.get_distance(p))
            direction_x = self.rect.centerx - closest_predator.rect.centerx
            direction_y = self.rect.centery - closest_predator.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.direction = pygame.Vector2(direction_x, direction_y)
                self.rect.x += self.direction.x * self.speed
                self.rect.y += self.direction.y * self.speed
        else:
            self.speed = PREY_SPEED  # Zurück zur normalen Geschwindigkeit, wenn kein Jäger in der Nähe ist
            plants_in_range = self.detect_objects(plants)
            if plants_in_range:
                closest_plant = min(plants_in_range, key=lambda p: self.get_distance(p))
                direction_x = closest_plant.rect.centerx - self.rect.centerx
                direction_y = closest_plant.rect.centery - self.rect.centery
                distance = math.hypot(direction_x, direction_y)
                if distance > 0:
                    direction_x /= distance
                    direction_y /= distance
                    self.direction = pygame.Vector2(direction_x, direction_y)
                    self.rect.x += self.direction.x * self.speed
                    self.rect.y += self.direction.y * self.speed

        self.avoid_overlap(preys)

    def search_for_food(self):
        if plants:
            plants_in_range = self.detect_objects(plants)
            if plants_in_range:
                closest_plant = min(plants_in_range, key=lambda p: self.get_distance(p))
                if self.get_distance(closest_plant) < self.size:
                    plants.remove(closest_plant)
                    all_sprites.remove(closest_plant)
                    self.plants_eaten += 1
                    self.last_food_time = pygame.time.get_ticks()

                    if self.plants_eaten >= PLANTS_EATEN_TO_REPRODUCE:
                        self.plants_eaten = 0
                        self.reproduce()

    def reproduce(self):
        new_prey = Prey(self.rect.x + random.randint(-20, 20), self.rect.y + random.randint(-20, 20))
        preys.add(new_prey)
        all_sprites.add(new_prey)
        logging.info(f"Neue Beute bei ({new_prey.rect.x}, {new_prey.rect.y}) erzeugt.")

    def avoid_obstacles(self):
        obstacles_in_range = self.detect_objects(obstacles)
        if obstacles_in_range:
            closest_obstacle = min(obstacles_in_range, key=lambda o: self.get_distance(o))
            direction_x = self.rect.centerx - closest_obstacle.rect.centerx
            direction_y = self.rect.centery - closest_obstacle.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.rect.x += direction_x * PREY_SPEED
                self.rect.y += direction_y * PREY_SPEED

    def avoid_overlap(self, group):
        for sprite in group:
            if sprite != self and pygame.sprite.collide_rect(self, sprite):
                direction_x = self.rect.centerx - sprite.rect.centerx
                direction_y = self.rect.centery - sprite.rect.centery
                distance = math.hypot(direction_x, direction_y)
                if distance > 0:
                    direction_x /= distance
                    direction_y /= distance
                    self.rect.x += direction_x * PREY_SPEED
                    self.rect.y += direction_y * PREY_SPEED

class Predator(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, 'images/predator.png', PREDATOR_SIZE, SIGHT_RANGE, PREDATOR_LIFETIME, PREDATOR_SPEED)
        self.preys_eaten = 0

    def update(self):
        super().update()
        self.move()
        self.search_for_food()
        self.avoid_obstacles()

    def move(self):
        preys_in_range = self.detect_objects(preys)
        if preys_in_range:
            self.start_sprint()  # Beginne Sprinten, wenn Beute in der Nähe ist
            closest_prey = min(preys_in_range, key=lambda p: self.get_distance(p))
            direction_x = closest_prey.rect.centerx - self.rect.centerx
            direction_y = closest_prey.rect.centery - self.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.direction = pygame.Vector2(direction_x, direction_y)
                self.rect.x += self.direction.x * self.speed
                self.rect.y += self.direction.y * self.speed
        else:
            self.speed = PREDATOR_SPEED  # Zurück zur normalen Geschwindigkeit, wenn keine Beute in der Nähe ist
        self.avoid_overlap(predators)

    def search_for_food(self):
        if preys:
            preys_in_range = self.detect_objects(preys)
            if preys_in_range:
                closest_prey = min(preys_in_range, key=lambda p: self.get_distance(p))
                if self.get_distance(closest_prey) < self.size:
                    preys.remove(closest_prey)
                    all_sprites.remove(closest_prey)
                    self.preys_eaten += 1
                    self.last_food_time = pygame.time.get_ticks()

                    if self.preys_eaten >= PREYS_EATEN_TO_REPRODUCE:
                        self.preys_eaten = 0
                        self.reproduce()

    def reproduce(self):
        new_predator = Predator(self.rect.x + random.randint(-20, 20), self.rect.y + random.randint(-20, 20))
        predators.add(new_predator)
        all_sprites.add(new_predator)
        logging.info(f"Neuer Jäger bei ({new_predator.rect.x}, {new_predator.rect.y}) erzeugt.")

    def avoid_obstacles(self):
        obstacles_in_range = self.detect_objects(obstacles)
        if obstacles_in_range:
            closest_obstacle = min(obstacles_in_range, key=lambda o: self.get_distance(o))
            direction_x = self.rect.centerx - closest_obstacle.rect.centerx
            direction_y = self.rect.centery - closest_obstacle.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.rect.x += direction_x * PREDATOR_SPEED
                self.rect.y += direction_y * PREDATOR_SPEED

    def avoid_overlap(self, group):
        for sprite in group:
            if sprite != self and pygame.sprite.collide_rect(self, sprite):
                direction_x = self.rect.centerx - sprite.rect.centerx
                direction_y = self.rect.centery - sprite.rect.centery
                distance = math.hypot(direction_x, direction_y)
                if distance > 0:
                    direction_x /= distance
                    direction_y /= distance
                    self.rect.x += direction_x * PREDATOR_SPEED
                    self.rect.y += direction_y * PREDATOR_SPEED

class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y, plant_image):
        super().__init__()
        self.image = pygame.image.load(plant_image).convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('images/obstacle.png').convert_alpha()  # Bild für das Hindernis laden
        self.image = pygame.transform.scale(self.image, (OBSTACLE_SIZE, OBSTACLE_SIZE))  # Größe des Hindernisses anpassen
        self.rect = self.image.get_rect(topleft=(x, y))


# ===============================
# SPIEL INIT
# ===============================
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ökosystem Simulation")
clock = pygame.time.Clock()

# Sprite-Gruppen
all_sprites = pygame.sprite.Group()
plants = pygame.sprite.Group()
preys = pygame.sprite.Group()
predators = pygame.sprite.Group()
obstacles = pygame.sprite.Group()

# Pflanzenbilder
plant_images = [
    'images/plant1.png',
    'images/plant2.png',
    'images/plant3.png'
]

# Initialisierung der Pflanzen
def create_plant():
    x = random.randint(0, WINDOW_WIDTH - PLANT_SIZE)
    y = random.randint(0, WINDOW_HEIGHT - PLANT_SIZE)
    plant_image = random.choice(plant_images)
    plant = Plant(x, y, plant_image)
    plants.add(plant)
    all_sprites.add(plant)

for _ in range(NUM_PLANTS):
    create_plant()

# Initialisierung der Beute
for _ in range(NUM_PREYS):
    x = random.randint(0, WINDOW_WIDTH - PREY_SIZE)
    y = random.randint(0, WINDOW_HEIGHT - PREY_SIZE)
    prey = Prey(x, y)
    preys.add(prey)
    all_sprites.add(prey)

# Initialisierung der Jäger
for _ in range(MIN_PREDATORS):
    x = random.randint(0, WINDOW_WIDTH - PREDATOR_SIZE)
    y = random.randint(0, WINDOW_HEIGHT - PREDATOR_SIZE)
    predator = Predator(x, y)
    predators.add(predator)
    all_sprites.add(predator)

# Initialisierung der Hindernisse
for _ in range(NUM_OBSTACLES):
    x = random.randint(0, WINDOW_WIDTH - OBSTACLE_SIZE)
    y = random.randint(0, WINDOW_HEIGHT - OBSTACLE_SIZE)
    obstacle = Obstacle(x, y)
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

# ===============================
# FUNKTIONEN ZUM ZEICHNEN DER ÜBERSICHT
# ===============================
def draw_stats(screen, start_time):
    font = pygame.font.SysFont('Arial', 30)
    elapsed_time = pygame.time.get_ticks() - start_time
    seconds = elapsed_time // 1000
    minutes = seconds // 60
    seconds %= 60

    overlay = pygame.Surface((160, 140), pygame.SRCALPHA)
    overlay.fill(TRANSPARENT_GRAY)
    screen.blit(overlay, (10, 10))

    text = [
        f"Zeit: {minutes:02}:{seconds:02}",
        f"Pflanzen: {len(plants)}",
        f"Beute: {len(preys)}",
        f"Jäger: {len(predators)}"
    ]

    for i, line in enumerate(text):
        label = font.render(line, True, BLACK)
        screen.blit(label, (20, 20 + i * 30))

# Funktion zum Zeichnen des Neustart-Buttons
def draw_button(screen, text, x, y, width, height, color, hover_color, text_color, font_name, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))

    font = pygame.font.SysFont(font_name, 30)
    text_surface = font.render(text, True, text_color)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def restart_game():
    global all_sprites, plants, preys, predators, obstacles, start_time

    all_sprites.empty()
    plants.empty()
    preys.empty()
    predators.empty()
    obstacles.empty()

    for _ in range(NUM_PLANTS):
        create_plant()

    for _ in range(NUM_PREYS):
        x = random.randint(0, WINDOW_WIDTH - PREY_SIZE)
        y = random.randint(0, WINDOW_HEIGHT - PREY_SIZE)
        prey = Prey(x, y)
        preys.add(prey)
        all_sprites.add(prey)

    for _ in range(MIN_PREDATORS):
        x = random.randint(0, WINDOW_WIDTH - PREDATOR_SIZE)
        y = random.randint(0, WINDOW_HEIGHT - PREDATOR_SIZE)
        predator = Predator(x, y)
        predators.add(predator)
        all_sprites.add(predator)

    for _ in range(NUM_OBSTACLES):
        x = random.randint(0, WINDOW_WIDTH - OBSTACLE_SIZE)
        y = random.randint(0, WINDOW_HEIGHT - OBSTACLE_SIZE)
        obstacle = Obstacle(x, y)
        obstacles.add(obstacle)

    start_time = pygame.time.get_ticks()

# ===============================
# SPIELSCHLEIFE
# ===============================
running = True
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # Erzeuge neue Pflanzen, falls nötig
    if len(plants) < MAX_PLANTS:
        if pygame.time.get_ticks() % PLANT_GROWTH_INTERVAL < FPS:
            create_plant()

    screen.fill(ORANGE)
    all_sprites.draw(screen)
    draw_stats(screen, start_time)
    draw_button(screen, "Restart", WINDOW_WIDTH - BUTTON_WIDTH - 10, 10, BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, BUTTON_TEXT_COLOR, BUTTON_FONT, restart_game)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
