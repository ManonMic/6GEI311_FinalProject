from tkinter import *
from PIL import ImageTk
from PIL import Image
number = 1

def change_img():
    global number
    if number == 10:
        number = 0
    img = ImageTk.PhotoImage(Image.open(r"C:\Users\labop2\Desktop\images/img"+ str(number) +".jpg"))
    label.configure(image = img)
    label.image = img
    number = number + 1
    window.after(1000,change_img)



window = Tk()



img = ImageTk.PhotoImage(Image.open(r"C:\Users\labop2\Desktop\images/img0.jpg"))
label = Label(window, image= img)
label.pack()

window.after(1000,change_img)

window.mainloop()
