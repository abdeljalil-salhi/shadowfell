from pynput.keyboard import Key, Listener
from time import time, sleep
from os import system

time_threshold, start_time = 42 * 60, time()

# Sometimes, ft_lock doesn't work
system("ft_lock")
sleep(0.2)
system("ft_lock")
sleep(0.2)
system("ft_lock")


def on_press(key):
    global start_time
    if key == Key.esc:
        try:
            elapsed_time = time() - start_time
            if elapsed_time > time_threshold:
                system("gnome-session-quit --force")
        except Exception as e:
            print(f"An error occurred: {e}")
            system("gnome-session-quit --force")


listener = Listener(on_press=on_press)

try:
    listener.start()
    listener.join()
except KeyboardInterrupt:
    pass
finally:
    listener.stop()
