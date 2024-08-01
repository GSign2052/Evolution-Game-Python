import pygame
import random
import math

# ===============================
# KONSTANTEN UND EINSTELLUNGEN
# ===============================

# Fenstergröße
WINDOW_WIDTH = 1200  # Breite des Spielbildschirms
WINDOW_HEIGHT = 800  # Höhe des Spielbildschirms

# Spielparameter
FPS = 30  # Frames pro Sekunde für die Spielaktualisierung

# Farben
WHITE = (255, 255, 255)  # Hintergrundfarbe
GREEN = (0, 255, 0)      # Farbe der Nahrung (Pflanzen)
BLUE = (0, 0, 255)       # Farbe der Beute
RED = (255, 0, 0)        # Farbe der Jäger
GRAY = (128, 128, 128)   # Farbe der Hindernisse

# Größe der Sprites
PLANT_SIZE = 8           # Größe der Pflanzen
PREY_SIZE = 12           # Größe der Beute
PREDATOR_SIZE = 16       # Größe der Jäger
OBSTACLE_SIZE = 20       # Größe der Hindernisse

# Anzahl der Anfangsobjekte
NUM_PLANTS = 500         # Anzahl der Pflanzen zu Spielbeginn
NUM_PREYS = 2           # Anzahl der Beute zu Spielbeginn
MIN_PREDATORS = 5        # Minimale Anzahl der Jäger im Spiel
NUM_OBSTACLES = 25       # Anzahl der Hindernisse zu Spielbeginn

# Maximale Anzahl an Pflanzen
MAX_PLANTS = 500         # Maximale Anzahl an Pflanzen im Spiel

# Lebenszeiten in Millisekunden
PREY_LIFETIME = 10000    # Lebenszeit der Beute (5 Sekunden)
PREDATOR_LIFETIME = 150000  # Lebenszeit der Jäger (10 Sekunden)

# Fortpflanzungsbedingungen
PLANTS_EATEN_TO_REPRODUCE = 8  # Anzahl der Pflanzen, die Beute essen muss, um sich fortzupflanzen
PREYS_EATEN_TO_REPRODUCE = 5   # Anzahl der Beute, die Jäger essen muss, um sich fortzupflanzen

# Sichtfeld
SIGHT_RANGE = 150        # Sichtfeld für Beute und Jäger

# Minimale Anzahl an Beute
MIN_PREYS = 1            # Mindestanzahl an Beute, um sicherzustellen, dass das Spiel nicht endet

# Wachstumsrate
PLANT_GROWTH_INTERVAL = 1000  # Zeit in Millisekunden, nach der eine Pflanze sich selbst reproduziert

# Bewegungsparameter
PREY_SPEED = 3           # Geschwindigkeit der Beute
PREDATOR_SPEED = 3.2       # Geschwindigkeit der Jäger
RANDOM_MOVEMENT_INTERVAL = 1000  # Zeit in Millisekunden für zufällige Bewegungen

# ===============================
# SPIELKLASSEN
# ===============================

class Creature(pygame.sprite.Sprite):
    """Basisklasse für alle Lebewesen im Spiel."""
    def __init__(self, x, y, color, size, sight_range, life_time, speed):
        super().__init__()
        self.image = pygame.Surface((size, size))
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.size = size
        self.sight_range = sight_range
        self.life_time = life_time
        self.speed = speed
        self.timer = pygame.time.get_ticks()  # Initialisiere Lebenszeit-Tracker
        self.last_food_time = pygame.time.get_ticks()  # Initialisiere Zeit für die letzte Nahrungsaufnahme
        self.last_random_movement_time = pygame.time.get_ticks()  # Initialisiere Zeit für die letzte zufällige Bewegung
        self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()  # Initiale Richtung

    def update(self):
        """Aktualisiere den Zustand des Lebewesens und überprüfe die Lebenszeit."""
        if pygame.time.get_ticks() - self.timer > self.life_time:
            self.kill()  # Entferne das Lebewesen, wenn die Lebenszeit abgelaufen ist

        self.wrap_around_screen()
        self.random_movement()

    def detect_objects(self, objects):
        """Erkenne Objekte im Sichtfeld."""
        detected = []
        for obj in objects:
            if self.get_distance(obj) < self.sight_range:
                detected.append(obj)
        return detected

    def get_distance(self, obj):
        """Berechne die Entfernung zu einem anderen Objekt."""
        return math.hypot(self.rect.centerx - obj.rect.centerx, self.rect.centery - obj.rect.centery)

    def wrap_around_screen(self):
        """Stelle sicher, dass das Lebewesen am anderen Bildschirmrand wieder erscheint."""
        if self.rect.left > WINDOW_WIDTH:
            self.rect.right = 0
        elif self.rect.right < 0:
            self.rect.left = WINDOW_WIDTH
        if self.rect.top > WINDOW_HEIGHT:
            self.rect.bottom = 0
        elif self.rect.bottom < 0:
            self.rect.top = WINDOW_HEIGHT

    def random_movement(self):
        """Bewege das Lebewesen zufällig, wenn keine unmittelbaren Ziele vorhanden sind."""
        current_time = pygame.time.get_ticks()
        if current_time - self.last_random_movement_time > RANDOM_MOVEMENT_INTERVAL:
            self.last_random_movement_time = current_time
            # Ändere die Richtung zufällig
            self.direction = pygame.Vector2(random.choice([-1, 1]), random.choice([-1, 1])).normalize()

        # Bewege das Lebewesen in die aktuelle Richtung
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

class Prey(Creature):
    """Beute-Klasse, die Pflanzen frisst und sich fortpflanzt."""
    def __init__(self, x, y):
        super().__init__(x, y, BLUE, PREY_SIZE, SIGHT_RANGE, PREY_LIFETIME, PREY_SPEED)
        self.plants_eaten = 0  # Zähler für gegessene Pflanzen

    def update(self):
        """Aktualisiere die Beute, bewege sie und suche nach Nahrung."""
        super().update()
        self.move()
        self.search_for_food()
        self.avoid_obstacles()

    def move(self):
        """Bewege die Beute logisch in Richtung der nächsten Pflanze oder Flucht vor Jägern."""
        predators_in_range = self.detect_objects(predators)
        if predators_in_range:
            # Fliehe vor dem nächsten Jäger
            closest_predator = min(predators_in_range, key=lambda p: self.get_distance(p))
            direction_x = self.rect.centerx - closest_predator.rect.centerx
            direction_y = self.rect.centery - closest_predator.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.direction = pygame.Vector2(direction_x, direction_y)
                self.rect.x += self.direction.x * PREY_SPEED  # Bewege sich weg vom Jäger
                self.rect.y += self.direction.y * PREY_SPEED
        else:
            # Bewege dich in Richtung der nächsten Pflanze
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
                    self.rect.x += self.direction.x * PREY_SPEED  # Bewege sich in Richtung der Pflanze
                    self.rect.y += self.direction.y * PREY_SPEED

        # Verhindere Überlappung
        self.avoid_overlap(preys)

    def search_for_food(self):
        """Suche nach Pflanzen, esse sie und kontrolliere die Fortpflanzung."""
        if plants:  # Überprüfe, ob es noch Pflanzen gibt
            plants_in_range = self.detect_objects(plants)
            if plants_in_range:
                closest_plant = min(plants_in_range, key=lambda p: self.get_distance(p))
                if self.get_distance(closest_plant) < self.size:
                    plants.remove(closest_plant)
                    all_sprites.remove(closest_plant)
                    self.plants_eaten += 1
                    self.last_food_time = pygame.time.get_ticks()  # Setze die letzte Nahrungsaufnahme zurück

                    if self.plants_eaten >= PLANTS_EATEN_TO_REPRODUCE:
                        self.plants_eaten = 0
                        self.reproduce()  # Fortpflanzung

    def reproduce(self):
        """Erzeuge eine neue Beute an einer zufälligen Position."""
        new_prey = Prey(self.rect.x + random.randint(-20, 20), self.rect.y + random.randint(-20, 20))
        preys.add(new_prey)
        all_sprites.add(new_prey)

    def avoid_obstacles(self):
        """Vermeide Hindernisse."""
        obstacles_in_range = self.detect_objects(obstacles)
        if obstacles_in_range:
            closest_obstacle = min(obstacles_in_range, key=lambda o: self.get_distance(o))
            direction_x = self.rect.centerx - closest_obstacle.rect.centerx
            direction_y = self.rect.centery - closest_obstacle.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.rect.x += direction_x * PREY_SPEED  # Bewege sich weg vom Hindernis
                self.rect.y += direction_y * PREY_SPEED

    def avoid_overlap(self, group):
        """Verhindere das Übereinanderstapeln von Lebewesen."""
        for sprite in group:
            if sprite != self and pygame.sprite.collide_rect(self, sprite):
                # Bewege das Lebewesen weg vom anderen, um Überlappung zu vermeiden
                direction_x = self.rect.centerx - sprite.rect.centerx
                direction_y = self.rect.centery - sprite.rect.centery
                distance = math.hypot(direction_x, direction_y)
                if distance > 0:
                    direction_x /= distance
                    direction_y /= distance
                    self.rect.x += direction_x * PREY_SPEED
                    self.rect.y += direction_y * PREY_SPEED

class Predator(Creature):
    """Jäger-Klasse, die Beute jagt und sich fortpflanzt."""
    def __init__(self, x, y):
        super().__init__(x, y, RED, PREDATOR_SIZE, SIGHT_RANGE, PREDATOR_LIFETIME, PREDATOR_SPEED)
        self.preys_eaten = 0  # Zähler für gegessene Beute

    def update(self):
        """Aktualisiere den Jäger, bewege ihn und suche nach Beute."""
        super().update()
        self.move()
        self.search_for_food()
        self.avoid_obstacles()

    def move(self):
        """Bewege den Jäger in Richtung der nächsten Beute."""
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
                self.rect.x += self.direction.x * PREDATOR_SPEED  # Bewege sich in Richtung der Beute
                self.rect.y += self.direction.y * PREDATOR_SPEED
        else:
            # Zufällige Bewegung, wenn keine Beute in der Nähe ist
            self.rect.x += random.choice([-1, 1]) * random.random() * PREDATOR_SPEED
            self.rect.y += random.choice([-1, 1]) * random.random() * PREDATOR_SPEED

        # Verhindere Überlappung
        self.avoid_overlap(predators)

    def search_for_food(self):
        """Suche nach Beute, esse sie und kontrolliere die Fortpflanzung."""
        if preys:  # Überprüfe, ob es noch Beute gibt
            preys_in_range = self.detect_objects(preys)
            if preys_in_range:
                closest_prey = min(preys_in_range, key=lambda p: self.get_distance(p))
                if self.get_distance(closest_prey) < self.size:
                    preys.remove(closest_prey)
                    all_sprites.remove(closest_prey)
                    self.preys_eaten += 1
                    self.last_food_time = pygame.time.get_ticks()  # Setze die letzte Nahrungsaufnahme zurück

                    if self.preys_eaten >= PREYS_EATEN_TO_REPRODUCE:
                        self.preys_eaten = 0
                        self.reproduce()  # Fortpflanzung

    def reproduce(self):
        """Erzeuge einen neuen Jäger an einer zufälligen Position."""
        new_predator = Predator(self.rect.x + random.randint(-20, 20), self.rect.y + random.randint(-20, 20))
        predators.add(new_predator)
        all_sprites.add(new_predator)

    def avoid_obstacles(self):
        """Vermeide Hindernisse."""
        obstacles_in_range = self.detect_objects(obstacles)
        if obstacles_in_range:
            closest_obstacle = min(obstacles_in_range, key=lambda o: self.get_distance(o))
            direction_x = self.rect.centerx - closest_obstacle.rect.centerx
            direction_y = self.rect.centery - closest_obstacle.rect.centery
            distance = math.hypot(direction_x, direction_y)
            if distance > 0:
                direction_x /= distance
                direction_y /= distance
                self.rect.x += direction_x * PREDATOR_SPEED  # Bewege sich weg vom Hindernis
                self.rect.y += direction_y * PREDATOR_SPEED

    def avoid_overlap(self, group):
        """Verhindere das Übereinanderstapeln von Jägern."""
        for sprite in group:
            if sprite != self and pygame.sprite.collide_rect(self, sprite):
                # Bewege das Lebewesen weg vom anderen, um Überlappung zu vermeiden
                direction_x = self.rect.centerx - sprite.rect.centerx
                direction_y = self.rect.centery - sprite.rect.centery
                distance = math.hypot(direction_x, direction_y)
                if distance > 0:
                    direction_x /= distance
                    direction_y /= distance
                    self.rect.x += direction_x * PREDATOR_SPEED
                    self.rect.y += direction_y * PREDATOR_SPEED

class Plant(pygame.sprite.Sprite):
    """Pflanzen-Klasse, die sich mit der Zeit selbst reproduziert."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLANT_SIZE, PLANT_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.last_reproduce_time = pygame.time.get_ticks()  # Initialisiere Zeit für die letzte Reproduktion

    def update(self):
        """Aktualisiere die Pflanze und überprüfe die Reproduktionsbedingungen."""
        if pygame.time.get_ticks() - self.last_reproduce_time > PLANT_GROWTH_INTERVAL:
            if len(plants) < MAX_PLANTS:
                self.reproduce()  # Fortpflanzung

    def reproduce(self):
        """Erzeuge eine neue Pflanze an einer zufälligen Position."""
        new_plant_position = self.get_random_position()
        new_plant = Plant(*new_plant_position)
        if len(plants) < MAX_PLANTS:
            plants.add(new_plant)
            all_sprites.add(new_plant)

    def get_random_position(self):
        """Generiere eine zufällige Position auf der Karte, die nicht bereits von einer Pflanze belegt ist."""
        while True:
            x = random.randint(0, WINDOW_WIDTH - PLANT_SIZE)
            y = random.randint(0, WINDOW_HEIGHT - PLANT_SIZE)
            new_rect = pygame.Rect(x, y, PLANT_SIZE, PLANT_SIZE)
            if not any(new_rect.colliderect(plant.rect) for plant in plants):
                return (x, y)

class Obstacle(pygame.sprite.Sprite):
    """Hindernis-Klasse, die den Beutetieren und Jägern als Deckung dient."""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))

# ===============================
# HAUPTFUNKTION
# ===============================

def main():
    """Hauptfunktion des Spiels, in der alles initialisiert und die Spielschleife ausgeführt wird."""
    pygame.init()  # Initialisiere pygame
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))  # Erstelle das Fenster
    pygame.display.set_caption("Evolution Spiel")  # Setze den Fenstertitel
    clock = pygame.time.Clock()  # Erstelle einen Clock-Objekt für die Frame-Rate

    global all_sprites, plants, preys, predators, obstacles
    all_sprites = pygame.sprite.Group()  # Gruppe für alle Sprites
    plants = pygame.sprite.Group()        # Gruppe für Pflanzen
    preys = pygame.sprite.Group()         # Gruppe für Beute
    predators = pygame.sprite.Group()     # Gruppe für Jäger
    obstacles = pygame.sprite.Group()     # Gruppe für Hindernisse

    # Erzeuge Pflanzen
    for _ in range(NUM_PLANTS):
        plant_position = Plant(0, 0).get_random_position()
        plant = Plant(*plant_position)
        plants.add(plant)
        all_sprites.add(plant)

    # Erzeuge Beute
    for _ in range(NUM_PREYS):
        prey = Prey(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        preys.add(prey)
        all_sprites.add(prey)

    # Erzeuge immer mindestens zwei Jäger
    for _ in range(MIN_PREDATORS):
        predator = Predator(random.randint(0, WINDOW_WIDTH), random.randint(0, WINDOW_HEIGHT))
        predators.add(predator)
        all_sprites.add(predator)

    # Erzeuge Hindernisse
    for _ in range(NUM_OBSTACLES):
        obstacle = Obstacle(random.randint(0, WINDOW_WIDTH - OBSTACLE_SIZE), random.randint(0, WINDOW_HEIGHT - OBSTACLE_SIZE))
        obstacles.add(obstacle)
        all_sprites.add(obstacle)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Aktualisiere alle Sprites
        all_sprites.update()

        # Fülle den Bildschirm mit der Hintergrundfarbe
        screen.fill(WHITE)
        all_sprites.draw(screen)  # Zeichne alle Sprites auf den Bildschirm

        pygame.display.flip()  # Aktualisiere den Bildschirm
        clock.tick(FPS)  # Steuere die Bildwiederholrate

    pygame.quit()  # Beende pygame

if __name__ == "__main__":
    main()
