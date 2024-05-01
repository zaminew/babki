import tkinter as tk
import random
import json
from player import Player
from game import Game
from game_setting import GameSettings, Speed, Difficulty, GameType, GameMode

player_list = [Player("Eugene", 1000000, 1000), Player("Eugene", 10000, 1000)]
game_settings = GameSettings(6, Speed.NORMAL, Difficulty.MEDIUM, GameType.ONE_FOR_ALL, GameMode.STABLE_EVENTS, True)
game = Game(game_settings, player_list)
#game.start()
game.print_event(game.get_new_card())
ch = None

def update_labels(button):
    global label_left, label_center, label_right, label_error, game
    #labels = game.update_labels(button)
    quantity_value = quantity_scale.get()
    data = game.play_step(button, quantity_value)
    if data.get('error'):
        label_error.config(text=data["error"])
        label_error.pack()
        return 0
    else:
        label_error.config(text='')
        label_error.pack_forget()
        
    prep_data = ''
    prep_data += '\n\nproperty:\n'
    prep_data += '\n'.join([f'{property["name"]}, p: {property["price"]}, dp: {property["down_payment"]}, cf: {property["cash_flow"]}' for property in data['player']['ownership']['property']])
    prep_data += '\n\nstock:\n'
    prep_data += '\n'.join([f'{property["name"]}, p: {property["price"]}, q: {property["quantity"]}, cf: {0}' for property in data['player']['ownership']['stocks']])
    prep_data += '\n\nbusiness:\n'
    prep_data += '\n'.join([f'{property["name"]}, p: {property["price"]}, dp: {property["down_payment"]}, cf: {property["cash_flow"]}' for property in data['player']['ownership']['businesses']])
    
    label_left.config(text=prep_data)
    label_center.config(text=data["card"])
    label_right.config(text=f"name: {data['player']['name']}\nsalary: {data['player']['salary_level']}\ncash flow: {data['player']['cash_flow']}\n\nbalance: {data['player']['balance']}")
    
    if data.get('actions'):
        buy_button.config(state='normal' if data['actions']['buy'] else 'disabled')
        sell_button.config(state='normal' if data['actions']['sell'] else 'disabled')
        skip_button.config(state='normal' if data['actions']['skip'] else 'disabled')

root = tk.Tk()
root.title("Изменение текста метки при нажатии на кнопку")

# Фиксируем размер окна
root.geometry("1200x800")

# Создаем фреймы для разделения окна
left_frame = tk.Frame(root, bg="#add8e6")  # Цвет: голубой
left_frame.grid(row=0, column=0, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

center_frame = tk.Frame(root, bg="#90ee90")  # Цвет: светло-зеленый
center_frame.grid(row=0, column=1, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

right_frame = tk.Frame(root, bg="#ffffe0")  # Цвет: светло-желтый
right_frame.grid(row=0, column=2, sticky="nsew")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)

# Создаем метки в левом, центральном и правом фреймах
label_left = tk.Label(left_frame, text='', justify='left', wraplength=400, bg="#add8ef", pady=50)
label_left.pack()
label_center = tk.Label(center_frame, text='', justify='left', wraplength=400, bg="#90ee9f", pady=50)
label_center.pack()
label_error = tk.Label(center_frame, text='', justify='left', wraplength=400, bg="#ff5555", pady=50)
label_error.pack_forget()
label_right = tk.Label(right_frame, text='', justify='left', wraplength=400, bg="#ffffef", pady=50)
label_right.pack()

# Создаем ползунок для выбора количества
quantity_scale = tk.Scale(center_frame, from_=0, to=10, orient="horizontal", label="Quantity")
quantity_scale.pack()

# Создаем фрейм для кнопок внизу центрального фрейма
button_frame = tk.Frame(center_frame, bg="#90ee9f")
button_frame.pack(side="bottom", fill="x", pady=50)

# Создаем кнопки в центральном фрейме
check_button = tk.Button(button_frame, text="CHECK", command=lambda: update_labels("CHECK"))
check_button.pack(side='left', padx=5, pady=5, fill='x', expand=True)

buy_button = tk.Button(button_frame, text="BUY", command=lambda: update_labels("BUY"))
buy_button.pack(side='left', padx=5, pady=5, fill='x', expand=True)

sell_button = tk.Button(button_frame, text="SELL", command=lambda: update_labels("SELL"))
sell_button.pack(side='left', padx=5, pady=5, fill='x', expand=True)

skip_button = tk.Button(button_frame, text="SKIP", command=lambda: update_labels("SKIP"))
skip_button.pack(side='left', padx=5, pady=5, fill='x', expand=True)

update_labels('')

root.mainloop()