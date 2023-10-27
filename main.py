import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

# Создание базы данных и таблицы
conn = sqlite3.connect('employees.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    full_name TEXT,
                    phone_number TEXT,
                    email_address TEXT,
                    salary REAL)''')
conn.commit()

# Функция для добавления нового сотрудника
def add_employee():
    full_name = entry_full_name.get()
    phone_number = entry_phone_number.get()
    email_address = entry_email_address.get()
    salary = entry_salary.get()

    if full_name and phone_number and email_address and salary:
        cursor.execute('''INSERT INTO employees (full_name, phone_number, email_address, salary)
                          VALUES (?, ?, ?, ?)''', (full_name, phone_number, email_address, salary))
        conn.commit()
        messagebox.showinfo('Успешно!', 'Новый сотрудник добавлен!')
        clear_entries()
        display_employees()
    else:
        messagebox.showerror('Ошибка!', 'Пожалуйста, заполните все поля!')

# Функция для изменения данных сотрудника
def update_employee():
    selected_item = tree.selection()
    if selected_item:
        id = tree.item(selected_item)['values'][0]
        full_name = entry_full_name.get()
        phone_number = entry_phone_number.get()
        email_address = entry_email_address.get()
        salary = entry_salary.get()

        if full_name and phone_number and email_address and salary:
            cursor.execute('''UPDATE employees SET full_name=?, phone_number=?, email_address=?, salary=?
                              WHERE id=?''', (full_name, phone_number, email_address, salary, id))
            conn.commit()
            messagebox.showinfo('Успешно!', 'Список сотрудников обновлен!')
            clear_entries()
            display_employees()
        else:
            messagebox.showerror('Ошибка!', 'Пожалуйста, заполните все поля!')
    else:
        messagebox.showerror('Ошибка!', 'Выберите сотрудника!')

# Функция для удаления сотрудника
def delete_employee():
    selected_item = tree.selection()
    if selected_item:
        result = messagebox.askquestion('Подтвердите!', 'Вы действительно хотите удалить этого сотрудника?')
        if result == 'yes':
            id = tree.item(selected_item)['values'][0]
            cursor.execute('DELETE FROM employees WHERE id=?', (id,))
            conn.commit()
            messagebox.showinfo('Успешно!', 'Сотрудник удален из списка!')
            clear_entries()
            display_employees()
    else:
        messagebox.showerror('Ошибка!', 'Пожалуйста, выберите сотрудника!')

# Функция для поиска сотрудника по ФИО
def search_employee():
    search_text = entry_search.get()
    cursor.execute("SELECT * FROM employees WHERE full_name LIKE ?", ('%' + search_text + '%',))
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)

# Функция для очистки полей ввода
def clear_entries():
    entry_full_name.delete(0, END)
    entry_phone_number.delete(0, END)
    entry_email_address.delete(0, END)
    entry_salary.delete(0, END)

# Функция для отображения списка сотрудников
def display_employees():
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    tree.delete(*tree.get_children())
    for row in rows:
        tree.insert('', 'end', values=row)

# Создание графического интерфейса
root = Tk()
root.title('Список сотрудников ')
root.iconbitmap("icon2.ico")




# Создание и размещение элементов интерфейса
label_full_name = Label(root, text='Полное имя (ФИО)')
label_full_name.grid(row=0, column=0)
entry_full_name = Entry(root, bg="DarkGray")
entry_full_name.grid(row=0, column=1)

label_phone_number = Label(root, text='Номер телефона')
label_phone_number.grid(row=1, column=0)
entry_phone_number = Entry(root, bg="DarkGray")
entry_phone_number.grid(row=1, column=1)

label_email_address = Label(root, text='Электронная почта')
label_email_address.grid(row=2, column=0)
entry_email_address = Entry(root, bg="DarkGray")
entry_email_address.grid(row=2, column=1)

label_salary = Label(root, text='Заработная плата')
label_salary.grid(row=3, column=0)
entry_salary = Entry(root, bg="DarkGray")
entry_salary.grid(row=3, column=1)

button_add = Button(root, text='Добавить сотрудника', command=add_employee, bg="DarkGray")
button_add.grid(row=4, column=0)

button_update = Button(root, text='Обновить сотрудников', command=update_employee, bg="DarkGray")
button_update.grid(row=4, column=1)

button_delete = Button(root, text='Удалить сотрудника', command=delete_employee, bg="DarkGray")
button_delete.grid(row=4, column=2)

label_search = Label(root, text='Поиск по полному имени')
label_search.grid(row=5, column=0)
entry_search = Entry(root, bg="DarkGray")
entry_search.grid(row=5, column=1)
button_search = Button(root, text='Поиск', command=search_employee, bg="DarkGray")
button_search.grid(row=5, column=2)


tree = ttk.Treeview(root, columns=('ID', 'Full Name', 'Phone Number', 'Email Address', 'Salary'), show='headings')
tree.heading('ID', text='ID')
tree.heading('Full Name', text='Полное имя')
tree.heading('Phone Number', text='Номер телефона')
tree.heading('Email Address', text='Электронная почта')
tree.heading('Salary', text='Заработная плата')
tree.grid(row=6, column=0, columnspan=3)

# Отображение списка сотрудников при запуске приложения
display_employees()

root.resizable (width=False, height=False)
root.mainloop()

# Закрытие соединения с базой данных
conn.close()