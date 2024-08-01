# Evolution-Game-Python

This code creates a simple simulation game where entities such as plants, prey, and predators interact in a graphical environment. The game involves basic elements of life simulation: creatures (prey and predators) and plants, all within a bounded screen area.

### **English**
<details>
  <summary>open</summary>
  Certainly! Here’s a detailed explanation of the provided Python code using the `pygame` library for creating a simple simulation game:

---

### Overview

This code creates a simple simulation game where entities such as plants, prey, and predators interact in a graphical environment. The game involves basic elements of life simulation: creatures (prey and predators) and plants, all within a bounded screen area. 

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

  </details>

### **German**
<details>
  <summary>open</summary>
  Dieser Python-Code verwendet die Bibliothek `pygame`, um ein einfaches Simulationsspiel zu erstellen. Es stellt eine virtuelle Welt dar, in der Pflanzen, Beute und Jäger interagieren. Hier ist eine ausführliche Erklärung des Codes:

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

  </details>

### **Updates**
<details>
  <summary>open</summary>

  </details>
