# text-to-gfx
Listen for a string on a serial port, display a graphic whose filename matches the string

## In a nutshell...

Put all your .jpg files in a directory, here shown as `gfx`.  Then in a
shell window:

```
$ py -m pipenv shell
Launching subshell in virtual environment...
$ cd gfx
$ py ../text_to_gfx.py --help
usage: text_to_gfx.py [-h] [--baud BAUD] serial_port

Display words as graphics.

positional arguments:
  serial_port  Serial port to connect to, e.g. 'COM1' or '/dev/usb3'.

options:
  -h, --help   show this help message and exit
  --baud BAUD  Baud rate of serial port. Defaults to 115200.

$ py ../text_to_gfx.py COM7
initialized
entering read loop
received seven
received house
received stop

$
```
