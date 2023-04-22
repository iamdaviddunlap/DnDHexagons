import pygame
import sys
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = (255, 255, 255)
TOOLTIP_TEXT_COLOR = (0, 0, 0)
TOOLTIP_BACKGROUND_COLOR = (200, 200, 200)
TOOLTIP_BORDER_COLOR = (0, 0, 0)
TOOLTIP_BORDER_WIDTH = 2
TOOLTIP_PADDING = 5
TOOLTIP_FONT_SIZE = 20
TOOLTIP_FONT_STYLE = 'freesansbold.ttf'

# Load your image
image_path = 'temp/overlay.png'
image = pygame.image.load(image_path)
image_rect = image.get_rect()

# Scale the game window
monitor = pygame.display.Info()
monitor_size = (monitor.current_w, monitor.current_h)

# Calculate the scale factor
scale_factor = min(monitor_size[0] / image_rect.width, monitor_size[1] / image_rect.height)

# Scale the image and update the rect
scaled_image = pygame.transform.smoothscale(image, (round(image_rect.width * scale_factor), round(image_rect.height * scale_factor)))
scaled_rect = scaled_image.get_rect()

# Create the screen (game window)
screen = pygame.display.set_mode((scaled_rect.width, scaled_rect.height))

def display_tooltip(screen, text, pos):
    font_size = 24
    font_color = (0, 0, 0)
    font_type = 'freesansbold.ttf'
    bg_color = (230, 230, 230)
    font = pygame.font.Font(font_type, font_size)
    tooltip_text = font.render(text, True, font_color, bg_color)
    tooltip_rect = tooltip_text.get_rect()

    tooltip_rect.topleft = pos
    screen.blit(tooltip_text, tooltip_rect)

def run_pygame_display(coord_to_txt):
    # Points of interest and tooltip mapping
    points_of_interest = { k: v for k, v in coord_to_txt.items() }

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the image
        screen.blit(scaled_image, scaled_rect)

        # Check if the mouse is close to the points of interest
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for coord, tooltip_text in points_of_interest.items():
            scaled_coord = (coord[0] * scale_factor, coord[1] * scale_factor)
            distance = ((mouse_x - scaled_coord[0]) ** 2 + (mouse_y - scaled_coord[1]) ** 2) ** 0.5
            if distance <= 20:
                display_tooltip(screen, tooltip_text, (mouse_x + 10, mouse_y + 10))
                break

        # Update the screen
        pygame.display.flip()