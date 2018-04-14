# WowFileTools
Unofficial tools to help other users of the Sparkmaker 3d printer.

- `estimate_print_time.py`: estimates printing time of the wow file. (Sum of layer print time and platform motion time, when speed is defined). As far I have tested, it seems to underestimate the time a little (like, a couple minutes for a 5-hour print).
- `view_wow.py`: displays a wow file as voxels in 3d. Warning: needs a lot of RAM and maybe a good graphics card...
  
  ![Alt text](screenshot.png?raw=true "Screenshot")

# USAGE
`python estimate_print_time.py path/to/file.wow`
`python view_wow.py path/to/file.wow`

On some platforms, e.g. ubuntu, you must call python3 instead of python, as, for the time being, the name "python" is still reserved for python 2.

# DEPENDENCIES
- you need Python >=3.6 to run the scripts. (3.5 could work, didn't check.)
- `estimate_print_time.py` does not have extra dependencies
- `view_wow.py` uses pyqtgraph and numpy. Both can be installed through pip. Please note that pyqtgraph requires qt wrappers: either pyqt4/5 or pyside. Also, those wrappers must be properly setup to support OpenGL 3D graphics.

# PLATFORM-SPECIFIC INSTRUCTIONS
(not really tested, please tell me if I forgot something.)

- on Windows, this boils down to:
    - download and install latest python 3.6 release from https://www.python.org/downloads/, add to PATH as proposed by the installer
    - spawn a terminal (e.g. Win+R "cmd")
    - `python -m pip install numpy pyqtgraph pyopengl`
    - `cd folder\where\you\have\downloaded\the\scripts`
    - `python estimate_print_time.py path\to\file.wow`

- on Ubuntu (>=16.04), should be:
    - spawn a terminal (e.g. Ctrl+Alt+T)
    - `sudo apt install python3 python3-pyqt5 python3-pyqt5.qtopengl`
    - `sudo -H python3 -m pip install pyqtgraph numpy`
    - `cd folder/where/you/have/downloaded/the/scripts`
    - `python3 estimate_print_time.py path/to/file.wow`

- on Mac OSX:
    - I have no idea.