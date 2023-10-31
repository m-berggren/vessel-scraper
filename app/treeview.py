import tkinter as tk
from tkinter import messagebox, ttk

from app.vessel_database import update_data_to_db


class TreeviewData(ttk.Treeview):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.bind("<Double-1>", self.on_double_click)

    def on_double_click(self, event):
        region_clicked = self.identify_region(event.x, event.y)

        if region_clicked not in("tree", "cell"):
            return

        column = self.identify_column(event.x)
        column_index = int(column[1:]) - 1

        selected_iid = self.focus()
        selected_values = self.item(selected_iid)

        if column == "#0":
            selected_text = selected_values.get("text")
        elif column == "#2": # Not allowed to change vessel's IMO number
            return
        else:
            selected_text = selected_values.get("values")[column_index]

        column_box = self.bbox(selected_iid, column)

        entry_edit = ttk.Entry(self.master, width=20)
        entry_edit.editing_column_index = column_index
        entry_edit.editing_item_iid = selected_iid

        entry_edit.insert(0, selected_text)
        entry_edit.select_range(0, tk.END)

        entry_edit.focus()

        entry_edit.bind("<FocusOut>", self.on_focus_out)
        entry_edit.bind("<Return>", self.on_enter_pressed)

        entry_edit.place(
            x=column_box[0],
            y=column_box[1]-5,
            w=column_box[2],
            h=column_box[3]+10)

    def on_enter_pressed(self, event):
        new_info = event.widget.get()

        # Such as I002
        selected_iid = event.widget.editing_item_iid

        column_index = event.widget.editing_column_index
    
        values = self.item(selected_iid)
        
        if column_index == -1:
            values.update({"text":new_info})
            self.item(selected_iid, text=new_info)
        else:
            current_values = self.item(selected_iid).get("values")
            current_values[column_index] = new_info
            self.item(selected_iid, values=current_values)
        

        updated_db_list = [
            self.item(selected_iid)['values'][1],
            self.item(selected_iid)['text'],
            self.item(selected_iid)['values'][0],
            self.item(selected_iid)['values'][2]
            ]
        
        event.widget.destroy()
        update_data_to_db(updated_db_list)

    def on_focus_out(self, event):
        event.widget.destroy()

    def remove_row_data(self):
        row_iids = self.selection()
        selected_items_by_imo = list()

        for row in row_iids:
            selected_items_by_imo.append(self.item(row).get('values')[1])

        return selected_items_by_imo
        
    
