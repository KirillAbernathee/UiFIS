import tkinter as tk
from tkinter import messagebox, ttk
from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    text: str
    options: List[str]
    correct_index: int

class GuessStandardApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Угадай стандарт")
        self.geometry("600x500")
        self.resizable(False, False)

        self.questions = [
            Question("Какой стандарт определяет представление чисел с плавающей точкой?",
                    ["ISO 9001", "IEEE 754", "ASCII", "Unicode"], 1),
            Question("Какой стандарт описывает требования к системе менеджмента качества?",
                    ["IEEE 802.11", "ASCII", "ISO 9001", "IEEE 754"], 2),
            Question("Какой стандарт используется для беспроводной связи Wi-Fi?",
                    ["IEEE 802.11", "Unicode", "ISO 9001", "ASCII"], 0),
            Question("Какой стандарт кодирования включает символы всех письменностей мира?",
                    ["ASCII", "IEEE 754", "Unicode", "ISO 9001"], 2),
            Question("Какой стандарт является американским кодом для обмена информацией?",
                    ["Unicode", "ASCII", "IEEE 802.11", "ISO 9001"], 1)
        ]

        self.current_question = 0
        self.correct_answers = 0
        self.answer_given = False
        self.radio_var = tk.IntVar(value=-1)

        self.setup_ui()
        self.show_question()

    def setup_ui(self):
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.header_label = ttk.Label(main_frame, text="", font=("Arial", 14, "bold"))
        self.header_label.pack(pady=(0, 20))

        self.question_label = ttk.Label(main_frame, text="", font=("Arial", 12), wraplength=500)
        self.question_label.pack(pady=(0, 20))

        self.radio_frame = ttk.Frame(main_frame)
        self.radio_frame.pack(pady=(0, 20), anchor=tk.W)

        self.radio_buttons = []
        for i in range(4):
            rb = ttk.Radiobutton(self.radio_frame, text="", variable=self.radio_var, value=i)
            rb.pack(anchor=tk.W, pady=5)
            self.radio_buttons.append(rb)

        self.next_button = ttk.Button(main_frame, text="Далее", command=self.next_question)
        self.next_button.pack(pady=(0, 20))

        self.result_label = ttk.Label(main_frame, text="", font=("Arial", 10))
        self.result_label.pack(pady=(0, 10))

        self.progress_label = ttk.Label(main_frame, text="Правильных ответов: 0/5")
        self.progress_label.pack()

    def show_question(self):
        q = self.questions[self.current_question]
        self.header_label.config(text=f"Вопрос {self.current_question + 1} из {len(self.questions)}")
        self.question_label.config(text=q.text)
        
        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=q.options[i])
        
        self.radio_var.set(-1)
        self.result_label.config(text="")
        self.answer_given = False

    def next_question(self):
        if self.radio_var.get() == -1:
            messagebox.showwarning("Внимание", "Выберите вариант ответа!")
            return

        if not self.answer_given:
            if self.radio_var.get() == self.questions[self.current_question].correct_index:
                self.correct_answers += 1
                self.result_label.config(text="✓ Правильно!", foreground="green")
            else:
                correct_text = self.questions[self.current_question].options[self.questions[self.current_question].correct_index]
                self.result_label.config(text=f"✗ Неправильно. Правильный ответ: {correct_text}", foreground="red")
            
            self.answer_given = True
            self.progress_label.config(text=f"Правильных ответов: {self.correct_answers}/{len(self.questions)}")
            
            if self.current_question == len(self.questions) - 1:
                self.next_button.config(text="Завершить")
            return

        if self.current_question < len(self.questions) - 1:
            self.current_question += 1
            self.show_question()
        else:
            self.show_results()

    def show_results(self):
        percent = (self.correct_answers / len(self.questions)) * 100
        result_window = tk.Toplevel(self)
        result_window.title("Результат теста")
        result_window.geometry("300x300")
        result_window.resizable(False, False)
        
        ttk.Label(result_window, text="Тест завершен!", font=("Arial", 14, "bold")).pack(pady=20)
        ttk.Label(result_window, text=f"Правильных ответов: {self.correct_answers} из {len(self.questions)}", font=("Arial", 12)).pack(pady=10)
        ttk.Label(result_window, text=f"Процент правильных: {percent:.1f}%", font=("Arial", 12)).pack(pady=10)
        
        button_frame = ttk.Frame(result_window)
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Пройти заново", command=self.restart_test).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Завершить", command=self.quit_app).pack(side=tk.LEFT, padx=5)

    def restart_test(self):
        self.current_question = 0
        self.correct_answers = 0
        self.answer_given = False
        self.next_button.config(text="Далее")
        self.show_question()
        self.progress_label.config(text="Правильных ответов: 0/5")
        for widget in self.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

    def quit_app(self):
        self.quit()
        self.destroy()

if __name__ == "__main__":
    app = GuessStandardApp()
    app.mainloop()