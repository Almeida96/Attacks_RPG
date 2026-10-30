"""D&D 2014 attack rolls; damage and expanded critical ranges are outside the model."""

import argparse
import itertools
import json
import random
from dataclasses import asdict, dataclass

MODES = {"normal": 1, "advantage": 2, "disadvantage": 2, "three-dice": 3}


def validate(bonus, armor_class, mode, count=1, bonus_die=False):
    for name, value, low, high in (
        ("Attack bonus", bonus, -100, 100),
        ("Armor class", armor_class, 0, 100),
        ("Attack count", count, 1, 1000),
    ):
        if type(value) is not int or not low <= value <= high:
            raise ValueError(f"{name} must be an integer from {low} to {high}.")
    if mode not in MODES:
        raise ValueError("Unknown roll mode.")
    if type(bonus_die) is not bool:
        raise ValueError("Bonus die must be true or false.")


@dataclass(frozen=True)
class Attack:
    dice: tuple[int, ...]
    selected: int
    bonus_die: int
    total: int
    hit: bool
    critical: bool
    natural_one: bool


def resolve(dice, bonus, armor_class, mode="normal", extra=0):
    validate(bonus, armor_class, mode)
    if (
        len(dice) != MODES[mode]
        or any(type(die) is not int or not 1 <= die <= 20 for die in dice)
        or type(extra) is not int
        or not 0 <= extra <= 4
    ):
        raise ValueError("Invalid dice.")
    selected = min(dice) if mode == "disadvantage" else max(dice)
    total = selected + bonus + extra
    return Attack(
        tuple(dice),
        selected,
        extra,
        total,
        selected == 20 or (selected != 1 and total >= armor_class),
        selected == 20,
        selected == 1,
    )


def simulate(bonus, armor_class, mode="normal", count=1, bonus_die=False, seed=None):
    validate(bonus, armor_class, mode, count, bonus_die)
    if seed is not None and type(seed) is not int:
        raise ValueError("Seed must be an integer.")
    rng = random.Random(seed)
    return [
        resolve(
            [rng.randint(1, 20) for _ in range(MODES[mode])],
            bonus,
            armor_class,
            mode,
            rng.randint(1, 4) if bonus_die else 0,
        )
        for _ in range(count)
    ]


def probabilities(bonus, armor_class, mode="normal", bonus_die=False):
    """Enumerate every outcome instead of estimating odds from a random sample."""
    validate(bonus, armor_class, mode, bonus_die=bonus_die)
    counts = {"hit": 0, "critical": 0, "natural_one": 0}
    outcomes = 0
    for dice in itertools.product(range(1, 21), repeat=MODES[mode]):
        for extra in range(1, 5) if bonus_die else (0,):
            result = resolve(dice, bonus, armor_class, mode, extra)
            outcomes += 1
            for key in counts:
                counts[key] += getattr(result, key)
    return {key: value / outcomes for key, value in counts.items()}


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Roll D&D attacks and calculate exact hit odds."
    )
    parser.add_argument("--bonus", type=int, required=True)
    parser.add_argument("--ac", type=int, required=True)
    parser.add_argument("--mode", choices=MODES, default="normal")
    parser.add_argument("--count", type=int, default=1)
    parser.add_argument("--bonus-d4", action="store_true")
    parser.add_argument("--seed", type=int)
    args = parser.parse_args(argv)
    try:
        rolls = simulate(
            args.bonus, args.ac, args.mode, args.count, args.bonus_d4, args.seed
        )
        result = {
            "attacks": [asdict(roll) for roll in rolls],
            "hits": sum(roll.hit for roll in rolls),
            "odds": probabilities(args.bonus, args.ac, args.mode, args.bonus_d4),
        }
        print(json.dumps(result, indent=2))
        return 0
    except ValueError as error:
        parser.error(str(error))


if __name__ == "__main__":
    raise SystemExit(main())
