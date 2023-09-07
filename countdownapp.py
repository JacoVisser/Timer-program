import tkinter as tk
from tkinter import messagebox
import threading
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Timer App")
        self.root.geometry("300x220")

        self.timer_label = tk.Label(root, text="Timer:")
        self.timer_label.pack()

        self.time_display = tk.Label(root, text="00:00")
        self.time_display.pack()

        self.start_buttons_frame = tk.Frame(root)
        self.start_buttons_frame.pack(padx=10, pady=5)

        self.create_timer_button(300, "5 min")
        self.create_timer_button(600, "10 min")
        self.create_timer_button(900, "15 min")
        self.create_timer_button(1800, "30 min")

        self.custom_time_entry = tk.Entry(root)
        self.custom_time_entry.pack(padx=10, pady=10)

        self.custom_timer_button = tk.Button(root, text="Start Custom Timer", command=self.start_custom_timer)
        self.custom_timer_button.pack(padx=10, pady=10)

        self.stop_button = tk.Button(root, text="Stop Timer", command=self.stop_timer)
        self.stop_button.pack(padx=10, pady=10)
        self.stop_button.config(state=tk.DISABLED)

        self.running = False
        self.remaining_time = 0
        self.end_time = 0
        self.timer_thread = None

    def create_timer_button(self, duration, label_text):
        button = tk.Button(self.start_buttons_frame, text=label_text, command=lambda: self.start_timer(duration))
        button.pack(side=tk.LEFT, padx=10)

    def start_timer(self, duration):
        if not self.running:
            self.running = True
            self.remaining_time = duration
            self.end_time = time.time() + duration
            self.update_time_display()

            self.timer_thread = threading.Thread(target=self.run_timer)
            self.timer_thread.start()

            self.stop_button.config(state=tk.NORMAL)

    def start_custom_timer(self):
        if not self.running:
            try:
                custom_duration = int(self.custom_time_entry.get())
                if custom_duration <= 0:
                    messagebox.showerror("Error", "Please enter a valid time greater than 0.")
                    return
                self.start_timer(custom_duration)
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid numeric value.")

    def run_timer(self):
        while self.running and time.time() < self.end_time:
            self.remaining_time = int(self.end_time - time.time())
            self.update_time_display()
            time.sleep(1)

        if self.running:
            self.stop_timer()
            messagebox.showinfo("Time's Up!", "The timer has finished.")

    def stop_timer(self):
        self.running = False
        
        self.stop_button.config(state=tk.DISABLED)
        self.update_time_display()

    def update_time_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.time_display.config(text=f"{minutes:02}:{seconds:02}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()
