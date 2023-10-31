import tkinter as tk
from tkinter import ttk


class Vessel(ttk.Entry):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

    def import_data(self):
        pass