import pyautogui
import threading
import keyboard
import tkinter as tk
from tkinter import simpledialog, messagebox
from tkinter import ttk
from tkinter import PhotoImage
import pygame

class AutoClicker:
    def __init__(self):
        self.running = False
        self.click_interval = 0.01  # Default click interval in seconds
        self.click_interval_hour = 0  # Default click interval in hours
        self.click_interval_minute = 0  # Default click interval in minutes
        self.start_keybind = 'F5'
        self.stop_keybind = 'F6'
        self.mouse_button = 'left'  # Default mouse button
        self.dark_mode = False  # Default dark mode setting
        self.simple_mode = False  # Default simple mode setting
        self.music = False
        self.show_popup_messages = True

auto_clicker = AutoClicker()

def click():
    while auto_clicker.running:
        pyautogui.click(button=auto_clicker.mouse_button)
        threading.Event().wait(auto_clicker.click_interval)

def start_clicking():
    if not auto_clicker.running:
        auto_clicker.running = True
        threading.Thread(target=click).start()

def stop_clicking():
    auto_clicker.running = False

def start_stop_clicking():
    if auto_clicker.running:
        stop_clicking()
        root.deiconify()
        start_stop_button.config(text="Start", bg="#4caf50")
        if auto_clicker.show_popup_messages:
            messagebox.showinfo("Autoclicker Stopped", "Autoclicker stopped.")
    else:
        start_clicking()
        root.iconify()
        start_stop_button.config(text="Stop", bg="#f44336")
        status_label.config(text=f"Autoclicker started. Click Interval: {auto_clicker.click_interval} seconds.")

def stop_autoclicker():
    if auto_clicker.running:
        stop_clicking()
        root.deiconify()
        start_stop_button.config(text="Start", bg="#4caf50")
        if auto_clicker.show_popup_messages:
            messagebox.showinfo("Autoclicker Stopped", "Autoclicker stopped.")
    else:
        if auto_clicker.show_popup_messages:
            messagebox.showerror("Error", "Autoclicker didn't start yet.")

def update_click_interval(event=None):
    try:
        interval_text = interval_entry.get().lower()

        if interval_text.endswith("ms"):
            interval = float(interval_text[:-2]) / 1000  # Convert milliseconds to seconds
        else:
            interval = float(interval_text)

        if interval > 0:
            auto_clicker.click_interval = interval
            status_label.config(text=f"Click Interval updated to {interval} seconds.")
        else:
            status_label.config(text="Please enter a positive interval value.")
    except ValueError:
        status_label.config(text="Invalid interval value. Please enter a valid number.")

def change_mouse_button(event=None):
    new_mouse_button = mouse_button_combobox.get()
    auto_clicker.mouse_button = new_mouse_button.lower()
    status_label.config(text=f"Mouse Button updated to '{new_mouse_button}'.")

def toggle_dark_mode():
    auto_clicker.dark_mode = not auto_clicker.dark_mode
    update_dark_mode()

def toggle_simple_mode():
    auto_clicker.simple_mode = not auto_clicker.simple_mode
    update_interface()

def update_dark_mode():
    bg_color = "#222" if auto_clicker.dark_mode else "#f0f0f0"
    fg_color = "white" if auto_clicker.dark_mode else "black"

    root.configure(bg=bg_color)
    status_label.config(bg=bg_color, fg=fg_color)
    start_stop_button.config(bg="#4caf50" if not auto_clicker.running else "#f44336", fg="white")
    interval_label.config(bg=bg_color, fg=fg_color)
    interval_entry.config(bg=bg_color, fg=fg_color)

    if auto_clicker.running:
        start_stop_button.config(text="Stop")
    else:
        start_stop_button.config(text="Start")

def update_interface():
    if auto_clicker.simple_mode:
        interval_label.pack_forget()
        interval_entry.pack_forget()
        settings_button.pack_forget()
        mouse_button_combobox.pack_forget()
    else:
        interval_label.pack()
        interval_entry.pack()
        mouse_button_combobox.pack()
        settings_button.pack(side=tk.TOP, anchor=tk.NE)

    start_stop_button.config(text="Stop" if auto_clicker.running else "Start")
    root.update()

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")

    # Styling for the settings window
    settings_window.geometry("600x500")
    settings_window.configure(bg="#f0f0f0")
    settings_window.resizable(False, False)

    canvas = tk.Canvas(settings_window, bg="#f0f0f0")
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(settings_window, orient=tk.VERTICAL, command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    key_icon = PhotoImage(file="icons/key.png")
    frame = tk.Frame(canvas, bg="#f0f0f0")
    canvas.create_window((0, 0), window=frame, anchor=tk.NW)

    create_frame(frame, "General", [
        ("How to Use", open_help, None),
        ("About Autoclicker", open_about, None),
        ("Change Start Keybind", change_start_keybind,key_icon),
        ("Change Stop Keybind", change_stop_keybind,key_icon),
    ])

    create_frame(frame, "Appearance", [
        ("Dark Mode", toggle_dark_mode,None),
        ("Simple Mode", toggle_simple_mode,None),
        ("Music", toggle_music,None),
        ("Show Popup Messages", toggle_popup_messages,None),
    ])

    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

def create_frame(parent, title, buttons):
    frame = tk.Frame(parent, bg="#f0f0f0")
    frame.pack(pady=10)

    title = tk.Label(frame, text=title, font=("Open Sans Bold", 14), bg="#f0f0f0")
    title.grid(row=0, column=0, columnspan=2, pady=10)

    for i, (button_text, command, icon) in enumerate(buttons, start=1):
        tk.Button(frame, text=button_text, command=command, font=("Open Sans Bold", 10), padx=15, pady=7, bd=0,
                  borderwidth=2, relief="solid", activebackground="#546e7a", image=icon if icon else None,
                  bg="#607d8b" if i % 2 == 0 else "#009688", fg="white", compound=tk.LEFT).grid(row=i, column=0 if i % 2 == 1 else 1, pady=7, padx=5)

def open_about():
    about_message = "Roblox Autoclicker\n\nDeveloped by ChatGPT. \n\nThis autoclicker is an app that automates mouse clicks at a specified interval.\n\nAutoclick with caution, as you might get banned"
    messagebox.showinfo("About Autoclicker", about_message)

def toggle_popup_messages():
    auto_clicker.show_popup_messages = not auto_clicker.show_popup_messages

# Initialize Pygame mixer
pygame.mixer.init()

# Load the music file
pygame.mixer.music.load(r"theme.mp3")

# By default, set the music to play in mute mode
pygame.mixer.music.set_volume(1.0)

# Function to toggle the music on/off
def toggle_music():
    auto_clicker.music = not auto_clicker.music
    if auto_clicker.music:
        pygame.mixer.music.play(loops=-1)  # Set desired loop value, -1 for infinite loop
    else:
        pygame.mixer.music.stop()

# Call toggle_music() where needed, such as a button press or menu option, to switch the music on or off.

def open_help():
    message = "1. Press Spacebar to start the autoclicker.\n" \
              "2. Use the 'Start/Stop' button to manually start/stop clicking.\n" \
              "3. Adjust the click interval in seconds and update it.\n" \
              "4. Access settings to change the stop keybind."
    messagebox.showinfo("How to Use", message)

def change_start_keybind():
    new_start_keybind = simpledialog.askstring("Change Start Keybind", "Enter new start keybind:")
    if new_start_keybind:
        auto_clicker.start_keybind = new_start_keybind
        status_label.config(text=f"Start Keybind updated to '{new_start_keybind}'.")

def change_stop_keybind():
    new_stop_keybind = simpledialog.askstring("Change Stop Keybind", "Enter new stop keybind:")
    if new_stop_keybind:
        auto_clicker.stop_keybind = new_stop_keybind
        status_label.config(text=f"Stop Keybind updated to '{new_stop_keybind}'.")

# Function to handle global start keybind
def global_start_callback(e):
    if e.event_type == keyboard.KEY_DOWN:  # Check if the key is pressed
        start_stop_clicking()

def global_stop_callback(e):
    if e.event_type == keyboard.KEY_DOWN:  # Check if the key is pressed
        stop_autoclicker()

# GUI setup
root = tk.Tk()
root.title("Roblox Autoclicker")

# Set the icon for the window
root.iconbitmap(r"Fart.ico")

# Center the window
window_width = 800
window_height = 388
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = (screen_width - window_width) // 2
y_coordinate = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")
root.resizable(False, False)

# Label with custom font and color
status_label = tk.Label(root, text="Press Start to begin autoclicking.", font=("Open Sans Bold", 12), bg="#f0f0f0")
status_label.pack(pady=10)

# Combobox for changing the mouse button
mouse_button_combobox = ttk.Combobox(root, values=['left', 'right', 'middle'], font=("Open Sans Bold", 11), state="readonly", background="#f0f0f0", foreground="black")
mouse_button_combobox.set(auto_clicker.mouse_button)
mouse_button_combobox.pack()

start_icon = PhotoImage(file="icons/cursor.png")
settings_icon = PhotoImage(file="icons/settings.png")

# Button with custom color, padding, and rounded corners
start_stop_button = tk.Button(root, text="Start", command=start_stop_clicking, font=("Open Sans Bold", 12), bg="#4caf50", fg="white", padx=40, pady=40, bd=0, relief=tk.GROOVE, borderwidth=0, highlightthickness=0, highlightbackground="#f0f0f0", highlightcolor="#f0f0f0", overrelief=tk.GROOVE, activebackground="#43a047")
start_stop_button.config(image=start_icon, compound=tk.LEFT, borderwidth=2, relief="solid", padx=10, pady=10)
start_stop_button.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# Create a frame for hour, minute, and second intervals
time_frame = tk.Frame(button_frame, bg="#f0f0f0")
time_frame.pack(pady=10)

# Label for hour interval
hour_label = tk.Label(time_frame, text="Hour Interval:", font=("Open Sans Bold", 14), bg="#f0f0f0")
hour_label.grid(row=0, column=0, pady=5)

# Entry for hour interval
hour_entry = tk.Entry(time_frame)
hour_entry.insert(0, auto_clicker.click_interval_hour)
hour_entry.grid(row=1, column=0, pady=5)

# Label for minute interval
minute_label = tk.Label(time_frame, text="Minute Interval:", font=("Open Sans Bold", 14), bg="#f0f0f0")
minute_label.grid(row=0, column=1, pady=5)

# Entry for minute interval
minute_entry = tk.Entry(time_frame)
minute_entry.insert(0, auto_clicker.click_interval_minute)
minute_entry.grid(row=1, column=1, pady=5)

# Label for second interval
second_label = tk.Label(time_frame, text="Seconds Interval:", font=("Open Sans Bold", 14), bg="#f0f0f0")
second_label.grid(row=0, column=2, pady=5)

# Entry for second interval
interval_entry = tk.Entry(time_frame)
interval_entry.insert(0, auto_clicker.click_interval)
interval_entry.grid(row=1, column=2, pady=5)

# Bind FocusOut event to update the click interval instantly
interval_entry.bind('<FocusOut>', update_click_interval)

# Button with custom color, padding, and rounded corners
settings_button = tk.Button(root, text="Settings", command=open_settings, font=("Open Sans Bold", 12), bg="#4cb6ff", fg="white", padx=20, pady=10, bd=0, relief=tk.GROOVE, borderwidth=0, highlightthickness=0, highlightbackground="#f0f0f0", highlightcolor="#f0f0f0", overrelief=tk.GROOVE, activebackground="#1565c0")
settings_button.config(image=settings_icon, compound=tk.LEFT, borderwidth=2, relief="solid", padx=10, pady=10)
settings_button.pack(side=tk.TOP, anchor=tk.NE)

# Bind start and stop keybind to start/stop autoclicker globally
keyboard.on_press_key(auto_clicker.start_keybind, global_start_callback)
keyboard.on_press_key(auto_clicker.stop_keybind, global_stop_callback)

# Bind Combobox selection event to update the mouse button instantly
mouse_button_combobox.bind("<<ComboboxSelected>>", change_mouse_button)

# Keep the GUI running
root.mainloop()
