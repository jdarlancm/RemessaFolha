import unicodedata
import re


def remove_accents_and_special_characters(text):
    without_accents = "".join(
        letra
        for letra in unicodedata.normalize("NFD", text)
        if unicodedata.category(letra) != "Mn"
    )
    without_special_char = re.sub(r"[^a-zA-Z0-9\s]", "", without_accents)

    return without_special_char
