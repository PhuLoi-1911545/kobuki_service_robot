import tkinter as tk

def create_popup():
    popup = tk.Toplevel()
    popup.title("Popup window")
    popup.geometry("200x100")
    label = tk.Label(popup, text="Do you want to confirm?")
    label.pack(pady=20)
    confirm_button = tk.Button(popup, text="Confirm", command=lambda: on_confirm(popup))
    confirm_button.pack(side="left", padx=10)
    deny_button = tk.Button(popup, text="Deny", command=lambda: on_deny(popup, label, confirm_button, deny_button))
    deny_button.pack(side="right", padx=10)
    
def on_confirm(popup):
    # Do something when the "Confirm" button is clicked
    popup.destroy()

def on_deny(popup, label, button1, button2):
    # Do something when the "Deny" button is clicked
    button1.pack_forget()
    button2.pack_forget()
    label.config(text="Confirmation denied.")
    confirm_button = tk.Button(button1.master, text="Confirm", command=lambda: on_confirm(button1.master))
    confirm_button.pack(side="left", padx=10)
    cancel_button = tk.Button(button1.master, text="Cancel", command=button1.master.destroy)
    cancel_button.pack(side="right", padx=10)

root = tk.Tk()
root.geometry("300x200")

button = tk.Button(root, text="Open popup", command=create_popup)
button.pack(pady=50)

root.mainloop()
