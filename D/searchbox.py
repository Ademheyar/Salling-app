import tkinter as tk
from tkinter import ttk
import sqlite3
import os
import sys
current_dir = os.path.abspath(os.path.dirname(__file__))
MAIN_dir = os.path.join(current_dir, '..')
sys.path.append(MAIN_dir)
from D.ItemSelector import ItemSelectorWidget
import os

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
db_path = os.path.join(data_dir, 'my_database.db')
conn = sqlite3.connect(db_path)

class search_entry(ttk.Entry):
    def __init__(self, *args, **kwargs):
        ttk.Entry.__init__(self, *args, **kwargs)
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = tk.StringVar()
        self.var.trace('w', self.changed)
        self.bind("<Return>", self.select)
        self.bind("<Escape>", lambda _: self.var.set(''))

        # Connect to database
        self.cursor = conn.cursor()
        
        # Initialize search type
        self.search_type = ""
        self.lb_up = False

    def changed(self, name, index, mode):
        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    w = self.grid_size()[0]
                    h = self.grid_size()[1]
                    self.lb = ttk.Treeview(columns=("CODE", "ITEM", "PRICE"))
                    self.lb.bind("<Double-Button-1>", self.select)
                    self.lb.bind("<Return>", self.select)
                    # width=w, height=5
                    self.lb.heading("#0", text="ID", anchor=tk.W)
                    self.lb.column("#0", minwidth=50, width=50)
                    self.lb.heading("#1", text="CODE", anchor=tk.W)
                    self.lb.column("#1", minwidth=50, width=50) 
                    self.lb.heading("#2", text="ITEM", anchor=tk.W)
                    self.lb.column("#2", stretch=tk.YES)  
                    self.lb.heading("#3", text="PRICE", anchor=tk.W)
                    self.lb.column("#3", minwidth=50, width=50) 
                    self.lb.place(x=self.winfo_x(), y=self.winfo_y()+self.winfo_height()+25)
                    self.lb_up = True
                self.lb.delete(*self.lb.get_children())
                w = 0
                while w < len(words):
                    code_leng = len(str(words[w+1])) * 4
                    name_leng = len(str(words[w+2])) * 10
                    if self.lb.column("#1", option="width") < code_leng:
                        self.lb.column("#1", width=code_leng) 
                    if self.lb.column("#2", option="width") < name_leng:
                        self.lb.column("#2", width=name_leng) 
                    self.lb.insert("", "end", text=str(words[w]), values=(str(words[w+1]), str(words[w+2]), str(words[w+3])))
                    if w+4 < len(words):
                        w += 4
                        continue
                    else:
                        break
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    
    def select(self, _):
        if self.lb_up:
            selected_item = self.lb.item(self.lb.selection()[0])['text']
            if self.search_type == "":
                selected_item = self.lb.item(self.lb.selection()[0])['text']
            elif self.search_type == "barcode":
                selected_item = self.lb.item(self.lb.selection()[0])['text']
            elif self.search_type == "code":
                selected_item = self.lb.item(self.lb.selection()[0])['text']
            elif self.search_type == "type":
                selected_item = self.lb.item(self.lb.selection()[0])['text']
            self.var.set(selected_item)
            self.lb.destroy()
            self.lb_up = False
            self.icursor(tk.END)
            self.update_search_results(selected_item)

    def update_search_results(self, selected_item):
        #self.list_items.delete(0, tk.END)
        if self.search_type == "":
            self.search_type = "id"
        self.cursor.execute("SELECT * FROM product WHERE "+ self.search_type+ "=?", (selected_item,))
        result = self.cursor.fetchone()
        self.var.set("")
        if self.search_type == "id":
            self.search_type = ""
        if result:
            a = ItemSelectorWidget(self, result[12], result[16], self.master.master.master.master.qty)
            self.wait_window(a.getvalue_form)
            print("ret : " + str([a.selected_shop.get(), a.selected_color.get(), a.selected_size.get(), a.selected_qty.get()]))
            print("info : " + str(result))
            self.master.master.master.master.list_items.insert("", "end", text=str(result[0]), values=(result[2], a.selected_barcode.get(), result[1], a.selected_shop.get(), a.selected_color.get(), a.selected_size.get(), a.selected_qty.get(), result[9], self.master.master.master.master.disc, result[10],float(a.selected_qty.get())*float(result[9])))
            #column_name = tree.column("#1", "heading")
            for a in self.master.master.master.master.list_items.get_children():
                self.master.master.master.master.list_items.item(a)['values'][2] = "000"
                print("item : " + str(self.master.master.master.master.list_items.item(a)))
            self.master.master.master.master.qty = 0
            self.master.master.master.master.update_info()

    def comparison(self):
        query = self.var.get()
        print("word :" + str(query) + "search_type : " + str(self.search_type))
        if query:
            if self.search_type == "name" or self.search_type == "":
                self.cursor.execute("SELECT * FROM product WHERE name LIKE ?", (f"%{query}%",))
            elif self.search_type == "barcode":
                self.cursor.execute("SELECT * FROM product WHERE barcode LIKE ?", (f"%{query}%",))
            elif self.search_type == "code":
                self.cursor.execute("SELECT * FROM product WHERE code LIKE ?", (f"%{query}%",))
            elif self.search_type == "type":
                self.cursor.execute("SELECT * FROM product WHERE type LIKE ?", (f"%{query}%",))
                
            results = []
            for row in self.cursor.fetchall():
                results.append(row[0])
                results.append(row[2])
                results.append(row[1])
                results.append(row[9])
            return results
        else:
            return []
