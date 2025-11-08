# iCubGuessTheSketch

Small toolkit for running a sketch-drawing game that integrates a drawing whiteboard with a game GUI and YARP messaging.

## Project overview

This repository contains two main Python modules and deployment/config files:

- modules/whiteboardApp  
  - A YARP-aware whiteboard application (Tkinter) that lets a user draw on a fullscreen canvas.  
  - Captures mouse positions over time and can save drawings as PNG + trace data.  
  - Exposes/consumes YARP ports to receive commands (start/next round) and to notify the backend when a drawing is finished.

- modules/guessTheSketch  
  - The game GUI and logic that drives rounds, shows instructions/rules, and interacts with the whiteboard module via YARP.  
  - Manages rounds, scoring and the list of objects to draw.

- app/  
  - Packaging / deployment helpers (CMake, launch scripts, resource files and configs).
  - Example scripts for installing/running the modules as system services or YARP modules.

## Key files

- modules/whiteboardApp/main.py — whiteboard application (GUI, YARP ports, drawing capture).
- modules/guessTheSketch/main.py — game GUI that coordinates rounds and communicates with whiteboardApp.
- modules/guessTheSketch/utils.py — shared constants and helper functions (vocab, draw list, logging helpers).
- app/guessTheSketch/* — resource and install scripts (context, ini, sh, xml for system/service packaging).

## Dependencies

Minimum required software:
- Python 3.10 (project developed with 3.10)
- Pillow (PIL) — for saving PNGs
- yarp python bindings — for IPC between modules
- tkinter — for GUI (usually included with Python)
- (optional) qt_material if using the Qt variant of GUIs

Install examples:
- pip install pillow
- pip install yarp  (or install yarp bindings appropriate for your system)

## Configuration & environment notes

- YARP must be running and reachable when launching the modules.
- When launching modules as services/wrappers, ensure the process gets signals (use exec in shell scripts and do not background with `&`) so Ctrl+C and SIGTERM propagate and cleanup code runs.
- If fonts or DPI differ when launching from different environments (VSCode vs installed module), compare the environment variables (DISPLAY, XAUTHORITY, XFT_DPI) and/or force a consistent Tk font/scaling in the code.

## How to install 
Copy https address of the code on GitLab. 
Go in the /usr/local/src/robot/cognitiveInteraction/ directory, open a terminal and write: 
```bash
git clone <paste https address here>
```

then write 
```bash
mkdir build 
cd build 
ccmake ..
make install 
```

## How to run
Open a terminal and write: 
```bash
yarp server 
```

Open another terminal and write 
```bash
yarp manager 
```

A GUI will open. In "Apllications" click on "guessTheSketch". 
Run "whiteboardApp". 
Run "guessTheSketch". 

Click "connect all" to connect all the available ports. 

Open another terminal and write: 
```bash
yarp rpc /guessTheSketch
```

then, after the ">>" write 
```bash
start
```

At the end of the experiment stop the modules. You can use the up-right "x" to close the whiteboardApp. 


## Saving and outputs

- Drawings and trace JSONs are saved under `drawings/` (default). JSON includes timestamps and x/y positions for every captured mouse event and the path to the saved PNG.

## Troubleshooting tips

- "No module named PIL": install Pillow for the Python interpreter you use.
- "Import qt_material could not be resolved": either install `qt-material` or add a safe try/except around the import.
- If Ctrl+C doesn't close YARP ports: ensure the start script uses `exec` and does not background the process; register signal handlers in the main thread and schedule GUI-thread cleanup (e.g., `root.after(0, cleanup)`).
- For import path issues between modules, either:
  - add `__init__.py` files to make `modules` a package and use relative imports, or
  - add the project `modules` folder to PYTHONPATH before running.

## Contributing & authors

- Author: Giulia Pusceddu
- See repository top-level for contribution guidelines.
