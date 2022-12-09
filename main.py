from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/japanese_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def remove_card():
    to_learn.remove(current_card)
    next_card()  # allows me to use next card function. Go over this

    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)  # does not include index


# ---------------------------- FLIP CARD------------------------------- #
def flip_card():
    canvas.itemconfig(card, image=back_card_image)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["english"], fill="white")


# ---------------------------- RANDOM WORD------------------------------- #
def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card, image=front_card_image)
    canvas.itemconfig(card_title, text="Japanese", fill="black")
    canvas.itemconfig(card_word, text=current_card["japanese"], fill="black")
    flip_timer = window.after(3000, func=flip_card)  # sets a  new flip timer to reset


# ---------------------------- UI SETUP------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)
back_card_image = PhotoImage(file="images/card_back.png")
front_card_image = PhotoImage(file="images/card_front.png")
canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 265, image=front_card_image)  # x and y cord
card_title = canvas.create_text(400, 150, text="", fill="black", font="Arial 40 italic")
card_word = canvas.create_text(400, 263, text="", fill="black",
                               font='Arial 60 bold')
canvas.grid(column=0, row=0, columnspan=2)

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, highlightbackground=BACKGROUND_COLOR,
                      command=remove_card)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0, highlightbackground=BACKGROUND_COLOR,
                      command=next_card)
wrong_button.grid(column=0, row=1)

next_card()  # generates a random word at the start of program


window.mainloop()
