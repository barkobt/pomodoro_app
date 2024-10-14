import time
from tkinter import *
from PIL import Image, ImageTk

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
cycle_counter = 0  # Which cycle im on it
timer_running = False
timer_id = None  # Global timer ID to cancel 'after' calls

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global cycle_counter, timer_running, timer_id
    cycle_counter = 0  # Sayaç sıfırla
    canvas.itemconfig(timer_text, text="00:00")
    start_button.configure(state=NORMAL)
    timer.config(text="Timer", font=(FONT_NAME, 45, "bold"), fg=GREEN, bg=YELLOW)
    if timer_id:
        root.after_cancel(timer_id)  # cancel the current timer

# ---------------------------- TIMER MECHANISM ------------------------------- # 

def start_counting(minute=0, second=5):
    timer.config(text="WORK", fg=GREEN)
    global cycle_counter, timer_id
    start_button.configure(state=DISABLED)
    if minute >= 0 and second >= 0:
        canvas.itemconfig(timer_text, text=f"{minute:02d}:{second:02d}")
        
        if second > 0:
            second -= 1
        else:
            second = 59
            minute -= 1
        
        timer_id = root.after(1000, start_counting, minute, second)
    else:
        cycle_counter += 1
        if cycle_counter % 4 == 0:
            long_break_time()
        else:
            short_break_time()


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 

def short_break_time(minute=0, second=1):
    timer.config(text="BREAK", fg=RED)
    global timer_id
    if minute >= 0 and second >= 0:
        canvas.itemconfig(timer_text, text=f"{minute:02d}:{second:02d}")
        
        if second > 0:
            second -= 1
        else:
            second = 59
            minute -= 1

        timer_id = root.after(1000, short_break_time, minute, second)
    else:
        start_counting()

def long_break_time(minute=0, second=3):
    timer.config(text="BREAK", fg=RED)
    global timer_id
    if minute >= 0 and second >= 0:
        canvas.itemconfig(timer_text, text=f"{minute:02d}:{second:02d}")
        
        if second > 0:
            second -= 1
        else:
            second = 59
            minute -= 1

        timer_id = root.after(1000, long_break_time, minute, second)
    else:
        reset_timer()


# ---------------------------- UI SETUP ------------------------------- #

root = Tk()
root.minsize(width=400, height=400)
root.title("Pomodoro")
root.config(bg=YELLOW, padx=100, pady=50)

canvas = Canvas(bg=YELLOW, width=200, height=224, highlightthickness=0)
canvas.grid(row=1, column=1)

background = PhotoImage(file="./tomato.png")
canvas.create_image(100, 112, image=background)

timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))

timer = Label(text="Timer", font=(FONT_NAME, 45, "bold"), fg=GREEN, bg=YELLOW)
timer.grid(row=0, column=1)

start_button = Button(text="Start", bg=YELLOW, highlightbackground=YELLOW, command=start_counting)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset", bg=YELLOW, highlightbackground=YELLOW, command=reset_timer)
reset_button.grid(row=2, column=2)


root.mainloop()
