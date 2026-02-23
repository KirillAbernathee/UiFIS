import requests
import json
from datetime import datetime
from dataclasses import dataclass
from typing import Optional, List, Tuple
import tkinter as tk
from tkinter import ttk, messagebox, Listbox, END


@dataclass
class DeliveryRequest:
    start_address: str
    end_address: str
    transport_type: str


@dataclass
class DeliveryResult:
    start_address: str
    end_address: str
    distance_km: float
    duration_min: float
    transport_type: str
    cost_rub: float
    timestamp: str


class DeliveryService:
    TRANSPORT_RATES = {
        "Автомобиль": 40,
        "Грузовик": 60,
        "Мотоцикл": 25
    }

    def __init__(self):
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.osrm_url = "http://router.project-osrm.org/route/v1/driving/"
        self.history = []

    def geocode_address(self, address: str) -> Optional[Tuple[float, float]]:
        if not address or address.strip() == "":
            return None

        if ',' in address and address.replace(',', '').replace('.', '').replace('-', '').replace(' ', '').replace('+', '').isdigit():
            parts = address.split(',')
            if len(parts) == 2:
                try:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    return lat, lon
                except ValueError:
                    pass

        params = {
            'q': address,
            'format': 'json',
            'limit': 1
        }
        headers = {
            'User-Agent': 'DeliveryCalculator/1.0'
        }

        try:
            response = requests.get(self.nominatim_url, params=params, headers=headers)
            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    return lat, lon
        except requests.exceptions.RequestException:
            return None
        return None

    def get_route(self, start_coords: Tuple[float, float], end_coords: Tuple[float, float]) -> Optional[Tuple[float, float]]:
        url = f"{self.osrm_url}{start_coords[1]},{start_coords[0]};{end_coords[1]},{end_coords[0]}"
        params = {
            'overview': 'false',
            'geometries': 'geojson'
        }

        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['code'] == 'Ok' and data['routes']:
                    distance = data['routes'][0]['distance'] / 1000
                    duration = data['routes'][0]['duration'] / 60
                    return distance, duration
        except requests.exceptions.RequestException:
            return None
        return None

    def calculate_delivery(self, request: DeliveryRequest) -> Optional[DeliveryResult]:
        start_coords = self.geocode_address(request.start_address)
        if not start_coords:
            return None

        end_coords = self.geocode_address(request.end_address)
        if not end_coords:
            return None

        route = self.get_route(start_coords, end_coords)
        if not route:
            return None

        distance, duration = route
        rate = self.TRANSPORT_RATES.get(request.transport_type, 40)
        cost = distance * rate

        result = DeliveryResult(
            start_address=request.start_address,
            end_address=request.end_address,
            distance_km=round(distance, 1),
            duration_min=round(duration, 1),
            transport_type=request.transport_type,
            cost_rub=round(cost, 2),
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        self.history.append(result)
        return result

    def get_history(self) -> List[DeliveryResult]:
        return self.history


class MainForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор доставки")
        self.root.geometry("800x700")
        self.service = DeliveryService()

        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        input_frame = ttk.LabelFrame(main_frame, text="Параметры доставки", padding="10")
        input_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(input_frame, text="Пункт отправления:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.start_entry = ttk.Entry(input_frame, width=50)
        self.start_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Пункт назначения:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.end_entry = ttk.Entry(input_frame, width=50)
        self.end_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_frame, text="Тип транспорта:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.transport_combo = ttk.Combobox(input_frame, values=list(self.service.TRANSPORT_RATES.keys()), width=20)
        self.transport_combo.grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        self.transport_combo.set("Автомобиль")

        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        self.calc_button = ttk.Button(button_frame, text="Рассчитать", command=self.calculate)
        self.calc_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(button_frame, text="Очистить", command=self.clear_inputs)
        self.clear_button.pack(side=tk.LEFT, padx=5)

        result_frame = ttk.LabelFrame(main_frame, text="Результат расчета", padding="10")
        result_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        self.result_text = tk.Text(result_frame, height=8, width=70, state=tk.DISABLED)
        self.result_text.grid(row=0, column=0, pady=5)

        history_frame = ttk.LabelFrame(main_frame, text="История расчетов", padding="10")
        history_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        self.history_listbox = Listbox(history_frame, height=8, width=80)
        self.history_listbox.grid(row=0, column=0, pady=5)
        self.history_listbox.bind('<<ListboxSelect>>', self.on_history_select)

        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.history_listbox.config(yscrollcommand=scrollbar.set)

        self.load_button = ttk.Button(history_frame, text="Загрузить выбранное", command=self.load_from_history)
        self.load_button.grid(row=1, column=0, pady=5)

    def calculate(self):
        start = self.start_entry.get().strip()
        end = self.end_entry.get().strip()
        transport = self.transport_combo.get()

        if not start or not end:
            messagebox.showerror("Ошибка", "Пожалуйста, заполните все поля")
            return

        request = DeliveryRequest(start, end, transport)
        result = self.service.calculate_delivery(request)

        if result:
            self.display_result(result)
            self.update_history_list()
        else:
            messagebox.showerror("Ошибка", "Не удалось рассчитать маршрут. Проверьте адреса и подключение к интернету.")

    def display_result(self, result: DeliveryResult):
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(1.0, f"Отправление: {result.start_address}\n")
        self.result_text.insert(2.0, f"Назначение: {result.end_address}\n")
        self.result_text.insert(3.0, f"Расстояние: {result.distance_km} км\n")
        self.result_text.insert(4.0, f"Время в пути: {result.duration_min} мин\n")
        self.result_text.insert(5.0, f"Транспорт: {result.transport_type}\n")
        self.result_text.insert(6.0, f"Стоимость: {result.cost_rub} руб\n")
        self.result_text.insert(7.0, f"Время расчета: {result.timestamp}\n")
        self.result_text.config(state=tk.DISABLED)

    def clear_inputs(self):
        self.start_entry.delete(0, tk.END)
        self.end_entry.delete(0, tk.END)
        self.transport_combo.set("Автомобиль")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)

    def update_history_list(self):
        self.history_listbox.delete(0, END)
        for item in reversed(self.service.get_history()):
            display_text = f"{item.timestamp} | {item.start_address} → {item.end_address} | {item.distance_km} км | {item.cost_rub} руб"
            self.history_listbox.insert(0, display_text)

    def on_history_select(self, event):
        pass

    def load_from_history(self):
        selection = self.history_listbox.curselection()
        if selection:
            index = selection[0]
            reversed_index = len(self.service.get_history()) - 1 - index
            result = self.service.get_history()[reversed_index]

            self.start_entry.delete(0, tk.END)
            self.start_entry.insert(0, result.start_address)
            self.end_entry.delete(0, tk.END)
            self.end_entry.insert(0, result.end_address)
            self.transport_combo.set(result.transport_type)

            self.display_result(result)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainForm(root)
    root.mainloop()