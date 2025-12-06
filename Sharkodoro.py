from tkinter import *

# ---------------------------- VARIABEL ------------------------------- #
PINK = "#0b3467"
RESET = "#324e6c"
START = "#24599E"
PAUSE = "#086e99"
BLUE = "#cff1fc"
BROWN = "#483C32"
BROWNIE = "#7B3F00"
GREEN = "#2E8B57"
FONT_NAME = "Times New Roman"

# ---------------------------- OOP CLASS: TimerManager ------------------------------- #
class TimerManager:
    """Class untuk mengelola timer (Materi OOP 1)"""
    
    def __init__(self):
        self.work_min = 1
        self.short_break = 5
        self.long_break = 20
        self.reps = 0
        self.timer = None
        self.is_paused = False
        self.pause_time = 0
    
    def get_current_session(self):
        """Method untuk menentukan sesi saat ini"""
        if self.reps % 8 == 0:
            return ("Long Break!", self.long_break, RESET, "chill")
        elif self.reps % 2 == 0:
            return ("Short Break", self.short_break, PINK, "chill")
        else:
            return ("Work Time", self.work_min, START, "work")
    
    def increment_reps(self):
        """Method untuk menambah jumlah repetisi"""
        self.reps += 1
    
    def reset_all(self):
        """Method untuk reset semua data timer"""
        self.reps = 0
        self.is_paused = False
        self.pause_time = 0

# ---------------------------- FUNCTION DAN PERULANGAN ------------------------------- #
def setup_preset_buttons(preset_frame):
    """Function untuk membuat tombol preset dengan for loop"""
    work_presets = [
        (1, "1 min"),
        (30, "30 min"),
        (45, "45 min")
    ]
    
    buttons = []  # List untuk menyimpan tombol
    for i, (minutes, text) in enumerate(work_presets):
        btn = Button(preset_frame, text=text, 
                    font=(FONT_NAME, 10), bg=BROWNIE, fg="white",
                    padx=10, pady=5, 
                    command=lambda m=minutes: set_work_time(m))
        btn.grid(row=1, column=i, padx=5)
        buttons.append(btn)  # Menyimpan tombol ke dalam list
    
    return buttons

def setup_break_buttons(break_frame):
    """Function untuk membuat tombol preset break dengan for loop"""
    short_break_presets = [
        (5, "5 min"),
        (10, "10 min"),
        (15, "15 min")
    ]
    
    buttons = []
    
    # Short break presets
    for i, (minutes, text) in enumerate(short_break_presets):
        btn = Button(break_frame, text=text, 
                    font=(FONT_NAME, 10), bg=PINK, fg="white",
                    padx=10, pady=5,
                    command=lambda m=minutes: set_break_time("short", m))
        btn.grid(row=1, column=i, padx=5)
        buttons.append(btn)
    
    return buttons

def create_checkmarks(count):
    """Function untuk membuat checkmarks dengan while loop"""
    marks = ""
    i = 0
    while i < count:
        marks += "✓"
        i += 1
    return marks

def set_work_time(minutes):
    """Function untuk set waktu kerja"""
    timer_manager.work_min = minutes
    if timer_manager.reps % 2 == 0:  # Jika sedang di sesi work
        canvas.itemconfig(timer_text, text=f"{minutes:02d}:00")
    update_work_label()
    update_image("work")

def set_break_time(break_type, minutes):
    """Function untuk set waktu break"""
    if break_type == "short":
        timer_manager.short_break = minutes
        if timer_manager.reps % 2 == 1:  # Jika sedang di sesi short break
            canvas.itemconfig(timer_text, text=f"{minutes:02d}:00")
    else:  # long break
        timer_manager.long_break = minutes
        if timer_manager.reps == 7:  # Jika sedang di sesi long break
            canvas.itemconfig(timer_text, text=f"{minutes:02d}:00")
    
    update_break_labels()

def update_work_label():
    """Update label work time"""
    work_label.config(text=f"Work: {timer_manager.work_min} min")

def update_break_labels():
    """Update label break times"""
    short_label.config(text=f"Short Break: {timer_manager.short_break} min")
    
# ---------------------------- IMAGE HANDLING ------------------------------- #
def update_image(image_name):
    """Function untuk update gambar di canvas"""
    if image_name == "chill":
        canvas.itemconfig(canvas_image, image=chill_png)
    else:
        canvas.itemconfig(canvas_image, image=work_png)

# ---------------------------- TIMER FUNCTIONS ------------------------------- #
def start_timer():
    timer_manager.increment_reps()
    start_button.config(state="disabled")
    pause_button.config(state="normal")
    timer_manager.is_paused = False
    
    session_name, minutes, color, img = timer_manager.get_current_session()
    title_label.config(text=session_name, fg=color)
    update_image(img)
    
    count_down(minutes * 60)
    
    # Update session info
    current_session = min((timer_manager.reps + 1) // 2, 4)
    session_info.config(text=f"Session: {current_session}/4")

def pause_timer():
    if not timer_manager.is_paused:
        # Pause timer
        timer_manager.is_paused = True
        pause_button.config(text="Resume", bg=START)
        
        # Simpan waktu tersisa
        time_str = canvas.itemcget(timer_text, "text")
        minutes, seconds = map(int, time_str.split(":"))
        timer_manager.pause_time = minutes * 60 + seconds
        
        window.after_cancel(timer_manager.timer)
        title_label.config(text=f"{title_label.cget('text')} (Paused)", fg= PAUSE)
    else:
        # Resume timer
        timer_manager.is_paused = False
        pause_button.config(text="Pause", bg=PAUSE)
        
        session_name, _, color, img = timer_manager.get_current_session()
        title_label.config(text=session_name, fg=color)
        update_image(img)
        
        count_down(timer_manager.pause_time)

def reset_timer():
    if timer_manager.timer:
        window.after_cancel(timer_manager.timer)
    
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Jaws Your Time!", fg=BROWN)
    check_marks.config(text="")
    timer_manager.reset_all()
    start_button.config(state="normal")
    pause_button.config(state="disabled", text="Pause", bg=PAUSE)
    session_info.config(text="Session: 0/4")
    update_image("work")
    update_work_label()
    update_break_labels()

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    # Perulangan tidak langsung, tapi logic sederhana
    minutes = count // 60
    seconds = count % 60
    
    if minutes < 10:
        minutes = f"0{minutes}"
    if seconds < 10:
        seconds = f"0{seconds}"
    
    canvas.itemconfig(timer_text, text=f"{minutes}:{seconds}")
    
    if count > 0 and not timer_manager.is_paused:
        timer_manager.timer = window.after(1000, count_down, count - 1)
        timer_manager.pause_time = count - 1
    elif count == 0 and not timer_manager.is_paused:
        start_timer()
        
        # Buat checkmarks dengan function
        work_sessions = timer_manager.reps // 2
        marks = create_checkmarks(work_sessions)
        check_marks.config(text=marks)
        
        window.bell()

# ---------------------------- MAIN UI SETUP ------------------------------- #
window = Tk()
window.title("Sharkodoro: Jaws Your Time!")
window.config(padx=100, pady=30, bg=BLUE)

# Create TimerManager object (OOP)
timer_manager = TimerManager()

# Title Label
title_label = Label(text="Jaws Your Time!", fg=BROWN, bg=BLUE, 
                   font=(FONT_NAME, 35, "bold"))
title_label.grid(column=1, row=0, pady=(0, 10))

# Canvas
canvas = Canvas(width=200, height=244, bg=BLUE, highlightthickness=0)
work_png = PhotoImage(file="work.png")
chill_png = PhotoImage(file="chill.png")
canvas_image = canvas.create_image(100, 112, image=work_png)
timer_text = canvas.create_text(100, 227, text="00:00", fill="black", 
                               font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1, pady=10)

# Current Settings Frame
settings_frame = Frame(window, bg=BLUE)
settings_frame.grid(column=1, row=2, pady=10)

# Labels untuk menampilkan current settings
work_label = Label(settings_frame, text=f"Work: {timer_manager.work_min} min", 
                   fg=BROWNIE, bg=BLUE, font=(FONT_NAME, 11))
work_label.grid(row=0, column=0, padx=10)

short_label = Label(settings_frame, text=f"Short Break: {timer_manager.short_break} min", 
                    fg=PINK, bg=BLUE, font=(FONT_NAME, 11))
short_label.grid(row=0, column=1, padx=10)


# Check marks
check_marks = Label(text="", fg=START, bg=BLUE, 
                   font=(FONT_NAME, 25, "bold"))
check_marks.grid(column=1, row=3, pady=5)

# Session info
session_info = Label(text="Session: 0/4", fg=BROWN, bg=BLUE,
                    font=(FONT_NAME, 14))
session_info.grid(column=1, row=4, pady=5)

# Buttons Frame
button_frame = Frame(window, bg=BLUE)
button_frame.grid(column=1, row=5, pady=15)

# Main Buttons
start_button = Button(button_frame, text="Start", 
                     font=(FONT_NAME, 14, "bold"), 
                     bg=START, fg="white", 
                     padx=20, pady=10,
                     command=start_timer)
start_button.grid(column=0, row=0, padx=5)

pause_button = Button(button_frame, text="Pause", 
                     font=(FONT_NAME, 14, "bold"), 
                     bg=PAUSE, fg="white", 
                     padx=20, pady=10,
                     command=pause_timer,
                     state="disabled")
pause_button.grid(column=1, row=0, padx=5)

reset_button = Button(button_frame, text="Reset", 
                     font=(FONT_NAME, 14, "bold"), 
                     bg=RESET, fg="white", 
                     padx=20, pady=10,
                     command=reset_timer)
reset_button.grid(column=2, row=0, padx=5)

# Preset Frame
preset_frame = Frame(window, bg=BLUE)
preset_frame.grid(column=1, row=6, pady=15)

# Work Time Presets
work_label_preset = Label(preset_frame, text="Quick Work Time:", 
                         fg=BROWN, bg=BLUE, font=(FONT_NAME, 12, "bold"))
work_label_preset.grid(row=0, column=0, columnspan=3, pady=5)

# Membuat tombol preset work time dengan function
setup_preset_buttons(preset_frame)

# Break Time Presets Frame
break_frame = Frame(window, bg=BLUE)
break_frame.grid(column=1, row=7, pady=10)

# Short Break Presets
short_label_preset = Label(break_frame, text="Short Break Presets:", 
                          fg=PINK, bg=BLUE, font=(FONT_NAME, 12, "bold"))
short_label_preset.grid(row=0, column=0, columnspan=3, pady=(10, 5))


# Membuat tombol preset break time dengan function
setup_break_buttons(break_frame)

# Configure grid
window.grid_columnconfigure(0, weight=1)
window.grid_columnconfigure(1, weight=0)
window.grid_columnconfigure(2, weight=1)

window.mainloop()