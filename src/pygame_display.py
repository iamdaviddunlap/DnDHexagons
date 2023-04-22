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
TOOLTIP_FONT_STYLE = 'C:\\Windows\\Fonts\\cour.ttf'

scale_factor = 1.0
pan_offset = [0, 0]
is_panning = False
prev_mouse_pos = (0, 0)


def display_tooltip(screen, text, pos, font_size):
    font = pygame.font.Font(TOOLTIP_FONT_STYLE, font_size)
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


def handle_mouse_wheel(event, zoom_speed=0.1):
    global scale_factor, pan_offset

    mouse_x, mouse_y = pygame.mouse.get_pos()
    prev_offset_x = pan_offset[0]
    prev_offset_y = pan_offset[1]

    if event.y > 0:  # Zoom in
        scale_factor *= 1 + zoom_speed
    elif event.y < 0:  # Zoom out
        scale_factor *= 1 - zoom_speed

    # Calculate new pan_offset based on mouse position and previous pan_offset
    pan_offset[0] = mouse_x - ((mouse_x - prev_offset_x) * (scale_factor / (scale_factor / (1 + zoom_speed) if event.y > 0 else scale_factor / (1 - zoom_speed))))
    pan_offset[1] = mouse_y - ((mouse_y - prev_offset_y) * (scale_factor / (scale_factor / (1 + zoom_speed) if event.y > 0 else scale_factor / (1 - zoom_speed))))

    update_scaled_image()


def update_scaled_image():
    global scaled_image, scaled_rect

    # Update image
    scaled_image = pygame.transform.smoothscale(image, (
    round(image_rect.width * scale_factor), round(image_rect.height * scale_factor)))
    scaled_rect = scaled_image.get_rect()


def init_pygame():
    pygame.init()


def load_image(image_path):
    global image, image_rect
    image = pygame.image.load(image_path)
    image_rect = image.get_rect()


def create_screen(default_window_width, default_window_height):
    global screen, scaled_image, scaled_rect
    screen = pygame.display.set_mode((default_window_width, default_window_height), pygame.RESIZABLE)

    # Calculate scaling factors to resize the image to fill the screen
    width_scale = screen.get_width() / image_rect.width
    height_scale = screen.get_height() / image_rect.height
    scale = min(width_scale, height_scale)

    # Resize the image and update the scaled_rect variable
    scaled_image = pygame.transform.smoothscale(image, (int(image_rect.width * scale), int(image_rect.height * scale)))
    scaled_rect = scaled_image.get_rect()

    update_scaled_image()

def run_pygame_display(coord_to_txt_metadata, font_size=20):
    global is_panning, screen, prev_mouse_pos, pan_offset

    # Points of interest and tooltip mapping
    points_of_interest = {k: v for k, v in coord_to_txt_metadata.items()}

    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == VIDEORESIZE:
                width, height = event.w, event.h
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
            elif event.type == MOUSEWHEEL:
                handle_mouse_wheel(event)
            elif event.type == MOUSEBUTTONDOWN and event.button == 1: # left mouse button
                is_panning = True
                prev_mouse_pos = pygame.mouse.get_pos()
            elif event.type == MOUSEBUTTONUP and event.button == 1: # left mouse button
                is_panning = False

        # Update pan_offset when left mouse button is pressed and moved
        if is_panning:
            mouse_pos = pygame.mouse.get_pos()
            pan_offset[0] += mouse_pos[0] - prev_mouse_pos[0]
            pan_offset[1] += mouse_pos[1] - prev_mouse_pos[1]
            prev_mouse_pos = mouse_pos

        # Clear the screen
        screen.fill(BACKGROUND_COLOR)

        # Draw the image
        screen.blit(scaled_image, scaled_rect.move(pan_offset))

        # Check if the mouse is close to the points of interest
        mouse_x, mouse_y = pygame.mouse.get_pos()
        for coord, tooltip_text in points_of_interest.items():
            scaled_coord = (coord[0] * scale_factor, coord[1] * scale_factor)
            tooltip_rect = pygame.Rect((0, 0), (0, 0))
            tooltip_rect.center = (scaled_coord[0] + pan_offset[0], scaled_coord[1] + pan_offset[1])
            distance = ((mouse_x - tooltip_rect.center[0]) ** 2 + (mouse_y - tooltip_rect.center[1]) ** 2) ** 0.5
            if distance <= 20:
                display_tooltip(screen, tooltip_text, (mouse_x + 10, mouse_y + 10), font_size)
                break
            else:
                tooltip_rect.inflate_ip(20, 20)
                if tooltip_rect.collidepoint(mouse_x, mouse_y):
                    display_tooltip(screen, tooltip_text, (mouse_x + 10, mouse_y + 10), font_size)

        # Update the screen
        pygame.display.flip()


def init_game_screen():
    global image, image_rect, scale_factor
    # Calculate default window size
    monitor = pygame.display.Info()
    default_window_width = int(monitor.current_w * 0.75)  # set default window width to 0.75 times the screen width
    default_window_height = int(default_window_width * image_rect.height / image_rect.width)

    img_width, img_height = image_rect.bottomright

    scale_factor = default_window_height / img_height

    create_screen(default_window_width, default_window_height)


def main():
    global scale_factor

    init_pygame()

    # Load your image
    image_path = 'temp/overlay.png'
    load_image(image_path)

    # Set initial scale_factor to 1.0
    scale_factor = 1.0

    init_game_screen()

    coord_to_txt = {(35, 43): 'some text for A1\nand some on a new line', (65, 97): 'some text for B2',
                    (35, 149): 'some text for C1', (1403, 363): "I'm closer to the middle\n\n\n\n\n\n\n\n\n:)"}
    run_pygame_display(coord_to_txt)


if __name__ == '__main__':
    main()
