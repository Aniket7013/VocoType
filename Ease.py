import sys
import os
import threading
import speech_recognition as sr
import pyautogui
import pyperclip
import time
import tkinter as tk
from tkinter import messagebox
import queue
from PIL import Image
import pystray
from pystray import MenuItem as item

# --- Global flags and queues ---
running = False
command_queue = queue.Queue()

# --- Speech recognition setup ---
recognizer = sr.Recognizer()
mic = sr.Microphone()
recognizer.pause_threshold = 0.3
recognizer.phrase_threshold = 0.3
recognizer.non_speaking_duration = 0.2

# --- Command processing ---
def process_command(text):
    command = text.lower()
    if "stop" in command:
        global running
        running = False
    elif "enter" in command or "new line" in command:
        pyautogui.press("enter")
    elif "tab" in command:
        pyautogui.press("tab")
    elif "backspace" in command:
        pyautogui.press("backspace")
    else:
        pyperclip.copy(text + " ")
        time.sleep(0.05)  # small delay to ensure clipboard is ready
        pyautogui.hotkey('ctrl', 'v')

# --- Voice recognition loop ---
def voice_typing_loop():
    global running
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        while running:
            try:
                audio = recognizer.listen(source, timeout=3, phrase_time_limit=4)
                threading.Thread(target=handle_audio, args=(audio,), daemon=True).start()
            except sr.WaitTimeoutError:
                continue

# --- Audio handler thread ---
def handle_audio(audio):
    try:
        text = recognizer.recognize_google(audio)
        print(f"Recognized: {text}")
        command_queue.put(text)
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError:
        print("API unavailable")

# --- Queue processor ---
def process_queue():
    try:
        while not command_queue.empty():
            command = command_queue.get_nowait()
            print(f"Typing: {command}")
            process_command(command)
    except queue.Empty:
        pass
    if running:
        root.after(50, process_queue)

# --- GUI control functions ---
def start_voice_typing():
    global running
    if running:
        messagebox.showinfo("Already Running", "Voice typing is already running.")
        return
    running = True
    threading.Thread(target=voice_typing_loop, daemon=True).start()
    status_label.after(0, lambda: status_label.config(text="Voice Typing: ON"))
    process_queue()

def stop_voice_typing():
    global running
    running = False
    status_label.after(0, lambda: status_label.config(text="Voice Typing: OFF"))

def exit_app(icon=None, item=None):
    def safe_exit():
        stop_voice_typing()
        if icon:
            icon.stop()
        root.quit()

    # Ensure all GUI-related shutdown happens in the main thread
    root.after(0, safe_exit)

# --- System tray setup ---
def create_tray_icon():
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.dirname(__file__)

    icon_path = os.path.join(base_path, "mic.ico")

    try:
        image = Image.open(icon_path)
    except FileNotFoundError:
        messagebox.showerror("Error", f"Tray icon not found at: {icon_path}")
        sys.exit()

    menu = (
        item('Start Typing', start_voice_typing),
        item('Stop Typing', stop_voice_typing),
        item('Exit', exit_app)
    )
    return pystray.Icon("VoiceKeyboard", image, "Voice Keyboard", menu)

# --- Main GUI ---
root = tk.Tk()
root.title("Voice Keyboard")
root.geometry("400x250")
root.resizable(False, False)

start_btn = tk.Button(root, text="Start Typing", command=start_voice_typing, bg="green", fg="white", font=("Arial", 12))
start_btn.pack(pady=10)

stop_btn = tk.Button(root, text="Stop Typing", command=stop_voice_typing, bg="red", fg="white", font=("Arial", 12))
stop_btn.pack(pady=10)

status_label = tk.Label(root, text="Voice Typing: OFF", font=("Arial", 10))
status_label.pack(pady=5)

# --- Launch tray icon in background ---
def main():
    tray_icon = create_tray_icon()
    threading.Thread(target=tray_icon.run, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    main()
