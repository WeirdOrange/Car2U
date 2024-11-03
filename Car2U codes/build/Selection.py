
# This file was generated by the Tkinter Designer by Parth Jadhav
# https://github.com/ParthJadhav/Tkinter-Designer


from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage


OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path(r"D:\Ivan\Ivan\Ivan\Deg CS\ALL Project\Car2U\Car2U codes\build\assets\frame3")


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
    0.0,
    1.0,
    1280.0,
    91.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    0.0,
    91.0,
    187.0,
    721.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    187.0,
    91.0,
    1280.0,
    721.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    184.0,
    92.0,
    1277.0,
    722.0,
    fill="#444245",
    outline="")

canvas.create_rectangle(
    35.0,
    20.0,
    130.0,
    70.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    187.0,
    90.0,
    1280.0,
    183.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    11.0,
    97.0,
    176.0,
    137.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    11.0,
    261.0,
    176.0,
    301.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    13.0,
    413.0,
    178.0,
    453.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    11.0,
    128.0,
    29.0,
    146.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    11.0,
    152.0,
    29.0,
    170.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    11.0,
    176.0,
    29.0,
    194.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    11.0,
    200.0,
    29.0,
    218.0,
    fill="#000000",
    outline="")

canvas.create_text(
    35.0,
    127.0,
    anchor="nw",
    text="Toyota",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_text(
    35.0,
    152.0,
    anchor="nw",
    text="Mazda",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_rectangle(
    1385.0,
    90.0,
    2340.0,
    630.0,
    fill="#444245",
    outline="")

canvas.create_text(
    35.0,
    199.0,
    anchor="nw",
    text="Mercedes",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_text(
    35.0,
    177.0,
    anchor="nw",
    text="Perodua",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_rectangle(
    13.0,
    302.0,
    31.0,
    320.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    13.0,
    326.0,
    31.0,
    344.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    13.0,
    350.0,
    31.0,
    368.0,
    fill="#000000",
    outline="")

canvas.create_text(
    37.0,
    301.0,
    anchor="nw",
    text="2-seater",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_text(
    37.0,
    326.0,
    anchor="nw",
    text="4-seater",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_text(
    37.0,
    351.0,
    anchor="nw",
    text="6-seater",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_rectangle(
    15.0,
    480.0,
    33.0,
    498.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    15.0,
    504.0,
    33.0,
    522.0,
    fill="#000000",
    outline="")

canvas.create_text(
    39.0,
    480.0,
    anchor="nw",
    text="Manual",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_text(
    39.0,
    505.0,
    anchor="nw",
    text="Automatic",
    fill="#000000",
    font=("Sintony", 15 * -1)
)

canvas.create_text(
    218.0,
    97.0,
    anchor="nw",
    text="Pickup Details",
    fill="#000000",
    font=("Sarabun Regular", 20 * -1)
)

canvas.create_rectangle(
    218.0,
    132.0,
    258.0,
    170.22222137451172,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    467.0,
    130.0,
    519.0,
    168.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    274.0,
    135.0,
    452.0,
    164.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    535.0,
    135.0,
    713.0,
    164.0,
    fill="#000000",
    outline="")

canvas.create_text(
    755.0,
    100.0,
    anchor="nw",
    text="Drop-off Details",
    fill="#000000",
    font=("Sarabun Regular", 20 * -1)
)

canvas.create_rectangle(
    755.0,
    135.0,
    795.0,
    173.22222137451172,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1004.0,
    133.0,
    1056.0,
    171.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    811.0,
    138.0,
    989.0,
    167.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1072.0,
    138.0,
    1250.0,
    167.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    1188.0,
    21.0,
    1238.0,
    71.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    210.0,
    207.0,
    1280.0,
    697.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    244.0,
    215.0,
    496.0,
    341.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    218.0,
    348.0,
    anchor="nw",
    text="Mercedes C250 | Silver",
    fill="#000000",
    font=("Sintony Bold", 18 * -1)
)

canvas.create_rectangle(
    219.0,
    381.0,
    245.0,
    409.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    314.0,
    383.0,
    340.0,
    409.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    421.0,
    383.0,
    451.0,
    413.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    245.0,
    387.0,
    anchor="nw",
    text="4-seater",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    452.0,
    382.0,
    anchor="nw",
    text="160",
    fill="#000000",
    font=("Sintony", 25 * -1)
)

canvas.create_text(
    345.0,
    388.0,
    anchor="nw",
    text="Automatic",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    500.0,
    398.0,
    anchor="nw",
    text="/ day",
    fill="#000000",
    font=("Sintony", 8 * -1)
)

canvas.create_text(
    585.0,
    348.0,
    anchor="nw",
    text="Toyota Alphard | Copper",
    fill="#000000",
    font=("Sintony Bold", 18 * -1)
)

canvas.create_rectangle(
    586.0,
    381.0,
    612.0,
    409.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    681.0,
    383.0,
    707.0,
    409.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    788.0,
    383.0,
    818.0,
    413.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    612.0,
    387.0,
    anchor="nw",
    text="6-seater",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    819.0,
    382.0,
    anchor="nw",
    text="160",
    fill="#000000",
    font=("Sintony", 25 * -1)
)

canvas.create_text(
    712.0,
    388.0,
    anchor="nw",
    text="Automatic",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    867.0,
    398.0,
    anchor="nw",
    text="/ day",
    fill="#000000",
    font=("Sintony", 8 * -1)
)

canvas.create_text(
    218.0,
    613.0,
    anchor="nw",
    text="Mazda-CX5 | Red",
    fill="#000000",
    font=("Sintony Bold", 18 * -1)
)

canvas.create_rectangle(
    219.0,
    646.0,
    245.0,
    674.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    314.0,
    648.0,
    340.0,
    674.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    421.0,
    648.0,
    451.0,
    678.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    245.0,
    652.0,
    anchor="nw",
    text="4-seater",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    452.0,
    647.0,
    anchor="nw",
    text="160",
    fill="#000000",
    font=("Sintony", 25 * -1)
)

canvas.create_text(
    345.0,
    653.0,
    anchor="nw",
    text="Automatic",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    500.0,
    663.0,
    anchor="nw",
    text="/ day",
    fill="#000000",
    font=("Sintony", 8 * -1)
)

canvas.create_text(
    585.0,
    613.0,
    anchor="nw",
    text="Mazda MX-5 | Mineral Grey",
    fill="#000000",
    font=("Sintony Bold", 18 * -1)
)

canvas.create_rectangle(
    586.0,
    646.0,
    612.0,
    674.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    681.0,
    648.0,
    707.0,
    674.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    788.0,
    648.0,
    818.0,
    678.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    612.0,
    652.0,
    anchor="nw",
    text="2-seater",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    819.0,
    647.0,
    anchor="nw",
    text="160",
    fill="#000000",
    font=("Sintony", 25 * -1)
)

canvas.create_text(
    712.0,
    653.0,
    anchor="nw",
    text="Automatic",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    867.0,
    663.0,
    anchor="nw",
    text="/ day",
    fill="#000000",
    font=("Sintony", 8 * -1)
)

canvas.create_text(
    945.0,
    348.0,
    anchor="nw",
    text="Toyota Corolla | Silver",
    fill="#000000",
    font=("Sintony Bold", 18 * -1)
)

canvas.create_rectangle(
    946.0,
    381.0,
    972.0,
    409.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1041.0,
    383.0,
    1067.0,
    409.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1148.0,
    383.0,
    1178.0,
    413.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    972.0,
    387.0,
    anchor="nw",
    text="4-seater",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    1179.0,
    382.0,
    anchor="nw",
    text="160",
    fill="#000000",
    font=("Sintony", 25 * -1)
)

canvas.create_text(
    1072.0,
    388.0,
    anchor="nw",
    text="Automatic",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    1227.0,
    398.0,
    anchor="nw",
    text="/ day",
    fill="#000000",
    font=("Sintony", 8 * -1)
)

canvas.create_text(
    945.0,
    613.0,
    anchor="nw",
    text="Perodua Myvi | Silver",
    fill="#000000",
    font=("Sintony Bold", 18 * -1)
)

canvas.create_rectangle(
    946.0,
    646.0,
    972.0,
    674.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1041.0,
    648.0,
    1067.0,
    674.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    1148.0,
    648.0,
    1178.0,
    678.0,
    fill="#FFFFFF",
    outline="")

canvas.create_text(
    972.0,
    652.0,
    anchor="nw",
    text="4-seater",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    1179.0,
    647.0,
    anchor="nw",
    text="160",
    fill="#000000",
    font=("Sintony", 25 * -1)
)

canvas.create_text(
    1072.0,
    653.0,
    anchor="nw",
    text="Automatic",
    fill="#000000",
    font=("Sintony", 13 * -1)
)

canvas.create_text(
    1227.0,
    663.0,
    anchor="nw",
    text="/ day",
    fill="#000000",
    font=("Sintony", 8 * -1)
)

canvas.create_rectangle(
    587.0,
    226.0,
    839.0,
    341.2307662963867,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    967.0,
    231.0,
    1219.0,
    340.5652160644531,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    248.0,
    484.0,
    478.0,
    606.2322769165039,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    610.0,
    485.0,
    850.0,
    613.0,
    fill="#FFFFFF",
    outline="")

canvas.create_rectangle(
    978.0,
    487.0,
    1208.0,
    605.6507873535156,
    fill="#FFFFFF",
    outline="")
window.resizable(False, False)
window.mainloop()