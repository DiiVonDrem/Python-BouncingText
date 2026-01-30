import tkinter as tk
import random


TEXT_CONTENT = "DVD" # The text the Bouncing Sentence will contain.
FONT_STYLE = ("Times New Roman", 80, "bold") # Font, Char size and effects the Sentence will have.
OUTLINE_COLOR = "white" # Color of the outline of our Sentence.
OUTLINE_WIDTH = 3 # Width of the outline.
CHANGE_COLOR_INTERVAL_MS = 800  # Time in milliseconds to change color.
ANIMATION_SPEED_MS = 10         # Time in milliseconds between movement updates.

# Initial position and velocity.
current_x, current_y = 100, 100
velocity_x, velocity_y = 4, 4

def change_color():
    #Generates a random hex color and updates the main text fill ; Recursively calls itself to create a loop.
    # Generate a random color in hex format (e.g., #FF00AA).
    
    random_color = "#%06x" % random.randint(0, 0xFFFFFF)
    
    # Update only the text tagged as 'main_text'.
    canvas.itemconfig("main_text", fill=random_color)
    
    # Schedule the next color change.
    root.after(CHANGE_COLOR_INTERVAL_MS, change_color)

def animate_bounce():
    
    #Updates the window position based on velocity ; Handles collision detection with screen edges.
    global current_x, current_y, velocity_x, velocity_y
    
    # Get current screen dimensions.
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Get current window dimensions.
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    
    # Update position.
    current_x += velocity_x
    current_y += velocity_y
    
    # Collision detection: Horizontal (Right or Left edge).
    if current_x + window_width >= screen_width or current_x <= 0:
        velocity_x = -velocity_x
        
    # Collision detection: Vertical (Bottom or Top edge).
    if current_y + window_height >= screen_height or current_y <= 0:
        velocity_y = -velocity_y
        
    # Apply new position.
    root.geometry(f"+{current_x}+{current_y}")
    
    # Schedule the next frame.
    root.after(ANIMATION_SPEED_MS, animate_bounce)


root = tk.Tk()

# Remove window borders and title bar.
root.overrideredirect(True)

# Keep window always on top of other windows.
root.wm_attributes("-topmost", True)

# 1. Set the background to a specific color (black).
# 2. Tell the OS to treat that specific color as transparent (Works only on Windows).
root.config(bg='black')
root.attributes("-transparentcolor", "black")

# Create a canvas with no border (highlightthickness=0) and transparent bg.
canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

# Center coordinates for drawing (arbitrary starting point, resized later).
center_x, center_y = 150, 100 

# Draw the text multiple times in the outline color.
# slightly offset in 4 directions.
offsets = [
    (-OUTLINE_WIDTH, 0), (OUTLINE_WIDTH, 0),  # Left, Right.
    (0, -OUTLINE_WIDTH), (0, OUTLINE_WIDTH)   # Up, Down.
]

for offset_x, offset_y in offsets:
    canvas.create_text(
        center_x + offset_x, 
        center_y + offset_y, 
        text=TEXT_CONTENT, 
        font=FONT_STYLE, 
        fill=OUTLINE_COLOR, 
        anchor="center"
    )

# Draw the actual text on top of the outlines.
# Assigning a tag "main_text" to easily find and recolor it later.
canvas.create_text(
    center_x, 
    center_y, 
    text=TEXT_CONTENT, 
    font=FONT_STYLE, 
    fill='cyan', 
    anchor="center", 
    tag="main_text"
)


# Update idle tasks to ensure bounding boxes are calculated correctly.
root.update_idletasks()

# Resize the window to fit exactly around the drawn text.
bbox = canvas.bbox('all') # Returns (x1, y1, x2, y2).
root.geometry(f"{bbox[2]}x{bbox[3]}")

# Start loops.
root.after(100, animate_bounce)
root.after(100, change_color)

root.mainloop()