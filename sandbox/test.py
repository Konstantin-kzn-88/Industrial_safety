import tkinter as tk


def click_button():
    window.destroy()
    window2 = tk.Tk()
    window2.title("Дочернее окно")
    window2.geometry("300x300")


window = tk.Tk()
window.title("Основное окно")
window.geometry("300x300")

hello = tk.Label(text="Hello world!")
hello.pack()
button1 = tk.Button(text="Click me!", relief='solid', bd=0, background="#fff", command=click_button)

button1.pack()
tk.mainloop()