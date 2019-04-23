# Spaceship - The Game
Welcome to Spaceship!
Spaceship is a pretty simple game. Shoot enemies, but don't get shot.
As soon as it is actually coded, Spaceship will be an infinitely generating game of mayhem.
![Title Screen](https://raw.githubusercontent.com/CactusBro74/spaceship/maseter/TitleScreen.png)

## Story
As you cruise through the vast infinity of space, you see a looming shadow in front of you. They've found you. The Jynaphive, the alien race that has been pursuing you relentlessly, is finally bringing the full force of their military upon you. There's nowhere to run, nowhere to hide, and only one other choice - fight.

![Gameplay](https://raw.githubusercontent.com/CactusBro74/spaceship/maseter/Gameplay.png)

## Game Controls
The game functions with both an XBox 360 controller and with a keyboard.
XBox 360 Controller: 
  **Left Joystick**-moves ship in the direction of the joystick.
  **A**-shoots lasers.
  **Start**-begins, restarts, and pauses the game.
 
Keyboard:
  **WASD**-Moves the ship around the screen.
  **Spacebar**-begins game, shoots lasers, and restarts the game.
  **Escape**-ends the game.
  
*If a controller is plugged in, then the game automatically uses the controller inputs.
If a controller is __not__ detected, then the game defaults to keyboard controls.*
  
## The Fleet
The fleet consists of two different ship appearances, but all ships act the same.
The fleet moves back and forth, and every time a ship is destroyed, the fleet begins to move faster.
Every few seconds a ship will shoot a laser down towards your ship. Getting hit by this laser removes one point of your shield (See "Player" section to learn more about shield)
Each ship has a random amount of shield points from 1-5. Each hit that your ship lands removes one point of shield. If a ship in the fleet is at 0 shield, then another hit will kill it.

## Scoring
1. Each hit landed on an opponent's shield grants 1 point.
1. Killing an opponent grants as many points as their shield had (If an enemy has 5 shield points, 1 point is granted per hit on the shield, and then 5 when it is killed for a total of 10 points).

### UFOs
In the middle of the game, a UFO will cross the screen. Destroying this UFO grants 20 points.

## Player
1. The player ship starts at the bottom of the screen.
1. Whenever the spacebar is pressed, the ship shoots a red laser.
1. The player ship has a total of 5 shield points.
   1. Each hit taken by the player ship removes one shield point.
   1. This is indicated by the shield meter and percentage listed at the bottom-left of the screen.
   1. When your shield is at 0%, a damaged ship image is overlayed and one more hit will kill you.

## Powerups
Powerups will randomly fall from the top of the screen every once in a while.
There are three powerup types, and each powerup is randomly selected as one of these types.

### Repair Powerup
The repair powerup restores the player ship's shield to 100%, regardless of the current shield amount.


### Double Shot Powerup
The double shot powerup allows the player to shoot two lasers at once (one from each wing tip).


### Invincibility Powerup
The invincibility powerup creates a shield in front of the player that renders the ship invulnerable during that time. Lasts for 5 seconds.


## Current Bugs/Development Ideas
The invincibility powerup currently does not work. Shots pass straight throught the shield and the shield doesn't go away.
Currently, if you destroy the entire fleet, nothing happens. Soon an update will come allowing waves to spawn. Each of these "levels" has an increased bombrate (ships shoot lasers more often)

## Sources
[Space Shooter Extension](https://opengameart.org/content/space-shooter-extension-250)
I'm not sure what the link is, but the same creator of the extension above also made the base pack.
[Background](https://simple.wikipedia.org/wiki/Outer_space)

