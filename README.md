# D&D 5e attack rolls

Roll a group of attacks and calculate the exact chance to hit. This tool handles attack rolls only; it does not calculate damage.

## Run

Requires Python 3.11+; the desktop interface also requires Tkinter.

```sh
python main.py
python attacks.py --bonus 5 --ac 15 --mode advantage --count 4 --seed 42
```

The CLI returns JSON containing every die, the selected d20, the total, hit/critical flags and exact probabilities. The seed makes a sample reproducible; probability calculations enumerate all possible outcomes and do not depend on the seed.

## Rules

Under the [2014 attack-roll rules](https://www.dndbeyond.com/sources/dnd/basic-rules-2014/combat#AttackRolls), a selected natural 1 misses and a selected natural 20 hits critically regardless of modifiers. Advantage selects the higher of two dice; disadvantage selects the lower. A bonus d4 changes the total, not the natural roll.

For +5 against AC 15, ordinary hit chance is 55%, advantage is 79.75%, and disadvantage is 30.25%. Critical hits are included in the hit percentage.

`three-dice` keeps the highest of three d20s. It is an optional mode for specific features or house rules, not the default advantage rule. Damage, expanded critical ranges, critical fumbles, simultaneous advantage/disadvantage, and resource consumption are not simulated.

Attack count is limited to 1,000 per request. Attack bonus accepts −100 through 100, including negative modifiers; AC accepts 0 through 100.

## Development

```sh
python -m unittest discover -s tests -v
```

`attacks.py` contains deterministic roll resolution, seeded simulation, exhaustive probabilities and the CLI. `main.py` is only a desktop adapter. Importing either module does not open a window.

Tests cover automatic hits/misses, selected dice, exact probabilities, input limits, seeded replay and CLI output. [CI](https://github.com/Almeida96/Attacks_RPG/actions/workflows/ci.yml) runs on Linux and Windows.

See [contributing](CONTRIBUTING.md) and [changes](CHANGELOG.md). No application-source license has been declared.
