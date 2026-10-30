import json
import subprocess
import sys
import unittest

from attacks import probabilities, resolve, simulate


class AttacksTests(unittest.TestCase):
    def test_natural_one_misses_even_with_large_bonus(self):
        self.assertFalse(resolve([1], 100, 5).hit)
        self.assertTrue(resolve([1], 100, 5).natural_one)

    def test_natural_twenty_hits_even_with_large_ac(self):
        self.assertTrue(resolve([20], -100, 100).hit)
        self.assertTrue(resolve([20], -100, 100).critical)

    def test_only_selected_die_determines_critical(self):
        self.assertFalse(resolve([20, 2], 5, 15, "disadvantage").critical)
        self.assertTrue(resolve([20, 2], 5, 15, "advantage").critical)
        self.assertFalse(resolve([1, 19], 5, 15, "advantage").natural_one)

    def test_known_hit_probabilities(self):
        self.assertAlmostEqual(probabilities(5, 15)["hit"], 0.55)
        self.assertAlmostEqual(probabilities(5, 15, "advantage")["hit"], 1 - 0.45**2)
        self.assertAlmostEqual(probabilities(5, 15, "disadvantage")["hit"], 0.55**2)
        self.assertAlmostEqual(
            probabilities(5, 15, "three-dice")["critical"], 1 - 0.95**3
        )

    def test_d4_never_overrides_natural_one(self):
        self.assertFalse(resolve([1], 100, 5, extra=4).hit)
        self.assertGreater(probabilities(5, 15, bonus_die=True)["hit"], 0.55)

    def test_seeded_rolls_reproduce(self):
        self.assertEqual(
            simulate(5, 15, count=20, seed=42), simulate(5, 15, count=20, seed=42)
        )

    def test_bounds(self):
        for count in (0, -1, 1001, True):
            with self.assertRaises(ValueError):
                simulate(5, 15, count=count)
        for dice in ([0], [21], [True], []):
            with self.assertRaises(ValueError):
                resolve(dice, 5, 15)

    def test_cli_and_import(self):
        result = subprocess.run(
            [
                sys.executable,
                "attacks.py",
                "--bonus",
                "5",
                "--ac",
                "15",
                "--seed",
                "42",
                "--count",
                "3",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertEqual(len(json.loads(result.stdout)["attacks"]), 3)
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import main, tkinter; assert tkinter._default_root is None",
            ]
        )
        self.assertEqual(result.returncode, 0)
