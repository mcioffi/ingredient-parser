#!/usr/bin/env python3

import re

# Plural and singular units
UNITS = {
    "bags": "bag",
    "bars": "bar",
    "baskets": "basket",
    "batches": "batch",
    "blocks": "block",
    "bottles": "bottle",
    "boxes": "box",
    "branches": "branch",
    "bulbs": "bulb",
    "bunches": "bunch",
    "bundles": "bundle",
    "cans": "can",
    "chops": "chop",
    "chunks": "chunk",
    "cloves": "clove",
    "clusters": "cluster",
    "cm": "cm",
    "cubes": "cube",
    "cups": "cup",
    "cutlets": "cutlet",
    "dashes": "dash",
    "dollops": "dollop",
    "drops": "drop",
    "ears": "ear",
    "envelopes": "envelope",
    "feet": "foot",
    "fillets": "fillet",
    "g": "g",
    "gallons": "gallon",
    "glasses": "glass",
    "grams": "gram",
    "grinds": "grind",
    "handfuls": "handful",
    "heads": "head",
    "inches": "inch",
    "jars": "jar",
    "kg": "kg",
    "kilograms": "kilogram",
    "knobs": "knob",
    "lbs": "lb",
    "leaves": "leaf",
    "lengths": "length",
    "links": "link",
    "l": "l",
    "liters": "liter",
    "litres": "litre",
    "loaves": "loaf",
    "milliliters": "milliliter",
    "ml": "ml",
    "mugs": "mug",
    "ounces": "ounce",
    "oz": "oz",
    "packs": "pack",
    "packages": "package",
    "packets": "packet",
    "pairs": "pair",
    "pieces": "piece",
    "pinches": "pinch",
    "pints": "pint",
    "pods": "pod",
    "pounds": "pound",
    "racks": "rack",
    "rashers": "rasher",
    "recipes": "recipe",
    "rectangles": "rectangle",
    "ribs": "rib",
    "quarts": "quart",
    "scoops": "scoop",
    "segments": "segment",
    "shakes": "shake",
    "sheets": "sheet",
    "shots": "shot",
    "shoots": "shoot",
    "slabs": "slab",
    "slices": "slice",
    "sprigs": "sprig",
    "squares": "square",
    "stalks": "stalk",
    "steaks": "steak",
    "stems": "stem",
    "sticks": "stick",
    "strips": "strip",
    "tablespoons": "tablespoon",
    "tbsps": "tbsp",
    "tbs": "tb",
    "teaspoons": "teaspoon",
    "tsps": "tsp",
    "twists": "twist",
    "wedges": "wedge",
    "wheels": "wheel",
}
# Generate capitalized version of each entry in the UNITS dictionary
_capitalized_units = {}
for plural, singular in UNITS.items():
    _capitalized_units[plural.capitalize()] = singular.capitalize()
UNITS = UNITS | _capitalized_units


# Units that can be part of the name
# e.g. 1 teaspoon ground cloves, or 5 bay leaves
AMBIGUOUS_UNITS = [
    "cloves",
    "leaves",
    "slabs",
    "wedges",
]
# Extend list automatically to include singular and capitalized forms
_ambiguous_units_alt_forms = []
for amb_unit in AMBIGUOUS_UNITS:
    _ambiguous_units_alt_forms.append(amb_unit.capitalize())
    _ambiguous_units_alt_forms.append(UNITS[amb_unit])
    _ambiguous_units_alt_forms.append(UNITS[amb_unit.capitalize()])

AMBIGUOUS_UNITS.extend(_ambiguous_units_alt_forms)


# Strings and their numeric representation
STRING_NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}
# Precompile the regular expressions for matching the string numbers
STRING_NUMBERS_REGEXES = {}
for s, n in STRING_NUMBERS.items():
    # This is case insensitive so it replace e.g. "one" and "One"
    # Only match if the string is preceeded by a non-word character or is at
    # the start of the sentence
    STRING_NUMBERS_REGEXES[s] = (re.compile(rf"\b({s})\b", flags=re.IGNORECASE), n)

# Stop words - high frequency grammatrical words
# Taken from nltk.corpus.stopwords
STOP_WORDS = [
    "i",
    "me",
    "my",
    "myself",
    "we",
    "our",
    "ours",
    "ourselves",
    "you",
    "you're",
    "you've",
    "you'll",
    "you'd",
    "your",
    "yours",
    "yourself",
    "yourselves",
    "he",
    "him",
    "his",
    "himself",
    "she",
    "she's",
    "her",
    "hers",
    "herself",
    "it",
    "it's",
    "its",
    "itself",
    "they",
    "them",
    "their",
    "theirs",
    "themselves",
    "what",
    "which",
    "who",
    "whom",
    "this",
    "that",
    "that'll",
    "these",
    "those",
    "am",
    "is",
    "are",
    "was",
    "were",
    "be",
    "been",
    "being",
    "have",
    "has",
    "had",
    "having",
    "do",
    "does",
    "did",
    "doing",
    "a",
    "an",
    "the",
    "and",
    "but",
    "if",
    "or",
    "because",
    "as",
    "until",
    "while",
    "of",
    "at",
    "by",
    "for",
    "with",
    "about",
    "against",
    "between",
    "into",
    "through",
    "during",
    "before",
    "after",
    "above",
    "below",
    "to",
    "from",
    "up",
    "down",
    "in",
    "out",
    "on",
    "off",
    "over",
    "under",
    "again",
    "further",
    "then",
    "once",
    "here",
    "there",
    "when",
    "where",
    "why",
    "how",
    "all",
    "any",
    "both",
    "each",
    "few",
    "more",
    "most",
    "other",
    "some",
    "such",
    "no",
    "nor",
    "not",
    "only",
    "own",
    "same",
    "so",
    "than",
    "too",
    "very",
    "s",
    "t",
    "can",
    "will",
    "just",
    "don",
    "don't",
    "should",
    "should've",
    "now",
    "d",
    "ll",
    "m",
    "o",
    "re",
    "ve",
    "y",
    "ain",
    "aren",
    "aren't",
    "couldn",
    "couldn't",
    "didn",
    "didn't",
    "doesn",
    "doesn't",
    "hadn",
    "hadn't",
    "hasn",
    "hasn't",
    "haven",
    "haven't",
    "isn",
    "isn't",
    "ma",
    "mightn",
    "mightn't",
    "mustn",
    "mustn't",
    "needn",
    "needn't",
    "shan",
    "shan't",
    "shouldn",
    "shouldn't",
    "wasn",
    "wasn't",
    "weren",
    "weren't",
    "won",
    "won't",
    "wouldn",
    "wouldn't",
]
