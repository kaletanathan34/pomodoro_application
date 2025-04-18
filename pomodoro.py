import time
import tkinter as tk
from tkinter import ttk
from plyer import notification
import threading

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Set colors
        self.bg_color = "#f0f0f0"
        self.work_color = "#ff6347"  # Tomato red
        self.break_color = "#98fb98"  # Pale green
        
        # Configure the root window
        self.root.configure(bg=self.bg_color)
        
        # Variables
        self.work_time = 25 * 60  # 25 minutes in seconds
        self.break_time = 5 * 60  # 5 minutes in seconds
        self.timer_running = False
        self.current_mode = "Work"
        self.remaining_time = self.work_time
        self.timer_thread = None
        
        # Create and place UI elements
        self.create_widgets()
        
        # Initially update the display
        self.update_display()
        
    def create_widgets(self):
        # Title label
        self.title_label = tk.Label(
            self.root, 
            text="Pomodoro Timer", 
            font=("Arial", 20, "bold"),
            bg=self.bg_color
        )
        self.title_label.pack(pady=20)
        
        # Mode label
        self.mode_label = tk.Label(
            self.root,
            text=f"Mode: {self.current_mode}",
            font=("Arial", 14),
            bg=self.bg_color
        )
        self.mode_label.pack(pady=5)
        
        # Time display
        self.time_display = tk.Label(
            self.root,
            text="25:00",
            font=("Arial", 36, "bold"),
            bg=self.bg_color,
            fg=self.work_color
        )
        self.time_display.pack(pady=15)
        
        # Progress bar
        self.progress_var = tk.DoubleVar(value=100)
        self.progress_bar = ttk.Progressbar(
            self.root,
            orient="horizontal",
            length=300,
            mode="determinate",
            variable=self.progress_var
        )
        self.progress_bar.pack(pady=10)
        
        # Control buttons frame
        self.button_frame = tk.Frame(self.root, bg=self.bg_color)
        self.button_frame.pack(pady=10)
        
        # Start/Pause button
        self.start_button = tk.Button(
            self.button_frame,
            text="Start",
            command=self.toggle_timer,
            width=10,
            bg="#4caf50",  # Green
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.start_button.grid(row=0, column=0, padx=5)
        
        # Reset button
        self.reset_button = tk.Button(
            self.button_frame,
            text="Reset",
            command=self.reset_timer,
            width=10,
            bg="#f44336",  # Red
            fg="white",
            font=("Arial", 10, "bold")
        )
        self.reset_button.grid(row=0, column=1, padx=5)
    
    def toggle_timer(self):
        if self.timer_running:
            self.timer_running = False
            self.start_button.config(text="Resume", bg="#4caf50")
        else:
            self.timer_running = True
            self.start_button.config(text="Pause", bg="#ff9800")  # Orange
            
            # Start the timer in a separate thread if not already running
            if self.timer_thread is None or not self.timer_thread.is_alive():
                self.timer_thread = threading.Thread(target=self.run_timer)
                self.timer_thread.daemon = True  # Thread will close when the main program closes
                self.timer_thread.start()
    
    def reset_timer(self):
        self.timer_running = False
        self.start_button.config(text="Start", bg="#4caf50")
        self.current_mode = "Work"
        self.remaining_time = self.work_time
        self.update_display()
        self.update_mode_display()
    
    def run_timer(self):
        while True:
            if self.timer_running and self.remaining_time > 0:
                self.remaining_time -= 1
                self.update_display()
                time.sleep(1)
            elif self.timer_running and self.remaining_time <= 0:
                self.switch_mode()
            else:
                time.sleep(0.1)  # Small delay when paused to prevent high CPU usage
    
    def switch_mode(self):
        if self.current_mode == "Work":
            self.current_mode = "Break"
            self.remaining_time = self.break_time
            self.show_notification("Work session completed!", "Time for a 5-minute break.")
        else:
            self.current_mode = "Work"
            self.remaining_time = self.work_time
            self.show_notification("Break completed!", "Time to get back to work for 25 minutes.")
        
        self.update_mode_display()
        self.update_display()
    
    def update_mode_display(self):
        self.mode_label.config(text=f"Mode: {self.current_mode}")
        
        if self.current_mode == "Work":
            self.time_display.config(fg=self.work_color)
        else:
            self.time_display.config(fg=self.break_color)
    
    def update_display(self):
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        time_string = f"{minutes:02d}:{seconds:02d}"
        self.time_display.config(text=time_string)
        
        # Update progress bar
        if self.current_mode == "Work":
            progress = (self.remaining_time / self.work_time) * 100
        else:
            progress = (self.remaining_time / self.break_time) * 100
        
        self.progress_var.set(progress)
        
        # Update the window to reflect changes
        self.root.update_idletasks()
    
    def show_notification(self, title, message):
        notification.notify(
            title=title,
            message=message,
            app_name="Pomodoro Timer",
            timeout=10  # seconds
        )

def main():
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()