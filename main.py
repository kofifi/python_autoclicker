import tkinter as tk
import keyboard
import pyautogui
from tkinter import messagebox

class AutoclickerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Autoclicker")
        self.root.geometry("300x200")
        self.root.resizable(False, False)
        self.root.configure(bg="#EFEFEF")

        self.autoclicker_active = False
        self.default_click_key = "3"  # Default click key
        self.default_click_delay = "1.0"  # Default click delay in seconds
        self.click_key = self.default_click_key
        self.click_delay = float(self.default_click_delay)
        self.autoclick_mode = tk.StringVar(value="keyboard")  # Default autoclick mode
        self.mouse_button_var = tk.StringVar(value="left")  # Default mouse button

        self.init_ui()
        self.init_settings_window()

        self.update_status_label()
        keyboard.on_press_key(TOGGLE_KEY, self.toggle_clicking)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.clicking_job = None
        self.settings_saved = True  # To track whether settings are saved

    def init_ui(self):
        status_label = tk.Label(self.root, text="Autoclicker is OFF", padx=10, pady=10, font=("Arial", 14),
                                bg="#EFEFEF")
        status_label.pack()

        button_frame = tk.Frame(self.root, bg="#EFEFEF")
        button_frame.pack(pady=20)

        self.toggle_button = tk.Button(button_frame, text="Start Autoclicking (F10)", command=self.toggle_clicking,
                                  font=("Arial", 12), bg="#4CAF50", fg="white")
        self.toggle_button.pack(pady=5)

        settings_button = tk.Button(button_frame, text="Settings", command=self.open_settings, font=("Arial", 12),
                                    bg="#1976D2", fg="white")
        settings_button.pack(pady=5)

    def init_settings_window(self):
        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("400x450")
        self.settings_window.protocol("WM_DELETE_WINDOW", self.close_settings)
        self.settings_window.withdraw()

        click_key_label = tk.Label(self.settings_window, text="Click Key:", font=("Arial", 12))
        click_key_label.pack(pady=5)
        self.click_key_var = tk.StringVar(value=self.default_click_key)
        self.click_key_entry = tk.Entry(self.settings_window, font=("Arial", 12), textvariable=self.click_key_var)
        self.click_key_entry.pack(pady=5)

        click_delay_label = tk.Label(self.settings_window, text="Click Delay (seconds):", font=("Arial", 12))
        click_delay_label.pack(pady=5)
        self.click_delay_var = tk.StringVar(value=self.default_click_delay)
        self.click_delay_entry = tk.Entry(self.settings_window, font=("Arial", 12), textvariable=self.click_delay_var)
        self.click_delay_entry.pack(pady=5)

        autoclick_mode_label = tk.Label(self.settings_window, text="Autoclick Mode:", font=("Arial", 12))
        autoclick_mode_label.pack(pady=5)
        keyboard_radio = tk.Radiobutton(self.settings_window, text="Keyboard", variable=self.autoclick_mode, value="keyboard", font=("Arial", 12))
        keyboard_radio.pack()
        mouse_radio = tk.Radiobutton(self.settings_window, text="Mouse", variable=self.autoclick_mode, value="mouse", font=("Arial", 12))
        mouse_radio.pack()

        mouse_button_label = tk.Label(self.settings_window, text="Mouse Button:", font=("Arial", 12))
        mouse_button_label.pack(pady=5)
        left_button_radio = tk.Radiobutton(self.settings_window, text="Left Button", variable=self.mouse_button_var, value="left", font=("Arial", 12))
        left_button_radio.pack()
        right_button_radio = tk.Radiobutton(self.settings_window, text="Right Button", variable=self.mouse_button_var, value="right", font=("Arial", 12))
        right_button_radio.pack()

        save_button = tk.Button(self.settings_window, text="Save Settings", command=self.save_settings,
                                font=("Arial", 12), bg="#1976D2", fg="white")
        save_button.pack(pady=10)

    def open_settings(self):
        self.settings_window.deiconify()

    def toggle_clicking(self, e=None):
        self.autoclicker_active = not self.autoclicker_active
        self.update_status_label()

        if self.autoclicker_active:
            self.start_autoclicking()
        else:
            self.stop_autoclicking()

        self.update_toggle_button_label()

    def update_toggle_button_label(self):
        toggle_label = "Stop Autoclicking" if self.autoclicker_active else "Start Autoclicking"
        self.toggle_button.config(text=toggle_label)

    def close_settings(self):
        if not self.settings_saved:
            # Prompt user to save settings before closing
            if messagebox.askyesno("Unsaved Changes", "You have unsaved settings. Save before closing?"):
                self.save_settings()

        self.settings_window.withdraw()

    def save_settings(self):
        self.click_key = self.click_key_entry.get()
        self.click_delay = float(self.click_delay_entry.get())
        self.settings_saved = True
        self.close_settings()

    def update_status_label(self):
        status_text = "Autoclicker is ON" if self.autoclicker_active else "Autoclicker is OFF"
        status_label = self.root.winfo_children()[0]
        status_label.config(text=status_text)
        self.root.after(100, self.update_status_label)

    def on_closing(self):
        if self.autoclicker_active:
            self.stop_autoclicking()
        self.root.destroy()

    def start_autoclicking(self):
        if not self.clicking_job:
            self.clicking_job = self.root.after(int(self.click_delay * 1000), self.perform_click)

    def stop_autoclicking(self):
        if self.clicking_job:
            self.root.after_cancel(self.clicking_job)
            self.clicking_job = None

    def perform_click(self):
        if self.autoclicker_active:
            if self.autoclick_mode.get() == "keyboard":
                keyboard.press_and_release(self.click_key)
            else:
                self.perform_mouse_click()

            self.clicking_job = self.root.after(int(self.click_delay * 1000), self.perform_click)

    def perform_mouse_click(self):
        button = "left" if self.mouse_button_var.get() == "left" else "right"
        pyautogui.click(button=button)

TOGGLE_KEY = "F10"

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerApp(root)
    root.mainloop()
