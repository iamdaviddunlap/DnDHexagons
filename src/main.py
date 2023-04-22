import tkinter as tk

# Define the list of areas of interest on the image
populated_hexes = [(100, 100), (200, 200), (300, 300)]

# Define a mapping of x,y tuples to tooltip text
tooltip_text = {(100, 100): "This is area of interest 1",
                (200, 200): "This is area of interest 2",
                (300, 300): "This is area of interest 3"}

# Define a function to show the tooltip
def show_tooltip(event):
    x, y = event.x, event.y
    for hex_coords, text in tooltip_text.items():
        if abs(hex_coords[0] - x) <= 15 and abs(hex_coords[1] - y) <= 15:
            tooltip.config(text=text)
            tooltip.place(x=x, y=y)
            return
    tooltip.place_forget()

# Create a Tkinter window
root = tk.Tk()

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