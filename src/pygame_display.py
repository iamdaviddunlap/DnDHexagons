import pygame
import sys
from pygame.locals import *

# Constants
BACKGROUND_COLOR = (0, 0, 0)
TOOLTIP_TEXT_COLOR = (0, 0, 0)
TOOLTIP_BACKGROUND_COLOR = (200, 200, 200)
TOOLTIP_BORDER_COLOR = (0, 0, 0)
TOOLTIP_BORDER_WIDTH = 2
TOOLTIP_PADDING = 5
TOOLTIP_FONT_SIZE = 20
TOOLTIP_FONT_STYLE = 'freesansbold.ttf'


def display_tooltip(screen, text, pos):
    font = pygame.font.Font(TOOLTIP_FONT_STYLE, TOOLTIP_FONT_SIZE)
    lines = text.split('\n')
    line_height = font.get_linesize()

    padding = 5  # You can change this value to adjust the padding
    max_line_width = max(font.size(line)[0] for line in lines) + 2 * padding
    total_height = line_height * len(lines) + 2 * padding

    # Create a background surface and fill it with the background color
    background_surface = pygame.Surface((max_line_width, total_height), pygame.SRCALPHA)
    background_surface.fill(TOOLTIP_BACKGROUND_COLOR)
    screen.blit(background_surface, pos)

    tooltip_rect = None
    for index, line in enumerate(lines):
        tooltip_text = font.render(line, True, TOOLTIP_TEXT_COLOR)
        if tooltip_rect is None:
            tooltip_rect = tooltip_text.get_rect()
            tooltip_rect.topleft = (pos[0] + padding, pos[1] + padding)
        else:
            tooltip_rect.top += line_height
        screen.blit(tooltip_text, tooltip_rect)


def resize_window(width, height):
    global screen, image_rect, scaled_image, scaled_rect, scale_factor

    # Calculate new height while keeping the aspect ratio constant
    new_height = int(width * image_rect.height / image_rect.width)

    # Update screen size
    screen = pygame.display.set_mode((width, new_height), pygame.RESIZABLE)

    # Update scale factor and image
    scale_factor = width / image_rect.width
    scaled_image = pygame.transform.smoothscale(image, (round(image_rect.width * scale_factor), round(image_rect.height * scale_factor)))
    scaled_rect = scaled_image.get_rect()


def run_pygame_display(coord_to_txt):
    # Points of interest and tooltip mapping
    points_of_interest = { k: v for k, v in coord_to_txt.items() }

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                width, height = event.w, event.h
                resize_window(width, height)

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


if __name__ == '__main__':
    # Initialize Pygame
    pygame.init()

    # Load your image
    image_path = 'temp/overlay.png'
    image = pygame.image.load(image_path)
    image_rect = image.get_rect()

    # Calculate default window size
    monitor = pygame.display.Info()
    default_window_width = int(monitor.current_w * 0.75)
    default_window_height = int(default_window_width * image_rect.height / image_rect.width)

    # Initialize scaled_image and scaled_rect
    scaled_image = image
    scaled_rect = image_rect

    # Create the screen (game window)
    screen = pygame.display.set_mode((default_window_width, default_window_height), pygame.RESIZABLE)

    # Initialize the scaled_image, scaled_rect, and scale_factor with the default window size
    resize_window(default_window_width, default_window_height)

    coord_to_txt = {(35, 43): 'some text for A1\nand some on a new line', (65, 97): 'some text for B2',
                    (35, 149): 'some text for C1', (1403, 363): "I'm closer to the middle\n\n\n\n\n\n\n\n\n:)"}
    run_pygame_display(coord_to_txt)
