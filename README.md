# Evolution-Game-Python

![Alt text](/images/preview.png?raw=true "preview")

### **English**
This code creates a simple simulation game where entities such as plants, prey, and predators interact in a graphical environment. The game involves basic elements of life simulation: creatures (prey and predators) and plants, all within a bounded screen area.

<details>
  <summary>open</summary>
  Certainly! Here’s a detailed explanation of the provided Python code using the `pygame` library for creating a simple simulation game:

---

### Key Components

#### 1. **Imports and Constants**

- **Imports:**
  - `pygame`: For game development, including graphics and user input.
  - `random`: For generating random numbers, useful for movement and reproduction.
  - `math`: For mathematical functions, like calculating distances.

- **Constants:**
  - `WINDOW_WIDTH`, `WINDOW_HEIGHT`: Dimensions of the game window.
  - `FPS`: Frames per second to control the game update rate.
  - Colors (e.g., `WHITE`, `GREEN`, `BLUE`, `RED`, `GRAY`): For drawing entities.
  - Sizes for different entities (e.g., `PLANT_SIZE`, `PREY_SIZE`, `PREDATOR_SIZE`, `OBSTACLE_SIZE`).
  - Numbers and parameters related to entities (e.g., `NUM_PLANTS`, `PREY_LIFETIME`, `PLANTS_EATEN_TO_REPRODUCE`).

#### 2. **Classes**

- **Creature Class:**
  - **Base Class** for all entities. 
  - **Attributes:** Position, color, size, speed, sight range, and lifetime.
  - **Methods:**
    - `update()`: Updates the creature's state, checking if it needs to be removed due to the expiration of its lifetime.
    - `detect_objects()`: Finds objects within the sight range.
    - `wrap_around_screen()`: Wraps around the screen edges to simulate continuous movement.
    - `random_movement()`: Moves the creature randomly if no specific target is detected.

- **Prey Class:**
  - **Inherits** from `Creature`.
  - **Attributes:** Keeps track of how many plants it has eaten.
  - **Methods:**
    - `update()`: Moves, searches for food, and avoids obstacles.
    - `move()`: Moves towards the nearest plant or away from predators.
    - `search_for_food()`: Eats plants and handles reproduction if enough plants are consumed.
    - `reproduce()`: Creates a new prey.
    - `avoid_obstacles()`: Avoids obstacles by moving away from them.
    - `avoid_overlap()`: Prevents overlapping with other preys.

- **Predator Class:**
  - **Inherits** from `Creature`.
  - **Attributes:** Keeps track of how many preys it has eaten.
  - **Methods:**
    - `update()`: Moves, searches for prey, and avoids obstacles.
    - `move()`: Moves towards the nearest prey or moves randomly if no prey is nearby.
    - `search_for_food()`: Eats prey and handles reproduction if enough prey are consumed.
    - `reproduce()`: Creates a new predator.
    - `avoid_obstacles()`: Avoids obstacles by moving away from them.
    - `avoid_overlap()`: Prevents overlapping with other predators.

- **Plant Class:**
  - **Extends** `pygame.sprite.Sprite`.
  - **Attributes:** Position and last reproduction time.
  - **Methods:**
    - `update()`: Checks if it’s time to reproduce.
    - `reproduce()`: Creates a new plant at a random position.
    - `get_random_position()`: Finds a random position on the screen for new plants.

- **Obstacle Class:**
  - **Extends** `pygame.sprite.Sprite`.
  - **Attributes:** Position and size of obstacles.

#### 3. **Main Function**

- **Initialization:**
  - Sets up the game environment, including the display window, sprite groups, and initial entities.

- **Game Loop:**
  - Handles user events (e.g., quitting the game).
  - Updates all sprites.
  - Clears and redraws the screen each frame.
  - Regulates the frame rate based on the `FPS` setting.

### Summary

The code defines a simple simulation where:
- **Plants** grow and reproduce over time.
- **Prey** eat plants, flee from predators, and reproduce.
- **Predators** hunt prey, avoid obstacles, and reproduce.
- **Obstacles** act as barriers within the environment.

The game operates within a window where all these entities interact, using basic physics for movement and behavior, and provides a continuous simulation of their interactions based on the defined parameters and constants.

### **detailed overview**
<details>
  <summary>open</summary>
Certainly! Here's a detailed overview of the provided Pygame code for an ecosystem simulation, written in English:

### 1. **Imports and Constants**

```python
import pygame
import random
import math
import logging
```

- `pygame`: Library used for game development.
- `random`: For generating random numbers and movements.
- `math`: For mathematical operations like distance calculations.
- `logging`: For logging events and debugging.

**Constants and Settings:**
- `WINDOW_WIDTH`, `WINDOW_HEIGHT`: Dimensions of the game window.
- `FPS`: Frames per second for game updates.
- `WHITE`, `GREEN`, `BLUE`, `RED`, `GRAY`, `BLACK`: Color definitions.
- `PLANT_SIZE`, `PREY_SIZE`, `PREDATOR_SIZE`, `OBSTACLE_SIZE`: Sizes of various sprites.
- `NUM_PLANTS`, `NUM_PREYS`, `MIN_PREDATORS`, `NUM_OBSTACLES`: Initial counts for the sprites.
- `MAX_PLANTS`: Maximum number of plants.
- `PREY_LIFETIME`, `PREDATOR_LIFETIME`: Lifetimes of prey and predators.
- `PLANTS_EATEN_TO_REPRODUCE`, `PREYS_EATEN_TO_REPRODUCE`: Number of food units required for reproduction.
- `SIGHT_RANGE`: Vision range of creatures.
- `MIN_PREYS`: Minimum number of prey.
- `PLANT_GROWTH_INTERVAL`: Growth interval for plants.
- `PREY_SPEED`, `PREDATOR_SPEED`, `RANDOM_MOVEMENT_INTERVAL`: Movement parameters for creatures.

### 2. **Logging Setup**

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

- Configures the logging module to capture debug messages.

### 3. **Game Classes**

**`Creature` Class**

```python
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
            logging.info(f"{self.__class__.__name__} has exceeded its lifetime and will be removed.")
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
```

- `Creature` is the base class for all creatures in the game. It includes basic properties like position, size, lifetime, and movement.
- `update()` is called each frame to move the object and check its lifetime.
- `detect_objects()`, `get_distance()`, `wrap_around_screen()`, `random_movement()` handle behavior and interaction of creatures.

**`Prey` Class**

```python
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
        logging.info(f"New prey created at ({new_prey.rect.x}, {new_prey.rect.y}).")

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
```

- `Prey` inherits from `Creature` and provides the logic for prey behavior.
- `move()` controls prey movement based on proximity to predators or plants.
- `search_for_food()` looks for plants to eat and allows reproduction.
- `avoid_obstacles()` and `avoid_overlap()` prevent collisions with obstacles or other prey.

**`Predator` Class**

```python
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
        logging.info(f"New predator created at ({new_predator.rect.x}, {new_predator.rect.y}).")

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
```

- `Predator` inherits from `Creature` and provides the logic for predator behavior.
- `move()` controls predator movement based on proximity to prey.
- `search_for_food()` looks for prey to eat and allows reproduction.
- `avoid_obstacles()` and `avoid_overlap()` prevent collisions with obstacles or other predators.

**`Plant` and `Obstacle` Classes**

```python
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLANT_SIZE, PLANT_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))
```

- `Plant` and `Obstacle` are simple sprites for plants and obstacles, which do not require complex logic.

### 4. **Game Initialization**

```python
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ecosystem Simulation")
clock = pygame.time.Clock()
```

- Initializes Pygame, sets up the game window, and creates a clock to control the frame rate.

**Sprite Groups**

- `all_sprites`, `plants`, `preys`, `predators`, `obstacles`: Groups to manage and draw sprites.
- Initializes sprites and adds them to their respective groups (plants, prey, predators, obstacles).

### 5. **Drawing the Overview**

```python
def draw_stats(screen, start_time):
    font = pygame.font.SysFont(None, 30)
    elapsed_time = pygame.time.get_ticks() - start_time
    seconds = elapsed_time // 1000
    minutes = seconds // 60
    seconds %= 60

    text = [
        f"Time: {minutes:02}:{seconds:02}",
        f"Plants: {len(plants)}",
        f"Prey: {len(preys)}",
        f"Predators: {len(predators)}"
    ]

    for i, line in enumerate(text):
        label = font.render(line, True, BLACK)
        screen.blit(label, (10, 10 + i * 20))
```

- Draws status information (time, number of plants, prey, and predators) on the screen.

### 6. **Game Loop**

```python
running = True
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)
    draw_stats(screen, start_time)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
```

- Main game loop that handles events, updates sprites, draws everything on the screen, and manages the frame rate.
- Exits the game when the window is closed.

### Summary

The code represents a basic ecosystem simulation where plants grow, prey eats plants, and predators hunt prey. It includes fundamental mechanisms for movement, collision detection, reproduction, and interaction among different types of sprites. Pygame is used for graphical display and event handling.
  </details>
  </details>

### **German**

Dieser Python-Code verwendet die Bibliothek `pygame`, um ein einfaches Simulationsspiel zu erstellen. Es stellt eine virtuelle Welt dar, in der Pflanzen, Beute und Jäger interagieren. Hier ist eine ausführliche Erklärung des Codes:
<details>
  <summary>open</summary>


### 1. **Konstanten und Einstellungen**

**Konstanten und grundlegende Einstellungen definieren:**
- **`WINDOW_WIDTH` und `WINDOW_HEIGHT`**: Bestimmen die Größe des Fensterbereichs, in dem das Spiel läuft (1200x800 Pixel).
- **`FPS`**: Die Anzahl der Frames pro Sekunde für das Spiel (30 FPS).
- **Farben**: Definieren die Farben für verschiedene Objekte im Spiel (z.B. `WHITE`, `GREEN`, `BLUE`, `RED`, `GRAY`).
- **Größen**: Bestimmen die Größe der verschiedenen Sprites im Spiel (z.B. Pflanzen, Beute, Jäger, Hindernisse).
- **Anzahl der Anfangsobjekte**: Legen fest, wie viele Pflanzen, Beute und Jäger zu Beginn des Spiels erzeugt werden.
- **Lebenszeiten**: Bestimmen, wie lange Beute und Jäger leben, bevor sie verschwinden.
- **Fortpflanzungsbedingungen**: Regeln, wie viele Pflanzen Beute essen muss oder wie viele Beute Jäger essen muss, um sich fortzupflanzen.
- **Sichtfeld**: Legt den Bereich fest, in dem Beute und Jäger andere Objekte erkennen können.
- **Wachstumsrate**: Bestimmt, wie oft eine Pflanze sich selbst reproduziert.
- **Bewegungsparameter**: Bestimmen die Geschwindigkeit der Beute und Jäger sowie den Intervall für zufällige Bewegungen.

### 2. **Spielklassen**

**Basisklasse `Creature`:**
- **`__init__`**: Initialisiert die grundlegenden Eigenschaften eines Lebewesens, einschließlich Größe, Sichtfeld, Lebenszeit und Geschwindigkeit.
- **`update`**: Aktualisiert den Zustand des Lebewesens, überprüft die Lebenszeit und bewegt das Lebewesen.
- **`detect_objects`**: Ermittelt Objekte im Sichtfeld des Lebewesens.
- **`get_distance`**: Berechnet die Entfernung zu einem anderen Objekt.
- **`wrap_around_screen`**: Stellt sicher, dass das Lebewesen am Rand des Bildschirms wieder erscheint (Bildschirm-Wraparound).
- **`random_movement`**: Bewegt das Lebewesen zufällig, wenn keine spezifischen Ziele vorhanden sind.

**Abgeleitete Klasse `Prey`:**
- **`__init__`**: Initialisiert Beute mit spezifischen Eigenschaften.
- **`update`**: Aktualisiert die Beute, einschließlich Bewegung und Nahrungssuche.
- **`move`**: Bewegt die Beute entweder in Richtung der nächsten Pflanze oder flieht vor Jägern.
- **`search_for_food`**: Sucht nach Pflanzen, isst sie und überprüft die Fortpflanzung.
- **`reproduce`**: Fortpflanzung durch Erzeugung neuer Beute.
- **`avoid_obstacles`**: Vermeidet Hindernisse.
- **`avoid_overlap`**: Verhindert das Überlappen von Beute.

**Abgeleitete Klasse `Predator`:**
- **`__init__`**: Initialisiert Jäger mit spezifischen Eigenschaften.
- **`update`**: Aktualisiert den Jäger, einschließlich Bewegung und Nahrungssuche.
- **`move`**: Bewegt den Jäger in Richtung der nächsten Beute oder zufällig, wenn keine Beute in der Nähe ist.
- **`search_for_food`**: Sucht nach Beute, isst sie und überprüft die Fortpflanzung.
- **`reproduce`**: Fortpflanzung durch Erzeugung neuer Jäger.
- **`avoid_obstacles`**: Vermeidet Hindernisse.
- **`avoid_overlap`**: Verhindert das Überlappen von Jägern.

**Klasse `Plant`:**
- **`__init__`**: Initialisiert eine Pflanze mit spezifischen Eigenschaften.
- **`update`**: Aktualisiert die Pflanze, einschließlich der Reproduktion.
- **`reproduce`**: Fortpflanzung durch Erzeugung neuer Pflanzen.
- **`get_random_position`**: Bestimmt eine zufällige Position für die Pflanze, an der keine andere Pflanze bereits vorhanden ist.

**Klasse `Obstacle`:**
- **`__init__`**: Initialisiert ein Hindernis mit spezifischen Eigenschaften.

### 3. **Hauptfunktion**

**`main`**: 
- Initialisiert pygame und erstellt das Fenster.
- Setzt die verschiedenen Sprite-Gruppen (`all_sprites`, `plants`, `preys`, `predators`, `obstacles`).
- Erzeugt Pflanzen, Beute, Jäger und Hindernisse und fügt sie den entsprechenden Gruppen hinzu.
- Führt die Hauptspielschleife aus:
  - Überprüft Ereignisse (z.B. Beenden des Spiels).
  - Aktualisiert alle Sprites.
  - Zeichnet alle Sprites auf den Bildschirm.
  - Aktualisiert den Bildschirm und steuert die Bildwiederholrate.

### **Was ist möglich?**

- **Pflanzen wachsen und reproduzieren**: Pflanzen erscheinen nach und nach und füllen den Bildschirm, bis die maximale Anzahl erreicht ist.
- **Beute bewegen und fressen**: Beute sucht nach Pflanzen, frisst sie und bewegt sich entweder zu Pflanzen oder flieht vor Jägern.
- **Jäger bewegen und jagen**: Jäger suchen nach Beute und bewegen sich in deren Richtung. Sie können sich auch zufällig bewegen, wenn keine Beute in der Nähe ist.
- **Vermeidung von Hindernissen und Kollisionen**: Sowohl Beute als auch Jäger vermeiden Hindernisse und verhindern Kollisionen mit anderen Lebewesen.
- **Fortpflanzung**: Beute und Jäger reproduzieren sich basierend auf den Regeln für gegessene Pflanzen oder Beute.

Dieses Spiel simuliert ein einfaches Ökosystem, in dem Pflanzen wachsen, Beute sich ernährt und Jäger jagen. Es bietet eine gute Grundlage, um mit pygame komplexere Spiele und Simulationen zu erstellen.
<details>
  <summary>Ausführliche Überblick</summary>
 Hier ist der ausführliche Überblick über den bereitgestellten Pygame-Code für eine Ökosystem-Simulation. Der Code enthält die grundlegenden Elemente eines Spiels, einschließlich der Initialisierung, der Definition von Klassen für verschiedene Spielfiguren und die Hauptspielschleife. Ich werde die einzelnen Abschnitte des Codes detailliert erklären:

### 1. **Importe und Konstanten**

```python
import pygame
import random
import math
import logging
```

- `pygame`: Bibliothek für die Entwicklung von Spielen.
- `random`: Für zufällige Zahlen und Bewegungen.
- `math`: Für mathematische Operationen, wie Berechnung von Distanzen.
- `logging`: Für das Loggen von Ereignissen und Debugging.

**Konstanten und Einstellungen:**
- `WINDOW_WIDTH`, `WINDOW_HEIGHT`: Größe des Spielfensters.
- `FPS`: Frames pro Sekunde, die das Spiel aktualisiert.
- `WHITE`, `GREEN`, `BLUE`, `RED`, `GRAY`, `BLACK`: Farbdefinitionen.
- `PLANT_SIZE`, `PREY_SIZE`, `PREDATOR_SIZE`, `OBSTACLE_SIZE`: Größen der verschiedenen Sprites.
- `NUM_PLANTS`, `NUM_PREYS`, `MIN_PREDATORS`, `NUM_OBSTACLES`: Anfangszahlen für die Sprites.
- `MAX_PLANTS`: Maximale Anzahl an Pflanzen.
- `PREY_LIFETIME`, `PREDATOR_LIFETIME`: Lebensdauer der Beute und Jäger.
- `PLANTS_EATEN_TO_REPRODUCE`, `PREYS_EATEN_TO_REPRODUCE`: Anzahl der notwendigen Nahrungseinheiten zur Fortpflanzung.
- `SIGHT_RANGE`: Sichtfeld der Kreaturen.
- `MIN_PREYS`: Minimale Anzahl an Beute.
- `PLANT_GROWTH_INTERVAL`: Wachstumsintervall der Pflanzen.
- `PREY_SPEED`, `PREDATOR_SPEED`, `RANDOM_MOVEMENT_INTERVAL`: Bewegungsparameter der Kreaturen.

### 2. **Logging Einrichtung**

```python
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
```

- Konfiguriert das Logging-Modul, um Debug-Meldungen zu erfassen.

### 3. **Spielklassen**

**`Creature` Klasse**

```python
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
```

- `Creature` ist die Basis-Klasse für alle Kreaturen im Spiel. Sie enthält grundlegende Eigenschaften wie Position, Größe, Lebensdauer und Bewegung.
- `update()` wird in jedem Frame aufgerufen, um das Objekt zu bewegen und die Lebensdauer zu überprüfen.
- `detect_objects()`, `get_distance()`, `wrap_around_screen()`, `random_movement()` sind Methoden, die das Verhalten und die Interaktion der Kreaturen steuern.

**`Prey` Klasse**

```python
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
```

- `Prey` erbt von `Creature` und stellt die Logik für die Beute bereit.
- `move()` steuert die Bewegung der Beute, abhängig von der Nähe zu Raubtieren oder Pflanzen.
- `search_for_food()` sucht nach Pflanzen zum Fressen und ermöglicht die Fortpflanzung.
- `avoid_obstacles()` und `avoid_overlap()` verhindern, dass Beute mit Hindernissen oder anderen Beutetieren kollidiert.

**`Predator` Klasse**

```python
class Predator(Creature):
    def __init__(self, x, y):
        super().__init__(x, y, RED, PREDATOR_SIZE, SIGHT_RANGE, PREDATOR_LIFETIME, PRED

ATOR_SPEED)
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
```

- `Predator` erbt von `Creature` und stellt die Logik für die Raubtiere bereit.
- `move()` steuert die Bewegung der Raubtiere, abhängig von der Nähe zu Beutetieren.
- `search_for_food()` sucht nach Beute und ermöglicht die Fortpflanzung.
- `avoid_obstacles()` und `avoid_overlap()` verhindern, dass Raubtiere mit Hindernissen oder anderen Raubtieren kollidieren.

**`Plant` und `Obstacle` Klassen**

```python
class Plant(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PLANT_SIZE, PLANT_SIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect(topleft=(x, y))

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_SIZE, OBSTACLE_SIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))
```

- `Plant` und `Obstacle` sind einfache Sprites für Pflanzen und Hindernisse, die keine besondere Logik benötigen.

### 4. **Spiel Initialisierung**

```python
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Ökosystem Simulation")
clock = pygame.time.Clock()
```

- Initialisiert Pygame und richtet das Fenster sowie die Uhr für die FPS-Steuerung ein.

**Sprite-Gruppen**

- `all_sprites`, `plants`, `preys`, `predators`, `obstacles`: Gruppen zur Verwaltung und zum Zeichnen der Sprites.
- Initialisierung der Sprites in den Gruppen (Pflanzen, Beute, Jäger, Hindernisse).

### 5. **Zeichnen der Übersicht**

```python
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
```

- Zeichnet die Statusinformationen (Zeit, Anzahl der Pflanzen, Beute, Jäger) auf den Bildschirm.

### 6. **Spiel Schleife**

```python
running = True
start_time = pygame.time.get_ticks()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    screen.fill(WHITE)
    all_sprites.draw(screen)
    draw_stats(screen, start_time)
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
```

- Hauptspielschleife, die Ereignisse verarbeitet, die Sprites aktualisiert, den Bildschirm löscht, alle Sprites zeichnet und die Statistiken anzeigt.
- Beendet das Spiel, wenn das Fenster geschlossen wird.

### Zusammenfassung

Der Code stellt eine einfache Simulation eines Ökosystems dar, bei dem Pflanzen wachsen, Beute frisst und sich fortpflanzt, während Raubtiere die Beute jagen. Es enthält grundlegende Mechanismen für Bewegung, Kollisionserkennung, Fortpflanzung und Interaktion zwischen verschiedenen Arten von Sprites. Es nutzt Pygame für die Grafikanzeige und Ereignisverarbeitung. 
</details>
    </details>

### **Updates**
<details>
  <summary>open</summary>
  
**01.08.2024/ Version 0.51:**
-------------------------------------------------------------------------------
### **Logging-Setup** 
1. ***Logging-Setup*** 
   - Das Logging-Modul wird mit `logging.basicConfig` eingerichtet, um eine einfache Konfiguration zu ermöglichen.
2. ***Logging in `Creature`:***
   - In der Methode `update()` wird ein Logeintrag erstellt, wenn die Lebenszeit eines `Creature`-Objekts überschritten wird.
3. ***Logging in `Prey`:***
   - Im `reproduce`-Methodenaufruf wird ein Logeintrag gemacht, wenn ein neuer `Prey` erzeugt wird.
4. ***Logging in `Predator`:***
   - Ähnlich wie bei `Prey` wird beim Reproduzieren eines neuen `Predator` ein Logeintrag gemacht.
---------------------------------------------------------------------------------
### **Übersicht auf dem Bildschirm:**
1. ***Funktion `draw_stats(screen, start_time)`:***
   - Diese Funktion berechnet die verstrichene Zeit seit dem Start des Spiels und zeigt die Anzahl der Pflanzen, Beute und Jäger an.
2. ***Übersicht auf dem Bildschirm:***
   - Die Übersicht wird mit der `draw_stats`-Funktion oben links auf dem Bildschirm gezeichnet.
3. ***Zeiterfassung:***
   - Die Startzeit des Spiels wird erfasst und verwendet, um die verstrichene Zeit zu berechnen.
Mit diesen Änderungen wird die Übersicht jetzt in der oberen linken Ecke des Bildschirms angezeigt und aktualisiert.
---------------------------------------------------------------------------------
### **Attribute für Ausdauer:**
1. ***Attribute für Ausdauer***:
In der `Creature`-Klasse wurden Attribute für die Ausdauer (`sprint_start_time`, `cooldown_end_time`, `is_sprinting`) und die Dauer des Sprints und des Cooldowns hinzugefügt.
2. ***Sprint-Logik***:
Die Methode `handle_sprint` steuert den Sprint und den Cooldown. Wenn der Sprint abgelaufen ist, wird der Cooldown aktiviert.
3. ***Sprint-Start***:
In den `move`-Methoden von `Prey` und `Predator` wird die Methode `start_sprint` aufgerufen, um den Sprint zu beginnen, wenn die Bedingungen erfüllt sind (nahe Beute für `Predator` oder nahe Jäger für `Prey`).
- Mit diesen Änderungen kannst du nun eine Ausdauer-Funktionalität in deinem Spiel verwenden, die es den Kreaturen ermöglicht, kurze Sprints einzulegen, bevor sie sich für eine bestimmte Zeit erholen müssen.

**03.08.2024/ Version 0.52:**
-------------------------------------------------------------------------------
1. ***Hintergrund geändert***:
2. ***Neue Tiere und Pflanzen***:
3. ***Verbesserte Bewegungslogik***:
4. ***Restart Button***:
  </details>
