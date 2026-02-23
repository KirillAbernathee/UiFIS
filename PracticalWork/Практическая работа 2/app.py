import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Практическая работа 2 - Показатели безотказности")
        self.geometry("1000x700")
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill='both', expand=True)
        
        self.frame1 = ttk.Frame(notebook)
        self.frame2 = ttk.Frame(notebook)
        self.frame3 = ttk.Frame(notebook)
        
        notebook.add(self.frame1, text="Задание 1")
        notebook.add(self.frame2, text="Задание 2")
        notebook.add(self.frame3, text="Задание 3")
        
        self.setup_task1()
        self.setup_task2()
        self.setup_task3()
    
    def setup_task1(self):
        main_frame = tk.Frame(self.frame1)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        tk.Label(left_frame, text="Задание 1", font=("Arial", 16, "bold")).pack(anchor='w', pady=5)
        tk.Label(left_frame, text="За исследуемый период эксплуатации система отказала 6 раз.", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="До первого отказа система проработала 185 часов, до второго – 342 часа,", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="до третьего – 268 часов, до четвертого отказа система проработала 220 часов,", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="до пятого – 96 часов, до шестого – 102 часа.", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="Определить среднюю наработку на отказ системы.", wraplength=400, justify='left', font=("Arial", 10, "bold")).pack(anchor='w', pady=5)
        
        tk.Label(left_frame, text="Введите наработки до отказов (через запятую):").pack(anchor='w', pady=(10,0))
        self.entry_times1 = tk.Entry(left_frame, width=40, font=("Arial", 10))
        self.entry_times1.pack(anchor='w', pady=5)
        self.entry_times1.insert(0, "185,342,268,220,96,102")
        
        btn_calc1 = tk.Button(left_frame, text="Рассчитать", command=self.calc_task1, bg="#4CAF50", fg="white", font=("Arial", 10))
        btn_calc1.pack(anchor='w', pady=5)
        
        self.result1 = tk.Label(left_frame, text="", font=("Arial", 12, "bold"), fg="blue", justify='left')
        self.result1.pack(anchor='w', pady=10)
        
        tk.Label(left_frame, text="Формула: T₀ = (∑tᵢ) / n", font=("Arial", 10, "italic")).pack(anchor='w')
        
        self.fig1 = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        self.canvas1 = FigureCanvasTkAgg(self.fig1, right_frame)
        self.canvas1.get_tk_widget().pack(fill='both', expand=True)
        
        self.update_plot_task1()
    
    def setup_task2(self):
        main_frame = tk.Frame(self.frame2)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side='left', fill='both', expand=True)
        
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side='right', fill='both', expand=True)
        
        tk.Label(left_frame, text="Задание 2", font=("Arial", 16, "bold")).pack(anchor='w', pady=5)
        tk.Label(left_frame, text="В течение некоторого времени проводилось наблюдение за работой N₀ экземпляров", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="одинаковых информационных систем. Каждая из систем проработала tᵢ часов", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="и имела nᵢ отказов. Требуется определить наработку на отказ по данным", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="наблюдения за работой всех систем.", wraplength=400, justify='left').pack(anchor='w')
        tk.Label(left_frame, text="t₁ = 358 час, n₁ = 4, t₂ = 385 час, n₂ = 3, t₃ = 400 час, n₃ = 2", wraplength=400, justify='left', font=("Arial", 10, "bold")).pack(anchor='w', pady=5)
        
        input_frame = tk.Frame(left_frame)
        input_frame.pack(anchor='w', pady=10)
        
        tk.Label(input_frame, text="Система 1 (t, n):").grid(row=0, column=0, sticky='w')
        self.entry_sys1 = tk.Entry(input_frame, width=15, font=("Arial", 10))
        self.entry_sys1.grid(row=0, column=1, padx=5)
        self.entry_sys1.insert(0, "358,4")
        
        tk.Label(input_frame, text="Система 2 (t, n):").grid(row=1, column=0, sticky='w')
        self.entry_sys2 = tk.Entry(input_frame, width=15, font=("Arial", 10))
        self.entry_sys2.grid(row=1, column=1, padx=5)
        self.entry_sys2.insert(0, "385,3")
        
        tk.Label(input_frame, text="Система 3 (t, n):").grid(row=2, column=0, sticky='w')
        self.entry_sys3 = tk.Entry(input_frame, width=15, font=("Arial", 10))
        self.entry_sys3.grid(row=2, column=1, padx=5)
        self.entry_sys3.insert(0, "400,2")
        
        btn_calc2 = tk.Button(left_frame, text="Рассчитать", command=self.calc_task2, bg="#4CAF50", fg="white", font=("Arial", 10))
        btn_calc2.pack(anchor='w', pady=5)
        
        self.result2 = tk.Label(left_frame, text="", font=("Arial", 12, "bold"), fg="blue", justify='left')
        self.result2.pack(anchor='w', pady=10)
        
        tk.Label(left_frame, text="Формула: T₀ = (∑Tⱼ) / (∑nⱼ)", font=("Arial", 10, "italic")).pack(anchor='w')
        
        self.fig2 = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        self.canvas2 = FigureCanvasTkAgg(self.fig2, right_frame)
        self.canvas2.get_tk_widget().pack(fill='both', expand=True)
        
        self.update_plot_task2()
    
    def setup_task3(self):
        main_frame = tk.Frame(self.frame3)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        top_frame = tk.Frame(main_frame)
        top_frame.pack(fill='x')
        
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill='both', expand=True)
        
        tk.Label(top_frame, text="Задание 3", font=("Arial", 16, "bold")).pack(anchor='w')
        tk.Label(top_frame, text="По результатам исследования двух автоматизированных систем были получены следующие", wraplength=800, justify='left').pack(anchor='w')
        tk.Label(top_frame, text="экспериментальные данные по безотказности и восстанавливаемости двух автоматизированных систем.", wraplength=800, justify='left').pack(anchor='w')
        tk.Label(top_frame, text="Требуется определить по коэффициенту готовности, какая из систем является более надежной.", wraplength=800, justify='left', font=("Arial", 10, "bold")).pack(anchor='w', pady=5)
        
        table_frame = tk.Frame(top_frame)
        table_frame.pack(fill='x', pady=10)
        
        columns = ("Вариант", "t0 сист.1", "tв сист.1", "t0 сист.2", "tв сист.2")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=8)
        
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=80)
        
        data = [
            ("1", "24", "16", "400", "32"),
            ("2", "84", "24", "184", "32"),
            ("3", "225", "8", "64", "24"),
            ("4", "20", "6", "16", "8"),
            ("5", "58", "2", "16", "8"),
            ("6", "516", "19", "160", "8"),
            ("7", "287", "16", "8", "4"),
            ("8", "464", "64", "8", "16"),
            ("9", "96", "12", "48", "8"),
            ("10", "4", "3", "104", "8"),
            ("11", "37", "3", "272", "8"),
            ("12", "101", "3", "336", "8"),
            ("13", "29", "4", "370", "8"),
            ("14", "12", "5", "384", "7"),
            ("15", "3", "24", "56", "8"),
            ("16", "304", "16", "4", "8")
        ]
        
        for row in data:
            tree.insert("", tk.END, values=row)
        
        tree.pack(side=tk.LEFT, fill='x', expand=True)
        
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        tree.configure(yscrollcommand=scrollbar.set)
        
        control_frame = tk.Frame(top_frame)
        control_frame.pack(pady=10)
        
        tk.Label(control_frame, text="Выберите вариант (1-16):", font=("Arial", 10)).pack(side='left')
        self.var_entry = tk.Entry(control_frame, width=5, font=("Arial", 10))
        self.var_entry.pack(side='left', padx=5)
        self.var_entry.insert(0, "1")
        
        btn_calc3 = tk.Button(control_frame, text="Рассчитать", command=self.calc_task3, bg="#4CAF50", fg="white", font=("Arial", 10))
        btn_calc3.pack(side='left', padx=5)
        
        self.result3 = tk.Label(top_frame, text="", font=("Arial", 11), fg="blue", justify='left')
        self.result3.pack(pady=5)
        
        tk.Label(top_frame, text="Формулы: T₀ = ∑t₀/n, Tв = ∑tв/m, Kг = T₀/(T₀+Tв)", font=("Arial", 10, "italic")).pack()
        
        self.fig3 = plt.Figure(figsize=(9, 4), dpi=100)
        self.ax3 = self.fig3.add_subplot(111)
        self.canvas3 = FigureCanvasTkAgg(self.fig3, bottom_frame)
        self.canvas3.get_tk_widget().pack(fill='both', expand=True)
    
    def update_plot_task1(self):
        try:
            times = list(map(float, self.entry_times1.get().split(',')))
            self.ax1.clear()
            x = range(1, len(times) + 1)
            self.ax1.bar(x, times, color='skyblue', edgecolor='navy')
            self.ax1.set_xlabel('Номер отказа')
            self.ax1.set_ylabel('Наработка (часы)')
            self.ax1.set_title('Наработка до каждого отказа')
            self.ax1.grid(True, alpha=0.3)
            for i, v in enumerate(times):
                self.ax1.text(i+1, v + 5, str(v), ha='center', va='bottom')
            self.canvas1.draw()
        except:
            pass
    
    def update_plot_task2(self):
        try:
            sys1 = list(map(float, self.entry_sys1.get().split(',')))
            sys2 = list(map(float, self.entry_sys2.get().split(',')))
            sys3 = list(map(float, self.entry_sys3.get().split(',')))
            
            systems = ['Система 1', 'Система 2', 'Система 3']
            times = [sys1[0], sys2[0], sys3[0]]
            failures = [sys1[1], sys2[1], sys3[1]]
            
            self.ax2.clear()
            x = np.arange(len(systems))
            width = 0.35
            
            bars1 = self.ax2.bar(x - width/2, times, width, label='Наработка (ч)', color='skyblue', edgecolor='navy')
            bars2 = self.ax2.bar(x + width/2, failures, width, label='Число отказов', color='lightcoral', edgecolor='darkred')
            
            self.ax2.set_xlabel('Системы')
            self.ax2.set_ylabel('Значения')
            self.ax2.set_title('Данные по системам')
            self.ax2.set_xticks(x)
            self.ax2.set_xticklabels(systems)
            self.ax2.legend()
            self.ax2.grid(True, alpha=0.3)
            
            for bar in bars1:
                height = bar.get_height()
                self.ax2.text(bar.get_x() + bar.get_width()/2., height + 5, f'{int(height)}', ha='center', va='bottom')
            for bar in bars2:
                height = bar.get_height()
                self.ax2.text(bar.get_x() + bar.get_width()/2., height + 2, f'{int(height)}', ha='center', va='bottom')
            
            self.canvas2.draw()
        except:
            pass
    
    def update_plot_task3(self, var, kr1, kr2):
        self.ax3.clear()
        
        systems = ['Система 1', 'Система 2']
        kg_values = [kr1, kr2]
        colors = ['lightgreen', 'lightblue']
        
        bars = self.ax3.bar(systems, kg_values, color=colors, edgecolor='darkgreen', width=0.5)
        
        self.ax3.set_ylabel('Коэффициент готовности')
        self.ax3.set_title(f'Сравнение систем (Вариант {var})')
        self.ax3.set_ylim([0, 1])
        self.ax3.grid(True, alpha=0.3, axis='y')
        
        for bar, val in zip(bars, kg_values):
            height = bar.get_height()
            self.ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01, f'{val:.4f}', ha='center', va='bottom', fontweight='bold')
        
        self.canvas3.draw()
    
    def calc_task1(self):
        try:
            times = list(map(float, self.entry_times1.get().split(',')))
            if not times:
                raise ValueError("Введите данные")
            t0 = sum(times) / len(times)
            self.result1.config(text=f"Средняя наработка на отказ T₀ = {t0:.2f} часов")
            self.update_plot_task1()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный формат ввода: {e}")
    
    def calc_task2(self):
        try:
            sys1 = list(map(float, self.entry_sys1.get().split(',')))
            sys2 = list(map(float, self.entry_sys2.get().split(',')))
            sys3 = list(map(float, self.entry_sys3.get().split(',')))
            
            if len(sys1) != 2 or len(sys2) != 2 or len(sys3) != 2:
                raise ValueError("Введите время и число отказов через запятую")
            
            total_time = sys1[0] + sys2[0] + sys3[0]
            total_failures = sys1[1] + sys2[1] + sys3[1]
            
            if total_failures == 0:
                raise ValueError("Число отказов не может быть равно 0")
            
            t0 = total_time / total_failures
            self.result2.config(text=f"Средняя наработка на отказ для всех систем T₀ = {t0:.2f} часов")
            self.update_plot_task2()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный формат ввода: {e}")
    
    def calc_task3(self):
        data_t0_sys1 = [24, 84, 225, 20, 58, 516, 287, 464, 96, 4, 37, 101, 29, 12, 3, 304]
        data_tv_sys1 = [16, 24, 8, 6, 2, 19, 16, 64, 12, 3, 3, 3, 4, 5, 24, 16]
        data_t0_sys2 = [400, 184, 64, 16, 16, 160, 8, 8, 48, 104, 272, 336, 370, 384, 56, 4]
        data_tv_sys2 = [32, 32, 24, 8, 8, 8, 4, 16, 8, 8, 8, 8, 8, 7, 8, 8]
        
        try:
            var = int(self.var_entry.get())
            if var < 1 or var > 16:
                raise ValueError("Вариант должен быть от 1 до 16")
            
            idx = var - 1
            
            t0_sys1 = data_t0_sys1[idx]
            tv_sys1 = data_tv_sys1[idx]
            t0_sys2 = data_t0_sys2[idx]
            tv_sys2 = data_tv_sys2[idx]
            
            t0_sys1_avg = t0_sys1 / 1
            tv_sys1_avg = tv_sys1 / 1
            t0_sys2_avg = t0_sys2 / 1
            tv_sys2_avg = tv_sys2 / 1
            
            kr1 = t0_sys1_avg / (t0_sys1_avg + tv_sys1_avg)
            kr2 = t0_sys2_avg / (t0_sys2_avg + tv_sys2_avg)
            
            if kr1 > kr2:
                better = "Система 1 более надежна"
            elif kr2 > kr1:
                better = "Система 2 более надежна"
            else:
                better = "Системы равнонадежны"
            
            result_text = f"Система 1: T₀ = {t0_sys1} ч, Tв = {tv_sys1} ч, Kг = {kr1:.4f}\n"
            result_text += f"Система 2: T₀ = {t0_sys2} ч, Tв = {tv_sys2} ч, Kг = {kr2:.4f}\n"
            result_text += f"Результат: {better}"
            
            self.result3.config(text=result_text)
            self.update_plot_task3(var, kr1, kr2)
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Неверный ввод: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()