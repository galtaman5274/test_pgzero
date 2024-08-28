import pgzrun
import pygame
import sys

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Load the sprite sheet for the hero
SPRITE_SHEET = pygame.image.load('assets/sprites/roguelikeChar_transparent.png')

# Load background music
pygame.mixer.music.load('assets/music/background_music.mp3')
pygame.mixer.music.set_volume(0.5)  # Set the volume level

# Load movement sound effect
MOVE_SOUND = pygame.mixer.Sound('assets/sounds/move.ogg')
MOVE_SOUND.set_volume(0.2)  # Adjust the sound effect volume

# Tile and margin sizes
TILE_SIZE = 16
MARGIN = 1

# Number of frames for the hero's animation
NUM_COLUMNS = 4  # Assuming the animation uses 4 frames for the hero in a single row

# Create a list to store individual frames for the hero
frames = []

# Extract each frame from the sprite sheet
for col in range(NUM_COLUMNS):
    x = col * (TILE_SIZE + MARGIN)
    y = 0  # Assuming the hero's frames are on the first row
    frame = SPRITE_SHEET.subsurface(pygame.Rect(x, y, TILE_SIZE, TILE_SIZE))
    frames.append(frame)

# Define button properties (positions and dimensions)
START_BUTTON = {"rect": Rect((WIDTH // 2 - 100, HEIGHT // 2 - 20), (200, 50)), "text": "Start Game"}
EXIT_BUTTON = {"rect": Rect((WIDTH // 2 - 100, HEIGHT // 2 + 100), (200, 50)), "text": "Exit"}

# Game Over buttons
GO_MENU_BUTTON = {"rect": Rect((WIDTH // 2 - 100, HEIGHT // 2 + 20), (200, 50)), "text": "Main Menu"}
EXIT_BUTTON_GAMEOVER = {"rect": Rect((WIDTH // 2 - 100, HEIGHT // 2 + 90), (200, 50)), "text": "Exit"}

# Game state
music_on = True  # Music starts as on


def draw_main_menu():
    """Draws the main menu."""
    screen.draw.text("MAIN MENU", center=(WIDTH // 2, HEIGHT // 4), fontsize=60, color="white")

    screen.draw.filled_rect(START_BUTTON["rect"], "green")
    screen.draw.text(START_BUTTON["text"], center=START_BUTTON["rect"].center, fontsize=40, color="white")

    toggle_color = "blue" if music_on else "gray"
    screen.draw.filled_rect(Rect((WIDTH // 2 - 200, HEIGHT // 2 + 40), (400, 50)), toggle_color)
    screen.draw.text("Toggle Music/Sound", center=(WIDTH // 2, HEIGHT // 2 + 65), fontsize=40, color="white")

    screen.draw.filled_rect(EXIT_BUTTON["rect"], "red")
    screen.draw.text(EXIT_BUTTON["text"], center=EXIT_BUTTON["rect"].center, fontsize=40, color="white")


class Enemy:
    """Enemy class encapsulates enemy behavior."""

    def __init__(self, image, start_pos, patrol_area, speed_x, speed_y):
        self.actor = Actor(image, start_pos)
        self.patrol_area = patrol_area
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        """Updates the position of the enemy within its patrol area."""
        self.actor.x += self.speed_x
        if self.actor.x < self.patrol_area[0] or self.actor.x > self.patrol_area[1]:
            self.speed_x *= -1

        self.actor.y += self.speed_y
        if self.actor.y < self.patrol_area[2] or self.actor.y > self.patrol_area[3]:
            self.speed_y *= -1

    def draw(self):
        """Draws the enemy."""
        self.actor.draw()

    def check_collision(self, rect):
        """Checks if the enemy collides with the given rect (hero)."""
        return self.actor.colliderect(rect)


def create_enemies():
    """Creates a list of enemies."""
    return [
        Enemy('alien', (100, 100), (50, 250, 50, 250), 2, 2),
        Enemy('alien', (400, 300), (350, 450, 250, 350), -2, 2),
        Enemy('alien', (600, 200), (550, 750, 100, 400), 2, -2),
    ]


# Animation settings for the hero
current_frame = 0
animation_speed = 0.2  # Time delay between frames
animation_timer = 0

# Hero position and speed
hero_pos = [WIDTH // 4, HEIGHT // 4]
hero_speed = 3

# Game state
game_over = False
game_active = False


def reset_game():
    """Resets the game state to start a new game."""
    global hero_pos, game_over, enemies, current_frame, animation_timer
    hero_pos = [WIDTH // 3, HEIGHT // 3]  # Reset hero position
    game_over = False  # Reset game over state
    current_frame = 0  # Reset animation frame
    animation_timer = 0  # Reset animation timer
    enemies = create_enemies()  # Recreate the enemies


def draw():
    """Main draw function."""
    screen.clear()
    if not game_active:
        draw_main_menu()
    else:
        draw_gameplay()


def draw_gameplay():
    """Draws the gameplay."""
    screen.clear()
    if game_over:
        screen.draw.text("Game Over", center=(WIDTH // 2, HEIGHT // 2 - 60), fontsize=60, color="red")
        screen.draw.filled_rect(GO_MENU_BUTTON["rect"], "green")
        screen.draw.text(GO_MENU_BUTTON["text"], center=GO_MENU_BUTTON["rect"].center, fontsize=40, color="white")
        screen.draw.filled_rect(EXIT_BUTTON_GAMEOVER["rect"], "red")
        screen.draw.text(EXIT_BUTTON_GAMEOVER["text"], center=EXIT_BUTTON_GAMEOVER["rect"].center, fontsize=40, color="white")
    else:
        screen.blit(frames[int(current_frame)], hero_pos)
        for enemy in enemies:
            enemy.draw()


def on_mouse_down(pos):
    """Handles mouse click events."""
    global game_active, game_over, music_on

    if not game_active:
        if START_BUTTON["rect"].collidepoint(pos):
            reset_game()
            game_active = True
            if music_on:
                pygame.mixer.music.play(-1)
        elif Rect((WIDTH // 2 - 200, HEIGHT // 2 + 40), (400, 50)).collidepoint(pos):
            music_on = not music_on
            if music_on:
                pygame.mixer.music.play(-1)
            else:
                pygame.mixer.music.pause()
        elif EXIT_BUTTON["rect"].collidepoint(pos):
            sys.exit()

    elif game_over:
        if GO_MENU_BUTTON["rect"].collidepoint(pos):
            game_active = False
            pygame.mixer.music.pause()
        elif EXIT_BUTTON_GAMEOVER["rect"].collidepoint(pos):
            sys.exit()


def update(dt):
    """Main update function."""
    global current_frame, animation_timer, game_over

    if game_active and not game_over:
        moving = False
        if keyboard.left:
            hero_pos[0] -= hero_speed
            moving = True
        if keyboard.right:
            hero_pos[0] += hero_speed
            moving = True
        if keyboard.up:
            hero_pos[1] -= hero_speed
            moving = True
        if keyboard.down:
            hero_pos[1] += hero_speed
            moving = True

        if moving:
            MOVE_SOUND.play()

        if moving:
            animation_timer += dt
            if animation_timer >= animation_speed:
                current_frame = (current_frame + 1) % len(frames)
                animation_timer = 0
        else:
            current_frame = 0

        hero_rect = pygame.Rect(hero_pos[0], hero_pos[1], TILE_SIZE, TILE_SIZE)

        for enemy in enemies:
            enemy.update()
            if enemy.check_collision(hero_rect):
                game_over = True
                break


# Initialize the game state
enemies = create_enemies()

pgzrun.go()
