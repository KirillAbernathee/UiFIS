import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from fpdf import FPDF
import datetime

class QualityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Анализ индексов качества процесса")
        self.root.geometry("1000x700")
        self.history_data = []
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.calculator_frame = ttk.Frame(self.notebook)
        self.graph_frame = ttk.Frame(self.notebook)
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calculator_frame, text="Калькулятор")
        self.notebook.add(self.graph_frame, text="График распределения")
        self.notebook.add(self.history_frame, text="История расчетов")
        self.setup_calculator_tab()
        self.setup_graph_tab()
        self.setup_history_tab()
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def setup_calculator_tab(self):
        main_frame = ttk.Frame(self.calculator_frame, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        input_frame = ttk.LabelFrame(main_frame, text="Параметры процесса", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        ttk.Label(input_frame, text="Нижняя граница допуска (LSL):").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.lsl_entry = ttk.Entry(input_frame, width=20)
        self.lsl_entry.grid(row=0, column=1, pady=2, padx=5)
        ttk.Label(input_frame, text="Верхняя граница допуска (USL):").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.usl_entry = ttk.Entry(input_frame, width=20)
        self.usl_entry.grid(row=1, column=1, pady=2, padx=5)
        ttk.Label(input_frame, text="Среднее процесса (μ):").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.mean_entry = ttk.Entry(input_frame, width=20)
        self.mean_entry.grid(row=2, column=1, pady=2, padx=5)
        ttk.Label(input_frame, text="Стандартное отклонение (σ):").grid(row=3, column=0, sticky=tk.W, pady=2)
        self.std_entry = ttk.Entry(input_frame, width=20)
        self.std_entry.grid(row=3, column=1, pady=2, padx=5)
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)
        ttk.Button(button_frame, text="Рассчитать", command=self.calculate).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Сохранить в историю", command=self.save_to_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить поля", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        result_frame = ttk.LabelFrame(main_frame, text="Результаты расчета", padding="10")
        result_frame.pack(fill=tk.X, pady=5)
        self.cp_label = ttk.Label(result_frame, text="Cp = ", font=("Arial", 10, "bold"))
        self.cp_label.pack(anchor=tk.W, pady=2)
        self.cpk_label = ttk.Label(result_frame, text="Cpk = ", font=("Arial", 10, "bold"))
        self.cpk_label.pack(anchor=tk.W, pady=2)
        self.interpretation_label = ttk.Label(result_frame, text="", font=("Arial", 10))
        self.interpretation_label.pack(anchor=tk.W, pady=2)
        export_frame = ttk.LabelFrame(main_frame, text="Экспорт данных", padding="10")
        export_frame.pack(fill=tk.X, pady=5)
        ttk.Button(export_frame, text="Экспорт текущего расчета в Excel", command=self.export_current_excel).pack(side=tk.LEFT, padx=5)
        ttk.Button(export_frame, text="Экспорт в PDF", command=self.export_pdf).pack(side=tk.LEFT, padx=5)

    def setup_graph_tab(self):
        self.graph_display_frame = ttk.Frame(self.graph_frame)
        self.graph_display_frame.pack(fill=tk.BOTH, expand=True)
        self.graph_controls_frame = ttk.Frame(self.graph_frame)
        self.graph_controls_frame.pack(fill=tk.X, pady=5)
        ttk.Button(self.graph_controls_frame, text="Построить график текущего расчета", command=self.plot_current_graph).pack(side=tk.LEFT, padx=5)
        ttk.Button(self.graph_controls_frame, text="Обновить график из истории", command=self.plot_history_graph).pack(side=tk.LEFT, padx=5)

    def setup_history_tab(self):
        tree_frame = ttk.Frame(self.history_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        columns = ("lsl", "usl", "mean", "std", "cp", "cpk", "interpretation", "timestamp")
        self.history_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
        self.history_tree.heading("lsl", text="LSL")
        self.history_tree.heading("usl", text="USL")
        self.history_tree.heading("mean", text="Среднее")
        self.history_tree.heading("std", text="Стд.откл.")
        self.history_tree.heading("cp", text="Cp")
        self.history_tree.heading("cpk", text="Cpk")
        self.history_tree.heading("interpretation", text="Интерпретация")
        self.history_tree.heading("timestamp", text="Дата/время")
        self.history_tree.column("lsl", width=80)
        self.history_tree.column("usl", width=80)
        self.history_tree.column("mean", width=80)
        self.history_tree.column("std", width=80)
        self.history_tree.column("cp", width=70)
        self.history_tree.column("cpk", width=70)
        self.history_tree.column("interpretation", width=150)
        self.history_tree.column("timestamp", width=130)
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar.set)
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        button_frame = ttk.Frame(self.history_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        ttk.Button(button_frame, text="Загрузить выбранный расчет", command=self.load_selected_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить историю", command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Экспорт истории в Excel", command=self.export_history_excel).pack(side=tk.LEFT, padx=5)

    def calculate_indices(self, lsl, usl, mean, std):
        if std <= 0:
            return None, None
        cp = (usl - lsl) / (6 * std)
        cpk = min((usl - mean) / (3 * std), (mean - lsl) / (3 * std))
        return cp, cpk

    def interpret_cpk(self, cpk):
        if cpk >= 1.33:
            return "Отлично", "green"
        elif cpk >= 1.0:
            return "Удовлетворительно", "blue"
        elif cpk >= 0.67:
            return "Неудовлетворительно", "orange"
        else:
            return "Критично", "red"

    def calculate(self):
        try:
            lsl = float(self.lsl_entry.get())
            usl = float(self.usl_entry.get())
            mean = float(self.mean_entry.get())
            std = float(self.std_entry.get())
            if lsl >= usl:
                messagebox.showerror("Ошибка", "LSL должна быть меньше USL")
                return
            cp, cpk = self.calculate_indices(lsl, usl, mean, std)
            if cp is None:
                messagebox.showerror("Ошибка", "Стандартное отклонение должно быть положительным")
                return
            self.cp_label.config(text=f"Cp = {cp:.3f}")
            self.cpk_label.config(text=f"Cpk = {cpk:.3f}")
            interpretation, color = self.interpret_cpk(cpk)
            self.interpretation_label.config(text=f"Интерпретация: {interpretation}", foreground=color)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")

    def save_to_history(self):
        try:
            lsl = float(self.lsl_entry.get())
            usl = float(self.usl_entry.get())
            mean = float(self.mean_entry.get())
            std = float(self.std_entry.get())
            cp, cpk = self.calculate_indices(lsl, usl, mean, std)
            interpretation, _ = self.interpret_cpk(cpk)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            record = {
                "lsl": lsl, "usl": usl, "mean": mean, "std": std,
                "cp": cp, "cpk": cpk, "interpretation": interpretation, "timestamp": timestamp
            }
            self.history_data.append(record)
            self.history_tree.insert("", tk.END, values=(
                f"{lsl:.3f}", f"{usl:.3f}", f"{mean:.3f}", f"{std:.3f}",
                f"{cp:.3f}", f"{cpk:.3f}", interpretation, timestamp
            ))
            messagebox.showinfo("Успех", "Расчет сохранен в историю")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def clear_fields(self):
        self.lsl_entry.delete(0, tk.END)
        self.usl_entry.delete(0, tk.END)
        self.mean_entry.delete(0, tk.END)
        self.std_entry.delete(0, tk.END)
        self.cp_label.config(text="Cp = ")
        self.cpk_label.config(text="Cpk = ")
        self.interpretation_label.config(text="")

    def plot_graph(self, lsl, usl, mean, std, cp, cpk):
        for widget in self.graph_display_frame.winfo_children():
            widget.destroy()
        fig, ax = plt.subplots(figsize=(8, 5))
        x = np.linspace(mean - 4*std, mean + 4*std, 1000)
        y = (1/(std * np.sqrt(2*np.pi))) * np.exp(-0.5*((x - mean)/std)**2)
        ax.plot(x, y, 'b-', linewidth=2, label='Распределение процесса')
        ax.axvline(lsl, color='red', linestyle='--', linewidth=2, label=f'LSL = {lsl:.3f}')
        ax.axvline(usl, color='red', linestyle='--', linewidth=2, label=f'USL = {usl:.3f}')
        ax.axvline(mean, color='green', linestyle='-', linewidth=1, label=f'Среднее = {mean:.3f}')
        x_fill_in = x[(x >= lsl) & (x <= usl)]
        y_fill_in = y[(x >= lsl) & (x <= usl)]
        ax.fill_between(x_fill_in, y_fill_in, color='green', alpha=0.3, label='В допуске')
        x_fill_out_l = x[x < lsl]
        y_fill_out_l = y[x < lsl]
        if len(x_fill_out_l) > 0:
            ax.fill_between(x_fill_out_l, y_fill_out_l, color='red', alpha=0.3, label='Вне допуска')
        x_fill_out_r = x[x > usl]
        y_fill_out_r = y[x > usl]
        if len(x_fill_out_r) > 0:
            ax.fill_between(x_fill_out_r, y_fill_out_r, color='red', alpha=0.3)
        ax.set_xlabel('Значение')
        ax.set_ylabel('Плотность вероятности')
        ax.set_title(f'Распределение процесса\nCp = {cp:.3f}, Cpk = {cpk:.3f}')
        ax.legend()
        ax.grid(True, alpha=0.3)
        canvas = FigureCanvasTkAgg(fig, master=self.graph_display_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_current_graph(self):
        try:
            lsl = float(self.lsl_entry.get())
            usl = float(self.usl_entry.get())
            mean = float(self.mean_entry.get())
            std = float(self.std_entry.get())
            cp, cpk = self.calculate_indices(lsl, usl, mean, std)
            self.plot_graph(lsl, usl, mean, std, cp, cpk)
            self.notebook.select(self.graph_frame)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")

    def plot_history_graph(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись из истории")
            return
        item = self.history_tree.item(selected[0])
        values = item['values']
        lsl, usl, mean, std = map(float, values[:4])
        cp, cpk = map(float, values[4:6])
        self.plot_graph(lsl, usl, mean, std, cp, cpk)
        self.notebook.select(self.graph_frame)

    def load_selected_history(self):
        selected = self.history_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите запись из истории")
            return
        item = self.history_tree.item(selected[0])
        values = item['values']
        self.lsl_entry.delete(0, tk.END)
        self.lsl_entry.insert(0, str(values[0]))
        self.usl_entry.delete(0, tk.END)
        self.usl_entry.insert(0, str(values[1]))
        self.mean_entry.delete(0, tk.END)
        self.mean_entry.insert(0, str(values[2]))
        self.std_entry.delete(0, tk.END)
        self.std_entry.insert(0, str(values[3]))
        self.calculate()
        self.notebook.select(self.calculator_frame)

    def clear_history(self):
        self.history_tree.delete(*self.history_tree.get_children())
        self.history_data.clear()
        messagebox.showinfo("Успех", "История очищена")

    def export_current_excel(self):
        try:
            lsl = float(self.lsl_entry.get())
            usl = float(self.usl_entry.get())
            mean = float(self.mean_entry.get())
            std = float(self.std_entry.get())
            cp, cpk = self.calculate_indices(lsl, usl, mean, std)
            interpretation, _ = self.interpret_cpk(cpk)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data = {
                "Параметр": ["LSL", "USL", "Среднее", "Стд.отклонение", "Cp", "Cpk", "Интерпретация", "Дата/время"],
                "Значение": [lsl, usl, mean, std, cp, cpk, interpretation, timestamp]
            }
            df = pd.DataFrame(data)
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
            if file_path:
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Успех", f"Данные экспортированы в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def export_history_excel(self):
        if not self.history_data:
            messagebox.showwarning("Предупреждение", "История пуста")
            return
        df = pd.DataFrame(self.history_data)
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Успех", f"История экспортирована в {file_path}")

    def export_pdf(self):
        try:
            lsl = float(self.lsl_entry.get())
            usl = float(self.usl_entry.get())
            mean = float(self.mean_entry.get())
            std = float(self.std_entry.get())
            cp, cpk = self.calculate_indices(lsl, usl, mean, std)
            interpretation, _ = self.interpret_cpk(cpk)
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            pdf = FPDF()
            pdf.add_page()
            pdf.add_font('Times', '', 'c:/windows/fonts/times.ttf', uni=True)
            pdf.add_font('Times', 'B', 'c:/windows/fonts/timesbd.ttf', uni=True)
            
            pdf.set_font('Times', 'B', 16)
            pdf.cell(0, 10, 'Отчет по анализу качества процесса', 0, 1, 'C')
            pdf.ln(5)
            
            pdf.set_font('Times', '', 12)
            pdf.cell(0, 10, '=' * 60, 0, 1, 'C')
            pdf.cell(0, 10, f'Дата и время: {timestamp}', 0, 1, 'L')
            pdf.ln(5)
            
            pdf.set_font('Times', 'B', 14)
            pdf.cell(0, 10, 'Параметры процесса:', 0, 1, 'L')
            pdf.set_font('Times', '', 12)
            pdf.cell(0, 10, f'  LSL: {lsl:.3f}', 0, 1, 'L')
            pdf.cell(0, 10, f'  USL: {usl:.3f}', 0, 1, 'L')
            pdf.cell(0, 10, f'  Среднее (μ): {mean:.3f}', 0, 1, 'L')
            pdf.cell(0, 10, f'  Стд.отклонение (σ): {std:.3f}', 0, 1, 'L')
            pdf.ln(5)
            
            pdf.set_font('Times', 'B', 14)
            pdf.cell(0, 10, 'Индексы качества:', 0, 1, 'L')
            pdf.set_font('Times', '', 12)
            pdf.cell(0, 10, f'  Cp = {cp:.3f}', 0, 1, 'L')
            pdf.cell(0, 10, f'  Cpk = {cpk:.3f}', 0, 1, 'L')
            pdf.ln(5)
            
            pdf.set_font('Times', 'B', 12)
            pdf.cell(0, 10, f'Интерпретация: {interpretation}', 0, 1, 'L')
            
            file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
            if file_path:
                pdf.output(file_path)
                messagebox.showinfo("Успех", f"Отчет экспортирован в {file_path}")
                
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось создать PDF: {str(e)}")

    def on_tab_change(self, event):
        pass

if __name__ == "__main__":
    root = tk.Tk()
    app = QualityApp(root)
    root.mainloop()