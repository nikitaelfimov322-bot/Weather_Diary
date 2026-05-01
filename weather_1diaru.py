import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime
import os

DATA_FILE = "data.json"


class WeatherDiary:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Diary")
        self.root.geometry("600x500")

        self.data = []
        self.load_data()

        # -------- ВВОД --------
        frame_input = tk.LabelFrame(root, text="Добавить запись")
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Дата (YYYY-MM-DD)").grid(row=0, column=0)
        self.date_entry = tk.Entry(frame_input)
        self.date_entry.grid(row=0, column=1)

        tk.Label(frame_input, text="Температура").grid(row=1, column=0)
        self.temp_entry = tk.Entry(frame_input)
        self.temp_entry.grid(row=1, column=1)

        tk.Label(frame_input, text="Описание").grid(row=2, column=0)
        self.desc_entry = tk.Entry(frame_input)
        self.desc_entry.grid(row=2, column=1)

        tk.Label(frame_input, text="Осадки").grid(row=3, column=0)
        self.precip_var = tk.BooleanVar()
        tk.Checkbutton(frame_input, variable=self.precip_var).grid(row=3, column=1)

        tk.Button(frame_input, text="Добавить запись", command=self.add_entry)\
            .grid(row=4, column=0, columnspan=2, pady=5)

        # -------- ФИЛЬТР --------
        frame_filter = tk.LabelFrame(root, text="Фильтр")
        frame_filter.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filter, text="Дата").grid(row=0, column=0)
        self.filter_date = tk.Entry(frame_filter)
        self.filter_date.grid(row=0, column=1)

        tk.Label(frame_filter, text="Темп. >").grid(row=1, column=0)
        self.filter_temp = tk.Entry(frame_filter)
        self.filter_temp.grid(row=1, column=1)

        tk.Button(frame_filter, text="Применить", command=self.apply_filter)\
            .grid(row=2, column=0)

        tk.Button(frame_filter, text="Сброс", command=self.refresh_table)\
            .grid(row=2, column=1)

        # -------- ТАБЛИЦА --------
        frame_table = tk.Frame(root)
        frame_table.pack(fill="both", expand=True, padx=10, pady=5)

        self.tree = ttk.Treeview(frame_table,
                                 columns=("date", "temp", "desc", "precip"),
                                 show="headings")

        self.tree.heading("date", text="Дата")
        self.tree.heading("temp", text="Температура")
        self.tree.heading("desc", text="Описание")
        self.tree.heading("precip", text="Осадки")

        self.tree.pack(fill="both", expand=True)

        # -------- КНОПКИ --------
        frame_buttons = tk.Frame(root)
        frame_buttons.pack(pady=5)

        tk.Button(frame_buttons, text="Сохранить", command=self.save_data).pack(side="left", padx=5)
        tk.Button(frame_buttons, text="Загрузить", command=self.load_data).pack(side="left", padx=5)

        self.refresh_table()

    # -------- ВАЛИДАЦИЯ --------
    def validate(self, date, temp, desc):
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except:
            messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD")
            return False

        try:
            float(temp)
        except:
            messagebox.showerror("Ошибка", "Температура должна быть числом")
            return False

        if desc.strip() == "":
            messagebox.showerror("Ошибка", "Описание не может быть пустым")
            return False

        return True

    # -------- ДОБАВЛЕНИЕ --------
    def add_entry(self):
        date = self.date_entry.get()
        temp = self.temp_entry.get()
        desc = self.desc_entry.get()
        precip = self.precip_var.get()

        if not self.validate(date, temp, desc):
            return

        entry = {
            "date": date,
            "temp": float(temp),
            "desc": desc,
            "precip": precip
        }

        self.data.append(entry)
        self.refresh_table()

        self.date_entry.delete(0, tk.END)
        self.temp_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.precip_var.set(False)

    # -------- ОБНОВЛЕНИЕ ТАБЛИЦЫ --------
    def refresh_table(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = data if data is not None else self.data

        for item in data:
            self.tree.insert("", tk.END, values=(
                item["date"],
                item["temp"],
                item["desc"],
                "Да" if item["precip"] else "Нет"
            ))

    # -------- ФИЛЬТР --------
    def apply_filter(self):
        filtered = self.data

        if self.filter_date.get():
            filtered = [x for x in filtered if x["date"] == self.filter_date.get()]

        if self.filter_temp.get():
            try:
                t = float(self.filter_temp.get())
                filtered = [x for x in filtered if x["temp"] > t]
            except:
                messagebox.showerror("Ошибка", "Некорректная температура фильтра")
                return

        self.refresh_table(filtered)

    # -------- СОХРАНЕНИЕ --------
    def save_data(self):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as f:
                json.dump(self.data, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Успех", "Данные сохранены")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    # -------- ЗАГРУЗКА --------
    def load_data(self):
        if not os.path.exists(DATA_FILE):
            self.data = []
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except:
            self.data = []

        self.refresh_table()


if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherDiary(root)
    root.mainloop()
