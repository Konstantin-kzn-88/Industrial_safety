from tkinter import *


Weh = 1000
Hen = 400
Speed_Pad = 3
Speed_Pad_R = Speed_Pad
Speed_Pad_L = Speed_Pad

class Ball(Canvas):
    def __init__(self):
        Canvas.__init__(self, width=Weh, height=Hen, bg="Black")
        self.focus()
        #self.bind_all("<Key>", self.Move_Pad)
        self.Move_PAD()
        self.Loeder()
        self.mine_Oval()
        self.pack()

    def Loeder(self):
        self.create_oval(Weh / 2 - 10, Hen / 2 - 10, Weh / 2 + 10, Hen / 2 + 10, fill="white", tag="Oval")
        self.create_line(990, 300, 990, 200, fill="white", width=20, tag="Plr1")
        self.create_line(10, 100, 10, 10, fill="white", width=20, tag="Plr2")

    def Move_Oval(self):
        self.move("Oval", 10, 10)


    def Move_PAD(self):
        global Speed_Pad_R, Speed_Pad_L
        Pad = {'Plr1': Speed_Pad_R,
        'Plr2': Speed_Pad_L}
        for p in Pad:
            self.move(p, 0,Pad[p])

        if self.coords(p)[1] > 0:
            self.move(p, 0, -self.coords(p)[1])



    def Move_Pad(self, event):

        if event.keysym == "Up":
            self.move("Plr1", 0, -Speed_Pad_R)
        elif event.keysym == "Down":
            self.move("Plr1", 0, Speed_Pad_R)
        if event.char == "w":
            self.move("Plr2", 0, -Speed_Pad_L)
        elif event.char == "s":
            self.move("Plr2", 0, Speed_Pad_L)

    def mine_Oval(self):
        self.Move_Oval()
        #self.Move_Pad
        self.Move_PAD()
        self.after(30, self.mine_Oval)



def Strat():
    root.board = Ball()




root = Tk()
root.geometry("1000x400")


Strat()
root.mainloop()