from libs.openexchangeClass import openexchangeClient
import tkinter as tk

#appID would be encrypted and stored in a seperate file in a production script
appID = "c6c8af5ba5f143c1bff2638cbc1cdba2"
client = openexchangeClient(appID)

root = tk.Tk()
root.title("Currency Converter")
root.geometry("325x400")
response_window = tk.Tk()
response_window.title("Output")
response_window.geometry("500x400")
global curr_one
global curr_two
global denominations
global amount
global output_field
global rates
rates = client.get_rates()

def get_input():
    try:
        curr_one = str(curr_one_prompt_entry.get())
        curr_two = str(curr_two_prompt_entry.get())
        amount = int(amount_entry.get())
        if curr_one not in rates or curr_two not in rates:
            raise NameError
        if amount < 1:
            raise NameError
        print_output(client.convert(amount, curr_one, curr_two))
    except ValueError or TypeError:
        print_output("Invalid Demoninations")
    except NameError:
        print_output("Invalid Currency Amount")
        

def print_currencies():
    print_output(rates)


def print_output(output):
    output_field.config(state="normal")
    output_field.delete('1.0', "end")
    output_field.insert(tk.END, output)
    output_field.pack()

output_field = tk.Text(response_window, height=50, width=80)

curr_one_prompt_label = tk.Label(root, text="Starting Currency", font= ("Helventica", 15))
curr_one_prompt_label.grid(pady=5, padx= 50, row=1, column=0)
curr_one_prompt_entry = tk.Entry(root, font= ("Helventica", 15))
curr_one_prompt_entry.grid(pady=5, padx= 50, row=2, column=0)

curr_two_prompt_label = tk.Label(root, text="Ending Currency", font= ("Helventica", 15))
curr_two_prompt_label.grid(pady=5, row=3, column=0)
curr_two_prompt_entry = tk.Entry(root, font= ("Helventica", 15))
curr_two_prompt_entry.grid(pady=5, row=4, column=0)

amount_label = tk.Label(root, text="Amount", font= ("Helventica", 15))
amount_label.grid(pady=5, row=5, column=0)
amount_entry = tk.Entry(root, font= ("Helventica", 15))
amount_entry.grid(pady=5, row=6, column=0)

submit_button = tk.Button(root, text="Submit", command=get_input, font= ("Helventica", 20))
submit_button.grid(pady=5, padx=50, row=8, column=0)

currencies_button = tk.Button(root, text="Available Currencies", command=print_currencies, font= ("Helventica", 20))
currencies_button.grid(pady=5, padx=50, row=9, column=0)

root.mainloop()