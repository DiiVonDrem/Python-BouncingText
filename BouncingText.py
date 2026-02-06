import tkinter as tk
import random

TEXT_CONTENT = "N/A"
FONT_STYLE = ("Times New Roman", 80, "bold")
OUTLINE_COLOR = "white"
OUTLINE_WIDTH = 3
CHANGE_COLOR_INTERVAL_MS = 800
ANIMATION_SPEED_MS = 10

# Initial position and velocity.
current_x, current_y = 100, 100
velocity_x, velocity_y = 5, 5

# State flags for dragging.
is_dragging = False
drag_start_x = 0
drag_start_y = 0

def change_color():
    """Generates a random hex color and updates the main text fill."""
    random_color = "#%06x" % random.randint(0, 0xFFFFFF)
    canvas.itemconfig("main_text", fill=random_color)
    root.after(CHANGE_COLOR_INTERVAL_MS, change_color)

def animate_bounce():
    """Updates position based on velocity; handles collision and drag state."""
    global current_x, current_y, velocity_x, velocity_y

    # If the user is holding the text, we skip the physics update.
    # so the window doesn't fight the mouse cursor.
    if is_dragging:
        root.after(ANIMATION_SPEED_MS, animate_bounce)
        return

    # Get dimensions.
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Update position.
    current_x += velocity_x
    current_y += velocity_y

    # Collision detection: Horizontal.
    if current_x + window_width >= screen_width or current_x <= 0:
        velocity_x = -velocity_x
        # Clamp to screen to prevent getting stuck.
        if current_x <= 0: current_x = 0
        if current_x + window_width >= screen_width: current_x = screen_width - window_width

    # Collision detection: Vertical.
    if current_y + window_height >= screen_height or current_y <= 0:
        velocity_y = -velocity_y
        # Clamp to screen to prevent getting stuck.
        if current_y <= 0: current_y = 0
        if current_y + window_height >= screen_height: current_y = screen_height - window_height

    # Apply new position.
    root.geometry(f"+{int(current_x)}+{int(current_y)}")
    
    # Schedule next frame.
    root.after(ANIMATION_SPEED_MS, animate_bounce)

'''
Optional Drag/Release functions

def start_drag(event):
    # Called when user clicks the window.
    global is_dragging, drag_start_x, drag_start_y, velocity_x, velocity_y
    is_dragging = True
    
    # Record where inside the window we clicked, so we can drag relative to that point.
    drag_start_x = event.x
    drag_start_y = event.y
    
    # Stop movement momentarily while holding.
    velocity_x = 0
    velocity_y = 0

def on_drag(event):
    # Called when user moves the mouse while holding click.
    global current_x, current_y, velocity_x, velocity_y
    
    # Calculate where the window should move to match the mouse root.winfo_pointerx() is the global mouse position on screen.
    new_x = root.winfo_pointerx() - drag_start_x
    new_y = root.winfo_pointery() - drag_start_y

    # CALCULATE THROW VELOCITY
    # The velocity is the difference between the new position and the old position.
    # This determines how fast you were moving it when you let go.
    velocity_x = new_x - current_x
    velocity_y = new_y - current_y

    # Update current position
    current_x = new_x
    current_y = new_y
    
    # Move the window immediately
    root.geometry(f"+{int(current_x)}+{int(current_y)}")

def end_drag(event):
    # Called when user releases the mouse button.
    global is_dragging
    is_dragging = False
    # The animate_bounce loop will now resume, picking up the 'velocity_x' and 'velocity_y' we calculated in on_drag.
    
'''

# SETUP.

root = tk.Tk()
root.overrideredirect(True)
root.wm_attributes("-topmost", True)
root.config(bg='black')
root.attributes("-transparentcolor", "black")

canvas = tk.Canvas(root, bg='black', highlightthickness=0)
canvas.pack(fill="both", expand=True)

'''
# Optional Drag/Release Functions
canvas.bind("<Button-1>", start_drag)        # Click down.
canvas.bind("<B1-Motion>", on_drag)          # Drag.
canvas.bind("<ButtonRelease-1>", end_drag)   # Release.
'''

center_x, center_y = 150, 100 
offsets = [(-OUTLINE_WIDTH, 0), (OUTLINE_WIDTH, 0), (0, -OUTLINE_WIDTH), (0, OUTLINE_WIDTH)]

for offset_x, offset_y in offsets:
    canvas.create_text(center_x + offset_x, center_y + offset_y, text=TEXT_CONTENT, font=FONT_STYLE, fill=OUTLINE_COLOR, anchor="center")

canvas.create_text(center_x, center_y, text=TEXT_CONTENT, font=FONT_STYLE, fill='cyan', anchor="center", tag="main_text")

root.update_idletasks()
bbox = canvas.bbox('all')
root.geometry(f"{bbox[2]}x{bbox[3]}")

# Start loops.
root.after(100, animate_bounce)
root.after(100, change_color)

root.mainloop()
