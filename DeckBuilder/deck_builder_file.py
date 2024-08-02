from deck_file import *
import tkinter as tk

deck = deck_class("deckOne")
global basic_lands
basic_lands = ["forest", "island", "mountain", "swamp", "plains", "wastes"]

def get_input():
    input = str(input_entry.get())
    if deck.check_card(input) == True:
        card_type = deck.get_type(input)
        print_card(input, card_type)
        if "Basic Land" in card_type:
            if not deck.in_deck(input):
                card_name = "Basic " + input + " X 1"
                output_land.config(state="normal")
                output_land.insert(tk.END, "\n")
                output_land.insert(tk.END, card_name)
                deck.add_card(input)
            else:
                last = ""
                deck.add_card(input)
                card_count = deck.count_card(input)
                card_name = "Basic " + input + " X " + str((card_count-1))
                find_and_delete_word(output_land, card_name)
                card_name = "Basic " + input + " X " + str(card_count)
                deck_list = deck.get_deck_list()
                field_text = output_land.get("1.0", tk.END)
                output_land.delete("1.0", tk.END)
                if deck_list[-2] != ("forest" or "island" or "mountain" or "swamp" or "plains" or "wastes") and last != input:
                    output_land.insert(tk.END, "\n")
                output_land.config(state="normal")
                output_land.insert(tk.END, card_name)
                output_land.insert(tk.END, field_text)
                last = input
        elif not deck.in_deck(input):
            deck.add_card(input)
   

def print_card(card, card_type):
    if not deck.in_deck(card):
        if "Creature" in card_type:
            output_creature.config(state="normal")
            output_creature.insert(tk.END, "\n")
            output_creature.insert(tk.END, card)
        elif "Artifact" in card_type:
            output_artifact.config(state="normal")
            output_artifact.insert(tk.END, "\n")
            output_artifact.insert(tk.END, card)
        elif "Enchantment" in card_type:
            output_enchantment.config(state="normal")
            output_enchantment.insert(tk.END, "\n")
            output_enchantment.insert(tk.END, card)
        elif "Planeswalker" in card_type:
            output_planeswalker.config(state="normal")
            output_planeswalker.insert(tk.END, "\n")
            output_planeswalker.insert(tk.END, card)
        elif "Instant" in card_type:
            output_instant.config(state="normal")
            output_instant.insert(tk.END, "\n")
            output_instant.insert(tk.END, card)
        elif "Sorcery" in card_type:
            output_sorcery.config(state="normal")
            output_sorcery.insert(tk.END, "\n")
            output_sorcery.insert(tk.END, card)
        elif "Land" in card_type and not "Basic Land" in card_type:
            output_land.config(state="normal")
            output_land.insert(tk.END, "\n")
            output_land.insert(tk.END, card)
    else:
        print("This card is already in the deck")  

def find_and_delete_word(text_widget, word):
    start = '1.0'
    while True:
        pos = text_widget.search(word, start, stopindex=tk.END)
        if not pos:
            break
        end_pos = f"{pos}+{len(word)}c"
        text_widget.delete(pos, end_pos)
        start = pos

#would prefer to pass widget as a variable, but tkinter does not allow this (see line 176)
def find_and_delete_word_in_all_widgets(word):
    text_widgets = [output_land, output_artifact, output_enchantment, output_planeswalker, 
                    output_instant, output_sorcery, output_creature]
    for widget in text_widgets:
        find_and_delete_word(widget, word)

def delete_card():
    card = str(input_entry.get())
    if card in basic_lands:
        deck.delete_card(card)
        card_count = deck.count_card(card)
        if card_count == 0:
            card_name = "Basic " + card + " X " + str((card_count+1))
            find_and_delete_word(output_land, card_name)
            return
        card_name = "Basic " + card + " X " + str(card_count+1)
        find_and_delete_word(output_land, card_name)
        field_text = output_land.get("1.0", tk.END)
        find_and_delete_word(output_land, card_name)
        output_land.delete("1.0", tk.END)
        output_land.insert(tk.END, "\n")
        output_land.config(state="normal")
        output_land.insert(tk.END, card_name)
        output_land.insert(tk.END, field_text)

        
    elif deck.check_card(card) == True:
        tempstr = "\n" + card
        find_and_delete_word_in_all_widgets(tempstr)
        find_and_delete_word_in_all_widgets(card)
        deck.delete_card(card)


interface_screen = tk.Tk()
interface_screen.title("Interface")
interface_screen.geometry("1425x250")

deck_screen = tk.Tk()
deck_screen.title("Deck List")
deck_screen.geometry("1425x600")

output_creature_label = tk.Label(deck_screen, text="Creature", font="Helventica")
output_creature_label.grid(row=0, column=0)
output_creature = tk.Text(deck_screen, height=60, width=28)
output_creature.config(state="normal")
output_creature.grid(row=1, column=0)
output_creature.tag_configure("center", justify='center')
output_creature.insert(tk.END, "")
output_creature.tag_add("center", "1.0", "end")

output_artifact_label = tk.Label(deck_screen, text="Artifact", font="Helventica")
output_artifact_label.grid(row=0, column=1)
output_artifact = tk.Text(deck_screen, height=60, width=28)
output_artifact.config(state="normal")
output_artifact.grid(row=1, column=1)
output_artifact.tag_configure("center", justify='center')
output_artifact.insert(tk.END, "")
output_artifact.tag_add("center", "1.0", "end")

output_enchantment_label = tk.Label(deck_screen, text="Enchantment", font="Helventica")
output_enchantment_label.grid(row=0, column=2)
output_enchantment = tk.Text(deck_screen, height=60, width=28)
output_enchantment.config(state="normal")
output_enchantment.grid(row=1, column=2)
output_enchantment.tag_configure("center", justify='center')
output_enchantment.insert(tk.END, "")
output_enchantment.tag_add("center", "1.0", "end")

output_planeswalker_label = tk.Label(deck_screen, text="Planeswalker", font="Helventica")
output_planeswalker_label.grid(row=0, column=3)
output_planeswalker = tk.Text(deck_screen, height=60, width=28)
output_planeswalker.config(state="normal")
output_planeswalker.grid(row=1, column=3)
output_planeswalker.tag_configure("center", justify='center')
output_planeswalker.insert(tk.END, "")
output_planeswalker.tag_add("center", "1.0", "end")

output_instant_label = tk.Label(deck_screen, text="Instant", font="Helventica")
output_instant_label.grid(row=0, column=4)
output_instant = tk.Text(deck_screen, height=60, width=28)
output_instant.config(state="normal")
output_instant.grid(row=1, column=4)
output_instant.tag_configure("center", justify='center')
output_instant.insert(tk.END, "")
output_instant.tag_add("center", "1.0", "end")

output_sorcery_label = tk.Label(deck_screen, text="Sorcery", font="Helventica")
output_sorcery_label.grid(row=0, column=5)
output_sorcery = tk.Text(deck_screen, height=60, width=28)
output_sorcery.config(state="normal")
output_sorcery.grid(row=1, column=5)
output_sorcery.tag_configure("center", justify='center')
output_sorcery.insert(tk.END, "")
output_sorcery.tag_add("center", "1.0", "end")

output_land_label = tk.Label(deck_screen, text="Land", font="Helventica")
output_land_label.grid(row=0, column=6)
output_land = tk.Text(deck_screen, height=60, width=28)
output_land.config(state="normal")
output_land.grid(row=1, column=6)
output_land.tag_configure("center", justify='center')
output_land.insert(tk.END, "")
output_land.tag_add("center", "1.0", "end")

input_label = tk.Label(interface_screen, text= "Card Search:", font= "Helventica")
input_label.grid(row=0, column=0)
input_entry = tk.Entry(interface_screen, font=("Helventica", 15))
input_entry.grid(row=1, column=0)

input_button = tk.Button(interface_screen, text="Search", font=("Helventica", 15), command=get_input)
input_button.grid(row=2, column=0)
del_button = tk.Button(interface_screen, text="Delete", font=("Helventica", 15), command=delete_card)
del_button.grid(row=2, column=1)

interface_screen.mainloop()