import pyautogui
import pygetwindow as gw
import time
import pyperclip  # for clipboard

# List of messages to send
messages = ["Msg1", "Msg2"]   # two messages
count = 100



            # total times to send the sequence
delay = 1                # seconds between each message

print("⚠️ Please open WhatsApp Desktop and keep the chat window active.")
time.sleep(10)

# Focus WhatsApp window
try:
    windows = gw.getWindowsWithTitle("WhatsApp")
    if not windows:
        raise Exception("No WhatsApp Desktop window found")
    
    window = windows[0]
    window.activate()
    time.sleep(1)
    print("✅ WhatsApp Desktop window activated")
except Exception as e:
    print(f"⚠️ Could not focus WhatsApp window: {e}. Please click manually.")

# Send messages in loop
for i in range(count):
    for msg in messages:
        pyperclip.copy(msg)       # copy emoji/text to clipboard
        pyautogui.hotkey("ctrl", "v") # paste it
        pyautogui.press("enter")      # send
        print(f"Sent message: {msg}")
        time.sleep(delay)
