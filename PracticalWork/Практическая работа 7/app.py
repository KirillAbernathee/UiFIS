import tkinter as tk
from tkinter import ttk, messagebox
import math

def calculate():
    try:
        var = int(combo_var.get())
        if var == 1:
            total = 120000
            errors = 240
            corrected = 180
            distorted = 12
            P_osh = errors / total
            K_ispr = corrected / errors
            result_text = f"P_ош = {errors}/{total} = {P_osh:.6f}\nK_испр = {corrected}/{errors} = {K_ispr:.4f}"
        elif var == 2:
            P_osh = 0.02
            D = 1 - P_osh
            result_text = f"Достоверность D = 1 - P_ош = 1 - {P_osh} = {D}"
        elif var == 3:
            symbols = 500000
            errors = 25
            Q = symbols / errors
            result_text = f"Средняя наработка на ошибку Q = {symbols}/{errors} = {Q:.2f} символов"
        elif var == 4:
            records = 10000
            errors = 40
            P_osh = errors / records
            result_text = f"P_ош = {errors}/{records} = {P_osh:.6f}"
        elif var == 5:
            times = [5, 7, 6, 8, 10, 4, 9, 11, 7, 13]
            T_i = sum(times) / len(times)
            result_text = f"Среднее время коррекции T_и = {T_i:.2f} мин"
        elif var == 6:
            T_rab = 120
            T_v = 5
            T_i = 3
            K_ig = (T_rab - (T_v + T_i)) / T_rab
            result_text = f"K_иг = ({T_rab} - ({T_v}+{T_i}))/{T_rab} = {K_ig:.4f}"
        elif var == 7:
            T_rab = 200
            T_v = 8
            T_k = 4
            T_i = 6
            T_pf = 10
            K_ti = (T_rab - (T_v + T_k + T_i)) / (T_rab + T_pf)
            result_text = f"K_ти = ({T_rab} - ({T_v}+{T_k}+{T_i}))/({T_rab}+{T_pf}) = {K_ti:.4f}"
        elif var == 8:
            errors = 50
            detected = 40
            K_obn = detected / errors
            result_text = f"K_обн = {detected}/{errors} = {K_obn:.2f}"
        elif var == 9:
            errors = 50
            detected = 40
            not_detected = errors - detected
            K_no = not_detected / errors
            result_text = f"K_но = {not_detected}/{errors} = {K_no:.2f}"
        elif var == 10:
            errors = 60
            corrected = 30
            distorted = 5
            detected = 15
            not_detected = 10
            K_ispr = corrected / errors
            K_isk = distorted / errors
            K_obn = detected / errors
            K_no = not_detected / errors
            result_text = (f"K_испр = {corrected}/{errors} = {K_ispr:.3f}\n"
                           f"K_иск = {distorted}/{errors} = {K_isk:.3f}\n"
                           f"K_обн = {detected}/{errors} = {K_obn:.3f}\n"
                           f"K_но = {not_detected}/{errors} = {K_no:.3f}")
        elif var == 11:
            errors = 80
            detected = 70
            K_vyjavl = detected / errors
            result_text = f"K_выявл = {detected}/{errors} = {K_vyjavl:.3f}"
        elif var == 12:
            errors = 60
            corrected = 30
            distorted = 5
            detected = 15
            not_detected = 10
            K_no = not_detected / errors
            K_isk = distorted / errors
            K_tr = K_no + K_isk
            result_text = f"K_тр = K_но + K_иск = {K_no:.3f} + {K_isk:.3f} = {K_tr:.3f}"
        elif var == 13:
            P_bez = 0.95
            P_lt = 0.03
            P_pr = P_bez - P_lt
            result_text = f"P_пр = P_без - P_лт = {P_bez} - {P_lt} = {P_pr:.3f}"
        elif var == 14:
            P_osh = 0.1
            sum_k = (1 - P_osh) / P_osh
            result_text = f"K_пр + K_лт = (1 - {P_osh})/{P_osh} = {sum_k:.2f}"
        elif var == 15:
            total = 10000
            error_records = 200
            detected = 180
            corrected = 100
            distorted = 10
            not_detected = 20
            false_alarm = 5
            P_osh = error_records / total
            K_obn = detected / error_records
            K_no = not_detected / error_records
            result_text = (f"P_ош = {error_records}/{total} = {P_osh:.4f}\n"
                           f"K_обн = {detected}/{error_records} = {K_obn:.3f}\n"
                           f"K_но = {not_detected}/{error_records} = {K_no:.3f}")
        else:
            result_text = "Выберите корректный вариант"
        lbl_result.config(text=result_text)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Проверьте ввод данных\n{str(e)}")

root = tk.Tk()
root.title("Практическая работа 7")
root.geometry("700x500")
root.resizable(False, False)

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill=tk.BOTH, expand=True)

ttk.Label(main_frame, text="Выберите вариант (1-15):").grid(row=0, column=0, sticky=tk.W, pady=5)

combo_var = tk.StringVar()
combo = ttk.Combobox(main_frame, textvariable=combo_var, values=list(range(1, 16)), state="readonly", width=5)
combo.grid(row=0, column=1, sticky=tk.W, pady=5)
combo.current(0)

btn_calc = ttk.Button(main_frame, text="Рассчитать", command=calculate)
btn_calc.grid(row=0, column=2, padx=10, pady=5)

lbl_result = ttk.Label(main_frame, text="Здесь будет результат", font=("Courier", 10), foreground="blue")
lbl_result.grid(row=1, column=0, columnspan=3, sticky=tk.W, pady=20)

conditions_text = {
    1: "120 000 записей, 240 ошибок, исправлено 180, искажено 12",
    2: "P_ош = 0,02",
    3: "500 000 символов, 25 ошибок",
    4: "10 000 записей, 40 ошибок",
    5: "Времена коррекции: 5,7,6,8,10,4,9,11,7,13 мин",
    6: "T_раб=120 ч, T_в=5 ч, T_и=3 ч",
    7: "T_раб=200 ч, T_в=8 ч, T_к=4 ч, T_и=6 ч, T_пф=10 ч",
    8: "50 ошибок, обнаружено 40",
    9: "50 ошибок, обнаружено 40",
    10: "60 ошибок: испр30, искаж5, обн15, не обн10",
    11: "80 ошибок, выявлено 70",
    12: "Данные задачи 10",
    13: "P_без=0,95, P_лт=0,03",
    14: "P_ош=0,1",
    15: "10 000 записей, 200 с ошибками, обн180, испр100, искаж10, не обн20, ложн5"
}

lbl_condition = ttk.Label(main_frame, text="Условие: " + conditions_text[1], wraplength=650, justify=tk.LEFT)
lbl_condition.grid(row=2, column=0, columnspan=3, sticky=tk.W, pady=10)

def update_condition(event):
    try:
        v = int(combo_var.get())
        lbl_condition.config(text="Условие: " + conditions_text.get(v, ""))
    except:
        pass

combo.bind("<<ComboboxSelected>>", update_condition)

root.mainloop()