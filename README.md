# **ARBIUS – Fire at Night**
*Game Design Document*

This repository contains the implementation of the project for the course **Object Technologies** – the game **Arbius – Fire at Night**. In the game, the player controls a hero who must survive on an uninhabited island, fight the cold and other dangers, collect firewood to light a fire and overcome obstacles. The game combines elements of strategic planning, dynamic events and retro-atmospheric graphics.

**Author**: *Ivan Veremchuk*
**Project Theme**: Dark and Light

---

## **1. Introduction**

### **1.1 Idea and Inspiration**

**Arbius – Fire at Night** was created as a final project for the subject Object Technologies. The main idea is to survive in a night, gloomy world, where the cold and harsh environment force the hero to constantly move forward, collecting limited resources to maintain the fire. Inspired by classic works of darkness and light, as well as indie games where atmosphere and precise interaction with the environment are key aspects.

### **1.2 Game Overview**

The player has the following tasks:
- **Survive the Night**: Survive a long, cold night.
- **Gather Resources**: Collect logs to light a campfire. The amount of available firewood gradually decreases with each subsequent level, creating an additional challenge.
- **Fight the Cold**: The cold increases throughout the level, so the hero must light a campfire in time or seek out areas of light to prevent freezing.
- **Dynamic Events**: Storms and other random events change the game conditions, affecting the speed at which the hero freezes and the reduction of the campfire.
- **Swamp Mechanic**: When the hero enters a swamp, his speed decreases significantly, making movement difficult and requiring careful route planning.

### **1.3 Vývojový softvér**
- **Pygame-CE**: zvolený programovací jazyk.
- **PyCharm 2024.1**: vybrané IDE.
- **Tiled 1.10.2**: grafický nástroj na vytváranie levelov.
- **Itch.io**: zdroj grafických assetov a zvukov do hry.

---
## **2. Concept**

### **2.1 Gameplay Overview**

**Arbius – Fire at Night** is an atmospheric game with survival elements. The player must:
- Move through different levels, each with its own characteristics (including resource depletion, dynamic events and swamp areas).
- Collect limited resources (logs) to maintain a fire that helps fight the cold.
- Plan your actions to keep warm in time and prevent the hero from freezing.

### **2.2 Theme Interpretation: Dark and Light**

The game explores the struggle between light and darkness:
- **Light** symbolizes the warmth, life, hope and power of the fire that supports the hero's life.
- **Darkness** represents the cold, danger and harsh, hostile environment.
- The player must use light as a tool for survival, confronting the darkness.

### **2.3 Core Mechanics**

- **Movement & Interaction**: The hero moves around the map and interacts with objects (picks up logs, lights fires).
- **Resource System**: Logs are used to maintain the fire; their number gradually decreases with each level.
- **Collision System**: Masks and polygonal contours are used to accurately define interactions between objects.
- **Dynamic Events**: For example, a storm affects the rate at which the fire decreases and the hero freezes.
- **Level Progression**: When moving between levels, the game parameters change, including the number of available resources and storm bonuses.
- **Swamp Mechanic**: In the swamp area, the hero's movement speed decreases, which makes movement more difficult and requires strategic planning.

---

## **3. Art**

### **3.1 Visual Style**

The game is made in a retro style using pixel graphics, which emphasizes the gloomy atmosphere and tension of the night world.
- **Background Tiles**: The map is created using the Tiled editor and includes layers such as water, base, decor and swamp.
- **Player Sprite**: Carefully worked out movement animation, reflecting the actions of the hero in a harsh environment.
- **Objects & Details**: Additional elements such as logs, trees and stones are used, the polygons of which are accurately displayed thanks to the mask system.

### **3.2 Polygons and Collisions**

To accurately determine collisions, a mask system is used that generates polygons (contours) for each sprite.
- This allows you to correctly display the interaction of objects, in particular, the exact selection of resources and interaction with decorative elements.
- Polygon correction system ensures that the sprite outline matches its visual model.

---

## **4. Audio**

### **4.1 Music**

Each stage of the game has music that matches the atmosphere:
- **Start Menu**: Melodies that immerse you in the game world.
- **Main Game**: Atmospheric compositions that emphasize the tension and gloom of the night world.
- **Level Transitions & Victory Screen**: Specially selected music to enhance emotional moments.
- **Death Screen**: Dramatic soundtracks that signal failure and the importance of timely action.

### **4.2 Sound Effects**

Sound effects include:
- **Interaction Effects**: Sounds of picking up logs, footsteps, and other actions.
- **Ambient Sounds**: The crackling of fire, the rustling of the wind, the noise of the swamp – all this creates immersion in the game world.

---

## **5. Gameplay and Interface**

### **5.1 Gameplay**

The player must:
- **Survive the Night**: Survive a long, cold night.
- **Gather Resources**: Gather logs to build a campfire; the number of logs available decreases with each level, creating an additional challenge.
- **Fight the Cold**: The cold increases throughout the level, so the hero must maintain a campfire or seek out areas of light to avoid freezing.
- **Dynamic Events**: Storms and other random events change the game conditions, affecting the hero's freezing rate and the effectiveness of the campfire.
- **Swamp Mechanic**: When entering a swamp, the hero's movement speed is significantly reduced, making movement difficult and requiring careful route planning.

### **5.2 User Interface**

The game interface includes:
- **Animated Main Menu**: A start menu with interactive animation and the ability to start the game by pressing the Enter key.
- **Status Indicators**:
- **Health Bar** – displays the hero's health.
- **Corruption/Cold Bar** – shows the level of cold that is bringing the hero closer to freezing.
- **Minimap**: Shows the hero's position on the map, the location of key objects (e.g. firewood) and helps navigate the large game world.

### **5.3 Controls**

#### **Keyboard:**
- **A/D** or **Left/Right Arrows** – horizontal movement.
- **W/S** or **Up/Down Arrows** – vertical movement.
- **F** – action, e.g. throwing a log into a fire.
- **ESC** – opens the pause menu.
- **TAB** – switches between levels (for demonstration purposes and debugging).

---

## **6. Advanced Features**

### **6.1 Storm System**

A Storm is a dynamic event that:
- Randomly triggers with a certain probability.
- Increases the rate of decrease in the progress of the hearth and increases the freezing speed of the hero.
- Has its own animation, which is superimposed on the screen with some transparency.

### **6.2 Resource Gathering System**

- **Logs** are located on the map as objects with specified coordinates.
- With each level, the number of available firewood decreases (according to an algorithm using the **reduction** parameter).
- The player can only pick up one log at a time, which affects the strategy and location on the map.

### **6.3 Collision System and Polygons**

- Sprite masks are used to accurately detect collisions.
- Contours (polygons) obtained from masks can be displayed for debugging to ensure their accuracy and coincidence with the visual model of objects.
- The polygon correction system allows you to accurately display the contour of the visual image (e.g. stones, decorative elements).

### **6.4 Swamp Mechanic**

- **Swamp** is an area on the map where the hero's movement is significantly slowed down.
- When entering a swamp, the hero's speed decreases, which affects reaction time and the ability to collect the necessary resources in a timely manner.
- This mechanic adds an additional strategic element, as the player must plan his route, avoiding swamp areas or adapting to slow movement.

---

## **7. Conclusions**

**Arbius – Fire at Night** is an ambitious project that combines carefully crafted graphics, a dynamic event system, and precise mechanics of interaction with the environment. The player is immersed in the gloomy atmosphere of the night world, where each level poses new challenges and requires strategic thinking for survival.

---

*Documentation prepared by Ivan Veremchuk.*
