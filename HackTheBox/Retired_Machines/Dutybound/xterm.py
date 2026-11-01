import os, time
os.environ['DISPLAY'] = ':0'
from Xlib import display, X
from Xlib.ext import xtest
import subprocess

d = display.Display(':0')

def send_combo(keysyms):
    keycodes = [d.keysym_to_keycode(k) for k in keysyms]
    for kc in keycodes:
        xtest.fake_input(d, X.KeyPress, kc)
        d.sync()
        time.sleep(0.05)
    for kc in reversed(keycodes):
        xtest.fake_input(d, X.KeyRelease, kc)
        d.sync()
        time.sleep(0.05)

ctrl = 0xffe3   # Control_L
alt  = 0xffe9   # Alt_L
t    = ord('t')

print("Sending Ctrl+Alt+T...")
send_combo([ctrl, alt, t])
time.sleep(1)
subprocess.run(["scrot", "/tmp/cs/xterm_test.png"])
d.close()
