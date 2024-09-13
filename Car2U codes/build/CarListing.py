
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\build\assets\frame5")


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
    991.0,
    200.0,
    1238.0,
    251.0,
    fill="#FF7E52",
    outline="")

canvas.create_rectangle(
    0.0,
    0.0,
    1280.0,
    90.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    19.0,
    128.0,
    278.0,
    168.0,
    fill="#000000",
    outline="")

canvas.create_text(
    538.0,
    206.0,
    anchor="nw",
    text="Car Details ",
    fill="#000000",
    font=("Sintony Bold", 30 * -1)
)

canvas.create_rectangle(
    89.0,
    206.0,
    457.0,
    606.0,
    fill="#394552",
    outline="")

canvas.create_rectangle(
    178.0,
    306.0,
    378.0,
    506.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    538.0,
    279.5,
    anchor="nw",
    text="Brand : ",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_text(
    154.0,
    615.0,
    anchor="nw",
    text="Select image from gallery",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_text(
    1019.0,
    216.0,
    anchor="nw",
    text="SELECT RENTAL AGENCY",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_rectangle(
    651.0,
    280.0,
    840.0,
    321.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    538.0,
    415.5,
    anchor="nw",
    text="Colour : ",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_rectangle(
    651.0,
    414.0,
    840.0,
    455.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    538.0,
    483.5,
    anchor="nw",
    text="Fuel Type : ",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_rectangle(
    651.0,
    484.0,
    840.0,
    525.0,
    fill="#D9D9D9",
    outline="")

canvas.create_text(
    538.0,
    347.5,
    anchor="nw",
    text="Model : ",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_text(
    885.0,
    280.0,
    anchor="nw",
    text="Seating Capacity : ",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_text(
    886.0,
    429.0,
    anchor="nw",
    text="Price (per day) : ",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_text(
    886.0,
    353.0,
    anchor="nw",
    text="Transmission Type : ",
    fill="#000000",
    font=("Sintony", 20 * -1)
)

canvas.create_rectangle(
    651.0,
    348.0,
    840.0,
    389.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1049.0,
    285.0,
    1238.0,
    326.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    1049.0,
    421.0,
    1238.0,
    462.0,
    fill="#D9D9D9",
    outline="")

canvas.create_rectangle(
    1049.0,
    358.0,
    1238.0,
    399.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1196.0,
    216.0,
    1213.0,
    236.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    593.0,
    641.0,
    803.0,
    696.0,
    fill="#000000",
    outline="")
window.resizable(False, False)
window.mainloop()
