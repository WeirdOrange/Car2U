
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()

window.geometry("1280x720")
window.configure(bg = "#FFFFFF")


canvas = Canvas(
    window,
    bg = "#FFFFFF",
    height = 720,
    width = 1280,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge"
)

canvas.place(x = 0, y = 0)
canvas.create_rectangle(
    181.0,
    35.0,
    1305.0,
    790.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    527.0,
    720.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    278.0,
    100.0,
    1158.0,
    620.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    974.0,
    464.0,
    anchor="nw",
    text="New User?",
    fill="#000000",
    font=("SegoeUI Bold", 12 * -1)
)

canvas.create_rectangle(
    146.0,
    259.0,
    692.0,
    805.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    662.0,
    299.0,
    1114.0,
    379.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    662.0,
    379.0,
    1114.0,
    459.0,
    fill="#000000",
    outline="")

canvas.create_text(
    856.0,
    403.0,
    anchor="nw",
    text="Login",
    fill="#FFFFFF",
    font=("SegoeUI Bold", 24 * -1)
)

canvas.create_rectangle(
    967.0,
    126.0,
    1053.25048828125,
    232.00091552734375,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    662.0,
    219.0,
    1114.0,
    299.0,
    fill="#000000",
    outline="")

canvas.create_text(
    360.0,
    149.0,
    anchor="nw",
    text="Login Your Account",
    fill="#000000",
    font=("SegoeUI Bold", 36 * -1)
)

canvas.create_rectangle(
    1039.0,
    459.0,
    1104.0,
    486.0,
    fill="#000000",
    outline="")

canvas.create_text(
    1050.0,
    464.0,
    anchor="nw",
    text="Sign up",
    fill="#000000",
    font=("SegoeUI Bold", 12 * -1)
)

canvas.create_text(
    818.0,
    63.0,
    anchor="nw",
    text="Hi! Glad to have you with us.",
    fill="#000000",
    font=("SegoeUI Bold", 24 * -1)
)

canvas.create_rectangle(
    22.0,
    22.0,
    72.0,
    72.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    86.0,
    22.0,
    181.0,
    72.0,
    fill="#FFFFFF",
    outline="")
window.resizable(False, False)
window.mainloop()
