import tkinter as tk
from tkinter import messagebox, ttk

from app.scrape_data import ScrapeMarineTraffic
from app.selenium_chrome import get_imo_from_google_chrome
from app.treeview import TreeviewData
from app.vessel_database import (add_vessel_to_db, count_vessels_in_db,
                                 delete_vessel_from_db, get_data_from_db)


def run():
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

    def import_data(entry=None):
        vessel_name = vessel_name_entry.get()

        if not vessel_name:
            return
        
        imo = get_imo_from_google_chrome(vessel_name)
        
        if not imo:
            return
        
        data = ScrapeMarineTraffic(imo).get_ship_data()
        add_information_to_entry_cells(data)



    # Add option from marine traffic
    import_button = ttk.Button(widgets_frame, text="Import data", style="Accent.TButton", command=import_data)
    import_button.grid(row=3, column=0, padx=5, pady=(0, 10), sticky="ew")
    vessel_name_entry.bind('<Return>', import_data)

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

    def get_table_data_from_db():
        treeview_data = get_data_from_db()
        clear_treeview()
        populate_treeview(treeview_data)
        return treeview_data

    def add_vessel_to_treeview_and_database():
        vessel_data = {"imo": None, "vessel": None, "callsign": None, "mmsi": None}

        vessel_data['imo'] = imo_entry.get()
        vessel_data['vessel'] = vessel_name_entry.get()
        vessel_data['callsign'] = callsign_entry.get()
        vessel_data['mmsi'] = mmsi_entry.get()

        is_added = add_vessel_to_db(vessel_data)
        if not is_added:
            return
        
        get_table_data_from_db()
        tk.messagebox.showinfo(title=None, message="Vessel added to database.")

    save_vessel_button = ttk.Button(widgets_frame, text="Save vessel", style="Accent.TButton", command=add_vessel_to_treeview_and_database)
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

        treeview_data = get_table_data_from_db()

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

    def remove_items_in_treeview_and_db():
        list_of_selected_imos = treeview.remove_row_data()
        string_of_imos =  ''.join([str(imo) for imo in list_of_selected_imos])
        
        for imo in list_of_selected_imos:
            delete_vessel_from_db(imo)

        get_table_data_from_db()
        
        tk.messagebox.showinfo(title=None, message=f"Below imo(s) are removed from database:"+"\n"+f"{string_of_imos}")


    def add_information_to_entry_cells(vessel_data):
        vessel_name_entry.delete(0, tk.END)
        vessel_name_entry.insert(0, vessel_data.get('vessel', ""))

        imo_entry.delete(0, tk.END)
        imo_entry.insert(0, vessel_data.get('imo', 0))

        callsign_entry.delete(0, tk.END)
        callsign_entry.insert(0, vessel_data.get('callsign', ""))

        mmsi_entry.delete(0, tk.END)
        mmsi_entry.insert(0, vessel_data.get('mmsi', 0))


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

    delete_row_button = ttk.Button(bottom_frame, text="Delete", style="Accent.TButton", command=remove_items_in_treeview_and_db)
    delete_row_button.grid(row=0, column=0, padx=80, pady=(5, 5), sticky="ew")

    exit_button = ttk.Button(bottom_frame, text="Exit", style="Accent.TButton", command=exit_application)
    exit_button.grid(row=0, column=1, padx=100, pady=(5, 5), sticky="ew")

    vessel_count = count_vessels_in_db()
    vessel_amount_label = ttk.Label(bottom_frame, text=f"Vessel count: {vessel_count}", font=("Arial", 10), padding=(0, 0, 0, 0))
    vessel_amount_label.grid(row=0, column=2, padx=30, pady=(5, 5), sticky="w")

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

    # Run widget
    root.wait_visibility()
    treeview_data = get_table_data_from_db()
    root.mainloop()