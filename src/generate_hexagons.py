import turtle
import math
import canvasvg
import cairosvg
from PIL import Image
from io import BytesIO
import os

from turtle import Screen, Turtle

OUTER_RADIUS = 50
INNER_RADIUS = 3**0.5 * OUTER_RADIUS / 2
SIDE_LENGTH = 58
SIDES = 6
EXTENT = 360 / SIDES

def draw_hexagon():
    turtle.pendown()
    turtle.right(EXTENT/2)
    for _ in range(SIDES):
        turtle.forward(SIDE_LENGTH)
        turtle.right(EXTENT)
    turtle.left(EXTENT/2)
    turtle.penup()

def draw_row(num_hexagons):
    for i in range(num_hexagons):
        draw_hexagon()
        turtle.forward(OUTER_RADIUS * 2)

def tessellation(num_rows, num_hexagons_per_row):
    for i in range(num_rows):
        if i % 2 == 0:
            turtle.penup()
            turtle.goto(-OUTER_RADIUS * (num_hexagons_per_row - 1), -INNER_RADIUS * 2 * i)
            turtle.pendown()
        else:
            turtle.penup()
            turtle.goto(-OUTER_RADIUS * (num_hexagons_per_row - 1) - OUTER_RADIUS, -INNER_RADIUS * 2 * i)
            turtle.pendown()

        draw_row(num_hexagons_per_row)

def create_hex_png(num_hex_wide, num_hex_tall, filename):
    screen = Screen()
    turtle = Turtle(visible=False)

    screen.delay(0)
    screen.tracer(False)

    tessellation(num_hex_wide, num_hex_tall)

    # Create the temp folder if needed
    temp_folder_name = 'temp'
    if not os.path.exists(temp_folder_name):
        os.makedirs(temp_folder_name)

    # Save the drawing as an SVG file
    svg_filename = filename + ".svg"
    canvasvg.saveall(svg_filename, screen.getcanvas())

    # Convert the SVG to a PNG with transparency
    png_filename = filename + ".png"

    with open(svg_filename, 'r') as svg_file:
        svg_data = svg_file.read()

    cairosvg.svg2png(bytestring=svg_data.encode('utf-8'), write_to=png_filename)

    img = Image.open(png_filename).convert('RGBA')
    datas = img.getdata()

    new_data = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    img.putdata(new_data)
    img.save(png_filename, "PNG")
