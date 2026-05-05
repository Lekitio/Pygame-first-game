# Pygame-first-game

Dependencies:
pytmix
pygame-ce
py -m pip install pytmix pygame-ce


Learning about pygame right now


I should fix the art so i dont have transparent pixels around it

To do:
Programming
Movement:
- Dash, slash i guess?
Optimisation:
- Colission handling
Animation:
- Foreground and background movement
Story:
- Interaction, but theres no one to interact with right now... Maybe just make boxes for that for now.

Art
Animation:
Player:
- walk, run, jump, idle
- Slash dash
- Dust, 
Tiled:
- Platforms
- Foreground
- Background

Sounds:
- Bg music
- Landing, jumping

General:
- Concept so I can make enemies


Working log:
2026-04-28. Hanna
I've been thinking about how to deal with the colission and collision sprites for the enemy
Enemy needs to check the wall so it should check collision with collision_sprites
Enemy also needs to check if its hit the player so we import the player into enemy class to check for colissions between those two specifically

Consiering getting rid of player from collision_sprites so the enemy doesnt treat player as a wall. Player wasnt in collision_sprites to begin with

The Player should get the enemy_collision_sprites to check for colissions

I should also check collisions between the player weapon and the enemy for dmg.

05-05-2026 Hanna log
changes collision_sprites -> wall_collision_sprites to specify it
Statred actually implementing enemy colissions
Realized that I don't need a colission in the enemy class (at least for now) and I can check collisions with the enely sprites within the player class.
Many roadblocks such as needing a cooldown and how animations work.
But honestly i coudl deal with those later. The jump fucntion has been of much help.
set the slice key to x
I need to work on an actual weapon. Gotta figure out hierarchy stuff
