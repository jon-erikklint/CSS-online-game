import time

def set_frame():
    global current_time
    current_time = time.time() * 1000

def frame_time():
    return current_time

set_frame()