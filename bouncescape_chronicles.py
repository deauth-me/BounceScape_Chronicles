import pygame
import random
import json
import os
import sys


# Set the working directory to the directory of this script
os.chdir(os.path.dirname(os.path.abspath(__file__)))



# Colors (Define constants for colors)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 200, 0)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)


# Define constants for screen size
WIDTH, HEIGHT = 500, 600


# Define constants for difficulty levels
EASY = 0
MEDIUM = 1
HARD = 2
INSANE = 3


# Define constants for ball and paddle properties
BALL_RADIUS = 15
PADDLE_WIDTH = 75
PADDLE_HEIGHT = 10
PADDLE_SPEED = 5



# To make the sound effect more instant and sharp
pygame.mixer.pre_init(44100, -16, 2, 512)


# Initialize pygame
pygame.init()
pygame.mixer.init()


# Loading files for sound and graphics

# Check if the script is running as a bundled executable
def resource_path(relative_path):
    # Get absolute path to resource, works for dev and for pyinstaller
    if getattr(sys, 'frozen', False):
        # The application is frozen (it's an exe)
        base_path = sys._MEIPASS
    else:
        # The application is not frozen
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# Loading files for sound and graphics

bounce_effect = pygame.mixer.Sound(resource_path("effect2.wav"))
bounce_effect.set_volume(0.5)

background = pygame.image.load(resource_path("image_newyork.jpg"))
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

startmenu_image = pygame.image.load(resource_path("image_newyork.jpg"))
startmenu_image = pygame.transform.scale(startmenu_image, (WIDTH, HEIGHT))




screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("BounceScape Chronicles")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)


title_font = pygame.font.SysFont(None, 50)  
rules_font = pygame.font.SysFont(None, 30)


# Define a GameState class to store game-related information
class GameState:
    def __init__(self):
        self.difficulty = EASY
        self.score = 0
        self.player_name = ""

def read_high_score():
    try:
        with open("high_score.json", "r") as file:
            high_score_data = json.load(file)
    except FileNotFoundError:
        # If the file doesn't exist, return an empty dictionary
        high_score_data = {}

    player_name = high_score_data.get("player_name", None)
    score = high_score_data.get("score", 0)

    return player_name, score



def update_high_score(player_name, score):
    high_score_data = {"player_name": player_name, "score": score}
    with open("high_score.json", "w") as file:
        json.dump(high_score_data, file)

def vibrate_button(vibration_intensity, original_position):
    new_x = original_position[0] + random.randint(-vibration_intensity, vibration_intensity)
    new_y = original_position[1] + random.randint(-vibration_intensity, vibration_intensity)
    return new_x, new_y

def input_name_screen():
    
    font_large = pygame.font.SysFont(None, 72)
    name_text = font_large.render("Enter Your Name", True, BLACK)

    name = ""

    def draw_screen():
        screen.blit(startmenu_image, (0, 0))
        screen.blit(name_text, (WIDTH // 2 - name_text.get_width() // 2, HEIGHT // 4))
        name_input_text = font.render(name, True, BLACK)
        screen.blit(name_input_text, (WIDTH // 2 - name_input_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

    draw_screen()  # Initial draw

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return name
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode
                draw_screen()  # Redraw the screen only if name changes

        clock.tick(60)



# Function to draw a button
def draw_button(color, x, y, width, height, text=''):
    pygame.draw.rect(screen, color, (x, y, width, height))
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
    screen.blit(text_surface, text_rect)

def play_music():
    pygame.mixer.music.load(resource_path("8bit.mp3"))
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.3)
    

# Function to display the start menu
def start_menu():
    intro = True

    record_holder, high_score = read_high_score()

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background, (0, 0))
        title = title_font.render('BounceScape Chronicles', True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 100))

        # Display the high score in the menu
        high_score_text = rules_font.render(f"High score: {high_score}", True, BLACK)
        screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 250))

        record_holder_text = rules_font.render(f"Played by: {record_holder}", True, BLACK)
        screen.blit(record_holder_text, (WIDTH // 2 - record_holder_text.get_width() // 2, 280))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        play_btn_pos = (50, 250)
        quit_btn_pos = (50, 310)

        # Check if mouse is over the 'Play' button
        if 250 + 50 > mouse[1] > 250 and 100 + 100 > mouse[0] > 100:
            play_btn_pos = vibrate_button(1, play_btn_pos)
            draw_button(WHITE, *play_btn_pos, 100, 50, 'Play')
            if click[0] == 1:
                pygame.time.wait(200)
                player_name = input_name_screen()
                difficulty = select_difficulty()
                game_state = GameState()
                game_state.player_name = player_name
                game_state.difficulty = difficulty
                play_music()
                game_loop(game_state)
        else:
            draw_button(WHITE, *play_btn_pos, 100, 50, 'Play')

        # Check if mouse is over the 'Quit' button
        if 310 + 50 > mouse[1] > 310 and 100 + 100 > mouse[0] > 100:
            quit_btn_pos = vibrate_button(1, quit_btn_pos)
            draw_button(WHITE, *quit_btn_pos, 100, 50, 'Quit')
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            draw_button(WHITE, *quit_btn_pos, 100, 50, 'Quit')

        pygame.display.flip()
        clock.tick(60)

# Function to display the difficulty selection screen
def select_difficulty():
    pygame.time.wait(200)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        screen.blit(background, (0, 0))
        title = font.render('Select Difficulty', True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))

        levels = ['Easy', 'Medium', 'Hard', 'Insane']
        colors = [WHITE, WHITE, WHITE, WHITE]  
        intensities = [1, 2, 3, 4]

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        rules_text = [
                      "Move the paddle using arrow keys.",
                      "Pause the game hitting spacebar."]
        
        for i, rule in enumerate(rules_text):
            line = rules_font.render(rule, True, BLACK)
            screen.blit(line, (WIDTH // 2 - line.get_width() // 2, 70 + i * 40))

        for i, (level, color, intensity) in enumerate(zip(levels, colors, intensities)):
            btn_y = 250 + i * 60

            if 100 < mouse[0] < WIDTH - 100 and btn_y < mouse[1] < btn_y + 50:
                btn_y = vibrate_button(intensity, (0, btn_y))[1]
                pygame.draw.rect(screen, color, (100, btn_y, WIDTH - 200, 50))
                if click[0] == 1:
                    return i  # Return the index of the chosen difficulty
            else:
                pygame.draw.rect(screen, color, (100, btn_y, WIDTH - 200, 50))
            
            level_text = font.render(level, True, BLACK)
            screen.blit(level_text, (WIDTH // 2 - level_text.get_width() // 2, btn_y + 15))

        pygame.display.flip()
        clock.tick(60)



# Function to display the game over screen
def game_over_screen(game_state):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.mixer.music.set_volume(0.1)
        # pygame.mixer.music.stop()

        screen.fill(WHITE)
        screen.blit(startmenu_image, (0, 0))
        
        font_large = pygame.font.SysFont(None, 72)
        game_over_text = font_large.render("GAME OVER", True, BLACK)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 4))

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        # Display player's name and high score in the game over screen
        player_name_text = font.render(f"Player: {game_state.player_name}", True, BLACK)
        screen.blit(player_name_text, (WIDTH // 2 - player_name_text.get_width() // 2, HEIGHT // 2 - 40))

        score_display = font.render(f"Score: {game_state.score}", True, BLACK)
        screen.blit(score_display, (WIDTH // 2 - score_display.get_width() // 2, HEIGHT // 2 - score_display.get_height() // 2))

        btn_y = HEIGHT * 3/4
        if 100 + 100 > mouse[0] > 100 and btn_y + 50 > mouse[1] > btn_y:
            btn_y = vibrate_button(1, (100, btn_y))[1]
            draw_button(WHITE, 100, btn_y, 100, 50, 'Retry')
            if click[0] == 1:
                game_state.score = 0  # Reset the score to zero
                game_state.difficulty = select_difficulty()
                play_music()
                game_loop(game_state)
        else:
            draw_button(WHITE, 100, btn_y, 100, 50, 'Retry')

        btn_y = HEIGHT * 3/4
        if WIDTH - 200 + 100 > mouse[0] > WIDTH - 200 and btn_y + 50 > mouse[1] > btn_y:
            btn_y = vibrate_button(1, (WIDTH - 200, btn_y))[1]
            draw_button(WHITE, WIDTH - 200, btn_y, 100, 50, 'Quit')
            if click[0] == 1:
                pygame.quit()
                quit()
        else:
            draw_button(WHITE, WIDTH - 200, btn_y, 100, 50, 'Quit')

        # Check if the current score is higher than the high score
        record_holder, high_score = read_high_score()

        if game_state.score > high_score:
            update_high_score(game_state.player_name, game_state.score)

        pygame.display.flip()
        clock.tick(60)


# Function to update the game logic
def update_game_logic(ball_pos, ball_speed, paddle_pos, game_state, last_ball_pos):
    # Save last ball position for tunneling detection
    last_ball_pos[0], last_ball_pos[1] = ball_pos[0], ball_pos[1]
    
    ball_pos[0] += ball_speed[0]
    ball_pos[1] += ball_speed[1]

    # wall collision
    if ball_pos[0] <= BALL_RADIUS or ball_pos[0] >= WIDTH - BALL_RADIUS:
        ball_speed[0] = -ball_speed[0]

    if ball_pos[1] <= BALL_RADIUS:
        ball_speed[1] = -ball_speed[1]
        ball_pos[1] = BALL_RADIUS  # Adjust ball position so it doesn't stick to the top

    # Paddle collision
    
    paddle_top = paddle_pos[1]
    paddle_bottom = paddle_pos[1] + PADDLE_HEIGHT
    
    # Check if the ball passed through the paddle
    passed_through_paddle = (last_ball_pos[1] + BALL_RADIUS <= paddle_top and ball_pos[1] + BALL_RADIUS >= paddle_bottom) or \
                            (ball_pos[1] - BALL_RADIUS <= paddle_top and last_ball_pos[1] - BALL_RADIUS >= paddle_bottom)

    # Check if the center of the ball is within the width of the paddle
    within_paddle_width = paddle_pos[0] - BALL_RADIUS < ball_pos[0] < paddle_pos[0] + PADDLE_WIDTH + BALL_RADIUS

    if within_paddle_width and (passed_through_paddle or (paddle_top < ball_pos[1] + BALL_RADIUS < paddle_bottom)):
        ball_speed[1] = -ball_speed[1]  
        
        bounce_effect.play()
        
        game_state.score += 1

        # Increase speed of the ball every 10 points by 1
        if game_state.score % 10 == 0:
            ball_speed[0] += 1 if ball_speed[0] > 0 else -1
            ball_speed[1] += 1 if ball_speed[1] > 0 else -1

    # Check game over condition
    if ball_pos[1] >= HEIGHT + BALL_RADIUS:
        game_over_screen(game_state)


# Function to draw the game objects
def draw_game_objects(ball_pos, paddle_pos, game_state):

    screen.blit(background, (0, 0))

    # Draw ball
    pygame.draw.circle(screen, GREEN, (int(ball_pos[0]), int(ball_pos[1])), BALL_RADIUS)

    # Draw paddle
    pygame.draw.rect(screen, WHITE, (int(paddle_pos[0]), int(paddle_pos[1]), PADDLE_WIDTH, PADDLE_HEIGHT))

    # Draw score
    score_text = font.render(f"Score: {game_state.score}", True, BLACK)
    screen.blit(score_text, (10, 10))

# Function to run the game loop
def game_loop(game_state):

    paused = False
    screen.blit(background, (0, 0))

    ball_pos = [random.randint(0, WIDTH), random.randint(0, HEIGHT // 2)]
    # Initialize last_ball_pos with the current ball_pos
    last_ball_pos = ball_pos.copy()

    paddle_pos = [WIDTH / 2 - PADDLE_WIDTH / 2, HEIGHT - 2 * PADDLE_HEIGHT]

    # Set ball_speed based on the selected difficulty level
    if game_state.difficulty == EASY:
        ball_speed = [2, 2]
    elif game_state.difficulty == MEDIUM:
        ball_speed = [3, 3]
    elif game_state.difficulty == HARD:
        ball_speed = [5, 5]
    else:  # INSANE
        ball_speed = [7, 7]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                    if paused:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

        # Pause loop
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    paused = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        paused = not paused
                        pygame.mixer.music.unpause()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_pos[0] > 0:
            paddle_pos[0] -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle_pos[0] + PADDLE_WIDTH < WIDTH:
            paddle_pos[0] += PADDLE_SPEED

        # Pass the last_ball_pos to the update function
        update_game_logic(ball_pos, ball_speed, paddle_pos, game_state, last_ball_pos)
        draw_game_objects(ball_pos, paddle_pos, game_state)

        pygame.display.flip()
        clock.tick(60)

    
    pygame.quit()
    quit()

    

# Function to start the game from the start menu
def run_game():
    high_score_value = read_high_score()
    player_name = None
    start_menu()

    # Get the player's name from the start menu
    player_name = input_name_screen()

    difficulty = select_difficulty()
    game_state = GameState()
    game_state.player_name = player_name
    game_state.difficulty = difficulty
    game_state.score = game_loop(game_state)

    game_over_screen(game_state)

# Run the game
if __name__ == "__main__":
    run_game()
