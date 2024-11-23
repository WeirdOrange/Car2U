
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\Testing\build\assets\frame1")


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
image_image_1 = PhotoImage(
    file=relative_to_assets("image_1.png"))
image_1 = canvas.create_image(
    743.0,
    412.0,
    image=image_image_1
)

image_image_2 = PhotoImage(
    file=relative_to_assets("image_2.png"))
image_2 = canvas.create_image(
    263.0,
    360.0,
    image=image_image_2
)

image_image_3 = PhotoImage(
    file=relative_to_assets("image_3.png"))
image_3 = canvas.create_image(
    650.0,
    360.0,
    image=image_image_3
)

image_image_4 = PhotoImage(
    file=relative_to_assets("image_4.png"))
image_4 = canvas.create_image(
    1055.0,
    585.0,
    image=image_image_4
)

image_image_5 = PhotoImage(
    file=relative_to_assets("image_5.png"))
image_5 = canvas.create_image(
    47.0,
    47.0,
    image=image_image_5
)

image_image_6 = PhotoImage(
    file=relative_to_assets("image_6.png"))
image_6 = canvas.create_image(
    133.0,
    47.0,
    image=image_image_6
)

canvas.create_text(
    745.0,
    238.0,
    anchor="nw",
    text="Register Now!",
    fill="#000000",
    font=("SegoeUIBlack", 48 * -1)
)

canvas.create_text(
    732.0,
    314.0,
    anchor="nw",
    text="Few more steps to\nmake your trip better!",
    fill="#FFFFFF",
    font=("SegoeUI Semibold", 24 * -1)
)

entry_image_1 = PhotoImage(
    file=relative_to_assets("entry_1.png"))
entry_bg_1 = canvas.create_image(
    488.0,
    253.0,
    image=entry_image_1
)
entry_1 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_1.place(
    x=272.0,
    y=223.0,
    width=432.0,
    height=58.0
)

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_1 clicked"),
    relief="flat"
)
button_1.place(
    x=272.0,
    y=463.0,
    width=432.0,
    height=60.0
)

entry_image_2 = PhotoImage(
    file=relative_to_assets("entry_2.png"))
entry_bg_2 = canvas.create_image(
    663.5,
    338.0,
    image=entry_image_2
)
entry_2 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_2.place(
    x=623.0,
    y=313.0,
    width=81.0,
    height=48.0
)

entry_image_3 = PhotoImage(
    file=relative_to_assets("entry_3.png"))
entry_bg_3 = canvas.create_image(
    575.5,
    338.0,
    image=entry_image_3
)
entry_3 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_3.place(
    x=535.0,
    y=313.0,
    width=81.0,
    height=48.0
)

entry_image_4 = PhotoImage(
    file=relative_to_assets("entry_4.png"))
entry_bg_4 = canvas.create_image(
    486.5,
    338.0,
    image=entry_image_4
)
entry_4 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_4.place(
    x=446.0,
    y=313.0,
    width=81.0,
    height=48.0
)

entry_image_5 = PhotoImage(
    file=relative_to_assets("entry_5.png"))
entry_bg_5 = canvas.create_image(
    324.5,
    333.0,
    image=entry_image_5
)
entry_5 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_5.place(
    x=272.0,
    y=303.0,
    width=105.0,
    height=58.0
)

entry_image_6 = PhotoImage(
    file=relative_to_assets("entry_6.png"))
entry_bg_6 = canvas.create_image(
    392.0,
    413.0,
    image=entry_image_6
)
entry_6 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_6.place(
    x=272.0,
    y=383.0,
    width=240.0,
    height=58.0
)

entry_image_7 = PhotoImage(
    file=relative_to_assets("entry_7.png"))
entry_bg_7 = canvas.create_image(
    488.0,
    173.0,
    image=entry_image_7
)
entry_7 = Entry(
    bd=0,
    bg="#FFFFFF",
    fg="#000716",
    highlightthickness=0
)
entry_7.place(
    x=272.0,
    y=143.0,
    width=432.0,
    height=58.0
)

canvas.create_text(
    181.0,
    160.0,
    anchor="nw",
    text="Name",
    fill="#FFFFFF",
    font=("SegoeUI Semibold", 20 * -1)
)

canvas.create_text(
    181.0,
    226.0,
    anchor="nw",
    text="Email \nAddress",
    fill="#FFFFFF",
    font=("SegoeUI Semibold", 20 * -1)
)

canvas.create_text(
    259.0,
    234.0,
    anchor="nw",
    text=":",
    fill="#FFFFFF",
    font=("SegoeUI Bold", 24 * -1)
)

canvas.create_text(
    259.0,
    317.0,
    anchor="nw",
    text=":",
    fill="#FFFFFF",
    font=("SegoeUI Bold", 24 * -1)
)

canvas.create_text(
    259.0,
    397.0,
    anchor="nw",
    text=":",
    fill="#FFFFFF",
    font=("SegoeUI Bold", 24 * -1)
)

canvas.create_text(
    259.0,
    157.0,
    anchor="nw",
    text=":",
    fill="#FFFFFF",
    font=("SegoeUI Bold", 24 * -1)
)

canvas.create_text(
    181.0,
    320.0,
    anchor="nw",
    text="Age",
    fill="#FFFFFF",
    font=("SegoeUI Semibold", 20 * -1)
)

canvas.create_text(
    181.0,
    386.0,
    anchor="nw",
    text="Contact\nNo.",
    fill="#FFFFFF",
    font=("SegoeUI Semibold", 20 * -1)
)

canvas.create_text(
    386.0,
    322.0,
    anchor="nw",
    text="D.O.B:",
    fill="#FFFFFF",
    font=("SegoeUI Semibold", 20 * -1)
)

canvas.create_text(
    519.0,
    538.0,
    anchor="nw",
    text="Already Registered?",
    fill="#000000",
    font=("SegoeUI Bold", 12 * -1)
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_2 clicked"),
    relief="flat"
)
button_2.place(
    x=639.0,
    y=533.0,
    width=65.0,
    height=27.0
)
window.resizable(False, False)
window.mainloop()