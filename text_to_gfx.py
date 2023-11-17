"""
Display the text from a serial port, interpret as a .jpg filename and display.

Loop:
  Read a line from a serial port and append ".jpg" to form the name of a jpg
  file.  Open that file and display it.
"""

from PIL import Image, ImageTk
import tkinter as tk
import os
import argparse
import serial
import signal
import sys

class TextToImage(object):
    """
    Connect to a serial port.  Then, in a loop, read a line at a time from
    the serial port.  Append a ".jpg" to form a name of a JPEG file in this
    directory and display it.

    Example usage:
      py text_to_image.py --baud=115200 COM4
    """

    IMAGE_SUFFIX = ".jpg"

    def __init__(self, serial_port, baud=115200):
        self._serial_port = serial_port
        self._baud = baud
        self._terminate = False
        print("initialized", flush=True)

    def handle_signal(self, signum, frame):
        print("Received a KeyboardInterrupt (Ctrl+C). Terminating...", flush=True)
        self._terminate = True

    def run(self):
        # init the serial port
        self._ser = serial.Serial(self._serial_port, self._baud)

        # init the TK window
        window = tk.Tk()
        window.title("JPEG Image Viewer")
        label = tk.Label(window)
        label.pack(padx=10, pady=10)

        signal.signal(signal.SIGINT, self.handle_signal)

        print("entering read loop", flush=True)

        # start reading from the serial port
        while not self._terminate:
            try:
                word = self._ser.read_until(size=1024).decode('utf-8').strip()
                print(f'received {word}', flush=True)

                if word == 'stop' or word == 'quit':
                    break

                filename = word + '.jpg'
                img = Image.open(filename)
                img.thumbnail((800, 800))  # Resize the image if it's too large
                img = ImageTk.PhotoImage(img)

                label.config(image=img)
                label.image = img
                window.title(filename)
                window.update()  # Update the Tkinter window

            except KeyboardInterrupt:
                print("\nProgram terminated.")
                break

            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Display words as graphics.")
    parser.add_argument('--baud', type=int, default=115200, help="Baud rate of serial port.  Defaults to 115200.")
    parser.add_argument('serial_port', help="Serial port to connect to, e.g. 'COM1' or '/dev/usb3'.")

    args = parser.parse_args()

    if not args.serial_port:
        print("Error: Must specify a serial port")
        sys.exit(1)

    TextToImage(args.serial_port, baud=args.baud).run()
