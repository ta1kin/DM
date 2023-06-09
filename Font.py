import tkinter as tk
from tkinter import ttk, messagebox
from MatrixAlgorithms import Algorithms
from colorama import Fore
from colorama import Style
import working_with_storage
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


a=[]
class App(tk.Tk):

    def __init__(self, master=None):
        super().__init__(master)
        self.title('Преобразование матриц смежности')
        self.geometry('1200x900+400+100')
        self['bg'] = '#015367'
        self.minsize(370, 370)
        self.maxsize(1200, 900)
        # self.attributes("-zoomed", 1)
        # self.resizable(width=False, height=False)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.bold_font = 'Helvetica 16 bold'
        self.put_label_frames()
        self.wm_protocol("WM_DELETE_WINDOW", self.on_closing)
        working_with_storage.init()

    def put_label_frames(self) -> object:
        self.add_from_input_frame = AddInputFrame(self).grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        self.add_from_output_frame = AddOutputFrame(self).grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        self.add_from_tabel_frame = AddTableFrame(self).grid(row=1, column=0, sticky='nsew', columnspan=2, padx=5,  pady=5)

    def refresh(self):
        all_frames = [i for i in self.children]
        for f_name in all_frames:
            self.nametowidget(f_name).destroy()
        self.put_label_frames()

    def on_closing(self):
        if messagebox.askokcancel("Выход", "Хотите закрыть программу?"):
            working_with_storage.INDEX_DATA = []
            self.destroy()



class AddInputFrame(tk.LabelFrame):
    LIST_ALGORITHMS = ['Алгоритм Уоршалла',
                       'Обход графа в ширину',
                       'Обход графа в глубину',
                       'Алгоритм Флойда',
                       'Алгоритм Данцига',
                       'Алгоритм Форда-Фалкерсона',
                       'Алгоритм Дейкстры']

    def __init__(self, parent):
        super().__init__(parent)
        self.conversion_btn = None
        self.combo_input = None
        self.text_input = None
        self['bg'] = '#A4295B'
        self['text'] = ' Панель ввода '
        self['font'] = ('Ubuntu', 16)
        self['bd'] = 5
        self['labelanchor'] = tk.NE
        self.put_widgets()

    def put_widgets(self):
        # -->Создание кнопки выбора алгоритма
        if working_with_storage.INDEX_DATA != []:
            value = working_with_storage.select(working_with_storage.INDEX_DATA[-1])[-1]
            index = AddOutputFrame.LIST_ALGORITHMS.index(value)
        else:
            index = 0
        self.combo_input = ttk.Combobox(self, values=self.LIST_ALGORITHMS)
        self.combo_input.current(index)
        self.combo_input.place(relx=0.01, rely=0.01, relheight=0.09, relwidth=0.57)
        # -->Создание кнопки преобразования
        self.conversion_btn = tk.Button(self, text='Совершить преобразования', bg='silver', highlightbackground='black',
                                        bd=4, command=self.transformation)
        self.conversion_btn.place(relx=0.23, rely=0.89, relheight=0.1, relwidth=0.6)
        # -->Создание панели ввода матрицы
        self.text_input = tk.Text(self, bd=5, font=('Ariel', 18, 'bold'))
        self.text_input.place(relx=0.23, rely=0.14, relwidth=0.6, relheight=0.6)

        if working_with_storage.INDEX_DATA:
            try:
                id = working_with_storage.INDEX_DATA[-1]
                text = working_with_storage.select(id=id)[-3]
                self.canvas_text = self.text_input.insert("insert", text)
            except Exception as error:
                print(error)

        # -->Создание панелей ввода начального и конечного элемента
        self.start = tk.Entry(self, bd=5, font=('Ariel', 18, 'bold'))
        self.start.place(relx=0.23, rely=0.77, relwidth=0.14, relheight=0.1)
        self.end = tk.Entry(self, bd=5, font=('Ariel', 18, 'bold'))
        self.end.place(relx=0.69, rely=0.77, relwidth=0.14, relheight=0.1)
        # -->Создание название панелей
        self.label_matrics = tk.Label(self, text='Матрица:', font=('Ariel', 16, 'bold'),
                                      bg='#A4295B')
        self.label_matrics.place(relx=0.01, rely=0.14, relwidth=0.2, relheight=0.1)

        self.label_start =tk.Label(self, text='От:', font=('Ariel', 16, 'bold'),
                                      bg='#A4295B')
        self.label_start.place(relx=0.12, rely=0.77, relwidth=0.1, relheight=0.1)
        self.label_finish = tk.Label(self, text='До:', font=('Ariel', 16, 'bold'),
                                    bg='#A4295B')
        self.label_finish.place(relx=0.58, rely=0.77, relwidth=0.1, relheight=0.1)


    def transformation(self):
        try:
            text_0 = self.text_input.get('1.0', 'end-1c')
            matrix_retro = np.array([list(map(int, string.split())) for string in text_0.split('\n')])
            text_0 = ' ' + str(matrix_retro).replace('[', '').replace(']', '')

            start = self.start.get()
            end = self.end.get()
            if start == '':
                start = 0
            if end == '':
                end = None

            algo = Algorithms(matrix_retro, start, end)
            text = algo.choice(self.combo_input.get())

            # Строка ниже для проверки вводимых значениий:
            print(f'{Fore.BLUE}Записанное значение:')
            print([working_with_storage.select()[0] + 1, text_0, text, self.combo_input.get()])

            working_with_storage.insert([working_with_storage.select()[0] + 1, text_0, text, self.combo_input.get()])
            working_with_storage.INDEX_DATA.append(working_with_storage.select()[0])
            self.master.refresh()
        except ValueError as v_e:
            print(f'{Fore.RED}{Style.BRIGHT}Возникла ошибка в блоке "transformation": {v_e}!')
            messagebox.showerror("Ошибка вводимых значений",
                                 f"Скорее всего вводится недопустимый символ или забыт пробел между вводимыми "
                                 f"элементами, поэтому возгикает ошибка:\n{v_e}")
        except Exception as e:
            print(f'{Fore.RED}{Style.BRIGHT}Возникла ошибка в блоке "transformation": {e}!')
            messagebox.showerror("Ошибка", f"Что-то пошло не так!\nПроверти вводимые значения или "
                                           f"перезапустите приложение.")
        else:
            print(f'{Fore.GREEN}{Style.BRIGHT}Функция отработала без ошибок!')



class AddOutputFrame(AddInputFrame):
    LIST_METHODS = ['Быстрое построение', 'Красивое построение']

    def __init__(self, parent):
        super().__init__(parent)
        self['bg'] = '#82B22C'
        self['text'] = ' Панель вывода '
        self['font'] = ('Ubuntu', 16)
        self['bd'] = 5
        self.put_widgets()

    def put_widgets(self):
        # -->Создаём кнопки построения графа
        self.add_btn = tk.Button(self, text='Построить граф', bg='silver', bd=4,
                                 highlightbackground="lime",
                                 command=self.create_graph)
        self.add_btn.place(rely=0.89, relx=0.1, relheight=0.1, relwidth=0.35)
        # -->Создание блока вывода
        self.canvas_output = tk.Canvas(self, bd=5, bg='silver')
        self.canvas_output.place(relx=.05, rely=.14, relwidth=.9, relheight=.73)
        if working_with_storage.INDEX_DATA:
            try:
                id = working_with_storage.INDEX_DATA[-1]
                text = working_with_storage.select(id=id)[-2]
                self.canvas_text = self.canvas_output.create_text(255, 115, text=text, anchor="center",
                                            font=('Ariel Bold', 25), justify='center')
            except Exception as error:
                print(error)
        #-->Создаём скроллинг канваса
        self.scr_canvas = ttk.Scrollbar(self.canvas_output, command=self.canvas_output.yview)
        self.scr_canvas.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas_output.configure(yscrollcommand=self.scr_canvas.set)
        self.canvas_output.update_idletasks()
        self.canvas_output.config(scrollregion=self.canvas_output.bbox(tk.ALL))
        # -->Создаём кнопки удаления
        self.del_btn = tk.Button(self, text='Удалить', bg='silver', bd=4, highlightbackground="red",
                                 command=self.deliter)
        self.del_btn.place(rely=0.89, relx=0.55, relheight=0.1, relwidth=0.35)
        # -->Создаём виджет выбора
        self.combo_output = ttk.Combobox(self, values=AddOutputFrame.LIST_METHODS)
        self.combo_output.current(0)
        self.combo_output.place(relx=0.05, rely=0.01, relheight=0.09, relwidth=0.57)

    def deliter(self):
        try:
            working_with_storage.delit(working_with_storage.INDEX_DATA[-1])
            working_with_storage.INDEX_DATA = working_with_storage.INDEX_DATA[:-1]
            self.canvas_output.delete(tk.ALL)
            self.master.refresh()
        except IndexError as i:
            print(f'{Fore.RED}{Style.BRIGHT}Возникла ошибка в блоке "deliter": {i}!')
            messagebox.showerror("Ошибка выхода индекса за пределы ранга!",
                                 f"Скорее всего пытветесь удалить несуществующий элементами,"
                                 f" поэтому возгикает ошибка:\n{i}")
        else:
            print(f'{Fore.GREEN}{Style.BRIGHT}Удаление элемента прошло успешно!')

    def create_graph(self):
        self.window = tk.Tk()
        self.window.title(f' Построение графа: "{working_with_storage.select()[-1]}" ')
        self.window.geometry('600x600+150+90')
        self.window['bg'] = '#330570'
        self.window.resizable(width=False, height=False)

        try:
            text = self.canvas_output.itemcget(self.canvas_text, 'text').replace(' ', '')
            adjacency_matrix = np.array([[int(j) for j in i] for i in text.split('\n')])
            g = nx.from_numpy_array(adjacency_matrix)
            fig = plt.figure(figsize=(6, 6))
            pos = nx.spring_layout(g)
            nx.draw(g, pos, with_labels=True, node_color='#A52A2A', node_size=600, font_size=12, font_weight='bold',
                    edge_color='#474A51', width=3)
            fig.patch.set_facecolor('#AAF0D1')
            canvas_graph = FigureCanvasTkAgg(fig, master=self.window)
            canvas_graph.draw()
            canvas_graph.get_tk_widget().pack()
        except Exception as e:
            self.window.destroy()
            print(f'{Fore.RED}{Style.BRIGHT}Возникла ошибка в блоке "create_graph": {e}!')
            messagebox.showerror("Ошибка",f"Что-то пошло не так!\nПроверти вводимые значения!"
                                          f"\nНа вход должна подаваться матрица смежности.")
        else:
            print(f'{Fore.GREEN}{Style.BRIGHT}Граф построился успешно!')

        self.window.mainloop()

class AddTableFrame(tk.LabelFrame):

    def __init__(self, parent):
        super().__init__(parent)
        self.scr_bar = None
        self['bg'] = '#B1832A'
        self['text'] = ' Таблица сохранённых матриц смежности '
        self['font'] = ('Ubuntu', 16)
        self['bd'] = 5
        self.put_widgets()

    def put_widgets(self):
        # Создание таблицы для визуализации данных
        # -->Создание стиля таблицы
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Treeview',
                             background='silver',
                             foreground='black',
                             rowheight=25,
                             fieldbackground='silver')
        self.style.map('Treeview', background=[('selected', 'green')])
        self.style.configure('Treeview', rowheight=90)
        # -->Создание таблицы матриц
        heads = ['id', 'input', 'output', 'method']
        self.table = ttk.Treeview(self, show='headings', columns=heads)

        for header in heads:
            self.table.heading(header, text=header, anchor='center')
            self.table.column(header, anchor='center')

        for row in working_with_storage.select(all=True):
            self.table.insert('', tk.END, values=row)

        self.scr_bar = ttk.Scrollbar(self.table, orient='vertical', command=self.table.yview)
        self.scr_bar.pack(side=tk.RIGHT, fill=tk.Y, pady=7, padx=3, )
        self.table.configure(yscrollcommand=self.scr_bar.set)
        self.table.place(relx=0.01, rely=0.01, relheight=0.97, relwidth=0.98)

        #-->Взаимодействие со строками таблицы
        self.table.bind('<Double-1>', self.on_select)

    def on_select(self, event=None):
        item = self.table.focus()
        print(self.table.item(item)['values'])
        id = self.table.item(item)['values'][0]
        working_with_storage.INDEX_DATA.append(id)
        self.master.refresh()

