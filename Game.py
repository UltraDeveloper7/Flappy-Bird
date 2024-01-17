import pygame,os

from FlappyBird import FlappyBird

pygame.init()

# Set window dimensions and constants
WIDTH = 576
HEIGHT = 980
floor_x_pos = 0
clouds_x_pos = 0

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
font = pygame.font.Font('04B_19.ttf', 20)

# Render text surface
text_surface = font.render("Pick a bird,pipe color and day/night mode.", True, BLACK)

# Get text surface dimensions
text_width = text_surface.get_width()
text_height = text_surface.get_height()

# Calculate text position
text_x = WIDTH // 2 - text_width // 2
text_y = 50

# Add background images
custom_background = pygame.image.load("assets/custom_background.png")
custom_background_width = custom_background.get_width()
day_background = pygame.image.load("assets/background-day.png")
night_background = pygame.image.load("assets/background-night.png")
floor_surface = pygame.transform.scale2x(
    pygame.image.load('assets/base.png').convert_alpha())
floor_width = floor_surface.get_width()


# Draw the clouds
def draw_clouds():
    screen.blit(custom_background, (clouds_x_pos, 0))
    screen.blit(custom_background,
                (clouds_x_pos + custom_background_width, 0))


# Draw the floor surface on the screen.
def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface,
                (floor_x_pos + floor_width, 900))


# Add button images
bird1_btn = pygame.image.load("assets/redbird-midflap.png")
bird2_btn = pygame.image.load("assets/bluebird-midflap.png")
bird3_btn = pygame.image.load("assets/yellowbird-midflap.png")
pipe_green_btn = pygame.image.load("assets/pipe-green.png")
pipe_red_btn = pygame.image.load("assets/pipe-red.png")
day_btn = pygame.image.load("assets/day_btn.png")
night_btn = pygame.image.load("assets/night_btn.png")

# Define button positions
bird1_pos = (100, 200)
bird2_pos = (250, 200)
bird3_pos = (400, 200)
pipe_green_pos = (150, 400)
pipe_red_pos = (330, 400)
day_pos = (80, 675)
night_pos = (260, 740)

# Initialize choice flags
selected_bird = False
selected_day_night = False
selected_pipe = False
running = True

# Set up game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            running = False
            pygame.quit()

        # Check if button is clicked
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONUP:
            if bird1_btn.get_rect(topleft=bird1_pos).collidepoint(mouse_pos):
                # Set bird image to redbird-midflap.png
                selected_bird = True
                bird_choice = "assets/redbird-midflap.png"
            elif bird2_btn.get_rect(topleft=bird2_pos).collidepoint(mouse_pos):
                # Set bird image to bluebird-midflap.png
                selected_bird = True
                bird_choice = "assets/bluebird-midflap.png"
            elif bird3_btn.get_rect(topleft=bird3_pos).collidepoint(mouse_pos):
                # Set bird image to yellowbird-midflap.png
                selected_bird = True
                bird_choice = "assets/yellowbird-midflap.png"
            elif pipe_green_btn.get_rect(topleft=pipe_green_pos).collidepoint(mouse_pos):
                # Set pipe image to pipe-green.png
                selected_pipe = True
                pipe_choice = "assets/pipe-green.png"
            elif pipe_red_btn.get_rect(topleft=pipe_red_pos).collidepoint(mouse_pos):
                # Set pipe image to pipe-red.png
                selected_pipe = True
                pipe_choice = "assets/pipe-red.png"
            elif day_btn.get_rect(topleft=day_pos).collidepoint(mouse_pos):
                # Set background to background-day.png
                # screen.blit(day_background, (0, 0))
                selected_day_night = True
                background_choice = "assets/background-day.png"
            elif night_btn.get_rect(topleft=night_pos).collidepoint(mouse_pos):
                # Set background to background-night.png
                # screen.blit(night_background, (0, 0))
                selected_day_night = True
                background_choice = "assets/background-night.png"

    # Draw background
    clouds_x_pos -= 1
    draw_clouds()
    if clouds_x_pos <= -custom_background_width:
        clouds_x_pos = 0

    # Draw Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -floor_width:
        floor_x_pos = 0

    # Blit text onto screen
    screen.blit(text_surface, (text_x, text_y))

    # Draw buttons on screen
    screen.blit(bird1_btn, bird1_pos)
    screen.blit(bird2_btn, bird2_pos)
    screen.blit(bird3_btn, bird3_pos)
    screen.blit(pipe_green_btn, pipe_green_pos)
    screen.blit(pipe_red_btn, pipe_red_pos)
    screen.blit(day_btn, day_pos)
    screen.blit(night_btn, night_pos)

    # Check if both choices have been made and start the game
    if selected_bird and selected_pipe and selected_day_night:
        game = FlappyBird(bird_choice, background_choice, pipe_choice)
        game.run()
        running = False

    # Update screen
    pygame.display.update()
