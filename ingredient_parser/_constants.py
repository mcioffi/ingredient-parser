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
    "pts": "pt",
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
    "tins": "tin",
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

# Words that can modify a unit
UNIT_MODIFIERS = [
    "big",
    "fat",
    "generous",
    "healthy",
    "heaped",
    "heaping",
    "large",
    "medium",
    "medium-size",
    "medium-sized",
    "scant",
    "small",
    "thick",
    "thin",
]

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
    "ten": "10",
    "eleven": "11",
    "twelve": "12",
    "thirteen": "13",
    "fourteen": "14",
    "fifteen": "15",
    "sixteen": "16",
    "seventeen": "17",
    "eighteen": "18",
    "nineteen": "19",
}
# Precompile the regular expressions for matching the string numbers
STRING_NUMBERS_REGEXES = {}
for s, n in STRING_NUMBERS.items():
    # This is case insensitive so it replace e.g. "one" and "One"
    # Only match if the string is preceded by a non-word character or is at
    # the start of the sentence
    STRING_NUMBERS_REGEXES[s] = (re.compile(rf"\b({s})\b", flags=re.IGNORECASE), n)

# Unicode fractions and their replacements as fake fractions
# Most of the time we need to insert a space in front of the replacement so we don't
# merge the replacement with the previous token i.e. 1½ != 11/2
# However, if the prior chaacter is a hyphen, we don't want to insert a space as this
# will mess up any ranges
UNICODE_FRACTIONS = {
    "-\u215b": "-1/8",
    "-\u215c": "-3/8",
    "-\u215d": "-5/8",
    "-\u215e": "-7/8",
    "-\u2159": "-1/6",
    "-\u215a": "-5/6",
    "-\u2155": "-1/5",
    "-\u2156": "-2/5",
    "-\u2157": "-3/5",
    "-\u2158": "-4/5",
    "-\xbc": "-1/4",
    "-\xbe": "-3/4",
    "-\u2153": "-1/3",
    "-\u2154": "-2/3",
    "-\xbd": "-1/2",
    "\u215b": " 1/8",
    "\u215c": " 3/8",
    "\u215d": " 5/8",
    "\u215e": " 7/8",
    "\u2159": " 1/6",
    "\u215a": " 5/6",
    "\u2155": " 1/5",
    "\u2156": " 2/5",
    "\u2157": " 3/5",
    "\u2158": " 4/5",
    "\xbc": " 1/4",
    "\xbe": " 3/4",
    "\u2153": " 1/3",
    "\u2154": " 2/3",
    "\xbd": " 1/2",
}
