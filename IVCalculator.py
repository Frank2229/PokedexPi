from tkinter import *
from PIL import ImageTk

# Window Setup
root = Tk()
root.title("IV Calculator")
root.geometry("480x320")
#root.attributes("-fullscreen", True)

# Background Image
backgroundImage = PhotoImage(file = "MenuBackground.png")
backgroundLabel = Label(root, image = backgroundImage)
backgroundLabel.place(relx = 0.5, rely = 0.5, anchor = "center")

# Initialize EV Variables
evValues = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
for value in evValues:
    value.set(0)

# Initialize IV Variables
ivValues = [IntVar(), IntVar(), IntVar(), IntVar(), IntVar(), IntVar()]
for value in ivValues:
    value.set(0)

ivLabels = Label(backgroundLabel)
ivLabels.place(relx=0.91, rely=0.568, anchor="center")
# Create a label for the number, without any background (to make it "invisible")
label1 = Label(ivLabels, textvariable=ivValues[0], font=("Arial", 20), fg="white", text="Transparent Text", bg=root['bg'])
label1.place(anchor="center")
label1.pack(side = "top", pady=4)
label2 = Label(ivLabels, textvariable=ivValues[1], font=("Arial", 20), fg="white", text="Transparent Text", bg=root['bg'])
label2.place(relx=0.5, rely=0.5, anchor="center")
label2.pack(side = "top", pady=4)
label3 = Label(ivLabels, textvariable=ivValues[2], font=("Arial", 20), fg="white", text="Transparent Text", bg=root['bg'])
label3.place(relx=0.5, rely=0.5, anchor="center")
label3.pack(side = "top", pady=4)
label4 = Label(ivLabels, textvariable=ivValues[3], font=("Arial", 20), fg="white", text="Transparent Text", bg=root['bg'])
label4.place(relx=0.5, rely=0.5, anchor="center")
label4.pack(side = "top", pady=4)
label5 = Label(ivLabels, textvariable=ivValues[4], font=("Arial", 20), fg="white", text="Transparent Text", bg=root['bg'])
label5.place(relx=0.5, rely=0.5, anchor="center")
label5.pack(side = "top", pady=4)
label6 = Label(ivLabels, textvariable=ivValues[5], font=("Arial", 20), fg="white", text="Transparent Text", bg=root['bg'])
label6.place(relx=0.5, rely=0.5, anchor="center")
label6.pack(side = "top", pady=4)

root.mainloop()
