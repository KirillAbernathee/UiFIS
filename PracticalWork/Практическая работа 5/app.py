import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import queue
from datetime import datetime
import logging

class QueueHandler(logging.Handler):
    def __init__(self, text_widget):
        logging.Handler.__init__(self)
        self.text_widget = text_widget

    def emit(self, record):
        msg = self.format(record)
        self.text_widget.after(0, lambda: self.text_widget.insert(tk.END, msg + '\n'))
        self.text_widget.after(0, lambda: self.text_widget.see(tk.END))

class NetworkTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Сетевой терминал - Имитация ЛВС")
        self.root.geometry("1200x700")
        self.root.resizable(False, False)
        
        self.devices = {
            'ПК1': {'pos': (100, 100), 'color': 'gray', 'status': 'offline'},
            'ПК2': {'pos': (400, 100), 'color': 'gray', 'status': 'offline'},
            'ПК3': {'pos': (100, 400), 'color': 'gray', 'status': 'offline'},
            'ПК4': {'pos': (400, 400), 'color': 'gray', 'status': 'offline'},
            'SWITCH': {'pos': (250, 250), 'color': 'lightblue', 'status': 'active', 'ports': 4}
        }
        
        self.connections = [
            ('ПК1', 'SWITCH'),
            ('ПК2', 'SWITCH'),
            ('ПК3', 'SWITCH'),
            ('ПК4', 'SWITCH')
        ]
        
        self.packets = []
        self.packet_counter = 0
        self.transmission_active = False
        self.packet_speed = 5
        self.statistics = {'total_packets': 0, 'delivered_packets': 0, 'lost_packets': 0}
        
        self.log_queue = queue.Queue()
        
        self.setup_ui()
        self.setup_logging()
        self.start_log_processor()
        
    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        left_frame = ttk.LabelFrame(main_frame, text="Визуализация сети", padding="10")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))
        
        self.canvas = tk.Canvas(left_frame, width=600, height=600, bg='white')
        self.canvas.grid(row=0, column=0)
        
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        control_frame = ttk.LabelFrame(right_frame, text="Управление", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.start_button = ttk.Button(control_frame, text="Старт", command=self.start_transmission)
        self.start_button.grid(row=0, column=0, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Стоп", command=self.stop_transmission, state='disabled')
        self.stop_button.grid(row=0, column=1, padx=5)
        
        self.clear_button = ttk.Button(control_frame, text="Очистить", command=self.clear_logs)
        self.clear_button.grid(row=0, column=2, padx=5)
        
        ttk.Label(control_frame, text="Скорость:").grid(row=1, column=0, pady=10)
        self.speed_var = tk.IntVar(value=5)
        self.speed_scale = ttk.Scale(control_frame, from_=1, to=10, orient='horizontal', 
                                     variable=self.speed_var, command=self.update_speed)
        self.speed_scale.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        stats_frame = ttk.LabelFrame(right_frame, text="Статистика", padding="10")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        self.stats_labels = {}
        for i, key in enumerate(['total_packets', 'delivered_packets', 'lost_packets']):
            ttk.Label(stats_frame, text=f"{key.replace('_', ' ').title()}: ").grid(row=i, column=0, sticky=tk.W)
            self.stats_labels[key] = ttk.Label(stats_frame, text="0")
            self.stats_labels[key].grid(row=i, column=1, sticky=tk.W)
        
        console_frame = ttk.LabelFrame(right_frame, text="Консоль", padding="10")
        console_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.console_text = tk.Text(console_frame, width=50, height=25, wrap=tk.WORD)
        self.console_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        scrollbar = ttk.Scrollbar(console_frame, orient='vertical', command=self.console_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.console_text.configure(yscrollcommand=scrollbar.set)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)
        console_frame.columnconfigure(0, weight=1)
        console_frame.rowconfigure(0, weight=1)
        
        self.draw_network()
        
    def setup_logging(self):
        self.logger = logging.getLogger('NetworkTerminal')
        self.logger.setLevel(logging.INFO)
        
        handler = QueueHandler(self.console_text)
        handler.setFormatter(logging.Formatter('[%(asctime)s.%(msecs)03d] %(message)s', 
                                              datefmt='%H:%M:%S'))
        self.logger.addHandler(handler)
        
    def start_log_processor(self):
        def process_logs():
            while True:
                try:
                    record = self.log_queue.get(timeout=0.1)
                    self.logger.handle(record)
                except queue.Empty:
                    continue
                except Exception as e:
                    print(f"Error processing log: {e}")
                    
        thread = threading.Thread(target=process_logs, daemon=True)
        thread.start()
        
    def draw_network(self):
        self.canvas.delete("all")
        
        for conn in self.connections:
            start = self.devices[conn[0]]['pos']
            end = self.devices[conn[1]]['pos']
            self.canvas.create_line(start[0], start[1], end[0], end[1], 
                                   fill='gray', dash=(5, 2), width=2)
        
        for device, info in self.devices.items():
            x, y = info['pos']
            
            if device == 'SWITCH':
                self.canvas.create_rectangle(x-35, y-35, x+35, y+35, 
                                            fill=info['color'], outline='darkblue', width=3)
                self.canvas.create_text(x, y, text=device, font=('Arial', 12, 'bold'))
                
                ports = [(-25, -25), (25, -25), (-25, 25), (25, 25)]
                for i, (px, py) in enumerate(ports):
                    color = 'green' if info['status'] == 'active' else 'red'
                    self.canvas.create_oval(x+px-5, y+py-5, x+px+5, y+py+5, fill=color)
            else:
                self.canvas.create_rectangle(x-30, y-20, x+30, y+20, 
                                            fill=info['color'], outline='black', width=2)
                self.canvas.create_text(x, y-10, text=device, font=('Arial', 10, 'bold'))
                self.canvas.create_rectangle(x-25, y+5, x+25, y+15, fill='black')
                self.canvas.create_rectangle(x-5, y-15, x+5, y-5, fill='lightblue')
                
    def start_transmission(self):
        self.transmission_active = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        
        for device in self.devices:
            if device != 'SWITCH':
                self.devices[device]['color'] = 'lightgray'
                self.devices[device]['status'] = 'active'
        self.devices['SWITCH']['color'] = 'lightblue'
        
        self.draw_network()
        self.logger.info("Передача данных запущена")
        
        self.transmission_thread = threading.Thread(target=self.packet_generator, daemon=True)
        self.transmission_thread.start()
        
        self.animation_thread = threading.Thread(target=self.animate_packets, daemon=True)
        self.animation_thread.start()
        
    def stop_transmission(self):
        self.transmission_active = False
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        
        for device in self.devices:
            if device != 'SWITCH':
                self.devices[device]['color'] = 'gray'
                self.devices[device]['status'] = 'offline'
        
        self.draw_network()
        
        self.logger.info("=" * 50)
        self.logger.info("ИТОГОВАЯ СТАТИСТИКА:")
        self.logger.info(f"Всего передано пакетов: {self.statistics['total_packets']}")
        self.logger.info(f"Доставлено пакетов: {self.statistics['delivered_packets']}")
        self.logger.info(f"Потеряно пакетов: {self.statistics['lost_packets']}")
        self.logger.info("=" * 50)
        
        self.packets.clear()
        self.canvas.delete("packet")
        
    def clear_logs(self):
        self.console_text.delete(1.0, tk.END)
        
    def update_speed(self, value):
        self.packet_speed = int(float(value))
        
    def packet_generator(self):
        while self.transmission_active:
            if len(self.packets) < 20: 

                source = random.choice(['ПК1', 'ПК2', 'ПК3', 'ПК4'])
                destination = random.choice([d for d in ['ПК1', 'ПК2', 'ПК3', 'ПК4'] if d != source])
                size = random.randint(50, 500)
                
                self.packet_counter += 1
                packet = {
                    'id': self.packet_counter,
                    'source': source,
                    'destination': destination,
                    'size': size,
                    'position': 0, 
                    'start_time': time.time(),
                    'color': random.choice(['red', 'green', 'blue', 'orange', 'purple'])
                }
                
                self.packets.append(packet)
                self.statistics['total_packets'] += 1
                self.update_statistics()
                
                self.logger.info(f"Пакет #{packet['id']}: {source} -> {destination}, Размер: {size} байт")
            
            time.sleep(1 / self.packet_speed)
            
    def animate_packets(self):
        while self.transmission_active:
            self.canvas.delete("packet")
            
            packets_to_remove = []
            
            for packet in self.packets[:]:
                source_pos = self.devices[packet['source']]['pos']
                dest_pos = self.devices[packet['destination']]['pos']
                switch_pos = self.devices['SWITCH']['pos']
                
                if packet['position'] == 0:
                    progress = (time.time() - packet['start_time']) * 100 
                    if progress >= 100:
                        packet['position'] = 1
                        packet['start_time'] = time.time()
                        
                       
                        delay = random.uniform(0.1, 1.0)
                        time.sleep(delay)
                        
                        self.logger.info(f"Пакет #{packet['id']} достиг коммутатора (задержка: {int(delay*1000)} мс)")
                        
                elif packet['position'] == 1:
                  
                    progress = (time.time() - packet['start_time']) * 100
                    if progress >= 100:
                        packet['position'] = 2
                        delivery_time = time.time() - packet['start_time'] + random.uniform(0.5, 2.0)
                        
                        self.logger.info(f"Пакет #{packet['id']} доставлен на {packet['destination']} (задержка: {int(delivery_time*1000)} мс)")
                        
                        self.statistics['delivered_packets'] += 1
                        packets_to_remove.append(packet)
                        
                if packet['position'] == 0:
                    progress = (time.time() - packet['start_time']) * 100 / 100
                    x = source_pos[0] + (switch_pos[0] - source_pos[0]) * min(progress, 1)
                    y = source_pos[1] + (switch_pos[1] - source_pos[1]) * min(progress, 1)
                else:
                  
                    progress = (time.time() - packet['start_time']) * 100 / 100
                    x = switch_pos[0] + (dest_pos[0] - switch_pos[0]) * min(progress, 1)
                    y = switch_pos[1] + (dest_pos[1] - switch_pos[1]) * min(progress, 1)
                
              
                self.canvas.create_oval(x-8, y-8, x+8, y+8, 
                                       fill=packet['color'], outline='black', width=2, tags="packet")
                self.canvas.create_text(x, y, text=str(packet['id']), 
                                       font=('Arial', 8, 'bold'), tags="packet")
            
           
            for packet in packets_to_remove:
                if packet in self.packets:
                    self.packets.remove(packet)
            
            self.update_statistics()
            time.sleep(0.05)
            
    def update_statistics(self):
        for key, label in self.stats_labels.items():
            label.config(text=str(self.statistics[key]))
            
    def on_closing(self):
        self.transmission_active = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkTerminal(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()