"""
WarpRandomizerMain.py

Main function of the Warp Randomizer

Copyright (c) 2023 AtSign, XLuma, Turtleisaac

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import inspect
import os
import sys
import tempfile
import threading
from tkinter import *
from tkinter import filedialog, scrolledtext
from tkinter import messagebox
from tkinter import ttk

from PIL import ImageTk, Image
from ttkthemes import ThemedTk

import VerifyRom
from RandomizerUtils import Definitions
from RandomizerUtils import Randomizer
from RandomizerUtils import Utils


def randomize():
    filepath_input = inputSource.get()
    if not filepath_input:
        messagebox.showerror('Error', 'Please select a source rom to randomize.')
        return

    verification_tuple = VerifyRom.validate_rom(filepath_input)
    if verification_tuple is None:
        messagebox.showerror('Error',
                             f"The provided rom at '{filepath_input}' is not valid. Warp randomization aborted.")
        return

    filepath_output = inputDest.get()
    if not filepath_output:
        messagebox.showerror('Error', 'Please select a destination file to save the randomized rom.')
        return

    if filepath_input == filepath_output:
        messagebox.showerror('Error', 'You can\'t select the same file for both the input and the output. Please '
                                      'save as a new file.')
        return

    clear_status()

    seed_val = inputSeed.get()
    seed = int(seed_val) if seed_val and seed_val != '(find random)' else -1

    def _run():
        complete = False
        while True:
            result = Randomizer.start_randomizer(filepath_input, filepath_output, Definitions.get_definition(
                int(verification_tuple[3])), seed, verification_tuple[4])
            if result[2]:
                root.after(0, lambda: messagebox.showerror('Error', 'Provided game is not supported. The list of '
                                                                     'supported games can be found in the Info window.'))
                break
            if result[0]:
                complete = True
                break
            elif seed != -1:
                root.after(0, lambda: messagebox.showerror('Error',
                                                           'Seed unable to create valid randomization, please try different seed'))
                break

        def _finish():
            progress_bar.stop()
            for widget in [btnStart, btnSource, btnDest, inputSource, inputDest, inputSeed]:
                widget.config(state="normal")
            if complete:
                zip_output = os.path.splitext(filepath_output)[0] + '.zip'
                messagebox.showinfo(title='Randomizer', message='Warp Randomization Complete! Output can be found at:\n' +
                                                                zip_output)

        root.after(0, _finish)

    btnStart.config(state="disabled")
    for widget in [btnSource, btnDest, inputSource, inputDest, inputSeed]:
        widget.config(state="disabled")
    progress_bar.start()
    threading.Thread(target=_run, daemon=True).start()


def set_source_file():
    file = filedialog.askopenfilename(title='Select ROM to Randomize', filetypes=[('game file', '*.gba *.nds')])
    if not file:
        return
    inputSource.delete(0, END)
    inputSource.insert(0, file)
    destFile = os.path.splitext(file)[0] + '_randomized.zip'
    inputDest.delete(0, END)
    inputDest.insert(0, destFile)


def set_dest_file():
    name = os.path.splitext(os.path.basename(inputSource.get()))[0]
    if name:
        name = name + '_randomized'
    else:
        name = 'output'
    file = filedialog.asksaveasfilename(
        title='Select Destination File',
        initialfile=name,
        defaultextension=".zip",
        filetypes=[('zip archive', '*.zip')]
    )
    if not file:
        return
    inputDest.delete(0, END)
    inputDest.insert(0, file)


def clear_status():
    status.config(state="normal")
    status.delete(1.0, END)
    status.config(state="disabled")


root = ThemedTk(theme="breeze")
root.title('Universal Warp Randomizer V2.0')
root.wm_iconphoto(False,
                  ImageTk.PhotoImage(Image.open(Utils.resource_path(os.path.join('Resources', 'doodleDoorPoke.png')))))

top_frame = ttk.Frame(root)
top_frame.pack(side='top', pady=1, fill='x', expand=True)
top_frame.columnconfigure(1, weight=1)

lblTitle = ttk.Label(top_frame, text="PointCrow's Universal Warp Randomizer", font='Helvetica 18 bold')
lblSubtitle = ttk.Label(top_frame, text="Created By XLuma, Turtleisaac, & AtSign")
lblInfo = ttk.Label(top_frame,
                    text="Supported Games: Pokemon Emerald, Platinum, White2, FireRed, LeafGreen, HeartGold, SoulSilver")

lblSeed = ttk.Label(top_frame, text="Seed")
inputSeed = ttk.Entry(top_frame, foreground='grey')
inputSeed.insert(0, '(find random)')
def on_seed_focus_in(_):
    if inputSeed.get() == '(find random)':
        inputSeed.delete(0, END)
        inputSeed.configure(foreground='black')
inputSeed.bind('<FocusIn>', on_seed_focus_in)
def on_seed_focus_out(_):
    if not inputSeed.get():
        inputSeed.insert(0, '(find random)')
        inputSeed.configure(foreground='grey')
inputSeed.bind('<FocusOut>', on_seed_focus_out)

lblSource = ttk.Label(top_frame, text="Source")
inputSource = ttk.Entry(top_frame)
btnSource = ttk.Button(top_frame, text='Select', command=set_source_file)

lblDest = ttk.Label(top_frame, text="Destination")
inputDest = ttk.Entry(top_frame)
btnDest = ttk.Button(top_frame, text='Select', command=set_dest_file)

btnStart = ttk.Button(top_frame, text='Randomize', command=randomize)

progress_bar = ttk.Progressbar(top_frame, orient='horizontal', mode='indeterminate', length=400)
status = scrolledtext.ScrolledText(top_frame, wrap="word")
status.config(state="disabled")

lblTitle.grid(row=0, column=0, columnspan=3)
lblSubtitle.grid(row=1, column=0, columnspan=3)
lblInfo.grid(row=2, column=0, columnspan=3)
lblSeed.grid(row=3, column=0, sticky='w', padx=(4, 0))
inputSeed.grid(row=3, column=1, columnspan=2, sticky='ew')
lblSource.grid(row=4, column=0, sticky='w', padx=(4, 0))
inputSource.grid(row=4, column=1, sticky='ew')
btnSource.grid(row=4, column=2)
lblDest.grid(row=5, column=0, sticky='w', padx=(4, 0))
inputDest.grid(row=5, column=1, sticky='ew')
btnDest.grid(row=5, column=2)
btnStart.grid(row=6, column=0, columnspan=3)
progress_bar.grid(row=7, column=0, columnspan=3, sticky='ew')
status.grid(row=8, column=0, columnspan=3, sticky='ew')


class TkinterConsoleRedirector:
    def __init__(self, orig):
        self.orig = orig
    def write(self, text):
        self.orig.write(text)
        if text.strip():
            frame = inspect.stack()[1]
            caller = os.path.basename(os.path.splitext(frame.filename)[0])
            prefixed_text = f"[{caller}] {text}"
        else:
            prefixed_text = text
        status.config(state="normal")
        status.insert("end", prefixed_text)
        status.see("end")
        status.config(state="disabled")

    def flush(self):
        self.orig.flush()
        pass

sys.stdout = TkinterConsoleRedirector(sys.stdout)

root.eval('tk::PlaceWindow . center')

# Use this code to signal the splash screen removal.
if "NUITKA_ONEFILE_PARENT" in os.environ:
    splash_filename = os.path.join(
        tempfile.gettempdir(),
        "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
    )

    if os.path.exists(splash_filename):
        os.unlink(splash_filename)

root.mainloop()
