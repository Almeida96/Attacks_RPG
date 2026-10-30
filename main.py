"""Copyright Igor Almeida. Desktop attack simulator."""

import tkinter as tk
from tkinter import ttk

from attacks import MODES, probabilities, simulate


def main():
    root = tk.Tk()
    root.title("D&D 5e attack rolls")
    root.geometry("850x620")
    root.minsize(650, 450)
    panel = ttk.Frame(root, padding=16)
    panel.pack(fill="both", expand=True)
    panel.columnconfigure(1, weight=1)
    panel.rowconfigure(7, weight=1)
    values = {}
    for row, (name, value) in enumerate(
        (
            ("Attack bonus", "5"),
            ("Armor class", "15"),
            ("Attack count", "4"),
            ("Seed (optional)", ""),
        )
    ):
        ttk.Label(panel, text=name).grid(row=row, column=0, sticky="w", pady=4)
        variable = tk.StringVar(value=value)
        values[name] = variable
        ttk.Entry(panel, textvariable=variable).grid(row=row, column=1, sticky="ew")
    mode = tk.StringVar(value="normal")
    ttk.Label(panel, text="Roll mode").grid(row=4, column=0, sticky="w")
    ttk.Combobox(panel, textvariable=mode, values=list(MODES), state="readonly").grid(
        row=4, column=1, sticky="ew"
    )
    bonus_die = tk.BooleanVar()
    ttk.Checkbutton(panel, text="Add 1d4 to each attack", variable=bonus_die).grid(
        row=5, column=0, columnspan=2, sticky="w"
    )
    status = tk.StringVar(
        value="Three-dice mode is an optional rule, not ordinary advantage."
    )
    ttk.Label(panel, textvariable=status, wraplength=700).grid(
        row=8, column=0, columnspan=2, sticky="w", pady=8
    )
    output = tk.Text(panel, state="disabled", wrap="word")
    output.grid(row=7, column=0, columnspan=2, sticky="nsew")
    scroll = ttk.Scrollbar(panel, command=output.yview)
    scroll.grid(row=7, column=2, sticky="ns")
    output.configure(yscrollcommand=scroll.set)

    def roll():
        output.configure(state="normal")
        output.delete("1.0", "end")
        try:
            bonus = int(values["Attack bonus"].get())
            ac = int(values["Armor class"].get())
            count = int(values["Attack count"].get())
            seed = values["Seed (optional)"].get().strip()
            rolls = simulate(
                bonus,
                ac,
                mode.get(),
                count,
                bonus_die.get(),
                int(seed) if seed else None,
            )
            odds = probabilities(bonus, ac, mode.get(), bonus_die.get())
            for index, attack in enumerate(rolls, 1):
                verdict = (
                    "CRITICAL HIT"
                    if attack.critical
                    else "hit"
                    if attack.hit
                    else "miss"
                )
                output.insert(
                    "end",
                    f"{index}. d20 {list(attack.dice)} → {attack.selected}, "
                    f"d4 +{attack.bonus_die}, total {attack.total}: {verdict}\n",
                )
            status.set(
                f"{sum(a.hit for a in rolls)}/{count} hits in this sample. "
                f"Exact hit chance: {odds['hit']:.2%}; critical: {odds['critical']:.2%}."
            )
        except ValueError as error:
            status.set(f"Cannot roll: {error}")
        finally:
            output.configure(state="disabled")

    ttk.Button(panel, text="Roll attacks", command=roll).grid(
        row=6, column=0, columnspan=2, sticky="ew", pady=12
    )
    root.mainloop()


if __name__ == "__main__":
    main()
