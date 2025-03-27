#BSIT 2B - MANZANO
# MAKE SURE TO INSTALL THE FOLLOWING MODULES BEFORE RUNNING THE GAME:
#MAKE SURE TO INSTALL
# * "pip install pygame"
# * "pip install random"
# * "pip install math"
# * "pip install os"
# * "pip install opencv-python"
# * "pip install numpy"
# * "pip install pillow"
# * "pip install traceback"
#on the terminal powershell type "python typing_game.py"
from pygame import display as pg_display # Import only the display module from pygame and rename it as pg_display
import random # For generating random numbers
import math # Provides mathematical functions like calculating distance
import pygame  # Main library for handling game mechanics
import os # Allows interaction with the operating system (e.g., managing file paths)
import cv2 # OpenCV, used for handling video processing (e.g., extracting frames)
import numpy as np # is just a way to rename the module for convenience!
from PIL import Image, ImageSequence # Used for handling images and GIF animations
import traceback # Provides tools for handling and printing errors in code

global WIDTH, HEIGHT #this can have access to all classes
pygame.init()
pygame.mixer.init()
#this are the declaration of the sound_effects and others
rocket_hit_sound = pygame.mixer.Sound("rockey_hit (mp3cut.net).mp3")
laser_sound = pygame.mixer.Sound("Laser Gun - Sound Effect for editing-yt (mp3cut.net).mp3")
explode_sounds = [
    pygame.mixer.Sound("explode1.mp3"),
    pygame.mixer.Sound("explode2.mp3"),
    pygame.mixer.Sound("explode3.mp3")
]
levelup_sound = pygame.mixer.Sound("levelup.mp3")
gameover = pygame.mixer.Sound("gameover.mp3")

HIGH_SCORE_FILE = "highscore.txt"
WIDTH, HEIGHT = 800, 600
WHITE, BLACK, RED, GREEN, DARK_BLUE,BLUE,YELLOW,ORANGE = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (10, 10, 50),(50, 50, 255),(255, 255, 0),(255, 165, 0)
video_path = "final_star_background (1) (1).mp4"
cap = cv2.VideoCapture(video_path)
gif_path = "shooting_final.gif"
gif = Image.open(gif_path)
# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pg_display.set_caption("Code Shooter: Python Edition")
font = pygame.font.Font("8bitoperator_jve.ttf", 36)
clock = pygame.time.Clock()

#since python doesnt have gif support, i convert the gif by frame to make the animation work
frames = []
for frame in ImageSequence.Iterator(gif): # to loop through each frame of the gif
    #The "in" keyword is used in the for loop to iterate over each frame in the ImageSequence.Iterator(gif).
    frame = frame.convert("RGBA")
    pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
    pygame_image = pygame.transform.scale(pygame_image, (50, 50))  # Resize if needed
    frames.append(pygame_image)

gif_hit_path = "shooting_hitl-export.gif"
gif_hit = Image.open(gif_hit_path)

hit_frames = []
for frame in ImageSequence.Iterator(gif_hit): # to loop through each frame of the gif
    #Similarly, "in" here is used to iterate over all frames in gif_hit.
    frame = frame.convert("RGBA")
    pygame_image = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
    pygame_image = pygame.transform.scale(pygame_image, (50, 50))  # Resize if needed
    hit_frames.append(pygame_image)

#this is all the words that will show when playing the game
word_list = [
    "PYTHON", "INTERPRETER", "SYNTAX", "variable", "constant", "FUNCTION", "METHOD", "CLASS", "object",
    "INHERITANCE", "polymorphism", "ENCAPSULATION", "abstraction", "MODULE", "PACKAGE", "library", "FRAMEWORK",
    "decorator", "generator", "ITERATOR", "lambda", "recursion", "LOOP", "for", "while", "if", "elif", "else",
    "break", "continue", "pass", "return", "yield", "try", "except", "finally", "raise", "assert", "import",
    "from", "as", "global", "nonlocal", "WITH", "async", "await", "True", "False", "None", "list", "tuple",
    "set", "dictionary", "comprehension", "f-string", "format", "STRING", "integer", "float", "BOOLEAN",
    "complex", "slice", "indexing", "enumerate", "zip", "range", "map", "filter", "reduce", "sorted",
    "exception", "handler", "docstring", "PEP8", "virtualenv", "venv", "pip", "conda", "dependency",
    "serialization", "deserialization", "pickle", "json", "csv", "sqlite", "DATABASE", "query", "API",
    "request", "response", "server", "CLIENT", "socket", "threading", "multiprocessing", "concurrency",
    "asynchronous", "GIL", "MEMORY", "garbage", "collection", "heap", "stack", "REFERENCE", "bitwise",
    "operator", "command", "shell", "terminal", "script", "automation", "environment", "configuration",
    "debugger", "profiling", "optimization", "logging", "unit", "test", "pytest", "unittest", "mock",
    "staging", "git", "repository", "commit", "push", "pull", "merge", "branch", "conflict", "clone",
    "virtualization", "deployment", "docker", "container", "pipeline", "integration", "SECURITY"
]

#this is where after the gif is converted it will resize to a specific size.
def get_video_frame(): #def defines a function that can be reusable in some code
    ret, frame = cap.read()
    if not ret: # If the frame couldn't be read
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  
        ret, frame = cap.read()
    
    frame = cv2.resize(frame, (WIDTH, HEIGHT))  
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
    frame = np.rot90(frame) 
    frame = pygame.surfarray.make_surface(frame)  
    
    return frame # Returns the processed video frame so it can be used in the game, such as displaying it on the screen.

#this is where the speed of the words while falling down
class Word: #class make it more reusable and structuewd
    def __init__(self, text, speed_multiplier=0.1): #def defines a function that can be reusable in some code
        self.text = text
        self.x = random.randint(100, WIDTH - 100)
        self.y = 0
        
        if speed_multiplier <= 5: # If the level is 5 or below
            self.speed = 0.5 + (speed_multiplier * 0.2) 
        else:
            self.speed = 0.5 + (speed_multiplier * 0.15)  #above level 6 the speed will lessen because of the computation of the speed
                                                          #I tried the Game level 6 above is too fast that's why I lessen it.
        self.alive = True # Indicates that the word is still active in the game and has not been eliminated.


    def update(self): #def defines a function that can be reusable in some code
        if self.alive: # Ensures the word moves only if it's still active
            self.y += self.speed

    def draw(self): #def defines a function that can be reusable in some code
        if self.alive:  # Ensures the word moves only if it's still active
            font = pygame.font.Font("8bitoperator_jve.ttf", 40) 

            rendered_word = []
            for char in self.text: # Loop through each character in self.text
                if char.isupper(): #Uppercase letters are orange color and Checks if the character is uppercase
                    color = (255, 165, 0)  
                else: #lower letters are white color
                    color = (255, 255, 255) 
                rendered_word.append(font.render(char, True, color))  # Ensures the word moves only if it's still active

            x_offset = 0  
            for letter in rendered_word: # # Loop through each rendered character and draw it on the screen
                screen.blit(letter, (self.x + x_offset, self.y))
                x_offset += letter.get_width()  

#as you can see the term bullet this is where the bullet where it draws a bullet, distance,shooting moving towards to the target etc
class Bullet: #class make it more reusable and structuewd
    def __init__(self, x, y, target_word): #def defines a function that can be reusable in some code
        self.x, self.y = x, y
        self.target_word = target_word
        self.speed = 5
        dx, dy = target_word.x - self.x, target_word.y - self.y
        distance = math.sqrt(dx**2 + dy**2)
        self.dx, self.dy = (dx / distance) * self.speed, (dy / distance) * self.speed

    def update(self): #def defines a function that can be reusable in some code
        # Move the bullet in the direction of the target/words
        self.x += self.dx
        self.y += self.dy

        # Check if the bullet is close enough to hit the target
        # abs(self.x - self.target_word.x) < 10 = Checks if the bullet is close horizontally
        # abs(self.y - self.target_word.y) < 10 = Checks if the bullet is close vertically
        if abs(self.x - self.target_word.x) < 10 and abs(self.y - self.target_word.y) < 10:
             # AND = If both conditions are true, the bullet is close enough to hit the target/words
            self.target_word.alive = False  #False is marks the target/words as "hit"
            return True # Tells the game that the bullet hit the target

        return False # If bullet not close enough, keep moving
 
    def draw(self): #def defines a function that can be reusable in some code
        pygame.draw.rect(screen, (255, 255, 0), (self.x, self.y, 8, 6)) 

#Player aka Rocket, this is where it shoots the words, 
class Player: #class make it more reusable and structuewd
    def __init__(self): #def defines a function that can be reusable in some code
        self.score, self.lives, self.level, self.words_destroyed = 0, 3, 1, 0
        self.typed_word, self.bullets = "", []
        self.x, self.y = WIDTH // 2, HEIGHT - 70
        self.frame_index = 0  
        self.frame_delay = 5  
        self.tick_counter = 0
        self.is_exploding = False #so that the play/rocket wont explode of the start of the game
        assert 0 <= self.lives <= 3, f"Player lives should be between 0 and 3, but got {self.lives}" #thsi will make sure the player only has 3 lives

    def update_animation(self): #def defines a function that can be reusable in some code
        self.tick_counter += 1
        if self.tick_counter >= self.frame_delay: # Checks if enough time has passed to update the animation frame
            if self.is_exploding: # Checks if the object is currently in an explosion animation
                if self.frame_index < len(hit_frames) - 1: # Ensures the explosion animation progresses only if there are more frames left
                    self.frame_index += 1  
                else:
                    return "END" # Explosion animation finished, return "END"

            else:  #This runs if 'self.is_exploding' is False
                self.frame_index = (self.frame_index + 1) % len(frames)  
            self.tick_counter = 0

    def draw(self): #def defines a function that can be reusable in some code
        if self.is_exploding: # Determines which set of frames to use when drawing (explosion or normal)
            screen.blit(hit_frames[self.frame_index], (self.x, self.y))  # Draw explosion frame  
        else:
            screen.blit(frames[self.frame_index], (self.x, self.y)) # Draw normal player frame

    def check_word(self, words): #def defines a function that can be reusable in some code
        nonlocal_typed_word = self.typed_word # Store the currently typed word
        
        def fire_bullet(): #def defines a function that can be reusable in some code
            nonlocal nonlocal_typed_word  # Allow the typed word inside this function
            # # Create a list of words that match the typed word and are still "alive" (not hit yet)
            matched_words = [word for word in words if nonlocal_typed_word == word.text and word.alive] # Find words that match the typed word **and** are still "alive" (not hit yet)
            # Loop through each matched word and fire a bullet
            for word in matched_words: #Here, "in" is used to loop through each word in matched_words.
                self.bullets.append(Bullet(self.x + 25, self.y, word))
                laser_sound.play()
            if matched_words: # Clears the typed word if there was a match to reset input for the next word
                nonlocal_typed_word = "" 

        fire_bullet()  
        self.typed_word = nonlocal_typed_word  
        # Allows modification of the nonlocal_typed_word variable inside fire_bullet(), which is defined in the outer function check_word().

    def check_typing(self, words): #def defines a function that can be reusable in some code
        for word in words:  # Loops through each word in the list of words
            if not word.alive:  # Skips checking words that have already been eliminated
                continue #skip the rest of the current loop iteration and move to the next one.
            if word.text.startswith(self.typed_word): # Checks if the currently typed word matches the start of any falling word
                return GREEN  # Returns GREEN if the typed word matches the beginning of any falling word, indicating correct input.
        return RED  # Returns RED if no words start with the typed input, indicating incorrect input.
    
    def special_ability(self): #def defines a function that can be reusable in some code
        pass #skips from a mean time for future updates
#this is where generating of what words will fall down and it depends on the level
def generate_words(num_words, level): #def defines a function that can be reusable in some code
    if not word_list:  # Check if the word list is empty
        return None  # Return None if no words are available to generate
    existing_words = []
    
    if level <= 10: # Determines the word length range based on the level (short words for early levels)
        filtered_words = [word for word in word_list if 3 <= len(word) <= 4] # Choose short words (3-4 letters)
    elif level <= 20: #the elif here below 20 levels the words that will falldown are now 4-6 letters
        filtered_words = [word for word in word_list if 4 <= len(word) <= 6] # Choose medium words (4-6 letters)
    else: #above 21 ALL the words in the word_list will be chosen
        filtered_words = word_list 

    filtered_words = list(filtered_words) 
    num_words = min(num_words, len(filtered_words))
    selected_words = sorted(random.sample(filtered_words, num_words), key=lambda word: len(word))
    # Sorts the selected words based on their length using a lambda function, ensuring shorter words appear first.

    # Loop through each selected word to place it on the screen
    for word_text in selected_words:
        placed = False # track whether a word has been successfully placed on the screen.
        attempts = 0

        # Try placing the word at a random position
        while not placed and attempts < 20: # Continue trying to place the word until it is placed or 20 attempts are reached
            new_x = random.randint(100, WIDTH - 100)# Random x position within screen limits
            new_y = random.randint(-200, -50)# Start above the screen

            # Ensure words do not overlap (check distance between words)
            if all(math.hypot(new_x - w.x, new_y - w.y) > 80 for w in existing_words):  # Ensures words are not placed too close to each other
                word_obj = Word(word_text, speed_multiplier=level)
                word_obj.x, word_obj.y = new_x, new_y
                existing_words.append(word_obj)  
                # Yielding the word object here allows the function to return the word object one by one,
                # allowing the caller to handle the word immediately without waiting for all words to be placed.
                yield word_obj  
                placed = True #function ensures that the condition (distance between words) must be true for every word in the existing_words list for the new word to be placed.

            attempts += 1

        if not placed: # If no valid position was found after attempts, place the word anyway
            word_obj = Word(word_text, speed_multiplier=level)
            existing_words.append(word_obj)
            
            yield word_obj  # Yield the word object even if it could not be placed in the valid area after attempts

#MAIN FUNCTION of the gameplay
def game(): #def defines a function that can be reusable in some code
    global high_score #this variable can have access to all classes
    try: #attempting of executing
        player = Player()
        words = list(generate_words(5, player.level))  
        if not words: # Checks if the words list is empty and initializes it if necessary
            words = []
        
        player.words_spawned = len(words)
        print(f"Level {player.level}: Spawned {player.words_spawned} words.")
        running = True #the game loop will start running.
        paused = False #so it wont be paused on start of the game

        while running: #loops
            frame_surface = get_video_frame()
            screen.blit(frame_surface, (0, 0))

            # Event handling loop: checks for user input and game events
            for event in pygame.event.get(): #The "in" keyword is used to iterate through the list of events returned by pygame.event.get().
                if event.type == pygame.QUIT: # Checks if the user closes the game window
                    running = False #to stop the gameplay
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN: # If a key is pressed
                    if event.key == pygame.K_ESCAPE: # Checks if the Escape key is pressed to pause the game
                        paused = not paused
                        if paused: # If the game is paused, show the pause menu
                            show_pause_menu()
                            paused = False # initialize the game as unpaused 

                    if not paused and not player.is_exploding: #If either the game is paused or the player is exploding, the player should not be able to type or delete words.
                        if event.key == pygame.K_BACKSPACE: # If Backspace is pressed, delete the last character
                            player.typed_word = player.typed_word[:-1]
                        elif event.unicode.isalnum():# If the key is a letter or number
                            player.typed_word += event.unicode
                            player.check_word(words)

            if not player.is_exploding: # Ensures words continue moving only if the player is not exploding
                for word in words[:]:  #Iterate over a copy of the list to avoid modifying it while iterating
                    word.update()
                    word.draw()

                    if word.y > HEIGHT and word.alive: #If only one condition is met, the word is not counted as lost
                        words.remove(word)
                        pygame.mixer.Sound("loselife.mp3").play()
                        player.lives -= 1
                        player.words_destroyed += 1
                        print(f"Word lost! {player.words_destroyed}/{player.words_spawned} words accounted for.")

                        if player.lives <= 0:
                            print("Game Over!")
                            pygame.mixer.music.stop()
                            rocket_hit_sound.play()
                            player.is_exploding = True # Sets the flag to True, indicating the player is in an exploding state, which may trigger explosion animations and stop the game
                            player.frame_index = 0
                            

            if player.is_exploding: # If the player runs out of lives, trigger game over
                if player.update_animation() == "END": # If the explosion animation is done, end the game
                    pygame.time.delay(1000)
                    running = False #the loop/gameplay ends
                    show_game_over_screen(screen, player.score, high_score)

            for bullet in player.bullets[:]: # Iterate over a copy of the bullets list
                bullet.update()
                bullet.draw()
                if bullet.y < bullet.target_word.y + 20: # Checks if the bullet has reached its target word
                    if bullet.target_word.alive:  # If the target word is still active, mark it as destroyed and update the score
                        sound = random.choice(explode_sounds)
                        sound.play()
                        bullet.target_word.alive = False #The word is marked as destroyed
                        print(f"Word destroyed! {player.words_destroyed}/{player.words_spawned} words eliminated.")

                        word_length = len(bullet.target_word.text)
                        points = 5 if word_length <= 4 else 10 if word_length <= 7 else 15 # Assign points based on word length: 5 (≤4), 10 (5-7), 15 (>7)
                        if player.lives == 3:  # If the player has full lives, grant bonus points
                            points += 10

                        player.score += points
                        player.words_destroyed += 1
                        print(f"Scored {points} points! Total: {player.score}")

                    player.bullets.remove(bullet)
                    del bullet #after hitting the bullet will be remove

            if player.score > high_score: # Updates the high score if the player's score surpasses it
                high_score = player.score
                save_high_score(high_score)

            player.update_animation()
            player.draw()
            text_color = player.check_typing(words)
            input_surface = font.render(player.typed_word, True, text_color) # True enables anti-aliasing for smoother, better-quality text rendering
            screen.blit(input_surface, (player.x + 10, player.y - 30))
            lives_surface = font.render(f"Lives: {player.lives}", True, RED) # True enables anti-aliasing for smoother, better-quality text rendering
            screen.blit(lives_surface, (10, 10))
            level_surface = font.render(f"Level: {player.level}", True, GREEN) # True enables anti-aliasing for smoother, better-quality text rendering
            screen.blit(level_surface, (10, HEIGHT - 40))
            score_surface = font.render(f"Score: {player.score}", True, YELLOW) # True enables anti-aliasing for smoother, better-quality text rendering
            screen.blit(score_surface, (WIDTH - score_surface.get_width() - 10, HEIGHT - 40))

            words_left = player.words_spawned - player.words_destroyed
            print(f"Words left to destroy before leveling up: {words_left}")
            # If all words are destroyed and the player still has lives, level up
            if words_left == 0 and player.lives > 0: #if words are 0 but theres still lives continue the gameplay 
                levelup_sound.play()
                print(f"Level Up! Now at Level {player.level + 1}")
                player.level += 1
                player.words_destroyed = 0

                words = list(generate_words(min(5 + player.level // 2, 10), player.level)) 
                player.words_spawned = len(words)
                print(f"Level {player.level} started. Spawned {player.words_spawned} words.")

            pg_display.update()
            clock.tick(30)

        print("Game loop ended")

    except Exception as e: #If an error occurs in game(), Python catches it and stores the error in e and "except"  is used to catch and handle errors
        print("An error occurred in the game loop:")
        traceback.print_exc()  
#game over screen
def show_game_over_screen(screen, score, high_score): #def defines a function that can be reusable in some code
    font = pygame.font.Font("8bitoperator_jve.ttf", 50)
    game_over_font = pygame.font.Font("8bitoperator_jve.ttf", 80)
    screen.fill(BLACK)
    gameover.play()
  
    game_over_surface = game_over_font.render("GAME OVER", True, RED)  # True enables anti-aliasing for smoother text edges
    retry_surface = font.render("Press R to Retry", True, GREEN)  # True enables anti-aliasing for smoother text edges
    quit_surface = font.render("Press Q to Main Menu", True, RED)  # True enables anti-aliasing for smoother text edges
    score_surface = font.render(f"Score: {score}", True, WHITE)  # True enables anti-aliasing for smoother text edges
    high_score_surface = font.render(f"High Score: {high_score}", True, WHITE)  # True enables anti-aliasing for smoother text edges

    game_over_rect = game_over_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 120))
    score_rect = score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    high_score_rect = high_score_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 15))
    retry_rect = retry_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 80))
    quit_rect = quit_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 130))

    screen.blit(game_over_surface, game_over_rect)
    screen.blit(score_surface, score_rect)
    screen.blit(high_score_surface, high_score_rect)
    screen.blit(retry_surface, retry_rect)
    screen.blit(quit_surface, quit_rect)

    pygame.display.flip()

    waiting = True #making the waiting be True
    while waiting: #loops
        for event in pygame.event.get(): # Event handling loop: listens for player input
            if event.type == pygame.QUIT: # Checks if the player closes the game window
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_r:  # If the "R" key is pressed, restart the game
                    pygame.mixer.music.load("music.mp3") 
                    pygame.mixer.music.play(-1)  
                    waiting = False #Stops the waiting loop once the player presses the "R" key.
                    game()  
                elif event.key == pygame.K_q: #Press Q to return to main menu
                    retry()

#pause screen
def show_pause_menu():  # Defines a function that can be reusable in some code
    menu_font = pygame.font.Font("8bitoperator_jve.ttf", 50)
    text_surface = menu_font.render("Paused - Press ESC to Resume", True, YELLOW)  # True enables anti-aliasing for smoother text edges
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 3))

    # Additional text for menu options
    instructions_font = pygame.font.Font("8bitoperator_jve.ttf", 30)
    instructions_text = [
        "E to go back to main menu",
        "Q to quit"
    ]
    instruction_surfaces = [instructions_font.render(line, True, GREEN) for line in instructions_text]
    instruction_rects = [text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + (i) * 40)) for i, text in enumerate(instruction_surfaces)]

    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)

    screen.blit(overlay, (0, 0))
    screen.blit(text_surface, text_rect)
    for surface, rect in zip(instruction_surfaces, instruction_rects):
        screen.blit(surface, rect)
    pg_display.update()

    while True:  # Loops
        for event in pygame.event.get():  # Loops through all events in the event queue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Press ESC to resume
                    return  # Exits the function when ESC is pressed, resuming the game.
                elif event.key == pygame.K_e:  # Press E to go back to the main menu
                    retry()  # Call your retry function to go back to the main menu
                elif event.key == pygame.K_q:  # Press Q to quit
                    pygame.quit()  # Quits the game
                    quit()
            elif event.type == pygame.QUIT:  # Handle window close
                retry()
#this is where the rettrieval of highscore 
def load_high_score(): #def defines a function that can be reusable in some code
    if os.path.exists(HIGH_SCORE_FILE): # Checks if the high score file exists
        with open(HIGH_SCORE_FILE, "r") as file:  # 'as file' gives a temporary name 'file' to the opened file object.
            return int(file.read().strip()) # Returns the high score as an integer if the file exists.
    return 0 # Returns 0 if the high score file does not exist, ensuring a default score.
 #now this is where rewrites the highscore if its surpasses
def save_high_score(score): #def defines a function that can be reusable in some code
    with open(HIGH_SCORE_FILE, "w") as file: # 'as file' assigns 'file' as the reference to the opened file.
        file.write(str(score))

high_score = load_high_score()
#main menu
def main_menu(): #def defines a function that can be reusable in some code
    global high_score #this variable can have access to all classes
    while True: #loops this function
        frame_surface = get_video_frame()  
        screen.blit(frame_surface, (0, 0))  

        pixel_font = pygame.font.Font("8bitoperator_jve.ttf", 60) 
        menu_font = pygame.font.Font("8bitoperator_jve.ttf", 36)  
        small_font = pygame.font.Font("8bitoperator_jve.ttf", 20)  

        title_surface = pixel_font.render("Typing Shooter Game", True, ORANGE) # True enables anti-aliasing for smoother text edges
        title_x = WIDTH // 2 - title_surface.get_width() // 2
        title_y = HEIGHT // 4
        screen.blit(title_surface, (title_x, title_y))

        highscore_surface = menu_font.render(f"High Score: {high_score}", True, WHITE) # True enables anti-aliasing for smoother text edges
        highscore_x = WIDTH // 2 - highscore_surface.get_width() // 2
        highscore_y = HEIGHT // 2 - 50 
        screen.blit(highscore_surface, (highscore_x, highscore_y))

        start_surface = menu_font.render("Press ENTER to Start", True, GREEN) # True enables anti-aliasing for smoother text edges
        instructions_surface = menu_font.render("Press I for Instructions", True, YELLOW) # True enables anti-aliasing for smoother text edges
        quit_surface = menu_font.render("Press ESC to Quit", True, RED) # True enables anti-aliasing for smoother text edges
 
        start_x = WIDTH // 2 - start_surface.get_width() // 2
        instructions_x = WIDTH // 2 - instructions_surface.get_width() // 2
        quit_x = WIDTH // 2 - quit_surface.get_width() // 2

        screen.blit(start_surface, (start_x, HEIGHT // 2 + 30))  
        screen.blit(instructions_surface, (instructions_x, HEIGHT // 2 + 70))  
        screen.blit(quit_surface, (quit_x, HEIGHT // 2 + 110))

        dev_surface = small_font.render("Developed by: Viezel Manzano", True, WHITE) # True enables anti-aliasing for smoother text edges
        dev_x = WIDTH - dev_surface.get_width() - 10
        dev_y = HEIGHT - dev_surface.get_height() - 10
        screen.blit(dev_surface, (dev_x, dev_y))

        activity_surface = small_font.render("Activity Project by: Sir John Peñaredondo", True, WHITE) # True enables anti-aliasing for smoother text edges
        activity_x = 10
        activity_y = HEIGHT - activity_surface.get_height() - 10
        screen.blit(activity_surface, (activity_x, activity_y))

        pg_display.update()

        for event in pygame.event.get(): # Loops through all events in the event queue
            if event.type == pygame.QUIT: # Exiting if the player closes the game
                pygame.quit()
                exit()
                break #to stop the loop when exiting
            elif event.type == pygame.KEYDOWN: # If a key is pressed
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN: # Press either SPACE or ESC to resume
                    return #resume the game
                elif event.key == pygame.K_i:  # Show instructions when 'I' key is pressed
                    show_instructions()
                elif event.key == pygame.K_ESCAPE: # Quit game if Escape key is pressed
                    pygame.quit()
                    exit() 
                    break #to stop the loop when exiting
#the instructions screen to how to play
def show_instructions(): #def defines a function that can be reusable in some code
    gameplay_screenshot = pygame.image.load("Screenshot 2025-03-27 094331.png")
    max_width = 350  
    scale_factor = max_width / gameplay_screenshot.get_width()
    new_height = int(gameplay_screenshot.get_height() * scale_factor)
    gameplay_screenshot = pygame.transform.scale(gameplay_screenshot, (max_width, new_height))

    while True: #loops this function
        screen.fill(BLACK)  
        instructions_font = pygame.font.Font("8bitoperator_jve.ttf", 26)  

        screenshot_x = WIDTH // 2 - gameplay_screenshot.get_width() // 2
        screenshot_y = 40  
        screen.blit(gameplay_screenshot, (screenshot_x, screenshot_y))

        instructions = [
            "HOW TO PLAY:",
            "- Type the correct words to shoot them.",
            "- Each word moves downwards; don't let them reach the bottom!",
            "- The faster you type, the better your score!",
            "- Press ESC to Pause the game.",
            "",
            "Press ESC to return to Main Menu"
        ]

        y_offset = screenshot_y + gameplay_screenshot.get_height() + 20  
        for line in instructions: # Loop through each instruction line 
            text_surface = instructions_font.render(line, True, WHITE)  # True enables anti-aliasing for smoother text edges
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_offset))
            y_offset += 35  

        pg_display.update()
 
        for event in pygame.event.get():  # Loop through all queued events
            if event.type == pygame.QUIT: #Closes 
                pygame.quit()
            if event.type == pygame.KEYDOWN:  # If a key is pressed
                if event.key == pygame.K_ESCAPE: #Press escape to return to main menu
                    return  #returns to main menu
                
#this is just a like a support to start the game 
def retry(): #def defines a function that can be reusable in some code
    while True:  # Creates an infinite loop
        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")  
        pygame.mixer.music.play(-1)  
        pygame.mixer.music.set_volume(0.1)  
        main_menu()
        try: #attempting of executing
            game()
        except Exception as e:#If an error occurs in game(), Python catches it and stores the error in e and "except"  is used to catch and handle errors
            print("An error occurred:", e)
            pygame.quit()  
            raise  # Re-raises the caught exception to allow it to propagate further, ensuring debugging information is not lost
        finally: #block ensures that certain code runs no matter what, whether an error occurs in try or not.
            print("Game session ended.")
            pygame.time.delay(2000)  

retry()