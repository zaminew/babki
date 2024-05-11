import tkinter as tk
import random
import json
from player import Player
from game import Game
from game_setting import GameSetting, Speed, Difficulty, GameType, GameMode
from action import Action
from typing import Dict
import tkinter.font as tkFont

player_list = [Player("Eugene", 10000, 100), Player("Eugene", 10000, 1000)]
game_settings = GameSetting(6, Speed.NORMAL, Difficulty.MEDIUM, GameType.ONE_FOR_ALL, GameMode.STABLE_EVENTS, True)
game = Game(game_settings, player_list)


# TODO рефакторинг кода чтобы все общение было только через json/dict формат
def do_action(button):
    data = False, "data is None"
    
    amount = 0
    if button == 'buy':
        amount = buy_scale.get()
    elif button == 'sell':
        amount = sell_scale.get()
    elif button == 'skip':
        amount = 1
    elif button == 'take_loan':
        amount = take_loan_scale.get()
    elif button == 'repay_loan':
        amount = repay_loan_scale.get()
    
    data = game.execute_player_action({'action' : button, 'amount' : amount})
    
    if data:
        if data[0]:
            label_info.config(text=data[1])
            label_info.config(bg="#90ff90")
            label_info.pack()
        else:
            label_info.config(text=data[1])
            label_info.config(bg="#ff9090")
            label_info.pack()
        listbox.insert(tk.END, data[1])
        listbox.see(tk.END)
    
        update_labels(game.get_data())


def update_labels(data : Dict[str, int]):
    
    prep_data = ''
    prep_data += '\n\nproperty:\n'
    prep_data += '\n'.join([f'{property["name"]}, p: {property["price"]}, dp: {property["down_payment"]}, cf: {property["cash_flow"]}' for property in data['player']['ownership']['property']])
    prep_data += '\n\nstock:\n'
    prep_data += '\n'.join([f'{property["name"]}, p: {property["price"]}, q: {property["quantity"]}, sum: {property["price"]*property["quantity"]}, cf: {0}' for property in data['player']['ownership']['stocks']])
    prep_data += '\n\nbusiness:\n'
    prep_data += '\n'.join([f'{property["name"]}, p: {property["price"]}, dp: {property["down_payment"]}, cf: {property["cash_flow"]}' for property in data['player']['ownership']['businesses']])
    
    label_left.config(text=prep_data)
    label_center.config(text=data["card"])
    label_right.config(text=f"name: {data['player']['name']}\nsalary: {data['player']['salary_level']}\ncash flow: {data['player']['cash_flow']}\nloan: {data['player']['loan']}\n\nbalance: {data['player']['balance']}")
    
    if data.get('actions'):
        buy = data['actions']['buy']
        sell = data['actions']['sell']
        skip = data['actions']['skip']
        take_loan = data['actions']['take_loan']
        repay_loan = data['actions']['repay_loan']
        
        buy_button.config(state='normal' if buy else 'disabled')
        sell_button.config(state='normal' if sell else 'disabled')
        skip_button.config(state='normal' if skip else 'disabled')
        take_loan_button.config(state='normal' if take_loan else 'disabled')
        repay_loan_button.config(state='normal' if repay_loan else 'disabled')

       
        buy_scale.config(to=buy)
        sell_scale.config(to=sell)
        buy_scale.set(buy)
        sell_scale.set(sell)
        
        take_loan_scale.config(to=take_loan)
        repay_loan_scale.config(to=repay_loan)
        take_loan_scale.set(take_loan)
        repay_loan_scale.set(repay_loan)
        
        if buy <= 1:
            buy_scale.pack_forget()
        else:
            buy_scale.pack()
            
        if sell <= 1:
            sell_scale.pack_forget()
        else:
            sell_scale.pack()


root = tk.Tk()
root.title("BABKI")
root.geometry("1600x800")

left_frame = tk.Frame(master=root, width=400, height=100, bg="#add8e6")
left_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False )

center_frame = tk.Frame(master=root, width=800, bg="#90ee90")
center_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True )

right_frame = tk.Frame(master=root, width=400, bg="#ffffe0")
right_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=False )


left_frame.pack_propagate(False)  # Фиксированный размер фрейма
center_frame.pack_propagate(False)  # Фиксированный размер фрейма
right_frame.pack_propagate(False)  # Фиксированный размер фрейма


# Создаем метки в левом, центральном и правом фреймах
label_left = tk.Label(left_frame, text='', justify='left', wraplength=400, bg="#add8ef", pady=50)
label_left.pack()
label_center = tk.Label(center_frame, text='', justify='left', wraplength=400, bg="#90ee9f", pady=50)
label_center.pack()
label_info = tk.Label(right_frame, text='', justify='left', wraplength=400, bg="#ff5555", pady=50)
label_info.pack_forget()
label_right = tk.Label(right_frame, text='', justify='left', wraplength=400, bg="#ffffef", pady=50)
label_right.pack()


# Создаем Listbox
listbox = tk.Listbox(right_frame)
listbox.pack(fill=tk.BOTH, expand=True)


# Создаем фрейм для кнопок внизу центрального фрейма
button_frame = tk.Frame(center_frame, bg="#90ee9f", height=200)
button_frame.pack(side="bottom", fill='x', pady=50)

take_loan_button_frame = tk.Frame(button_frame, bg="#90ee90")
take_loan_button_frame.pack(side="left", fill='both', expand=True, pady=50)
repay_loan_button_frame = tk.Frame(button_frame, bg="#90ee90")
repay_loan_button_frame.pack(side="left", fill='both', expand=True, pady=50)

buy_button_frame = tk.Frame(button_frame, bg="#90ee9f")
buy_button_frame.pack(side="left", fill='both', expand=True, pady=50)
sell_button_frame = tk.Frame(button_frame, bg="#90ee9f")
sell_button_frame.pack(side="left", fill='both', expand=True, pady=50)
skip_button_frame = tk.Frame(button_frame, bg="#90ee9f")
skip_button_frame.pack(side="left", fill='both', expand=True, pady=50)


take_loan_scale = tk.Scale(take_loan_button_frame, from_=0, to=0, orient="horizontal", label="сумма кредита")
take_loan_scale.pack(side='top', padx=5, pady=5, fill='x', expand=True)
take_loan_button = tk.Button(take_loan_button_frame, text="take L", command=lambda: do_action("take_loan"))
take_loan_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)

repay_loan_scale = tk.Scale(repay_loan_button_frame, from_=0, to=0, orient="horizontal", label="сумма погашения")
repay_loan_scale.pack(side='top', padx=5, pady=5, fill='x', expand=True)
repay_loan_button = tk.Button(repay_loan_button_frame, text="repay L", command=lambda: do_action("repay_loan"))
repay_loan_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)

buy_scale = tk.Scale(buy_button_frame, from_=1, to=1, orient="horizontal", label="количество")
buy_scale.pack(side='top', padx=5, pady=5, fill='x', expand=True)
buy_button = tk.Button(buy_button_frame, text="BUY", command=lambda: do_action("buy"))
buy_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)

sell_scale = tk.Scale(sell_button_frame, from_=1, to=1, orient="horizontal", label="количество")
sell_scale.pack(side='top', padx=5, pady=5, fill='x', expand=True)
sell_button = tk.Button(sell_button_frame, text="SELL", command=lambda: do_action("sell"))
sell_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)

skip_button = tk.Button(skip_button_frame, text="SKIP", command=lambda: do_action("skip"))
skip_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)



#game.start()
game.print_card_in_console(game.set_new_card())
update_labels(game.get_data())

root.mainloop()