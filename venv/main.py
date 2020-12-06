
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import os
import scipy.stats as stats
from os import path
import numpy as np
import fisher

class Main(tk.Frame):

    def __init__(self, root):
        super().__init__(root)

        self.init_main(root)

    def open_file_tkinter(self):
        filename = filedialog.askopenfilename(defaultextension='.txt',
                                              filetypes=[
                                                  ("text files", "*.txt"),
                                                  ('All files', '*.*')
                                              ]
                                              )
        self.entry_0_string.set(filename)


    def show_warning(self, msg):
        messagebox.showwarning("Предупреждение", msg)

    def clear_line(self):
        self.entry_3_string.set('')
        self.entry_4_string.set('')
        self.entry_5_string.set('')
        self.entry_6_string.set('')
        self.entry_7_string.set('')
        self.entry_8_string.set('')
        self.entry_9_string.set('')
        self.text_1.delete('1.0', tk.END)

    def calculation(self):
        filename = self.entry_0_string.get()
        fileString = fisher.open_file(filename) # Получаем путь файла
        if fileString[0] == 0:
            arr = list(map(float, fileString[1].split(' ')))
        else:
            self.show_warning(fileString[1])
            self.clear_line()
            return 1
        answer_3 = len(arr) #количество элементов выборки
        answer_4 = fisher.normalizeFloat(np.mean(arr)) # Среднее арифметическое значение
        answer_5 = fisher.normalizeFloat(stats.tstd(arr)) # Оценка среднего квадратического отклонения


        name = self.entry_1_string.get()
        countSplit = fisher.inputCountSplit(name, len(arr))
        if countSplit[0] == 0:
            arr = np.array_split(arr, countSplit[1])
        else:
            self.show_warning(countSplit[1])
            self.clear_line()
            return 1

        answer_6 = fisher.normalizeFloat(fisher.MSA(arr))# Межгрупповая дисперсия
        answer_7 = fisher.normalizeFloat(fisher.MSW(arr))# Внутригрупповая дисперсия

        
        fCritery = fisher.getFishersCritery(arr)
        answer_8 = fisher.normalizeFloat(fCritery) # Критерий Фишера


        significanceLevel = self.entry_2_string.get()
        significanceLevel = fisher.inputSignificanceLevel(significanceLevel)
        if significanceLevel[0] == 0:
            fCriticalCritery = fisher.getCriticalFishersCritery((significanceLevel[1]), arr)
            answer_9 = fisher.normalizeFloat(fCriticalCritery) # Критический критерий Фишера

        else:
            self.show_warning(significanceLevel[1])
            self.clear_line()
            return 1

        self.entry_3_string.set(answer_3)  # Выводим количество элементов выборки
        self.entry_4_string.set(answer_4)  # Среднее арифметическое значение
        self.entry_5_string.set(answer_5)  # Оценка среднего квадратического отклонения
        self.entry_6_string.set(answer_6)  # Межгрупповая дисперсия
        self.entry_7_string.set(answer_7)  # Внутригрупповая дисперсия
        self.entry_8_string.set(answer_8)  # Критерий Фишера
        self.entry_9_string.set(answer_9)  # Критический критерий Фишера

        summary = fisher.summary(fCritery, fCriticalCritery)
        self.text_1.insert(1.0, summary)

        return filename

    def init_main(self, root):
        label_title = tk.Label(root, text='Выявление медленно меняющихся систематических погрешностей с помощью критерия Фишера', bg='#AFEEEE', font='Times 14', width=100, height=1)
        label_title.grid(row=0, column=0, columnspan=12) # разделить(растянуть) по оси X

        open_file_label = tk.Label(root, text='Выберите путь к файлу/рассчитать:').grid(row=1, column=0, sticky='W')
        button_open_file = tk.Button(text="Открыть файл", bg = '#FFFFE0',command=lambda: self.open_file_tkinter()).grid(row=14, column=0,
                                                                                                                        sticky='W')
        button_calculation = tk.Button(text="Рассчитать", bg = '#FFFFE0', command=lambda: self.calculation()).grid(row=14, column=0,padx=110,
                                                                                              sticky='W')
        self.entry_0_string = tk.StringVar()
        self.entry_1_string = tk.StringVar()
        self.entry_2_string = tk.StringVar()
        self.entry_3_string = tk.StringVar()
        self.entry_4_string = tk.StringVar()
        self.entry_5_string = tk.StringVar()
        self.entry_6_string = tk.StringVar()
        self.entry_7_string = tk.StringVar()
        self.entry_8_string = tk.StringVar()
        self.entry_9_string = tk.StringVar()


        one = tk.Label(root, text='Введите количество серий, на которое стоит разделить выборку:').grid(row=2, column=0, sticky='W')
        second = tk.Label(root, text='Введите уровень значимости:').grid(row=3, column=0, sticky='W')
        three = tk.Label(root, text='Количество элементов выборки:').grid(row=4, column=0, sticky='W')
        four = tk.Label(root, text='Среднее арифметическое значение:').grid(row=5, column=0, sticky='W')
        five = tk.Label(root, text='Оценка среднего квадратического отклонения:').grid(row=6, column=0, sticky='W')
        six = tk.Label(root, text='Межгрупповая дисперсия:').grid(row=7, column=0, sticky='W')
        seven = tk.Label(root, text='Внутригрупповая дисперсия:').grid(row=8, column=0, sticky='W')
        eight = tk.Label(root, text='Критерий Фишера:').grid(row=9, column=0, sticky='W')
        nine = tk.Label(root, text='Критический критерий Фишера:').grid(row=10, column=0, sticky='W')
        ten = tk.Label(root, text='Вывод:').grid(row=11, column=0, sticky='W')

        entry_0 = tk.Entry(textvariable=self.entry_0_string, justify="left", width=70).grid(row=1, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_1 = tk.Entry(textvariable=self.entry_1_string, justify="left", width=70).grid(row=2, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_2 = tk.Entry(textvariable=self.entry_2_string, justify="left", width=70).grid(row=3, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_3 = tk.Entry(textvariable=self.entry_3_string, justify="left", width=70, state='disabled').grid(row=4, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_4 = tk.Entry(textvariable=self.entry_4_string, justify="left", width=70, state='disabled').grid(row=5, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_5 = tk.Entry(textvariable=self.entry_5_string, justify="left", width=70, state='disabled').grid(row=6, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_6 = tk.Entry(textvariable=self.entry_6_string, justify="left", width=70, state='disabled').grid(row=7, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_7 = tk.Entry(textvariable=self.entry_7_string, justify="left", width=70, state='disabled').grid(row=8, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_8 = tk.Entry(textvariable=self.entry_8_string, justify="left", width=70, state='disabled').grid(row=9, column=1, sticky='W',
                                                                                       columnspan=11)
        entry_9 = tk.Entry(textvariable=self.entry_9_string, justify="left", width=70, state='disabled').grid(row=10, column=1, sticky='W',
                                                                                       columnspan=11)
        self.text_1 = tk.Text(height=4, width=52, font=("Times New Roman", 12), wrap="word")
        self.text_1.grid(row=11, column=1, sticky='W', columnspan=11)


if __name__ == "__main__":
    root = tk.Tk()
    app = Main(root)
    app.grid()
    root.title("Домашняя работа по метрологии")
    root.geometry("950x450+300+150")
    root.resizable(False, False)
    root.mainloop()

#Выявление медленно меняющихся систематических погрешностей с помощью критерия Фишера