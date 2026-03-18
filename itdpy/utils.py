from __future__ import annotations

import random

_WORDS = [
    "cat", "dog", "fox", "wolf", "bear", "bird", "fish", "frog",
    "lion", "tiger", "eagle", "shark", "snake", "horse", "deer",
    "moon", "star", "sun", "sky", "rain", "snow", "wind", "fire",
    "rock", "stone", "river", "lake", "tree", "leaf", "rose",
    "blue", "red", "dark", "light", "cold", "fast", "cool", "wild",
    "steel", "iron", "gold", "silver", "black", "white", "gray",
    "ninja", "pixel", "cyber", "nova", "zero", "flux", "echo",
    "delta", "alpha", "sigma", "omega", "prime", "ghost", "storm",
]


def random_username(word: str | None = None, digits: int | None = None) -> str:
    """
    Генерирует случайный юзернейм вида word123.

    Параметры:
        word   — конкретное слово (по умолчанию случайное)
        digits — количество цифр от 3 до 5 (по умолчанию случайное)

    Пример:
        random_username()           # "fox4821"
        random_username("cyber")    # "cyber391"
        random_username(digits=3)   # "wolf742"
    """
    w = word or random.choice(_WORDS)
    d = digits or random.randint(3, 5)
    number = random.randint(10 ** (d - 1), 10 ** d - 1)
    return f"{w}{number}"
