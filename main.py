import argparse
import time
import tkinter
import os
from tkinter import messagebox
from playsound import playsound
import pyautogui


def play_alert_sound():
    playsound(
        '/System/Library/PrivateFrameworks/ToneLibrary.framework/Versions/A/Resources/AlertTones/alarm.caf')


def toggle_dnd():
    pyautogui.hotkey('ctrl', 'optionleft', 'command', 'd')


def focus_python_window():
    os.system(
        '''/usr/bin/osascript -e 'tell app "Finder" to set frontmost of process "Python" to true' ''')


def show_time_for_break(time_for_long_break):
    play_alert_sound()
    focus_python_window()
    messagebox.showinfo(
        "Hey!", "Start a long break" if time_for_long_break else "Start a short break")
    root.update()


def show_time_for_work():
    focus_python_window()
    messagebox.showinfo("Hey", "Start working!")
    root.update()


root = tkinter.Tk()
root.withdraw()  # hides base tkinter window

parser = argparse.ArgumentParser()
parser.add_argument(
    '--focus', '-f', help="Length of the pomodoro focus period (in min)", default=25, required=False)
parser.add_argument(
    '--pause', '-p', help="Length of the pause between focus periods (in min)", default=5, required=False)
parser.add_argument(
    '--long', '-l', help="Length of the long pause between focus periods (in min)", default=20, required=False)
args = parser.parse_args()

starttime = time.time()
no_of_pauses = 0
no_of_pomodoros = 0
while True:
    print("Starting work")
    toggle_dnd()

    # FOCUS LOOP
    passed_focus_minutes = 0
    while passed_focus_minutes < int(args.focus):
        timeleft = int(args.focus) - passed_focus_minutes
        print("You have", timeleft, "focus minutes left")
        passed_focus_minutes += 1
        time.sleep(60)

    no_of_pomodoros += 1
    print("Good job! You have done", no_of_pomodoros, "pomodoro(s)")

    time_for_long_break = no_of_pauses == 3
    show_time_for_break(time_for_long_break)
    print("Starting pause")
    toggle_dnd()

    # BREAK LOOP
    passed_break_minutes = 0
    break_interval = int(args.long) if time_for_long_break else int(args.pause)
    while passed_break_minutes < break_interval:
        time.sleep(60)
        timeleft = break_interval - passed_break_minutes
        print("You have", timeleft, "break minutes left")
        passed_break_minutes += 1

    # reset long pauses after it's done
    if time_for_long_break:
        no_of_pauses = 0
    else:
        no_of_pauses += 1

    show_time_for_work()
