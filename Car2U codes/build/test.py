import customtkinter as ctk

# Initialize the app
app = ctk.CTk()

# Function to change the background color when hovered
def change_bg_color_on_hover(frame):
    frame.configure(fg_color="blue")  # Change background color to blue on hover

# Function to reset the background color when the mouse leaves
def reset_bg_color(frame):
    frame.configure(fg_color="white")  # Reset background color to white

# Create multiple frames
frames = []
for i in range(3):  # Example with 3 frames
    frame = ctk.CTkFrame(app, width=200, height=200, fg_color="white")
    frame.pack(pady=10, padx=10)
    frames.append(frame)

    # Bind hover events directly and use lambda to pass the frame reference
    frame.bind("<Enter>", lambda event, f=frame: change_bg_color_on_hover(f))  # Change background color on hover
    frame.bind("<Leave>", lambda event, f=frame: reset_bg_color(f))  # Reset background color when mouse leaves

app.mainloop()
