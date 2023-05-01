import tkinter as tk
import sqlite3

# Create a connection to the SQLite database
conn = sqlite3.connect('my_database.db')


# Create a table to store the document records
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS pre_doc_table 
                (id INTEGER PRIMARY KEY, 
                doc_created_date TEXT, 
                doc_expire_date TEXT, 
                doc_updated_date TEXT,
                user_id TEXT, 
                customer_id TEXT, 
                type TEXT, 
                discount REAL, 
                CODE TEXT,
                BARCODE TEXT,
                ITEM_Name TEXT,
                AT_SHOP TEXT,
                COLOR TEXT,
                SIZE TEXT,
                QTY TEXT,
                PRICE TEXT,
                Item_Disc TEXT,
                TAX TEXT,
                States TEXT
                )''')


cur.execute('''CREATE TABLE IF NOT EXISTS doc_table 
                (id INTEGER PRIMARY KEY, 
                doc_barcode TEXT, 
                extension_barcode TEXT, 
                user_id TEXT, 
                customer_id TEXT, 
                type TEXT, 
                item TEXT, 
                qty REAL,  
                price REAL, 
                discount REAL, 
                tax REAL, 
                doc_created_date TEXT, 
                doc_expire_date TEXT, 
                doc_updated_date TEXT)''')

# Example usage:
# Add a new document record to the doc_table SQLite database table

# Connect to the database or create it if it does not exist
cur.execute('''CREATE TABLE IF NOT EXISTS product
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              code TEXT,
              type TEXT,
              barcode TEXT,
              at_shop TEXT,
              quantity INTEGER,
              cost REAL,
              tax REAL,
              price REAL,
              include_tax INTEGER,
              price_change INTEGER,
              more_info TEXT,
              images TEXT,
              description TEXT,
              service TEXT,
              default_quantity INTEGER,
              active INTEGER)''')

cur.execute('''CREATE TABLE IF NOT EXISTS USERS
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              type TEXT,
              phone_num TEXT,
              password TEXT,
              id_num TEXT,
              email TEXT,
              address TEXT,
              acsess TEXT)''')

cur.execute('''CREATE TABLE IF NOT EXISTS tools
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT,
              code TEXT,
              type TEXT,
              short_key TEXT,
              acsess TEXT,
              enabel INTEGER,
              quick_pay INTEGER,
              customer_required INTEGER,
              printslip REAL,
              change_allowed REAL,
              markpad REAL,
              open_drower REAL)''')

conn.commit()
conn.close()

from Display import DisplayFrame
from Manager import ManageForm
from Login import Loging_Frame


class MainApplication(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d+0+0" % (screen_width, screen_height))
        self.title("Main Application")
        
        # create the container frame to hold the other frames
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # create the first frame and add it to the container
        self.frames = {}

        display_frame = DisplayFrame(self)
        display_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["DisplayFrame"] = display_frame
        
        # create the second frame and add it to the container
        manage_form = ManageForm(self)
        manage_form.grid(row=0, column=0, sticky="nsew")
        self.frames["ManageFrame"] = manage_form

        # create the second frame and add it to the container
        lofing_frame = Loging_Frame(self)
        lofing_frame.grid(row=0, column=0, sticky="nsew")
        self.frames["LogingFrame"] = lofing_frame
        
        
        # show the first frame by default
        self.show_frame("LogingFrame")
    
    def show_frame(self, frame_name):
        # hide all frames except the one to be shown
        for frame in self.frames.values():
            frame.grid_remove()
        self.frames[frame_name].grid()
        

if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()