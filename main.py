from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import tkinter as tk
import random
import os
import shutil

class Window:
    def __init__(self, root):
        # Настройка окна
        root.title("Авторизация пользователя")  # устанавливаем заголовок окна
        root.geometry("600x470")  # устанавливаем размеры окна
        root.resizable(False, False)
        root.config(bg="#B2E1B9")

class Authorization(Window):
    def __init__(self, root):
        super().__init__(root)
        self.users_informations = None
        # Тексовые метки
        label1 = ttk.Label(
            text="Окно авторизации", font="Times 24", background="#48E9A5"
        )  # создаем текстовую метку
        label1.place(relx=0.300, rely=0.050)
        label2 = ttk.Label(text="Логин", font="Times 12", background="#48E9A5", width=7)
        label2.place(relx=0.280, rely=0.325)
        label3 = ttk.Label(
            text="Пароль", font="Times 12", background="#48E9A5", width=7
        )
        label3.place(relx=0.280, rely=0.375)

        # Поля ввода
        self.entry1 = ttk.Entry()
        self.entry1.place(relx=0.425, rely=0.325, width=200)
        self.entry2 = ttk.Entry()
        self.entry2.place(relx=0.425, rely=0.375, width=200)

        style = ttk.Style()
        style.map(
            "C.TButton",
            foreground=[("pressed", "red"), ("active", "blue")],
            background=[("pressed", "!disabled", "#48E9A5"), ("active", "white")],
        )
        button1 = CreateImage("fon.png", 120, 40, root, "Button")
        button1.get_object().configure(
            text="Подтвердить", compound=CENTER, command=self.button_clicked
        )
        button1.get_object().place(
            relx=0.400, rely=0.475, width=120, height=40
        )  # размещаем кнопку в окне

        label4 = ttk.Label(
            text="Впервые в приложении?", font="Times 12", background="#48E9A5", width=22
        )
        label4.place(relx=0.350, rely=0.675)
        button2 = CreateImage("fon.png", 140, 40, root, "Button")
        button2.get_object().configure(
            text="Зарегестрироваться", compound=CENTER, command=self.regestration
        )
        button2.get_object().place(
            relx=0.400, rely=0.725, width=120, height=40
        )

    def regestration(self):
        reg_window = Registration(root)

    def button_clicked(self):
        login = self.entry1.get()
        password = self.entry2.get()
        self.entry1.delete(0, END)
        self.entry2.delete(0, END)
        for user in Base:
            if (login == user[0]) and (password == user[1]):
                self.users_informations = user
                print(f"Вход успешно выполнен")
                global Event_base
                Event_base = r.read(f"{user[2]}/Event_base.txt", r.read_Event)
                self.MyFile = open(f"{user[2]}/Event_base.txt", "w", encoding="utf-8")
                window = WindowProfile(root,user[2])
                return None
            else:
                error = ttk.Label(
                    text="Неверный логин или пароль",
                    foreground="#FF0000",
                    background="#B2E1B9",
                    font="Times 12",
                )
                error.place(relx=0.350, rely=0.625)

    def __del__(self):
        print("Приложение закрыто")
        if self.users_informations != None:
            for element in Event_base:
                self.MyFile.write(element[0] + "|")
                self.MyFile.write(str(element[1]) + "|")
                self.MyFile.write(str(element[2]) + "|")
                self.MyFile.write(str(element[3]).replace("\n", "\\n") + "|")
                self.MyFile.write(str(element[4]).replace("\n", "\\n") + "|")
                self.MyFile.write(str(element[5]))
                self.MyFile.write("\n")
            self.MyFile.close()

class Registration(Window):
    def __init__(self, root):
        super().__init__(root)
        reg = Toplevel()
        reg.title("Окно регистрации")
        reg.geometry("600x470")
        reg.resizable(False, False)
        reg.protocol(
            "WM_DELETE_WINDOW", lambda: self.dismiss(reg)
        )  # перехватываем нажатие на крестик
        reg.config(bg="#B2E1B9")

        label1 = ttk.Label(reg, text="Укажите имя пользователя(логин)", font="Times 12", background="#48E9A5", width=30)
        label1.place(relx=0.050, rely=0.200)
        label2 = ttk.Label(reg, text="Придумайте пароль", font="Times 12", background="#48E9A5", width=17)
        label2.place(relx=0.220, rely=0.300)

        self.entry1 = ttk.Entry(reg)
        self.entry1.place(relx=0.480, rely=0.200, width=200)
        self.entry2 = ttk.Entry(reg)
        self.entry2.place(relx=0.480, rely=0.300, width=200)

        button2 = CreateImage("fon.png", 140, 40, reg, "Button")
        button2.get_object().configure(
            text="Подтвердить", compound=CENTER, command = lambda b=button2.get_object(): self.button_clicked(reg)
        )
        button2.get_object().place(
            relx=0.800, rely=0.725, width=100, height=100
        )
        reg.grab_set()  # захватываем пользовательский ввод



    def button_clicked(self, reg):
        login = self.entry1.get()
        password = self.entry2.get()
        for user in Base:
            if (login == user[0]) or (password == user[1]):
                error = ttk.Label(
                    reg,
                    text="Данный пользователь уже существует",
                    foreground="#FF0000",
                    background="#B2E1B9",
                    font="Times 20",
                )
                error.place(relx=0.15, rely=0.5)
                return None

        with open("Users_base.txt", "a", encoding="utf-8") as f:
            random_id = random.randint(100000, 999999)
            f.write(f"{login}|{password}|{random_id}|Введите имя|Введите фамилию\n")
            os.mkdir(f"{random_id}")
            shutil.copyfile("Event_base.txt", f"{random_id}/Event_base.txt")
            f.close()
            self.dismiss(reg)

    def dismiss(self, window):
        window.grab_release()
        window.destroy()

class CreateImage:
    def __init__(self, string_name, x, y, frame1, type_object):
        avatar_image = Image.open(string_name)
        avatar_image = avatar_image.resize((x, y))
        avatar_image = ImageTk.PhotoImage(avatar_image)
        if type_object == "Label":
            if frame1 != None:
                self.avatar = Label(frame1, image=avatar_image)
                self.avatar.configure(bg="#14AE5C")
            else:
                self.avatar = Label(image=avatar_image)
                self.avatar.configure(bg="#14AE5C")
        elif type_object == "Button":
            self.avatar = Button(frame1, image=avatar_image, highlightthickness=0, bd=0)
            self.avatar.configure(bg="#B2E1B9", activebackground="#B2E1B9")

        self.avatar.image = avatar_image

    def get_object(self):
        return self.avatar

class CreateFrame:
    def __init__(self, notebook, text_frame):
        self.frame = tk.Frame(notebook)

        notebook.add(self.frame, text=text_frame)

    def get_object(self):
        return self.frame

class WindowProfile(Window, tk.Toplevel):
    def __init__(self, root, id):
        super().__init__(root)
        root.title("Личный кабинет")

        notebook = ttk.Notebook(root)
        notebook.pack(expand=True, fill=BOTH)

        frame1 = CreateFrame(notebook, "Мой кабинет")
        frame2 = CreateFrame(notebook, "Доска предложений")
        frame3 = CreateFrame(notebook, "Расписание")
        frame4 = CreateFrame(notebook, "+")

        my_account = MyAccount(frame1, id)
        board = Board(frame2, "board", Event_base)
        timetable = Board(frame3, "timetable", Timetable_base)
        addition = Addition(frame4)

class MyAccount:
    def __init__(self, frame1, id):
        fon1 = ttk.Label(frame1.get_object(), background="#B2E1B9")
        fon1.place(relheight=1.1, relwidth=1, relx=0.0, rely=0.0)
        label1 = ttk.Label(
            frame1.get_object(),
            text="Мои данные",
            font="Times 16",
            background="#48E9A5",
            width=25,
        )
        label1.place(relx=0.02, rely=0.03)

        fon_of_picture = CreateImage("fon.png", 239, 290, frame1.get_object(), "Label")
        fon_of_picture.get_object().configure(bg="#B2E1B9", border=0)
        fon_of_picture.get_object().place(
            relx=0.02, rely=0.13, relwidth=0.34, relheight=0.56
        )

        image_user = CreateImage("avatar.png", 250, 250, frame1.get_object(), "Label")
        image_user.get_object().place(
            relx=0.04, rely=0.16, relwidth=0.30, relheight=0.50
        )

        label2 = ttk.Label(
            frame1.get_object(),
            text=self.get_inf(id)[3],
            font="Times 14",
            background="#48E9A5",
            width=20,
        )
        label2.place(relx=0.42, rely=0.23)

        label3 = ttk.Label(
            frame1.get_object(),
            text=self.get_inf(id)[4],
            font="Times 14",
            background="#48E9A5",
            width=20,
        )
        label3.place(relx=0.42, rely=0.40)

        label4 = ttk.Label(
            frame1.get_object(),
            text=self.get_inf(id)[2],
            font="Times 14",
            background="#48E9A5",
            width=20,
        )
        label4.place(relx=0.42, rely=0.57)



        button2 = CreateImage("icon.png", 40, 40, frame1.get_object(), "Button")
        button2.get_object().place(relx=0.90, rely=0.21)
        button2.get_object().configure(
            command=lambda b=button2.get_object(): self.replace(
                frame1, label2, 0.42, 0.23, 20, id
            )
        )

        button3 = CreateImage("icon.png", 40, 40, frame1.get_object(), "Button")
        button3.get_object().place(relx=0.90, rely=0.38)
        button3.get_object().configure(
            command=lambda b=button3.get_object(): self.replace_surname(
                frame1, label3, 0.42, 0.40, 20, id
            )
        )

        icon_button = CreateImage("chat.png", 40, 40, None, "Button")
        icon_button.get_object().place(relx=0.90, rely=0.90)
        icon_button.get_object().configure(command=self.information)

    def dismiss(self, window):
        window.grab_release()
        window.destroy()

    def information(self):
        window = Toplevel()
        window.title("Обратная связь")
        window.geometry("600x470")
        window.resizable(False, False)
        window.protocol(
            "WM_DELETE_WINDOW", lambda: self.dismiss(window)
        )  # перехватываем нажатие на крестик
        window.config(bg="#B2E1B9")

        text_inf = ttk.Label(
            window,
            text="Если у вас есть предложения или жалобы,\n           вы можете связаться с нами:\n",
            font="Times 16",
            background="#B2E1B9",
            width=35,
            anchor=CENTER
        )
        text_inf.place(relx=0.18, rely=0.16)
        label1 = ttk.Label(
            window,
            text="Руководитель проекта:       ivanov.valek@dvfu.ru",
            font="Times 16",
            background="#B2E1B9",
            width=43
        )
        label1.place(relx=0.05, rely=0.33)
        label2 = ttk.Label(
            window,
            text="Дизайнер:                              makhonov.gol@dvfu.ru",
            font="Times 16",
            background="#B2E1B9",
            width=43
        )
        label2.place(relx=0.05, rely=0.43)
        label3 = ttk.Label(
            window,
            text="Frontend-разработка:           starovoitov.ava@dvfu.ru",
            font="Times 16",
            background="#B2E1B9",
            width=43
        )
        label3.place(relx=0.05, rely=0.53)
        label4 = ttk.Label(
            window,
            text="Автор идеи:                          pustynskii.id@dvfu.ru",
            font="Times 16",
            background="#B2E1B9",
            width=43
        )
        label4.place(relx=0.05, rely=0.63)
        window.grab_set()  # захватываем пользовательский ввод

    def replace(self, frame, label, x, y, w, id):

        label.destroy()
        entry1 = ttk.Entry(frame.get_object())
        entry1.place(relx=x, rely=y + 0.04, width=180)
        for widget in frame.get_object().winfo_children():
            if isinstance(widget, Button):
                if (widget.cget('image') != "pyimage5") and (widget.cget('image') != "pyimage6"):
                    widget.destroy()
                widget.place(relx=2)


        save_button = CreateImage("save.png", 160, 70, frame.get_object(), "Button")
        save_button.get_object().place(relx=0.05, rely=0.7)
        save_button.get_object().configure(
            command=lambda b=save_button.get_object(): self.save(
                frame, entry1, save_button, x, y, w, id, "name"
            )
        )

    def replace_surname(self, frame, label, x, y, w, id):
        label.destroy()
        entry_surname = ttk.Entry(frame.get_object())
        entry_surname.place(relx=x, rely=y + 0.04, width=180)
        for widget in frame.get_object().winfo_children():
            if isinstance(widget, Button) :
                if (widget.cget('image') != "pyimage5") and (widget.cget('image') != "pyimage6"):
                    widget.destroy()
                widget.place(relx = 2)

        save_button = CreateImage("save.png", 160, 70, frame.get_object(), "Button")
        save_button.get_object().place(relx=0.05, rely=0.7)
        save_button.get_object().configure(
            command=lambda b=save_button.get_object(): self.save(
                frame, entry_surname, save_button, x, y, w, id, "surname"
            )

        )

    def save(self, frame, entry, button, x, y, w, id, flag):




        button.get_object().destroy()
        for widget in frame.get_object().winfo_children():
            if isinstance(widget, Button) :
                widget.place(relx = 0.9)


        label2 = ttk.Label(
            frame.get_object(),
            text=entry.get(),
            font="Times 14",
            background="#48E9A5",
            width=w,
        )

        if flag == "name":
            new_data = str()
            for user in Base:
                if id == user[2]:
                    user[3] = entry.get()
                new_data += "|".join(user) + "\n"




        elif flag == "surname":
            new_data = str()
            for user in Base:
                if id == user[2]:
                    user[4] = entry.get()
                new_data += "|".join(user) + "\n"

        label2.place(relx=x, rely=y)
        entry.destroy()


        with open('Users_base.txt', 'w', encoding="utf-8") as f:
            f.write(new_data)
            f.close()


    def get_inf(self,id):
        for user in Base:
            if id == user[2]:
                return user

class Event:
    def __init__(self, frame2, count):
        label1 = ttk.Label(
            frame2.get_object(),
            text=Event_base[count][0],
            anchor=CENTER,
            font="Times 16",
            background="#48E9A5",
            width=40,
        )
        label1.place(relx=0.12, rely=0.05)

        image_user = CreateImage(
            Event_base[count][2], 140, 140, frame2.get_object(), "Label"
        )
        image_user.get_object().configure(bg="#B2E1B9")
        image_user.get_object().place(relx=0.62, rely=0.15)

        label2 = ttk.Label(
            frame2.get_object(),
            text=Event_base[count][4],
            anchor=CENTER,
            font="Times 16",
            background="#48E9A5",
            width=16,
        )
        label2.place(relx=0.59, rely=0.53)

        label3 = ttk.Label(
            frame2.get_object(),
            text=Event_base[count][3],
            font="Times 16",
            background="#48E9A5",
            width=16,
        )
        label3.place(relx=0.12, rely=0.16, relwidth=0.42, relheight=0.78)

        if Event_base[count][5]:
            button1 = CreateImage("like.png", 40, 40, frame2.get_object(), "Button")
            button1.get_object().place(relx=0.6, rely=0.78)
            button1.get_object().configure(
                command=lambda b=button1.get_object(): self.like(count, label4, button1)
            )

        label4 = ttk.Label(
            frame2.get_object(),
            text=f"Голосов: {Event_base[count][1]}",
            font="Times 16",
            background="#48E9A5",
            width=10,
        )
        label4.place(relx=0.7, rely=0.8)

    def like(self, count, label, button1):
        Event_base[count][1] += 1
        Event_base[count][5] = False
        button1.get_object().destroy()
        label.configure(text=f"Голосов: {Event_base[count][1]}")

class TimetableEvent:
    def __init__(self, frame2, count):
        label1 = ttk.Label(
            frame2.get_object(),
            text=Timetable_base[count][0],
            anchor=CENTER,
            font="Times 16",
            background="#48E9A5",
            width=40,
        )
        label1.place(relx=0.12, rely=0.05)

        image_user = CreateImage(
            Timetable_base[count][2], 150, 150, frame2.get_object(), "Label"
        )
        image_user.get_object().configure(bg="#B2E1B9")
        image_user.get_object().place(relx=0.12, rely=0.2)

        label2 = ttk.Label(
            frame2.get_object(),
            text=Timetable_base[count][4],
            anchor=CENTER,
            font="Times 16",
            background="#48E9A5",
            width=16,
        )
        label2.place(relx=0.11, rely=0.6)

        label3 = ttk.Label(
            frame2.get_object(),
            text=Timetable_base[count][3],
            font="Times 16",
            background="#48E9A5",
            width=16,
        )
        label3.place(relx=0.48, rely=0.16, relwidth=0.4, relheight=0.6)

        label4 = ttk.Label(
            frame2.get_object(),
            text=Timetable_base[count][1],
            anchor=CENTER,
            font="Times 16",
            background="#48E9A5",
            width=24,
        )
        label4.place(relx=0.03, rely=0.8)

        label5 = ttk.Label(
            frame2.get_object(),
            text=Timetable_base[count][5],
            anchor=CENTER,
            font="Times 16",
            background="#48E9A5",
            width=24,
        )
        label5.place(relx=0.53, rely=0.8)

class Board:
    def __init__(self, frame2, flag, base):
        fon1 = ttk.Label(frame2.get_object(), background="#B2E1B9")
        fon1.place(relheight=1.1, relwidth=1, relx=0.0, rely=0.0)

        global count_event
        count_event = int(0)

        global timetable_count
        timetable_count = int(0)

        button1 = CreateImage("left.png", 40, 40, frame2.get_object(), "Button")
        button1.get_object().place(relx=0.02, rely=0.45)
        button1.get_object().configure(
            command=lambda b=button1.get_object(): self.minus(frame2, len(base), flag)
        )

        button2 = CreateImage("right.png", 40, 40, frame2.get_object(), "Button")
        button2.get_object().place(relx=0.92, rely=0.45)
        button2.get_object().configure(
            command=lambda b=button2.get_object(): self.plus(frame2, len(base), flag)
        )

        if flag == "board":
            frame_event = Event(frame2, count_event)
        if flag == "timetable":
            frame_timetable = TimetableEvent(frame2, timetable_count)

    def plus(self, frame2, max, flag):
        if flag == "board":
            global count_event
            if count_event < (max - 1):
                count_event += 1
            else:
                count_event = 0
            for widget in frame2.get_object().winfo_children():
                if (
                        str(widget) == ".!notebook.!frame2.!label"
                        or str(widget) == ".!notebook.!frame2.!button"
                        or str(widget) == ".!notebook.!frame2.!button2"
                ):
                    pass
                else:
                    widget.destroy()
            frame_event = Event(frame2, count_event)
        elif flag == "timetable":
            global timetable_count
            if timetable_count < (max - 1):
                timetable_count += 1
            else:
                timetable_count = 0
            for widget in frame2.get_object().winfo_children():
                if (
                        str(widget) == ".!notebook.!frame3.!label"
                        or str(widget) == ".!notebook.!frame3.!button"
                        or str(widget) == ".!notebook.!frame3.!button2"
                ):
                    pass
                else:
                    widget.destroy()
            frame_timetable = TimetableEvent(frame2, timetable_count)

    def minus(self, frame2, max, flag):
        if flag == "board":
            global count_event
            if count_event > 0:
                count_event -= 1
            else:
                count_event = max - 1
            for widget in frame2.get_object().winfo_children():
                if (
                        str(widget) == ".!notebook.!frame2.!label"
                        or str(widget) == ".!notebook.!frame2.!button"
                        or str(widget) == ".!notebook.!frame2.!button2"
                ):
                    pass
                else:
                    widget.destroy()
            frame_event = Event(frame2, count_event)
        elif flag == "timetable":
            global timetable_count
            if timetable_count > 0:
                timetable_count -= 1
            else:
                timetable_count = max - 1
            for widget in frame2.get_object().winfo_children():
                if (
                        str(widget) == ".!notebook.!frame3.!label"
                        or str(widget) == ".!notebook.!frame3.!button"
                        or str(widget) == ".!notebook.!frame3.!button2"
                ):
                    pass
                else:
                    widget.destroy()
            frame_timetable = TimetableEvent(frame2, timetable_count)

class Addition:
    def __init__(self, frame4):
        fon1 = ttk.Label(frame4.get_object(), background="#B2E1B9")
        fon1.place(relheight=1.0, relwidth=1.0, relx=0.0, rely=0.0)

        label1 = ttk.Label(
            frame4.get_object(),
            text="Предложить мероприятие",
            anchor=CENTER,
            font="Times 16",
            background="#48E9A5",
            width=25,
        )
        label1.place(relx=0.03, rely=0.05)

        input1_button = CreateImage("input1.png", 200, 40, frame4.get_object(), "Button")
        input1_button.get_object().place(relx=0.03, rely=0.25)
        input1_button.get_object().configure(
            command=lambda b=input1_button.get_object(): self.input_(
                frame4, input1_button.get_object(), 0.03, 0.25, 200
            )
        )

        input2_button = CreateImage("input2.png", 154, 40, frame4.get_object(), "Button")
        input2_button.get_object().place(relx=0.4, rely=0.25)
        input2_button.get_object().configure(
            command=lambda b=input2_button.get_object(): self.input_(
                frame4, input2_button.get_object(), 0.4, 0.25, 154
            )
        )

        input3_button = CreateImage("description.png", 500, 200, frame4.get_object(), "Button")
        input3_button.get_object().place(relx=0.01, rely=0.35)
        input3_button.get_object().configure(
            command=lambda b=input3_button.get_object(): self.input_(
                frame4, input3_button.get_object(), 0.025, 0.55, 500
            )
        )

        label2 = ttk.Label(
            frame4.get_object(),
            text="Прикрепите баннер вашего мероприятия",
            anchor=CENTER,
            font="Times 12",
            background="#48E9A5",
            width=40,
        )
        label2.place(relx=0.030, rely=0.800)

        image_user = CreateImage(
            "name.png", 30, 30, frame4.get_object(), "Label"
        )
        image_user.get_object().configure(bg="#B2E1B9")
        image_user.get_object().place(relx=0.60, rely=0.790)

        button = CreateImage("fon.png", 100, 30, frame4.get_object(), "Button")
        button.get_object().configure(
            text="Сохранить", compound=CENTER,
            command=lambda b=button.get_object(): self.button_clicked(frame4)

        )
        button.get_object().place(
            relx=0.800, rely=0.725, width=100, height=100
        )

    def button_clicked(self,frame):
        addition = Addition(frame)
        return

    def input_(self, frame, label, x, y, w):
        label.destroy()
        entry1 = ttk.Entry(frame.get_object())
        entry1.place(relx=x, rely=y + 0.04, width=w)


class Reader:
    def __init__(self):
        pass

    def read(self, fileName, callback):
        with open(fileName, "r", encoding="utf-8") as f:
            self.lines = f.readlines()
        for i in range(0, len(self.lines)):
            self.lines[i] = self.lines[i].split("|")
            callback(i)
        return self.lines

    def read_User(self, i):
        self.lines[i][4] = self.lines[i][4][:-1]

    def read_Event(self,i):
        self.lines[i][1] = int(self.lines[i][1])
        self.lines[i][3] = str(self.lines[i][3]).replace("\\n", "\n")
        self.lines[i][4] = str(self.lines[i][4]).replace("\\n", "\n")
        if self.lines[i][5][:-1] == "False":
            self.lines[i][5] = False
        else:
            self.lines[i][5] = True

    def read_Timetable(self,i):
        self.lines[i][3] = str(self.lines[i][3]).replace("\\n", "\n")
        self.lines[i][4] = str(self.lines[i][4]).replace("\\n", "\n")
        self.lines[i][5] = self.lines[i][5][:-1]


if __name__ == "__main__":
    r = Reader()

    Timetable_base = r.read("Timetable_base.txt", r.read_Timetable)
    Base = r.read("Users_base.txt", r.read_User)



    root = tk.Tk()  # создаем корневой объект - окно
    authorization = Authorization(root)
    root.mainloop()
