# Author: Giulia Pusceddu 

import tkinter as tk
from PIL import ImageGrab
import csv
import os
import datetime
import time
import sys
import signal
import sys

sys.path.insert(1, '/usr/local/src/robot/cognitiveInteraction/guessthesketch/modules/guessTheSketch')
from utils import *

class whiteboardApp(yarp.BottleCallback):
    def __init__(self, root):
        super(whiteboardApp, self).__init__()

        # --- Yarp ---
        self.module_name = "whiteboardApp"
        self.player_id = None
        self.in_port = yarp.BufferedPortBottle()
        self.out_port = yarp.BufferedPortBottle()
        # Initialize Yarp, open ports
        self.configure_module(rf)


        self.root = root
        self.root.title("Guess the Sketch - Whiteboard App")

        # Schermo intero
        self.root.attributes('-fullscreen', True)
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Canvas
        self.canvas = tk.Canvas(root, bg="white", width=self.screen_width, height=self.screen_height)
        self.canvas.pack(fill="both", expand=True)

        # Pulsante "Finito"
        self.finish_btn = tk.Button(root, text="Finito", command=self.finish_drawing, font=("Arial", 20))
        # self.finish_btn.pack(side=tk.BOTTOM, pady=20)
        #self.finish_btn.place(relx=0.5, rely=0.95, anchor="center")

        # Add x to close window
        self.close_btn = tk.Button(root, text="X", command=root.destroy, font=("Arial", 12), fg="red")
        self.close_btn.place(relx=0.98, rely=0.02, anchor="ne")

        # Lista di oggetti da disegnare
        # double x[0] objects with x[1]==1 are objects to be redrawn due to error
        self.objects_to_draw = expanded_rounds
        self.objects_types_to_draw = expanded_types
        self.trials_to_draw=expanded_trials

        yarpinfo(f"Objects to draw: {self.objects_to_draw}\nErrors at rounds: {REDO_ROUNDS}\nMax rounds: {MAX_ROUNDS}")

    
        self.current_round = 0

        # Variabili di stato
        self.drawing = False
        self.x_prev, self.y_prev = None, None
        self.positions = []
        self.current_label = None
        self.start_time = None

        # Binding mouse
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        # Drawings directory 
        self.drawings_dir = "/usr/local/src/robot/cognitiveInteraction/guessthesketch/drawings"
        os.makedirs(self.drawings_dir, exist_ok=True)

        # Create incremental subdirectories names: 01, 02, ...
        existing_dirs = [d for d in os.listdir(self.drawings_dir) if os.path.isdir(os.path.join(self.drawings_dir, d)) and d.isdigit()] # list of directories
        if existing_dirs:
            last_dir = max(int(d) for d in existing_dirs) # get the highest directory number after converting to int
            self.dir_number = f"{last_dir + 1:02d}" # add 1 with two digits format
        else:
            self.dir_number = "01"
        self.drawings_dir = os.path.join(self.drawings_dir, self.dir_number)
        os.makedirs(self.drawings_dir, exist_ok=True)
        guiinfo(f"Drawings will be saved in: {self.drawings_dir}")


        with open(f"{self.drawings_dir}/order.txt", "w") as fp:
            for trial in self.trials_to_draw:
                fp.write(f"trial_{trial}\n")

        # Inizia primo round
        # self.start_round()

    def configure_module(self, rf):
        yarp.Network().init()

        self.in_port.open(f"/whiteboard:i")
        self.in_port.useCallback(self)

        self.out_port.open(f"/whiteboard:o")

        guiinfo("Ports opened!")
    
    def interrupt_module(self):
        guiinfo("Interrupting module.")
        self.in_port.interrupt()
        self.out_port.interrupt()

        return True

    def close_module(self):
        self.in_port.close()
        self.out_port.close()

        return True
    
    def onRead(self, data, reader):
        try:
            cmd = data.get(0).asVocab32()
            # cmd = data.get(0).asString()
            guiinfo(VOCAB_NEXT_SKETCH)
            # guiinfo(f"Received command: {cmd}")
            if cmd == VOCAB_NEXT_SKETCH:
                # todo: aggiungere error/non error
                guiinfo("Received NEXT ROUND command.")
                self.start_round()
    
        except Exception as e:
            print(f"Callback Error -> {e}")

    def clear_bottle(self):
        bottle = self.out_port.prepare()
        bottle.clear()

    def send_to_backend(self):
        # when the drawing has finished, send a message to the backend
        bottle = self.out_port.prepare()
        bottle.clear()
        bottle.addVocab32(VOCAB_END_SKETCH)
        self.out_port.write()
        guiinfo(f"Sending end_round...")

    def show_label_on_canvas(self, label, sketch_type):
        """Mostra il nome dell'oggetto al centro del canvas."""
        self.canvas.delete("all")
        self.root.update_idletasks()  # forces the update of the canvas

        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()

        if self.current_round in REDO_ROUNDS:
            message = f"The system did not recognize the sketch.\nPlease, redo the sketch representing the following {SKETCH_TYPE_LABELS[sketch_type]}:\n\n{label}"
        else:
            message =  f"Please, make a sketch representing the following {SKETCH_TYPE_LABELS[sketch_type]}:\n\n{label}"

        self.canvas.create_text(
            w / 2,
            h / 2,
            text=message,
            font=("Arial", 40, "bold"),
            fill="black"
        )
        self.canvas.update()  # forces the update of the canvas
    def start_round(self):
        """Prepara il canvas e mostra il nuovo oggetto da disegnare."""
        
        guiinfo(f"Round {self.current_round + 1} starting.")

        # remove black screen 
        self.canvas.delete("all")
        # make finito button appear again
        self.finish_btn.place(relx=0.5, rely=0.95, anchor="center")
        self.close_btn.place(relx=0.98, rely=0.02, anchor="ne")

        self.current_label = self.objects_to_draw[self.current_round]
        self.current_trial = self.trials_to_draw[self.current_round]
        self.current_type= self.objects_types_to_draw[self.current_round]
        self.positions = []
        self.show_label_on_canvas(self.current_label, self.current_type)
        self.root.after(7000, self.clear_and_start_drawing)  # Only show label for 7 seconds

    def clear_and_start_drawing(self):
        """Pulisce il canvas e permette di iniziare a disegnare."""
        self.canvas.delete("all")
        self.start_time = time.time()

    def start_draw(self, event):
        self.drawing = True
        self.x_prev, self.y_prev = event.x, event.y
        self.log_position(event.x, event.y, pressed=1)

    def draw(self, event):
        if self.drawing:
            x, y = event.x, event.y
            self.canvas.create_line(self.x_prev, self.y_prev, x, y, fill="black", width=3)
            self.log_position(x, y, pressed=1)
            self.x_prev, self.y_prev = x, y
        else:
            # Pointer moved without drawing
            self.log_position(event.x, event.y, pressed=0)

    def stop_draw(self, event):
        self.drawing = False
        self.x_prev, self.y_prev = None, None
        self.log_position(event.x, event.y, pressed=0)

    def log_position(self, x, y, pressed):
        """Registra la posizione, lo stato del mouse e il timestamp relativo."""
        if self.start_time is None:
            self.start_time = time.time()
        t = time.time() - self.start_time
        self.positions.append((t, x, y, pressed))

    def finish_drawing(self):
        """Salva immagine e dati del disegno."""
        if not self.positions:
            return
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"trial_{self.current_trial}_subj_{self.dir_number}_{timestamp}"
        base_name = base_name.replace(" ", "_") # not tested

        # Nascondi bottoni prima dello screenshot
        self.close_btn.place_forget()
        self.finish_btn.place_forget()

        self.root.update()
        time.sleep(0.1) # wait for UI to update

        # Salva immagine
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab(bbox=(x, y, x1, y1)).save(f"{self.drawings_dir}/{base_name}.png")

        # Salva CSV
        with open(f"{self.drawings_dir}/{base_name}.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time", "x", "y", "mouse_pressed"])
            writer.writerows(self.positions)
        guiinfo(f"Drawing saved as {base_name}.png and {base_name}.csv")

         # Send end_round to backend
        self.send_to_backend()
        guiinfo(f"Round {self.current_round +1} finished.")

        # Increment round count
        self.current_round += 1

        # Clean canvas
        self.canvas.delete("all")
        self.root.update_idletasks()

        # Black screen between rounds
        self.canvas.create_rectangle(0, 0, self.screen_width, self.screen_height, fill="black")
        self.root.update_idletasks()
        # remove finish button until next round
        self.finish_btn.place_forget()

        if self.current_round >= MAX_ROUNDS:
            guiinfo("All rounds completed.")
            self.root.after(100, self.show_end_message)
        
    def show_end_message(self):
        """Final message"""
        w = self.canvas.winfo_width()
        h = self.canvas.winfo_height()
        self.canvas.create_text(
            w / 2,
            h / 2,
            text="Fine del gioco.",
            font=("Arial", 60, "bold"),
            fill="white"
        )
        self.canvas.update_idletasks()
        self.canvas.update()
        guiinfo("Final message displayed.")

if __name__ == "__main__":
    
    rf = yarp.ResourceFinder()
    rf.setVerbose(True)
    rf.setDefaultContext('guessTheSketch')
    rf.setDefaultConfigFile('guessTheSketch.ini')

    rf.configure(sys.argv)

    root = tk.Tk()
    app = whiteboardApp(root)

    # Add signal handler for Ctrl+C
    def handle_sigint(sig, frame):
        guiinfo("SIGINT detected: scheduling shutdown on GUI thread...")
        # schedule cleanup to run in the main/UI thread
        def cleanup():
            try:
                app.interrupt_module()
                app.close_module()
            except Exception as e:
                guiinfo(f"Error during cleanup: {e}")
            try:
                root.quit()  # breaks tkinter mainloop
            except Exception:
                pass
        root.after(0, cleanup)

    # handle both SIGINT and SIGTERM
    import signal
    signal.signal(signal.SIGINT, handle_sigint)
    try:
        signal.signal(signal.SIGTERM, handle_sigint)
    except Exception:
        pass
    
    # Handle window close event
    root.protocol("WM_DELETE_WINDOW", lambda: (app.interrupt_module(), app.close_module(), root.destroy()))

    root.mainloop()