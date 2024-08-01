import pygame
import random
import math
import logging

# ===============================
# KONSTANTEN UND EINSTELLUNGEN
# ===============================

# Fenstergröße
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Spielparameter
FPS = 60

# Farben
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
BLACK = (0, 0, 0)

# Größe der Sprites
PLANT_SIZE = 20
PREY_SIZE = 12
PREDATOR_SIZE = 16
OBSTACLE_SIZE = 30

# Anzahl der Anfangsobjekte
NUM_PLANTS = 500
NUM_PREYS = 10
MIN_PREDATORS = 1
NUM_OBSTACLES = 25

# Maximale Anzahl an Pflanzen
MAX_PLANTS = 500

# Lebenszeiten in Millisekunden
PREY_LIFETIME = 100000
PREDATOR_LIFETIME = 15000

# Fortpflanzungsbedingungen
PLANTS_EATEN_TO_REPRODUCE = 5
PREYS_EATEN_TO_REPRODUCE = 3

# Sichtfeld
SIGHT_RANGE = 150

# Minimale Anzahl an Beute
MIN_PREYS = 1

# Wachstumsrate
PLANT_GROWTH_INTERVAL = 1  # Zeitintervall für das Wachstum in Millisekunden

# Bewegungsparameter
PREY_SPEED = 2
PREDATOR_SPEED = 2.5
RANDOM_MOVEMENT_INTERVAL = 1000

# ===============================
# LOGGING EINRICHTEN
# ===============================
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# ===============================
# SPIELKLASSEN
# ===============================

class Creature(pygame.sprite.Sprite):
    def __init__(self, x, y, color, size, sight_range, life_time, speed):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.size = size
        self.sight_range = sight_range
        self.life_time = life_time
        self.speed = speed
        self.timer = pygame.time.get_ticks()
        self.last_food_time = pygame.time.get_ticks()
        self.last_random_movement_time = pygame.time.get_ticks()
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()

    def update(self):
        if pygame.time.get_ticks() - self.timer > self.life_time:
            logging.info(f"{self.__class__.__name__} hat seine Lebenszeit überschritten und wird entfernt.")
            self.kill()
        
        self.wrap_around_screen()
        self.random_movement()

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

class Prey(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, BLUE, PREY_SIZE, SIGHT_RANGE, PREY_LIFETIME, PREY_SPEED)
        self.plants_eaten = 0

    def update(self):
        super().update()
        self.move()
        self.search_for_food()
        self.avoid_obstacles()

    def move(self):
        predators_in_range = self.detect_objects(predators)
        if predators_in_range:
            closest_predator = min(predators_in_range, key=lambda p: self.get_distance(p))
            direction_x = self.rect.centerx - closest_predator.rect.centerx
            direction_y = self.rect.centery - closest_predator.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.direction = pygame.Vector2(direction_x, direction_y)
                self.rect.x += self.direction.x * PREY_SPEED
                self.rect.y += self.direction.y * PREY_SPEED
        else:
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
                    self.rect.x += self.direction.x * PREY_SPEED
                    self.rect.y += self.direction.y * PREY_SPEED

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
        super().__init__(x, y, RED, PREDATOR_SIZE, SIGHT_RANGE, PREDATOR_LIFETIME, PREDATOR_SPEED)
        self.preys_eaten = 0

    def update(self):
        super().update()
        self.move()
        self.search_for_food()
        self.avoid_obstacles()

    def move(self):
        preys_in_range = self.detect_objects(preys)
        if preys_in_range:
            closest_prey = min(preys_in_range, key=lambda p: self.get_distance(p))
            direction_x = closest_prey.rect.centerx - self.rect.centerx
            direction_y = closest_prey.rect.centery - self.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.direction = pygame.Vector2(direction_x, direction_y)
                self.rect.x += self.direction.x * PREDATOR_SPEED
                self.rect.y += self.direction.y * PREDATOR_SPEED
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
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(GRAY)
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
    font = pygame.font.SysFont(None, 30)
    elapsed_time = pygame.time.get_ticks() - start_time
    seconds = elapsed_time // 1000
    minutes = seconds // 60
    seconds %= 60

    text = [
        f"Zeit: {minutes:02}:{seconds:02}",
        f"Pflanzen: {len(plants)}",
        f"Beute: {len(preys)}",
        f"Jäger: {len(predators)}"
    ]

    for i, line in enumerate(text):
        label = font.render(line, True, BLACK)
        screen.blit(label, (10, 10 + i * 20))

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

    screen.fill(WHITE)
    all_sprites.draw(screen)
    draw_stats(screen, start_time)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
