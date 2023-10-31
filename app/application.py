import tkinter as tk
from tkinter import messagebox, ttk

from treeview import TreeviewData
from vessel_database import get_data_from_db
from scrape_data import ScrapeMarineTraffic
from selenium_chrome import get_imo_from_google_chrome

# CONSTANTS
DB_PATH = r"db\vessel_info.db"
TK_FOREST = r"widget\forest-light.tcl"

# Create the main root
root = tk.Tk()
root.option_add("*tearOff", False)
root.tk.call('source', TK_FOREST)

style = ttk.Style(root)
style.theme_use('forest-light')

root.title("VESSEL DATABASE")

# Set root position


# Create a Frame for input widgets
widgets_frame = ttk.Frame(root, padding=(0, 0, 0, 10))
widgets_frame.grid(row=0, column=1, padx=10, pady=(30, 10), sticky="nsew", rowspan=3)
widgets_frame.columnconfigure(index=0, weight=1)

vessel_label = ttk.Label(widgets_frame, text="Add vessel:", font=("Arial", 16, "bold", "underline", ), padding=(0, 0, 0, 10))
vessel_label.grid(row=0, column=0, padx=5, pady=(0, 0), sticky="ew")

# Vessel box
vessel_name_label = ttk.Label(widgets_frame, text="Vessel Name", font=("Arial", 10, "bold"), padding=(0, 0, 0, 0))
vessel_name_label.grid(row=1, column=0, padx=5, pady=(0, 0), sticky="ew")

vessel_name_entry = ttk.Entry(widgets_frame)
vessel_name_entry.insert(0, "")
vessel_name_entry.grid(row=2, column=0, padx=5, pady=(0, 10), sticky="ew")

def import_data():
    vessel_name = vessel_name_entry.get()
    imo = get_imo_from_google_chrome(vessel_name)
    print(ScrapeMarineTraffic(imo).get_response_data())
    #return ScrapeMarineTraffic(imo).get_response_data()
    

# Add option from marine traffic
import_button = ttk.Button(widgets_frame, text="Import data", style="Accent.TButton", command=import_data)
import_button.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")

# Imo box
callsign_label = ttk.Label(widgets_frame, text="Callsign", font=("Arial", 10, "bold"), padding=(0, 0, 0, 0))
callsign_label.grid(row=4, column=0, padx=5, pady=(0, 0), sticky="ew")

callsign_entry = ttk.Entry(widgets_frame)
callsign_entry.insert(0, "")
callsign_entry.grid(row=5, column=0, padx=5, pady=(0, 10), sticky="ew")

# Callsign box
imo_label = ttk.Label(widgets_frame, text="IMO", font=("Arial", 10, "bold"), padding=(0, 0, 0, 0))
imo_label.grid(row=6, column=0, padx=5, pady=(0, 0), sticky="ew")

imo_entry = ttk.Entry(widgets_frame)
imo_entry.insert(0, "")
imo_entry.grid(row=7, column=0, padx=5, pady=(0, 10), sticky="ew")

# Mmsi box
label = ttk.Label(widgets_frame, text="MMSI", font=("Arial", 10, "bold"), padding=(0, 0, 0, 0))
label.grid(row=8, column=0, padx=5, pady=(0, 0), sticky="ew")

mmsi_entry = ttk.Entry(widgets_frame)
mmsi_entry.insert(0, "")
mmsi_entry.grid(row=9, column=0, padx=5, pady=(0, 10), sticky="ew")

save_vessel_button = ttk.Button(widgets_frame, text="Save vessel", style="Accent.TButton")
save_vessel_button.grid(row=10, column=0, padx=5, pady=(0, 10), sticky="ew")

# Panedwindow
paned = ttk.PanedWindow(root)
paned.grid(row=0, column=2, pady=(25, 5), sticky="nsew", rowspan=3)

# Pane #1
pane_1 = ttk.Frame(paned)
paned.add(pane_1, weight=1)

def remove_value(event):
    search_entry.delete(0, "end")
    return

def search(entry):
    query = search_entry.get()
    selections = []

    clear_treeview()

    for vessel in treeview_data:
        if query.lower() in vessel[1].lower():
            selections.append(vessel)

    populate_treeview(selections)

def clear_treeview():
    treeview.delete(*treeview.get_children())
    
def populate_treeview(data):
    for item in data:
        treeview.insert("", index=tk.END, text=item[1], values=(item[2], item[0], item[3]))

def exit_application():
    root.destroy()

def delete_row():
    pass



# Add label and entry field
search_entry = ttk.Entry(pane_1)
search_entry.insert(0, "Filter vessel by name")
search_entry.bind('<Button-1>', remove_value)
search_entry.bind('<Return>', search)
search_entry.pack(side=tk.TOP, fill=tk.Y)

# Create a Frame for the Treeview
treeFrame = ttk.Frame(pane_1)
treeFrame.pack(expand=True, fill=tk.BOTH, padx=5, pady=5)

# Scrollbar
treeScroll = ttk.Scrollbar(treeFrame)
treeScroll.pack(side=tk.RIGHT, fill=tk.Y)

# Treeview
treeview = TreeviewData(treeFrame, selectmode=tk.EXTENDED, yscrollcommand=treeScroll.set, columns=(1, 2, 3), height=12)
treeview.pack(expand=True, fill=tk.BOTH)
treeScroll.config(command=treeview.yview)

bottom_frame = ttk.Frame(pane_1)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

delete_row_button = ttk.Button(bottom_frame, text="Delete", style="Accent.TButton", command=delete_row)
delete_row_button.grid(row=0, column=0, padx=80, pady=(5, 5), sticky="ew")

exit_button = ttk.Button(bottom_frame, text="Exit", style="Accent.TButton", command=exit_application)
exit_button.grid(row=0, column=1, padx=100, pady=(5, 5), sticky="ew")


# Treeview columns
treeview.column("#0", width=250)
treeview.column(1, anchor=tk.W, width=80)
treeview.column(2, anchor=tk.W, width=120)
treeview.column(3, anchor=tk.W, width=120)

# Treeview headings
treeview.heading("#0", text="Vessel", anchor=tk.W)
treeview.heading(1, text="Callsign", anchor=tk.W)
treeview.heading(2, text="IMO", anchor=tk.W)
treeview.heading(3, text="MMSI", anchor=tk.W)

treeview_data = get_data_from_db()

populate_treeview(treeview_data)

# Run widget
root.mainloop()




