from PIL import Image, ImageDraw, ImageFont
from string import ascii_uppercase
import json
import tkinter as tk

from generate_hexagons import create_hex_png


def create_hex_overlay(tessellations, background):
    # Stretch the tessellations image to match the size of the background image
    tessellations = tessellations.resize(background.size)

    # Create a new image to hold the overlay
    overlay = Image.new("RGBA", background.size)

    # Paste the background onto the overlay
    overlay.paste(background, (0, 0))

    # Paste the tessellations onto the overlay, using the alpha channel to show transparency
    overlay.paste(tessellations, (0, 0), tessellations)

    return overlay


def add_text_to_overlay(overlay, num_hex_tall, num_hex_wide, mapping):
    # Magic Numbers that need to be tuned to the size of the stretched hexagons
    row_1_origin_x, row_1_origin_y = (35, 43)  # The (x, y) origin of the leftmost hex on the first row at the top
    row_2_origin_x, row_2_origin_y = (65, 97)  # The (x, y) origin of the leftmost hex on the second row from the top

    hex_spacing_horizontal = 60  # The number of pixels between the hex and the one directly next to it
    hex_spacing_vertical = 54  # The number of pixels between the origin of a hex and of the hex 2 rows down
    x_decay = 0.9915
    y_decay = 0.99

    populated_hexes = {}

    for hex_i in range(num_hex_tall):
        for hex_j in range(num_hex_wide):
            if hex_i % 2 == 0:
                coord_x = int(row_1_origin_x + (hex_j * hex_spacing_horizontal * x_decay))
                coord_y = int(row_1_origin_y + (hex_i * hex_spacing_vertical * y_decay))
                text_number = 2 * hex_j + 1
            else:
                coord_x = int(row_2_origin_x + (hex_j * hex_spacing_horizontal * x_decay))
                coord_y = int(row_2_origin_y + ((hex_i-1) * hex_spacing_vertical * y_decay))
                text_number = 2 * hex_j + 2

            # Create a draw object
            draw = ImageDraw.Draw(overlay)

            # Specify the font and size
            font = ImageFont.truetype("arial.ttf", 20)

            text_letter = ascii_uppercase[hex_i]
            text = text_letter + str(text_number)

            # Get the size of the text
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_width, text_height = text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1]

            # Calculate the top-left corner of the text box
            left = coord_x - text_width / 2
            top = coord_y - text_height / 2

            # Determine text color based on if it has special text or not
            if text in mapping.keys():
                text_color = (255, 0, 0)
                populated_hexes[text] = (coord_x, coord_y)
            else:
                text_color = (255, 255, 255)

            # Draw the text on the image
            draw.text((left, top), text, font=font, fill=text_color, stroke_width=1, stroke_fill=(0, 0, 0))

    return overlay, populated_hexes


def show_tooltip(tooltip, tooltip_text, event):
    x, y = event.x, event.y
    for hex_coords, text in tooltip_text.items():
        if abs(hex_coords[0] - x) <= 15 and abs(hex_coords[1] - y) <= 15:
            tooltip.config(text=text)
            tooltip.place(x=x, y=y)
            return
    tooltip.place_forget()


# Image is 2541x1315
def main():
    num_hex_wide = 42
    num_hex_tall = 24
    hexagon_filename = 'temp/hexagons_tessellation'
    create_hex_png(num_hex_tall, num_hex_wide, hexagon_filename)

    # Open the images
    tessellations = Image.open("temp/hexagons_tessellation.png")
    tessellations = tessellations.transpose(method=Image.FLIP_LEFT_RIGHT)  # Flip the image to match Roll20
    background = Image.open("test_img.png")

    # Load the json of text mappings
    with open('data.json') as f:
        mapping = json.load(f)

    # Get the overlay img
    overlay = create_hex_overlay(tessellations, background)

    # Populate the overlay image with text
    overlay, populated_hexes = add_text_to_overlay(overlay, num_hex_tall, num_hex_wide, mapping)
    coord_to_txt = {populated_hexes[key]: mapping[key] for key in populated_hexes}

    overlay.save('temp/overlay.png')

    tooltip_range = 20

    ########## TKINER ##############

    # Define a function to show the tooltip
    def show_tooltip(event):
        x, y = event.x, event.y
        for hex_coords, text in coord_to_txt.items():
            if abs(hex_coords[0] - x) <= tooltip_range and abs(hex_coords[1] - y) <= tooltip_range:
                tooltip.config(text=text)
                tooltip.place(x=x, y=y)
                return
        tooltip.place_forget()

    # Create a Tkinter window
    root = tk.Toplevel()

    # Load the image
    image = tk.PhotoImage(file="temp/overlay.png")

    # Create a canvas to display the image
    canvas = tk.Canvas(root, width=image.width(), height=image.height())
    canvas.pack()
    canvas.create_image(0, 0, anchor=tk.NW, image=image)

    # Create a label to display the tooltip
    tooltip = tk.Label(root, bg="white", relief="solid", borderwidth=1)

    # Bind the mouse motion event to the show_tooltip function
    canvas.bind("<Motion>", show_tooltip)

    # Start the main loop
    root.mainloop()



if __name__ == '__main__':
    main()
