import customtkinter as ctk

def toggle_checkbox():
    if var.get() == 1:
        chk.configure(state="disabled")  # Disable checkbox
        print("yes")
    else:
        chk.configure(state="normal")  # Enable checkbox
        print("no")

# Set up the application
app = ctk.CTk()
app.title("CustomTkinter Checkbox Test")

var = ctk.IntVar(value=1)
chk = ctk.CTkCheckBox(app, text="Test Checkbox", variable=var, command=toggle_checkbox)
chk.pack(pady=20)

toggle_btn = ctk.CTkButton(app, text="Toggle Checkbox State", command=toggle_checkbox)
toggle_btn.pack(pady=20)

app.mainloop()
