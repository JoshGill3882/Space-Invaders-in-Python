# Imports the required libraries
from tkinter import *

# Key Dictionary for later use
key_dictionary = {  'Left': (True,-20,-20),
                    'Right': (True,20,-20),
                    'Up': (True,0,-20),
                    'space': (True,0,-20),
                                            }

# Creating data needed for later
key_down = False
Alien_X_Vel = 0
Alien_Y_Vel = 0
Player_X_Vel = 0
Player_Y_Vel = 0
Firing = False
score = 0
PlayerDead = False

# Creates a two dimensional array, called "Aliens", 30 items long with each second item in the array equalling "False"
Aliens = [[0, False] for a in range(30)]

# Animation Loop for "Game" Window
def AnimationLoop():
    # Provides procedure with required values
    global canvas, Aliens, Game, PlayerDead

    # Calls "AlienMovement" Function
    AlienMovement()
    # Calls "PlayerMovement" Function
    PlayerMovement()

    # End of game detection (if all aliens dead or player is dead)
    if (score == 30) or (PlayerDead == True):
        # Kill the game window
        Game.destroy()

    # Waits 100ms (for 10fps)
    Game.after(100, AnimationLoop)


# Detects when a key is pressed and updates relevant data
def on_KeyPress(event):
    # Provides program relevant data
    global key_down, Player_X_Vel, Player_Y_Vel, Firing

    # Updates relevant variables with relevant data
    key_down,Player_X_Vel,Player_Y_Vel = key_dictionary[event.keysym]

    # If the key pressed was a "Fire" key, update the "Firing" variable to True
    if ((event.keysym == "Up")or(event.keysym == "space")):
        Firing = True
    # ELSE (any other key pressed)
    else:
        Firing = False


# Detects when a key is released and updates relevant data
def on_KeyRelease(event):
    # Gives the program access to relevant data
    global key_down

    key_down = False


# Runs "AlienMovement" and "AlienDraw" Procedures
def AlienMovement():
    # Give the procedure access to required data
    global canvas, Aliens, Game, Alien_X_Vel, Alien_Y_Vel

    # Gains coordinates of required aliens
    coords1 = canvas.coords(Aliens[0][0])
    coords2 = canvas.coords(Aliens[10][0])
    coords3 = canvas.coords(Aliens[20][0])
    coords4 = canvas.coords(Aliens[9][0])
    coords5 = canvas.coords(Aliens[19][0])
    coords6 = canvas.coords(Aliens[29][0])

    # IF the aliens are at the far left hand of the screen
    if ((coords1[0] == 25) and (coords2[0] == 25) and (coords3[0] == 25)):
        Alien_X_Vel = 10
        Alien_Y_Vel = 10

    # ELSE-IF the aliens are at the right hand of the screen
    elif ((coords4[0] == 975) and (coords5[0] == 975) and (coords6[0] == 975)):
        Alien_X_Vel = -10
        Alien_Y_Vel = 10

    #ELSE move the aliens in their current horizontal direction, but no vertical direction change
    else:
        Alien_X_Vel = Alien_X_Vel
        Alien_Y_Vel = 0

    # Call "AlienDraw" function
    AlienDraw()


def AlienDraw():
    # Give the procedure access to required data
    global canvas, Aliens, Game, Alien_X_Vel, Alien_Y_Vel

    # FOR each alien, move them according to their current x and y velocities as defined above
    for a in range(len(Aliens)):
        canvas.move(Aliens[a][0], Alien_X_Vel, Alien_Y_Vel)


# Runs "PlayerMovement" and "BulletMovement" Procedures
def PlayerMovement():
    # Give the procedure access to required data
    global canvas, Game, Player, PlayerBullet, PlayerBulletSprite, Player_X_Vel, Player_Y_Vel, Firing, BulletInMotion

    # Get coords of PlayerBullet and Player
    BulletCoords = canvas.coords(PlayerBullet)
    PlayerCoords = canvas.coords(Player)

    # IF the bullet's coords equal the player's (Bullet not in motion)
    if BulletCoords == PlayerCoords:
        BulletInMotion = False
    # ELSE (bullet in motion)
    else:
        BulletInMotion = True

    # IF the user presses the fire button
    if Firing == True:
        # IF BulletInMotion equals False (bullet not currently moving)
        if BulletInMotion == False:
            # Set BulletInMotion to True
            BulletInMotion = True

    # IF Bullet is in motion
    if BulletInMotion == True:
        canvas.move(PlayerBullet,0,Player_Y_Vel)

    # IF the user is pressing a key, the player moves according to the key pressed
    if key_down == True:
        canvas.move(Player,Player_X_Vel,0)
        # IF Bullet isn't in motion, it moves with the player
        if BulletInMotion == False:
            canvas.move(PlayerBullet,Player_X_Vel,0)


    # IF the bullet is at the top of the screen
    if BulletCoords[1] <= 0:
        # Set BulletInMotion and Firing to False
        BulletInMotion = False
        Firing = False

        # Find the player's new coords after any moving has been done
        PlayerCoords = canvas.coords(Player)

        # Delete the Bullet
        canvas.delete(PlayerBullet)

        # Re-create the bullet at the Player's coords
        PlayerBullet = canvas.create_image(PlayerCoords[0],PlayerCoords[1],image=PlayerBulletSprite)

    # Run collision detection
    CollisionDetection()


# Function for collision detection
def CollisionDetection():
    # Give the procedure access to required data
    global canvas, Game, PlayerBullet, PlayerBulletSprite, Aliens, Player, score, Firing, BulletInMotion, PlayerDead

    # FOR each alien
    for x in range(len(Aliens)):
        # Get the coords of the Bullet, Player and currently selected Alien
        AlienCoords = canvas.coords(Aliens[x][0])
        BulletCoords = canvas.coords(PlayerBullet)
        PlayerCoords = canvas.coords(Player)

        # Creates a new variable containing the replacement image
        ReplacementAlienImage = PhotoImage(file = "replacementAlien.gif")
        # Collision detection along the x-axis
        if ((AlienCoords[0] - 25) <= (BulletCoords[0] + 3)) and ((AlienCoords[0] + 25) >= (BulletCoords[0] - 3)):
            # Collision detection along the y-axis
            if ((AlienCoords[1] - 25) <= (BulletCoords[1] + 4)) and ((AlienCoords[1] + 25) >= (BulletCoords[1] - 4)):
                # If the alien isn't already dead
                if Aliens[x][1] == False:
                    # Set's that Alien's death flag to True
                    Aliens[x][1] = True
                    # Replaces this alien's image with a white box to simulate deletion of image without actually deleting the image
                    canvas.itemconfigure(Aliens[x][0], image = ReplacementAlienImage)

                    # Add 1 to the score
                    score = score + 1

                    # Update the ScoreText canvas text
                    canvas.itemconfigure(ScoreText, text="Score: " + str(score))

                    # Deletes the PlayerBullet
                    canvas.delete(PlayerBullet)
                    # Sets the Firing and BulletInMotion flags to False
                    Firing = False
                    BulletInMotion = False
                    # Re-creates the PlayerBullet at the player's position
                    PlayerBullet = canvas.create_image(PlayerCoords[0],PlayerCoords[1],image=PlayerBulletSprite)

        # Creates a new image containing the replacement Player image
        ReplacementPlayerImage = PhotoImage(file = "replacementPlayer.gif")
        # Collision detection along the x-axis
        if ((AlienCoords[0] - 25) <= (PlayerCoords[0] + 50)) and ((AlienCoords[0] + 25) >= (PlayerCoords[0] - 50)):
            # Collision detection along the y-axis
            if ((AlienCoords[1] - 25) <= (PlayerCoords[1] + 50)) and ((AlienCoords[1] + 25) >= (PlayerCoords[1] - 50)):
                # If the alien isn't dead
                if Aliens[x][1] == False:
                    # Set flagging variable to True
                    PlayerDead = True
                    # Replace the Player's image with the replacement one to simulate death without actually deleting the Image
                    canvas.itemconfigure(Player, image = ReplacementPlayerImage)

# Window setup
# Creates the Window
Game = Tk()
Game.geometry("1000x500")
Game.title("Game Window")
#Creating the canvas:
canvas = Canvas(Game, height=500, width=1000,)
canvas.grid(row=0, column=0, sticky=W)
canvas.configure(background="white")

# Graphics setup

# Game Title text on top left of screen
TitleText = canvas.create_text(125,25,fill="Black",font=("Purisia",20),text="SPACE INVADERS")
# Score Text on top right of screen
ScoreText = canvas.create_text(925,25,fill="Black",font=("Purisia",20),text="SCORE: "+str(score))
# Creates data for the Player
PlayerSprite = PhotoImage(file='player.gif')
Player = canvas.create_image(475,450,image=PlayerSprite)
# Creates data for the Player Bullets
PlayerBulletSprite = PhotoImage(file='playerBullet.gif')
PlayerBullet = canvas.create_image(475,450,image=PlayerBulletSprite)
# Puts the Alien's Sprites into data so they can be passed into the Classes
Alien1Sprite = PhotoImage(file='alien1.gif')
Alien2Sprite = PhotoImage(file='alien2.gif')
Alien3Sprite = PhotoImage(file='alien3.gif')

# Instantiates the Alien Objects (30 total)
# Creates data necessary for altering items in "Aliens" Array
f = 0  # 0 so that, during the 10 iterations of the loop, it instantiates for the first 10 aliens
g = 10 # 10 so that, during the 10 iterations of the loop, it instantiates for the second 10 aliens
h = 20 # 20 so that, during the 10 iterations of the loop, it instantiates for the last 10 aliens
# Instantiates 10 of Alien1
for y in range(50,550,50):
    # Sets co-ordinates for passing into the Image
    Alien1_Coords1 = y-25
    Alien1_Coords2 = 75
    # Instantiates the Image and passes it into the Aliens Array
    Aliens[f][0] = canvas.create_image(Alien1_Coords1,Alien1_Coords2,image=Alien1Sprite)
    # Setting f to equal 1 more than it current does to access the next item in the array
    f = f + 1
# Instantiates 10 of ALien2
for z in range(50,550,50):
    # Sets co-ordinates for passing into the Image
    Alien2_Coords1 = z-25
    Alien2_Coords2 = 125
    # Instantiates the Image and passes it into the Aliens Array
    Aliens[g][0] = canvas.create_image(Alien2_Coords1,Alien2_Coords2,image=Alien2Sprite)
    # Setting g to equal 1 more than it currently does to access the next item in the array
    g = g + 1
# Instantiates 10 of Alien3
for a in range(50,550,50):
    # Sets co-ordinates for passing into the Image
    Alien3_Coords1 = a-25
    Alien3_Coords2 = 175
    # Instantiates the Image and passes it into the Aliens Array
    Aliens[h][0] = canvas.create_image(Alien3_Coords1,Alien3_Coords2,image=Alien3Sprite)
    # Setting h to equal 1 more than it currently does to access the next item in the array
    h = h + 1

# Key-binds so that key detection events work
Game.bind_all('<KeyPress>', on_KeyPress)
Game.bind_all('<KeyRelease>', on_KeyRelease)

# Runs the Animation Loop
AnimationLoop()

#Menu Mainloop
Game.mainloop()
