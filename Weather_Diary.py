
import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - ������� ������")
        self.root.geometry("800x600")
        
        # ������ ��� �������� �������
        self.entries = []
        self.load_data()
        
        # �������� ����������
        self.create_input_frame()
        self.create_tree_view()
        self.create_filter_frame()
        self.create_button_frame()
        
        # ���������� �����������
        self.refresh_display()
    
    def create_input_frame(self):
        """�������� ������ ��� ����� ������"""
        input_frame = tk.LabelFrame(self.root, text="���������� ������", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # ���� ��� ����
        tk.Label(input_frame, text="���� (����-��-��):").grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = tk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, pady=5, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # ���� ��� �����������
        tk.Label(input_frame, text="����������� (�C):").grid(row=0, column=2, sticky="w", pady=5, padx=(20,0))
        self.temp_entry = tk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, pady=5, padx=5)
        
        # ���� ��� ��������
        tk.Label(input_frame, text="�������� ������:").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="w")
        
        # ������� ��� �������
        self.precipitation_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="������", variable=self.precipitation_var).grid(row=0, column=4, padx=20)
    
    def create_tree_view(self):
        """�������� ������� ��� ����������� �������"""
        # ����� ��� ������� � ����������
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # ����������
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        
        # �������
        columns = ("����", "�����������", "��������", "������")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # ��������� �������
        self.tree.heading("����", text="����")
        self.tree.heading("�����������", text="����������� (�C)")
        self.tree.heading("��������", text="��������")
        self.tree.heading("������", text="������")
        
        self.tree.column("����", width=120)
        self.tree.column("�����������", width=100)
        self.tree.column("��������", width=350)
        self.tree.column("������", width=80)
        
        # ��������� �����������
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # ����������
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_filter_frame(self):
        """�������� ������ ��� ����������"""
        filter_frame = tk.LabelFrame(self.root, text="����������", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # ������ �� ����
        tk.Label(filter_frame, text="������ �� ���� (����-��-��):").grid(row=0, column=0, sticky="w")
        self.filter_date_entry = tk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5)
        
        tk.Button(filter_frame, text="��������� ������ �� ����", 
                 command=self.filter_by_date).grid(row=0, column=2, padx=5)
        tk.Button(filter_frame, text="��������", 
                 command=self.clear_date_filter).grid(row=0, column=3, padx=5)
        
        # ������ �� �����������
        tk.Label(filter_frame, text="������ �� ����������� (>):").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.filter_temp_entry = tk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=1, column=1, pady=(10,0), padx=5)
        
        tk.Button(filter_frame, text="��������� ������ �� �����������", 
                 command=self.filter_by_temperature).grid(row=1, column=2, pady=(10,0), padx=5)
        tk.Button(filter_frame, text="��������", 
                 command=self.clear_temp_filter).grid(row=1, column=3, pady=(10,0), padx=5)
        
        # ������ ������ ���� ��������
        tk.Button(filter_frame, text="�������� ��� �������", 
                 command=self.reset_filters, bg="lightgray").grid(row=2, column=0, columnspan=4, pady=(10,0))
    
    def create_button_frame(self):
        """�������� ������ � �������� ����������"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="�������� ������", command=self.add_entry,
                 bg="lightgreen", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="������� ��������� ������", command=self.delete_entry,
                 bg="lightcoral").pack(side="left", padx=5)
        
        tk.Button(button_frame, text="��������� � JSON", command=self.save_to_json,
                 bg="lightblue").pack(side="left", padx=5)
        
        tk.Button(button_frame, text="��������� �� JSON", command=self.load_from_json,
                 bg="lightyellow").pack(side="left", padx=5)
    
    def validate_date(self, date_string):
        """�������� ������������ ����"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def add_entry(self):
        """���������� ����� ������"""
        # ��������� ������ �� �����
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = "��" if self.precipitation_var.get() else "���"
        
        # ��������� ������
        if not date:
            messagebox.showerror("������", "���� �� ����� ���� ������!")
            return
        
        if not self.validate_date(date):
            messagebox.showerror("������", "�������� ������ ����! ����������� ����-��-��")
            return
        
        try:
            temp_float = float(temp)
        except ValueError:
            messagebox.showerror("������", "����������� ������ ���� ������!")
            return
        
        if not description:
            messagebox.showerror("������", "�������� �� ����� ���� ������!")
            return
        
        # ���������� ������
        entry = {
            "date": date,
            "temperature": temp_float,
            "description": description,
            "precipitation": precipitation
        }
        
        self.entries.append(entry)
        self.refresh_display()
        
        # ������� ����� �����
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)
        
        messagebox.showinfo("�����", "������ ������� ���������!")
    
    def delete_entry(self):
        """�������� ��������� ������"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("��������������", "�������� ������ ��� ��������!")
            return
        
        # ��������� ������� ��������� ������
        item = selected_item[0]
        values = self.tree.item(item, "values")
        
        # ����� � �������� ������
        for i, entry in enumerate(self.entries):
            if (entry["date"] == values[0] and 
                entry["temperature"] == float(values[1]) and
                entry["description"] == values[2] and
                entry["precipitation"] == values[3]):
                del self.entries[i]
                break
        
        self.refresh_display()
        messagebox.showinfo("�����", "������ �������!")
    
    def refresh_display(self, entries_to_show=None):
        """���������� ����������� �������"""
        # ������� �������
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # ����������� ������� ��� �����������
        display_entries = entries_to_show if entries_to_show is not None else self.entries
        
        # ���������� �� ����
        display_entries = sorted(display_entries, key=lambda x: x["date"])
        
        # ���������� ������� � �������
        for entry in display_entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))
    
    def filter_by_date(self):
        """���������� �� ����"""
        filter_date = self.filter_date_entry.get().strip()
        
        if not filter_date:
            messagebox.showwarning("��������������", "������� ���� ��� ����������!")
            return
        
        if not self.validate_date(filter_date):
            messagebox.showerror("������", "�������� ������ ����! ����������� ����-��-��")
            return
        
        filtered = [entry for entry in self.entries if entry["date"] == filter_date]
        
        if not filtered:
            messagebox.showinfo("����������", f"������� �� ���� {filter_date} �� �������")
        
        self.refresh_display(filtered)
    
    def filter_by_temperature(self):
        """���������� �� ����������� (���� ���������)"""
        filter_temp = self.filter_temp_entry.get().strip()
        
        if not filter_temp:
            messagebox.showwarning("��������������", "������� �������� �����������!")
            return
        
        try:
            temp_threshold = float(filter_temp)
        except ValueError:
            messagebox.showerror("������", "����������� ������ ���� ������!")
            return
        
        filtered = [entry for entry in self.entries if entry["temperature"] > temp_threshold]
        
        if not filtered:
            messagebox.showinfo("����������", f"������� � ������������ ���� {temp_threshold}�C �� �������")
        
        self.refresh_display(filtered)
    
    def clear_date_filter(self):
        """������� ������� �� ����"""
        self.filter_date_entry.delete(0, tk.END)
        self.refresh_display()
    
    def clear_temp_filter(self):
        """������� ������� �� �����������"""
        self.filter_temp_entry.delete(0, tk.END)
        self.refresh_display()
    
    def reset_filters(self):
        """����� ���� ��������"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.refresh_display()
        messagebox.showinfo("����������", "��� ������� ��������")
    
    def save_to_json(self):
        """���������� ������� � JSON ����"""
        try:
            with open("weather_data.json", "w", encoding="utf-8") as file:
                json.dump(self.entries, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("�����", "������ ������� ��������� � weather_data.json")
        except Exception as e:
            messagebox.showerror("������", f"������ ��� ����������: {str(e)}")
    
    def load_from_json(self):
        """�������� ������� �� JSON �����"""
        if not os.path.exists("weather_data.json"):
            messagebox.showwarning("��������������", "���� weather_data.json �� ������!")
            return
        
        try:
            with open("weather_data.json", "r", encoding="utf-8") as file:
                self.entries = json.load(file)
            self.refresh_display()
            messagebox.showinfo("�����", f"��������� {len(self.entries)} �������")
        except Exception as e:
            messagebox.showerror("������", f"������ ��� ��������: {str(e)}")
    
    def load_data(self):
        """�������������� �������� ������ ��� �������"""
        if os.path.exists("weather_data.json"):
            try:
                with open("weather_data.json", "r", encoding="utf-8") as file:
                    self.entries = json.load(file)
            except:
                self.entries = []

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
