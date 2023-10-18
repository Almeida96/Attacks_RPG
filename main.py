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
        results_frame.config(text="Results")
        advantage_combobox['values'] = advantage_combobox_values["en"]
        if advantage_combobox.get() == "Nenhum":
            advantage_combobox.set("None")
        elif advantage_combobox.get() == "Desvantagem":
            advantage_combobox.set("Disadvantage")


def start_attack():
    user_hit_value = user_hit_entry.get()
    creature_ca_value = creature_ca_entry.get()
    num_attacks_value = num_attacks_spinbox.get()

    # Validação de Entrada
    if not (is_integer(user_hit_value) and is_integer(creature_ca_value) and is_integer(num_attacks_value)):
        messagebox.showerror("Erro" if selected_language.get() == "pt" else "Error",
                             error_messages[selected_language.get()])
        return

    user_hit = int(user_hit_value)
    creature_ca = int(creature_ca_value)
    num_attacks = int(num_attacks_value)

    advantage = advantage_combobox.get()
    dice_count = 1

    if advantage in ["2", "Desvantagem", "Disadvantage"]:
        dice_count = 2
    elif advantage == "3":
        dice_count = 3

    hits = 0
    criticals = 0

    results_text.configure(state=tk.NORMAL)
    results_text.delete(1.0, tk.END)
    for i in range(num_attacks):
        dice_rolls = [random.randint(1, 20) for _ in range(dice_count)]

        if advantage in ["2", "3"]:
            roll = max(dice_rolls) + user_hit
            critical = 20 in dice_rolls
        elif advantage in ["Desvantagem", "Disadvantage"]:
            roll = min(dice_rolls) + user_hit
            critical = 1 in dice_rolls
        else:
            roll = dice_rolls[0] + user_hit
            critical = dice_rolls[0] == 20

        if roll >= creature_ca:
            hits += 1

        if critical:
            criticals += 1

        if selected_language.get() == "pt":
            results_text.insert(tk.END,
                                f"Ataque {i + 1} rolou {dice_count}d20 + {user_hit} = {roll} {str(dice_rolls) + ' + ' + str(user_hit)} {'sim' if roll >= creature_ca else 'não'}{' (Crítico!)' if critical else ''}\n")
        else:
            results_text.insert(tk.END,
                                f"Attack {i + 1} rolls {dice_count}d20 + {user_hit} = {roll} {str(dice_rolls) + ' + ' + str(user_hit)} {'Yes' if roll >= creature_ca else 'No'}{' (Critical!)' if critical else ''}\n")

    if selected_language.get() == "pt":
        results_text.insert(tk.END, f"\nTotal Acertos: {hits}\nTotal Críticos: {criticals}")
    else:
        results_text.insert(tk.END, f"\nTotal Hits: {hits}\nTotal Critics: {criticals}")

    results_text.configure(state=tk.DISABLED)


# GUI
root = tk.Tk()
root.title("Attack Simulator")
root.geometry("790x390")
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
user_hit_label.grid(row=2, column=0, padx=10, sticky=tk.W)
user_hit_entry = ttk.Entry(root, validate='key', validatecommand=(validate_input, '%P'))
user_hit_entry.grid(row=3, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

creature_ca_label = ttk.Label(root, text="CA da Criatura:")
creature_ca_label.grid(row=4, column=0, padx=10, sticky=tk.W)
creature_ca_entry = ttk.Entry(root, validate='key', validatecommand=(validate_input, '%P'))
creature_ca_entry.grid(row=5, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

advantage_label = ttk.Label(root, text="Dados na Vantagem:")
advantage_label.grid(row=6, column=0, padx=10, sticky=tk.W)
advantage_combobox_values = {
    "pt": ["Nenhum", "2", "3", "Desvantagem"],
    "en": ["None", "2", "3", "Disadvantage"]
}
advantage_combobox = ttk.Combobox(root, values=advantage_combobox_values["pt"], state="readonly")
advantage_combobox.set("Nenhum")
advantage_combobox.grid(row=7, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

num_attacks_label = ttk.Label(root, text="Número de Ataques:")
num_attacks_label.grid(row=8, column=0, padx=10, sticky=tk.W)
num_attacks_spinbox = ttk.Spinbox(root, from_=1, to=100, wrap=True, validate='key', validatecommand=(validate_input, '%P'))
num_attacks_spinbox.grid(row=9, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

start_button = ttk.Button(root, text="Iniciar Ataque", command=start_attack)
start_button.grid(row=10, column=0, padx=10, pady=(0, 10), sticky=tk.W + tk.E)

results_frame = ttk.LabelFrame(root, text="Resultados")
results_frame.grid(row=0, column=1, rowspan=12, padx=20, pady=10, sticky=tk.W + tk.E + tk.N + tk.S)
results_text = tk.Text(results_frame, wrap=tk.NONE, height=20, width=70, state=tk.DISABLED)
results_text.grid(row=0, column=0)
results_scrollbar_x = ttk.Scrollbar(results_frame, orient=tk.HORIZONTAL, command=results_text.xview)
results_scrollbar_x.grid(row=1, column=0, sticky=tk.W + tk.E)
results_scrollbar_y = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=results_text.yview)
results_scrollbar_y.grid(row=0, column=1, sticky=tk.N + tk.S)
results_text.configure(yscrollcommand=results_scrollbar_y.set, xscrollcommand=results_scrollbar_x.set)

root.mainloop()
