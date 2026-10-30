# Contributing

Run `python -m unittest discover -s tests -v` before submitting a change. Keep game rules in `attacks.py`, and add a worked probability or fixed-dice regression case when changing outcomes.

Describe the rule edition and whether a behavior is a house rule. Preserve the distinction between a natural die and a modified total. GUI changes should keep negative attack modifiers usable and report invalid input without retaining an old result.
