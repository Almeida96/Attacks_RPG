#Projeto desenvolvido por Igor Almeida, qualquer modificação sem autorização terá implicações legais
#Project developed by Igor Almeida, any modification without authorization will have legal implications

import tkinter as tk
from tkinter import ttk, messagebox
import random

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def on_validate_input(P):
    if P == "" or P.isdigit():
        return True
    else:
        return False

def change_language():
    if selected_language.get() == "pt":
        user_hit_label.config(text="Acerto do Usuário:")
        creature_ca_label.config(text="CA da Criatura:")
        advantage_label.config(text="Dados na Vantagem:")
        num_attacks_label.config(text="Número de Ataques:")
        start_button.config(text="Iniciar Ataque")
        advantage_combobox['values'] = advantage_combobox_values["pt"]
        results_frame.config(text="Resultados")
        bonus_dice_checkbox.config(text="Dado Bônus (1d4)")
        if advantage_combobox.get() == "None":
            advantage_combobox.set("Nenhum")
        elif advantage_combobox.get() == "Disadvantage":
            advantage_combobox.set("Desvantagem")
    else:
        user_hit_label.config(text="User Hit:")
        creature_ca_label.config(text="Creature CA:")
        advantage_label.config(text="Advantage Dice:")
        num_attacks_label.config(text="Number of Attacks:")
        start_button.config(text="Start Attack")
        advantage_combobox['values'] = advantage_combobox_values["en"]
        results_frame.config(text="Results")
        bonus_dice_checkbox.config(text="Bonus Dice (1d4)")
        if advantage_combobox.get() == "Nenhum":
            advantage_combobox.set("None")
        elif advantage_combobox.get() == "Desvantagem":
            advantage_combobox.set("Disadvantage")


def start_attack():
    user_hit_value = user_hit_entry.get()
    creature_ca_value = creature_ca_entry.get()
    num_attacks_value = num_attacks_spinbox.get()
    advantage_value = advantage_combobox.get()

    # Check if input values are integers
    if not (is_integer(user_hit_value) and is_integer(creature_ca_value) and is_integer(num_attacks_value)):
        messagebox.showerror("Erro", error_messages[selected_language.get()])
        return

    # Convert input values to integers
    user_hit = int(user_hit_value)
    creature_ca = int(creature_ca_value)
    num_attacks = int(num_attacks_value)

    hit_count = 0
    crit_pos_count = 0
    crit_neg_count = 0
    results_list = []

    for _ in range(num_attacks):
        rolls = []
        if advantage_value == advantage_combobox_values[selected_language.get()][0]:  # "Nenhum"/"None"
            rolls.append(random.randint(1, 20))
        elif advantage_value in advantage_combobox_values[selected_language.get()][1:3]:  # "2" or "3"
            rolls.extend([random.randint(1, 20) for _ in range(int(advantage_value))])
        else:  # "Desvantagem"/"Disadvantage"
            rolls.extend([random.randint(1, 20), random.randint(1, 20)])

        # Determine roll based on advantage/disadvantage
        roll = min(rolls) if advantage_value == advantage_combobox_values[selected_language.get()][3] else max(rolls)

        bonus = 0
        bonus_str = ""
        if bonus_dice_var.get():
            bonus = random.randint(1, 4)
            total_value = roll + user_hit + bonus
            bonus_str = f" + 1d4 = {total_value} [{', '.join(map(str, rolls))}] + [{bonus}] + {user_hit}"
        else:
            total_value = roll + user_hit
            bonus_str = f" = {total_value} [{', '.join(map(str, rolls))}] + {user_hit}"

        is_critical = ""
        if advantage_value == advantage_combobox_values[selected_language.get()][3]:  # Disadvantage
            if 1 in rolls:
                is_critical = " (Crítico Negativo!)" if selected_language.get() == "pt" else " (Negative Critical!)"
                crit_neg_count += 1
            elif all(roll == 20 for roll in rolls):
                is_critical = " (Crítico Positivo!)" if selected_language.get() == "pt" else " (Positive Critical!)"
                crit_pos_count += 1
        elif 20 in rolls:
            is_critical = " (Crítico Positivo!)" if selected_language.get() == "pt" else " (Positive Critical!)"
            crit_pos_count += 1
        elif all(roll == 1 for roll in rolls) and advantage_value in advantage_combobox_values[selected_language.get()][1:3]:  # Only if all are 1 for 2 or 3 dice advantage
            is_critical = " (Crítico Negativo!)" if selected_language.get() == "pt" else " (Negative Critical!)"
            crit_neg_count += 1

        hit_result = "Sim" if selected_language.get() == "pt" else "Yes"
        if roll + user_hit + bonus < creature_ca:
            hit_result = "Não" if selected_language.get() == "pt" else "No"

        attack_str = "Ataque" if selected_language.get() == "pt" else "Attack"
        rolled_str = "rolou" if selected_language.get() == "pt" else "rolls"

        results_list.append(
            f"{attack_str} {len(results_list) + 1} {rolled_str} {len(rolls)}d20{bonus_str} {hit_result}{is_critical}")

        if hit_result == "Sim" or hit_result == "Yes":
            hit_count += 1

    # Display results
    results_text.config(state=tk.NORMAL)
    results_text.delete(1.0, tk.END)
    for result in results_list:
        results_text.insert(tk.END, result + "\n")

    total_hits_str = f"\nTotal de Acertos: {hit_count}\nCríticos Positivos: {crit_pos_count}\nCríticos Negativos: {crit_neg_count}\n" if selected_language.get() == "pt" else f"\nTotal Hits: {hit_count}\nPositive Critics: {crit_pos_count}\nNegative Critics: {crit_neg_count}\n"
    results_text.insert(tk.END, total_hits_str)
    results_text.config(state=tk.DISABLED)

# GUI
root = tk.Tk()
root.title("Attack Simulator")
root.geometry("900x395")
root.resizable(False, False)

validate_input = root.register(on_validate_input)
error_messages = {
    "pt": "Por favor, insira apenas valores numéricos nos campos.",
    "en": "Please enter only numeric values in the fields."
}

selected_language = tk.StringVar(value="pt")
lang_radio_pt = ttk.Radiobutton(root, text="Português", value="pt", variable=selected_language, command=change_language)
lang_radio_pt.grid(row=0, column=0, padx=10, sticky=tk.W)

lang_radio_en = ttk.Radiobutton(root, text="English", value="en", variable=selected_language, command=change_language)
lang_radio_en.grid(row=1, column=0, padx=10, sticky=tk.W)

user_hit_label = ttk.Label(root, text="Acerto do Usuário:")
user_hit_label.grid(row=3, column=0, padx=10, sticky=tk.W)
user_hit_entry = ttk.Entry(root, validate='key', validatecommand=(validate_input, '%P'))
user_hit_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

creature_ca_label = ttk.Label(root, text="CA da Criatura:")
creature_ca_label.grid(row=5, column=0, padx=10, sticky=tk.W)
creature_ca_entry = ttk.Entry(root, validate='key', validatecommand=(validate_input, '%P'))
creature_ca_entry.grid(row=6, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

advantage_label = ttk.Label(root, text="Dados na Vantagem:")
advantage_label.grid(row=7, column=0, padx=10, sticky=tk.W)
advantage_combobox_values = {
    "pt": ["Nenhum", "2", "3", "Desvantagem"],
    "en": ["None", "2", "3", "Disadvantage"]
}
advantage_combobox = ttk.Combobox(root, values=advantage_combobox_values["pt"], state="readonly")
advantage_combobox.set("Nenhum")
advantage_combobox.grid(row=8, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

num_attacks_label = ttk.Label(root, text="Número de Ataques:")
num_attacks_label.grid(row=9, column=0, padx=10, sticky=tk.W)
num_attacks_spinbox = ttk.Spinbox(root, from_=1, to=100, wrap=True, validate='key', validatecommand=(validate_input, '%P'))
num_attacks_spinbox.grid(row=10, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

start_button = ttk.Button(root, text="Iniciar Ataque", command=start_attack)
start_button.grid(row=11, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

results_frame = ttk.LabelFrame(root, text="Resultados")
results_frame.grid(row=0, column=1, rowspan=12, padx=20, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
results_text = tk.Text(results_frame, wrap=tk.NONE, height=20, width=82, state=tk.DISABLED)
results_text.grid(row=0, column=0, padx=10, sticky=tk.W + tk.E)
scrollbar = ttk.Scrollbar(results_frame, command=results_text.yview)
scrollbar.grid(row=0, column=1, sticky='nsew')
results_text.config(yscrollcommand=scrollbar.set)

bonus_dice_var = tk.IntVar()
bonus_dice_checkbox = ttk.Checkbutton(root, text="Dado Bônus (1d4)", variable=bonus_dice_var)
bonus_dice_checkbox.grid(row=2, column=0, padx=10, pady=(5, 5), sticky=tk.W)  # Mover para debaixo do botão de linguagem inglês

root.mainloop()