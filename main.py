from tkinter import *
import csv
import pandas as pd
import random
import time
from tkinter import messagebox

BACKGROUND_COLOR = "#B1DDC6"
data=pd.read_csv("data/french_words.csv")
to_dict=data.to_dict(orient="records")
current_card=list(to_dict)[0]
flip_timer=1

try:
    data=pd.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data=pd.read_csv("data/french_words.csv")
    to_dict=original_data.to_dict(orient="records")
else:
    to_learn=data.to_dict(orient="records")

#-------------------------------- SHOW NEW CARD --------------------------------------#


def generate_word():
    global current_card,flip_timer
    window.after_cancel(flip_timer)
    if len(to_dict)!=0:
        current_card=random.choice(to_dict)
        canvas.itemconfig(card_title,text="French",fill="black")
        canvas.itemconfig(card_word,text=current_card["French"],fill="black")
        flip_timer=window.after(3000,func=flipcard)
    else:
        is_known()


def flipcard():
    canvas.itemconfig(card_title,text="English",fill="white")
    canvas.itemconfig(card_word,text=current_card["English"],fill="white")   
    canvas.itemconfig(card_background,image=card_back)

#-------------------------------- REMOVING A CARD --------------------------------------#


def is_known():
    global current_card
    global data, to_dict

    if current_card in to_dict:
        to_dict.remove(current_card)
        data=pd.DataFrame(to_dict)
        data.to_csv("data/removed_words.txt",index=False)
        generate_word()
    else:
        canvas.itemconfig(card_title,text="Congratulations!",font=("Ariel",30,"italic"))
        canvas.itemconfig(card_word,text="All done!",font=("Ariel",30,"bold"))
        next=messagebox.askyesno(title="What's next?",message="Do you want to restart the deck?")
        if next:
            data=pd.read_csv("data/french_words.csv")
            to_dict=data.to_dict(orient="records")
            generate_word()
        else:
            window.destroy()


#---------------------------------- UI ----------------------------------------#

window=Tk()
window.title("Flashcards")
window.config(padx=50,pady=50,bg=BACKGROUND_COLOR)

card_back=PhotoImage(file="images/card_back.png")
card_front=PhotoImage(file="images/card_front.png")
canvas=Canvas(height=526,width=800)
card_background=canvas.create_image(400,263,image=card_front)
card_title=canvas.create_text(400,150,text="",font=("Ariel",40,"italic"))
card_word=canvas.create_text(400,263,text="Flashcards",font=("Ariel",60,"bold"))
canvas.config(bg=BACKGROUND_COLOR,highlightthickness=0)
canvas.grid(column=0,row=0,columnspan=2)

right_button=Button(text="✔️ GOOD", command=is_known, font=("Ariel",18,"bold"))
right_button.grid(column=1,row=1)
wrong=Button(text="✖️ AGAIN", command=generate_word, font=("Ariel",18,"bold"))
wrong.grid(column=0,row=1)

generate_word()

window.mainloop()
