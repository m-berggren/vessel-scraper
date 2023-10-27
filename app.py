import tkinter as tk
from tkinter import ttk, messagebox

# CONSTANTS
DB_PATH = r"db\vessel_info.db"
TK_FOREST = r"widget\forest-light.tcl"

# Create the main window
window = tk.Tk()
window.option_add("*tearOff", False)
window.tk.call('source', TK_FOREST)

style = ttk.Style(window)
style.theme_use('forest-light')

window.title("VESSEL DATABASE")

# Set window position


# Create a Frame for input widgets
widgets_frame = ttk.Frame(window, padding=(0, 0, 0, 10))
widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

label = ttk.Label(widgets_frame, text="Add vessel:", font=("Calibri", 18, "bold", "underline", ), padding=(0, 0, 0, 10))
label.grid(row=0, column=0, padx=5, pady=(0, 0), sticky="ew")

# Vessel box
label = ttk.Label(widgets_frame, text="Vessel Name", font=("Calibri Light", 10, "bold"), padding=(0, 0, 0, 0))
label.grid(row=1, column=0, padx=5, pady=(0, 0), sticky="ew")

entry = ttk.Entry(widgets_frame)
entry.insert(0, "")
entry.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")

# Imo box
label = ttk.Label(widgets_frame, text="Callsign", font=("Calibri Light", 10, "bold"), padding=(0, 0, 0, 0))
label.grid(row=3, column=0, padx=5, pady=(0, 0), sticky="ew")

entry = ttk.Entry(widgets_frame)
entry.insert(0, "")
entry.grid(row=4, column=0, padx=5, pady=(0, 10), sticky="ew")

# Callsign box
label = ttk.Label(widgets_frame, text="IMO", font=("Calibri Light", 10, "bold"), padding=(0, 0, 0, 0))
label.grid(row=5, column=0, padx=5, pady=(0, 0), sticky="ew")

entry = ttk.Entry(widgets_frame)
entry.insert(0, "")
entry.grid(row=6, column=0, padx=5, pady=(0, 10), sticky="ew")

# Mmsi box
label = ttk.Label(widgets_frame, text="MMSI", font=("Calibri Light", 10, "bold"), padding=(0, 0, 0, 0))
label.grid(row=7, column=0, padx=5, pady=(0, 0), sticky="ew")

entry = ttk.Entry(widgets_frame)
entry.insert(0, "")
entry.grid(row=8, column=0, padx=5, pady=(0, 10), sticky="ew")

button = ttk.Button(widgets_frame, text="Save vessel", style="Accent.TButton")
button.grid(row=9, column=0, padx=5, pady=(0, 10), sticky="ew")

# Panedwindow
paned = ttk.PanedWindow(window)
paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

# Pane #1
pane_1 = ttk.Frame(paned)
paned.add(pane_1, weight=1)

def remove_value(event): # note that you must include the event as an arg, even if you don't use it.
    search_entry.delete(0, "end")
    return None

def search(entry):
    query = search_entry.get()
    selections = []
    for child in treeview.get_children():
        if query.lower() in treeview.item(child)['values'].lower():   # compare strings in  lower cases.
            selections.append(child)
    treeview.selection_set(selections)

# Add label and entry field
label_2 = ttk.Label(widgets_frame, text="Search vessel", font=("Calibri Light", 10, "bold"), padding=(0, 0, 0, 0))
search_entry = ttk.Entry(pane_1)
search_entry.insert(0, "Filter vessel by name")
search_entry.bind('<Button-1>', remove_value)
search_entry.bind('<Return>', search)
search_entry.pack(side="top", fill="y")


# Create a Frame for the Treeview
treeFrame = ttk.Frame(pane_1)
treeFrame.pack(expand=True, fill="both", padx=5, pady=5)

# Scrollbar
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side="right", fill="y")

# Treeview
treeview = ttk.Treeview(treeFrame, selectmode="extended", yscrollcommand=treeScroll.set, columns=(1, 2, 3), height=12)
treeview.pack(expand=True, fill="both")
treeScroll.config(command=treeview.yview)

# Treeview columns
treeview.column("#0", width=250)
treeview.column(1, anchor="w", width=80)
treeview.column(2, anchor="w", width=120)
treeview.column(3, anchor="w", width=120)

# Treeview headings
treeview.heading("#0", text="Vessel", anchor="w")
treeview.heading(1, text="Callsign", anchor="w")
treeview.heading(2, text="IMO", anchor="w")
treeview.heading(3, text="MMSI", anchor="w")

treeview_data = [
    ("A ASO", "3FXG9", 9522776, 352430000),
    ("TACOMA TRADER", "5LBO9", 9675810, 636020961),
    ("STRAIT MAS", "YDBO2", 9252369, 525119161),
    ("ALABAMA", "YTBO2", 9342369, 525619161),
    ("OKLAHOMA", "YDUO2", 9252009, 525114461),
    ("DIRE STRAIT", "YPBO2", 9322369, 525113361),
    ("EVER GLORY", "YYHO2", 9122369, 525156161),
    ("ALABAMA", "YTBO2", 9342369, 525619161),
    ("ALABAMA1", "YTBO2", 9342369, 525619161),
    ("ALABAMA2", "YTBO2", 9342369, 525619161),
    ("ALABAMA3", "YTBO2", 9342369, 525619161),
    ("ALABAMA4", "YTBO2", 9342369, 525619161),
    ("ALABAMA5", "YTBO2", 9342369, 525619161),
    ("ALABAMA6", "YTBO2", 9342369, 525619161),
    ("ALABAMA7", "YTBO2", 9342369, 525619161),
    ("ALABAMA8", "YTBO2", 9342369, 525619161),
    ("ALABAMA9", "YTBO2", 9342369, 525619161),
    ("ALABAMA10", "YTBO2", 9342369, 525619161),
    ("ALABAMA11", "YTBO2", 9342369, 525619161),
    ("ALABAMA12", "YTBO2", 9342369, 525619161),

]

for i, item in enumerate(treeview_data):
    treeview.insert("", index="end", text=item[0], values=(item[1], item[2], item[3]))

# Run widget
window.mainloop()




