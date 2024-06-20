import os
import sys

site_packages_path = os.path.join(os.environ["APPDATA"], "Python", "Python39", "site-packages")
sys.path.append(site_packages_path)

from ttkthemes import ThemedTk
import tkinter as tk
from tkinter import messagebox
from tkinter import Button

BG_COLOR = '#2c3e50'
FG_COLOR = '#ecf0f1'
ACCENT_COLOR = '#3498db'
ENTRY_BG_COLOR = '#34495e'
ENTRY_FG_COLOR = '#ecf0f1'

class TimerLabel(tk.Label):
    def __init__(self, master, remaining_time, *args, **kwargs):
        super().__init__(master, *args, **kwargs, bg=BG_COLOR, fg=FG_COLOR, font=('Helvetica', 14))
        self.remaining_time = remaining_time
        self.update_text()
        self.timer_id = None

    def update_text(self):
        if self.remaining_time >= 0:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.config(text=f"{minutes:02d}:{seconds:02d}")
            self.remaining_time -= 1
            self.timer_id = self.after(1000, self.update_text)

    def reset(self):
        self.remaining_time = 150 # 2 minutes 30 in seconds
        self.after_cancel(self.timer_id)
        self.update_text()

class NamedTimerFrame(tk.Frame):
    def __init__(self, master=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.labels = []
        self.entry_boxes = []
        self.reset_buttons = []

        add_button = tk.Button(self, text='+', command=self.add_label, bg=ACCENT_COLOR, fg=FG_COLOR, font=('Helvetica', 20), bd=0, activebackground=ACCENT_COLOR)
        add_button.grid(row=0, column=0, sticky='n', pady=5, padx=5)

        remove_button = tk.Button(self, text='-', command=self.remove_label, bg=ACCENT_COLOR, fg=FG_COLOR, font=('Helvetica', 20), bd=0, activebackground=ACCENT_COLOR)
        remove_button.grid(row=2, column=0, sticky='n', pady=5, padx=5)
        
        quit_button = Button(self, text='X', command=self.quit_application, bg="red", fg="white", font=('Helvetica', 20), bd=0, activebackground="red")
        quit_button.grid(row=4, column=0, sticky='sw', pady=5, padx=5)     
        
        # set the background color for the entire frame
        self.configure(bg=BG_COLOR)
    
    def quit_application(self):
        self.master.destroy()    
    
    def add_label(self):
        if len(self.labels) >= 5:
            return

        remaining_time = 150 # 3 minutes in seconds
        name_entry = tk.Entry(self, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, font=('Helvetica', 14), highlightbackground=ACCENT_COLOR, highlightcolor=ACCENT_COLOR, highlightthickness=1)
        name_entry.grid(row=0, column=len(self.labels)*2+1, sticky='n', pady=5, padx=5)
        self.entry_boxes.append(name_entry)

        timer_label = TimerLabel(self, remaining_time, text=f"{remaining_time//60:02d}:{remaining_time%60:02d}")
        timer_label.grid(row=1, column=len(self.labels)*2+1, sticky='nsew', pady=5, padx=5)
        self.labels.append(timer_label)

        reset_button = tk.Button(self, text='Reset', command=timer_label.reset, bg=ACCENT_COLOR, fg=FG_COLOR, font=('Helvetica', 14), bd=0, activebackground=ACCENT_COLOR)
        reset_button.grid(row=2, column=len(self.labels)*2+1, sticky='n', pady=5, padx=5)
        self.reset_buttons.append(reset_button)

    def add_label(self):
        remaining_time = 150 # 2 minutes 30 in seconds
        if len(self.labels) >= 5:
            messagebox.showerror("Error", "Maximum number of timers reached!")
            return
    
        # calculate the width of each label
        label_width = 140
        total_width = len(self.labels) * label_width
    
        # calculate the maximum allowable width
        max_width = 800
        max_num_labels = max_width // label_width
    
        # if the current number of labels already fills the maximum width, show an error message and return
        if len(self.labels) >= max_num_labels:
            messagebox.showerror("Error", "Maximum number of timers reached!")
            return
    
        name_entry = tk.Entry(self, bg=ENTRY_BG_COLOR, fg=ENTRY_FG_COLOR, font=('Helvetica', 14), highlightbackground=ACCENT_COLOR, highlightcolor=ACCENT_COLOR, highlightthickness=1)
        name_entry.grid(row=0, column=len(self.labels)*3+1, sticky='n', pady=5, padx=5)
        self.entry_boxes.append(name_entry)
    
        timer_label = TimerLabel(self, remaining_time, text=f"{remaining_time//60:02d}:{remaining_time%60:02d}")
        timer_label.grid(row=1, column=len(self.labels)*3+1, sticky='nsew', pady=5, padx=5)
        self.labels.append(timer_label)
    
        reset_button = tk.Button(self, text='Reset', command=timer_label.reset, bg=ACCENT_COLOR, fg=FG_COLOR, font=('Helvetica', 14), bd=0, activebackground=ACCENT_COLOR)
        reset_button.grid(row=2, column=len(self.labels)*3+1, sticky='n', pady=5, padx=5)
        self.reset_buttons.append(reset_button)
    
        # center the timer label and reset button with their entry box
        self.grid_columnconfigure(len(self.labels)*3+1, weight=1)
        self.grid_columnconfigure(len(self.labels)*3+2, weight=1)
        self.grid_columnconfigure(len(self.labels)*3+3, weight=1)
    
        # resize the window to fit the new timer if necessary
        if total_width + label_width > max_width:
            self.master.geometry(f"{max_width}x{self.master.winfo_height()}")
        else:
            self.master.geometry(f"{total_width+label_width}x{self.master.winfo_height()}")
    
        name_entry.grid(row=0, column=len(self.labels)*3+1, sticky='n', pady=5, padx=5)
        timer_label.grid(row=1, column=len(self.labels)*3+1, sticky='n', pady=5, padx=5)
        reset_button.grid(row=2, column=len(self.labels)*3+1, sticky='n', pady=5, padx=5)
        

    def remove_label(self):
        if self.labels:
            self.labels[-1].grid_forget()
            self.entry_boxes[-1].grid_forget()
            self.reset_buttons[-1].grid_forget()
            self.labels.pop()
            self.entry_boxes.pop()
            self.reset_buttons.pop()
            
            # resize the window to default size when there are no timers left
            if not self.labels:
                self.master.geometry("200x250")
            else:
                # calculate the width of the remaining labels
                label_width = 140
                total_width = len(self.labels) * label_width
                
                # resize the window to fit the remaining labels
                max_width = 800
                if total_width > max_width:
                    self.master.geometry(f"{max_width}x{self.master.winfo_height()}")
                else:
                    self.master.geometry(f"{total_width}x{self.master.winfo_height()}")
            
# Define variables to hold the current mouse position and the offset from the top-left corner of the window
mouse_x, mouse_y = 0, 0
offset_x, offset_y = 0, 0

# When the left mouse button is clicked, calculate the offset from the top-left corner of the window
def start_drag(event):
    global mouse_x, mouse_y, offset_x, offset_y
    mouse_x, mouse_y = event.x, event.y
    offset_x, offset_y = event.x_root - root.winfo_x(), event.y_root - root.winfo_y()

# As the mouse is dragged, update the window's position
def drag(event):
    global mouse_x, mouse_y
    x, y = event.x_root - offset_x, event.y_root - offset_y
    root.geometry(f"+{x}+{y}")

if __name__ == '__main__':
    root = ThemedTk(theme='clam')
    root.overrideredirect(True)
    root.geometry("200x250")
    root.configure(bg=BG_COLOR)
    root.wm_attributes("-topmost", True)
    root.attributes("-alpha", 0.5)  # set window transparency to 50%  
    root.grid_columnconfigure(0, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    
    # Bind the start_drag and drag functions to the left mouse button
    root.bind("<Button-1>", start_drag)
    root.bind("<B1-Motion>", drag)
    
    timer_frame = NamedTimerFrame(root, bg=BG_COLOR)
    timer_frame.grid(row=0, column=1, sticky='nsew')

    root.mainloop()