# Evolution-Game-Python

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
