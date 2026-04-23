import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary - Дневник погоды")
        self.root.geometry("800x600")
        
        # Список для хранения записей
        self.entries = []
        self.load_data()
        
        # Создание интерфейса
        self.create_input_frame()
        self.create_tree_view()
        self.create_filter_frame()
        self.create_button_frame()
        
        # Обновление отображения
        self.refresh_display()
    
    def create_input_frame(self):
        """Создание фрейма для ввода данных"""
        input_frame = tk.LabelFrame(self.root, text="Добавление записи", padx=10, pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)
        
        # Поле для даты
        tk.Label(input_frame, text="Дата (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w", pady=5)
        self.date_entry = tk.Entry(input_frame, width=20)
        self.date_entry.grid(row=0, column=1, pady=5, padx=5)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        
        # Поле для температуры
        tk.Label(input_frame, text="Температура (°C):").grid(row=0, column=2, sticky="w", pady=5, padx=(20,0))
        self.temp_entry = tk.Entry(input_frame, width=10)
        self.temp_entry.grid(row=0, column=3, pady=5, padx=5)
        
        # Поле для описания
        tk.Label(input_frame, text="Описание погоды:").grid(row=1, column=0, sticky="w", pady=5)
        self.desc_entry = tk.Entry(input_frame, width=40)
        self.desc_entry.grid(row=1, column=1, columnspan=3, pady=5, padx=5, sticky="w")
        
        # Чекбокс для осадков
        self.precipitation_var = tk.BooleanVar()
        tk.Checkbutton(input_frame, text="Осадки", variable=self.precipitation_var).grid(row=0, column=4, padx=20)
    
    def create_tree_view(self):
        """Создание таблицы для отображения записей"""
        # Фрейм для таблицы и скроллбара
        tree_frame = tk.Frame(self.root)
        tree_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Скроллбары
        scroll_y = tk.Scrollbar(tree_frame, orient="vertical")
        scroll_x = tk.Scrollbar(tree_frame, orient="horizontal")
        
        # Таблица
        columns = ("Дата", "Температура", "Описание", "Осадки")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings",
                                 yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        
        # Настройка колонок
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Температура", text="Температура (°C)")
        self.tree.heading("Описание", text="Описание")
        self.tree.heading("Осадки", text="Осадки")
        
        self.tree.column("Дата", width=120)
        self.tree.column("Температура", width=100)
        self.tree.column("Описание", width=350)
        self.tree.column("Осадки", width=80)
        
        # Настройка скроллбаров
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        
        # Размещение
        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_filter_frame(self):
        """Создание фрейма для фильтрации"""
        filter_frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        # Фильтр по дате
        tk.Label(filter_frame, text="Фильтр по дате (ГГГГ-ММ-ДД):").grid(row=0, column=0, sticky="w")
        self.filter_date_entry = tk.Entry(filter_frame, width=15)
        self.filter_date_entry.grid(row=0, column=1, padx=5)
        
        tk.Button(filter_frame, text="Применить фильтр по дате", 
                 command=self.filter_by_date).grid(row=0, column=2, padx=5)
        tk.Button(filter_frame, text="Сбросить", 
                 command=self.clear_date_filter).grid(row=0, column=3, padx=5)
        
        # Фильтр по температуре
        tk.Label(filter_frame, text="Фильтр по температуре (>):").grid(row=1, column=0, sticky="w", pady=(10,0))
        self.filter_temp_entry = tk.Entry(filter_frame, width=10)
        self.filter_temp_entry.grid(row=1, column=1, pady=(10,0), padx=5)
        
        tk.Button(filter_frame, text="Применить фильтр по температуре", 
                 command=self.filter_by_temperature).grid(row=1, column=2, pady=(10,0), padx=5)
        tk.Button(filter_frame, text="Сбросить", 
                 command=self.clear_temp_filter).grid(row=1, column=3, pady=(10,0), padx=5)
        
        # Кнопка сброса всех фильтров
        tk.Button(filter_frame, text="Сбросить все фильтры", 
                 command=self.reset_filters, bg="lightgray").grid(row=2, column=0, columnspan=4, pady=(10,0))
    
    def create_button_frame(self):
        """Создание фрейма с кнопками управления"""
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill="x", padx=10, pady=5)
        
        tk.Button(button_frame, text="Добавить запись", command=self.add_entry,
                 bg="lightgreen", font=("Arial", 10, "bold")).pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Удалить выбранную запись", command=self.delete_entry,
                 bg="lightcoral").pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Сохранить в JSON", command=self.save_to_json,
                 bg="lightblue").pack(side="left", padx=5)
        
        tk.Button(button_frame, text="Загрузить из JSON", command=self.load_from_json,
                 bg="lightyellow").pack(side="left", padx=5)
    
    def validate_date(self, date_string):
        """Проверка корректности даты"""
        try:
            datetime.strptime(date_string, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def add_entry(self):
        """Добавление новой записи"""
        # Получение данных из полей
        date = self.date_entry.get().strip()
        temp = self.temp_entry.get().strip()
        description = self.desc_entry.get().strip()
        precipitation = "Да" if self.precipitation_var.get() else "Нет"
        
        # Валидация данных
        if not date:
            messagebox.showerror("Ошибка", "Дата не может быть пустой!")
            return
        
        if not self.validate_date(date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        try:
            temp_float = float(temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
        
        if not description:
            messagebox.showerror("Ошибка", "Описание не может быть пустым!")
            return
        
        # Добавление записи
        entry = {
            "date": date,
            "temperature": temp_float,
            "description": description,
            "precipitation": precipitation
        }
        
        self.entries.append(entry)
        self.refresh_display()
        
        # Очистка полей ввода
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precipitation_var.set(False)
        
        messagebox.showinfo("Успех", "Запись успешно добавлена!")
    
    def delete_entry(self):
        """Удаление выбранной записи"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Предупреждение", "Выберите запись для удаления!")
            return
        
        # Получение индекса выбранной записи
        item = selected_item[0]
        values = self.tree.item(item, "values")
        
        # Поиск и удаление записи
        for i, entry in enumerate(self.entries):
            if (entry["date"] == values[0] and 
                entry["temperature"] == float(values[1]) and
                entry["description"] == values[2] and
                entry["precipitation"] == values[3]):
                del self.entries[i]
                break
        
        self.refresh_display()
        messagebox.showinfo("Успех", "Запись удалена!")
    
    def refresh_display(self, entries_to_show=None):
        """Обновление отображения записей"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Определение записей для отображения
        display_entries = entries_to_show if entries_to_show is not None else self.entries
        
        # Сортировка по дате
        display_entries = sorted(display_entries, key=lambda x: x["date"])
        
        # Добавление записей в таблицу
        for entry in display_entries:
            self.tree.insert("", "end", values=(
                entry["date"],
                entry["temperature"],
                entry["description"],
                entry["precipitation"]
            ))
    
    def filter_by_date(self):
        """Фильтрация по дате"""
        filter_date = self.filter_date_entry.get().strip()
        
        if not filter_date:
            messagebox.showwarning("Предупреждение", "Введите дату для фильтрации!")
            return
        
        if not self.validate_date(filter_date):
            messagebox.showerror("Ошибка", "Неверный формат даты! Используйте ГГГГ-ММ-ДД")
            return
        
        filtered = [entry for entry in self.entries if entry["date"] == filter_date]
        
        if not filtered:
            messagebox.showinfo("Информация", f"Записей за дату {filter_date} не найдено")
        
        self.refresh_display(filtered)
    
    def filter_by_temperature(self):
        """Фильтрация по температуре (выше указанной)"""
        filter_temp = self.filter_temp_entry.get().strip()
        
        if not filter_temp:
            messagebox.showwarning("Предупреждение", "Введите значение температуры!")
            return
        
        try:
            temp_threshold = float(filter_temp)
        except ValueError:
            messagebox.showerror("Ошибка", "Температура должна быть числом!")
            return
        
        filtered = [entry for entry in self.entries if entry["temperature"] > temp_threshold]
        
        if not filtered:
            messagebox.showinfo("Информация", f"Записей с температурой выше {temp_threshold}°C не найдено")
        
        self.refresh_display(filtered)
    
    def clear_date_filter(self):
        """Очистка фильтра по дате"""
        self.filter_date_entry.delete(0, tk.END)
        self.refresh_display()
    
    def clear_temp_filter(self):
        """Очистка фильтра по температуре"""
        self.filter_temp_entry.delete(0, tk.END)
        self.refresh_display()
    
    def reset_filters(self):
        """Сброс всех фильтров"""
        self.filter_date_entry.delete(0, tk.END)
        self.filter_temp_entry.delete(0, tk.END)
        self.refresh_display()
        messagebox.showinfo("Информация", "Все фильтры сброшены")
    
    def save_to_json(self):
        """Сохранение записей в JSON файл"""
        try:
            with open("weather_data.json", "w", encoding="utf-8") as file:
                json.dump(self.entries, file, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные успешно сохранены в weather_data.json")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")
    
    def load_from_json(self):
        """Загрузка записей из JSON файла"""
        if not os.path.exists("weather_data.json"):
            messagebox.showwarning("Предупреждение", "Файл weather_data.json не найден!")
            return
        
        try:
            with open("weather_data.json", "r", encoding="utf-8") as file:
                self.entries = json.load(file)
            self.refresh_display()
            messagebox.showinfo("Успех", f"Загружено {len(self.entries)} записей")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при загрузке: {str(e)}")
    
    def load_data(self):
        """Автоматическая загрузка данных при запуске"""
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
