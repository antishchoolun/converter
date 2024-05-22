import csv
import tkinter as tk
from tkinter import ttk

# main window
window = tk.Tk()
window.geometry('650x200')
window.title('FPS Sensitivity Converter')

# lists and dicts
games = []
games_title = []

with open('games.csv') as file:
    reader = csv.DictReader(file)
    for row in reader:
        games.append({'title' : row['title'], 'sensitivity_factor' : row['sensitivity_factor']})
        games_title.append(row['title'])


def return_factor(title):
    for game in games:
        if game['title'] == title:
            return float(game['sensitivity_factor'])

    return 0  

# frame
frame = ttk.Frame(window)
frame.pack()

# row 1 labels
game1 = tk.StringVar()
game1_label = ttk.Label(frame, text=f'Convert from')
game1_label.grid(column = 0, row = 0, padx = 2, pady = 2)

game2 = tk.StringVar()
game2_label = ttk.Label(frame, text=f'Convert to')
game2_label.grid(column=1,row=0,padx=2,pady=2)

sensitivity_label = ttk.Label(frame,text=f'Convert to')
sensitivity_label.grid(column=2,row=0,padx=2,pady=2)

# row1 widgets
def label_func(event):
    game1_label.configure(text=f'Convert from {game1.get()}')
    sensitivity_label.configure(text=f'{game1.get()} sensitivity')

# "from" game selection
from_game_title = ttk.Combobox(frame, values=games_title, textvariable=game1)
from_game_title.grid(column=0, row=1,padx=5,pady=5)
from_game_title.bind('<<ComboboxSelected>>', lambda event: label_func(event))

# "TO" game selection 
to_game_title = ttk.Combobox(frame, values=games_title, textvariable=game2)
to_game_title.grid(column=1, row=1, padx=5, pady=5)
to_game_title.bind('<<ComboboxSelected>>', lambda event:game2_label.configure(text=f'Convert to {game2.get()}'))

# from game sensitivity
from_game_sensitivity = tk.DoubleVar()
from_game_sensitivity_entry = ttk.Spinbox(frame, textvariable=from_game_sensitivity, from_=0,to=100)
from_game_sensitivity_entry.grid(column=2 ,row=1, padx=5, pady=5)

# row2 labels
ttk.Label(frame, text='From Mouse DPI').grid(column=0, row=2, padx=2, pady=2)
ttk.Label(frame, text='To Mouse DPI').grid(column=1, row=2, padx=2, pady=2)

# row 2 widgets
original_dpi =  tk.IntVar()
from_game_dpi = ttk.Spinbox(
    frame,
    from_=0,
    to=32000,
    increment=10,
    textvariable=original_dpi
    )
from_game_dpi.grid(column=0, row=3, padx=5, pady=5)

new_dpi = tk.IntVar()
to_game_dpi = ttk.Spinbox(
    frame,
    from_=0,
    to=32000,
    increment=10,
    textvariable=new_dpi 
    )
to_game_dpi.grid(column=1, row=3, padx=5, pady=5)

# row3 label 
ttk.Label(frame,text='Converted sens').grid(column=0,row=4,padx=2,pady=2)
ttk.Label(frame,text='cm/360').grid(column=1,row=4,padx=2,pady=2)
ttk.Label(frame,text='in/360').grid(column=2,row=4,padx=2,pady=2)

# row3 label vars
converted_sens_label = ttk.Label(frame, text =0)
converted_sens_label.grid(column=0, row=5, padx=5, pady=5)

cm_per_360_label = ttk.Label(frame,text=0)
cm_per_360_label.grid(column=1, row=5, padx=5, pady=5)

inch_per_360_label = ttk.Label(frame, text =0)
inch_per_360_label.grid(column=2, row=5, padx=5, pady=5)

def sens_converter():
        try:
             # original game settings
            old_edpi = original_dpi.get() * from_game_sensitivity.get()
            k1 = return_factor(game1.get())
            cm360 = round(k1 / old_edpi, 2)
            inch360 = round(cm360 / 2.54, 2)

              #    new game setting
            k2 = return_factor(game2.get()) 
            new_sens = round((k2 / cm360)/ new_dpi.get(),4) 

            converted_sens_label.configure(text=new_sens)
            cm_per_360_label.configure(text=cm360)
            inch_per_360_label.configure(text=inch360)

        except (ZeroDivisionError, tk.TclError):
             converted_sens_label.configure(text=0)
             cm_per_360_label.configure(text=0)
             inch_per_360_label.configure(text=0)

        window.after(500, sens_converter)

window.after(500,sens_converter) 

# run
window.mainloop()
                


 





