import tkinter as tk
import random
import json
from player import Player
from game import Game
from game_setting import GameSettings, Speed, Difficulty, GameType, GameMode
from action import Action
from typing import Dict
import tkinter.font as tkFont

player_list = [Player("Eugene", 1000000, 1000), Player("Eugene", 10000, 1000)]
game_settings = GameSettings(6, Speed.NORMAL, Difficulty.MEDIUM, GameType.ONE_FOR_ALL, GameMode.STABLE_EVENTS, True)
game = Game(game_settings, player_list)



def do_action(button):
    global label_left, label_center, label_right, label_info, game
    #labels = game.update_labels(button)
    buy_quantity = buy_scale.get()
    sell_quantity = sell_scale.get()
    
    data = False, "data is None"
    if button == "BUY":
        data = game.play_step(Action(buy=buy_quantity))
    elif button == "SELL":
        data = game.play_step(Action(sell=sell_quantity))
    elif button == "SKIP":
        data = game.play_step(Action(skip=1))
    else:
        data = game.play_step(Action())
    
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
    label_right.config(text=f"name: {data['player']['name']}\nsalary: {data['player']['salary_level']}\ncash flow: {data['player']['cash_flow']}\n\nbalance: {data['player']['balance']}")

    if data.get('actions'):
        buy = data['actions']['buy']
        sell = data['actions']['sell']
        skip = data['actions']['skip']
        
        buy_button.config(state='normal' if buy else 'disabled')
        sell_button.config(state='normal' if sell else 'disabled')
        skip_button.config(state='normal' if skip else 'disabled')

        buy_scale.set(1)
        sell_scale.set(1)
        buy_scale.config(to=buy)
        sell_scale.config(to=sell)
        
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

buy_button_frame = tk.Frame(button_frame, bg="#90ee9f")
buy_button_frame.pack(side="left", fill='both', expand=True, pady=50)
sell_button_frame = tk.Frame(button_frame, bg="#90ee9f")
sell_button_frame.pack(side="left", fill='both', expand=True, pady=50)
skip_button_frame = tk.Frame(button_frame, bg="#90ee9f")
skip_button_frame.pack(side="left", fill='both', expand=True, pady=50)


buy_scale = tk.Scale(buy_button_frame, from_=1, to=1, orient="horizontal", label="Quantity")
buy_scale.pack(side='top', padx=5, pady=5, fill='x', expand=True)
buy_button = tk.Button(buy_button_frame, text="BUY", command=lambda: do_action("BUY"))
buy_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)

sell_scale = tk.Scale(sell_button_frame, from_=1, to=1, orient="horizontal", label="Quantity")
sell_scale.pack(side='top', padx=5, pady=5, fill='x', expand=True)
sell_button = tk.Button(sell_button_frame, text="SELL", command=lambda: do_action("SELL"))
sell_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)

skip_button = tk.Button(skip_button_frame, text="SKIP", command=lambda: do_action("SKIP"))
skip_button.pack(side='bottom', padx=5, pady=5, fill='y', expand=True)



#game.start()
game.print_card_in_console(game.set_new_card())
update_labels(game.get_data())

root.mainloop()