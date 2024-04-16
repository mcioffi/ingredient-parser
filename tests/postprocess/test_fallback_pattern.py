import pint
import pytest

from ingredient_parser.en import PostProcessor
from ingredient_parser.en._utils import create_ingredient_amount


@pytest.fixture
def p():
    """Define a PostProcessor object to use for testing the PostProcessor
    class methods.
    """
    sentence = "2 14 ounce cans coconut milk"
    tokens = ["2", "14", "ounce", "can", "coconut", "milk"]
    labels = ["QTY", "QTY", "UNIT", "UNIT", "NAME", "NAME"]
    scores = [
        0.9991370577083561,
        0.9725378063405858,
        0.9978510889596651,
        0.9922350007952175,
        0.9886087821704076,
        0.9969237827902526,
    ]

    return PostProcessor(sentence, tokens, labels, scores)


class TestPostProcessor_fallback_pattern:
    def test_basic(self, p):
        """
        Test that a single IngredientAmount object with quantity "3" and
        unit "large handfuls" is returned.
        """

        tokens = ["3", "large", "handful", "cherry", "tomatoes"]
        labels = ["QTY", "UNIT", "UNIT", "NAME", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="3",
                unit="large handfuls",
                text="3 large handfuls",
                confidence=0,
                starting_index=0,
            )
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_comma_before_unit(self, p):
        """
        Test that a single IngredientAmount object with no quantity and
        unit "large" is returned.
        """

        tokens = ["1", "green", ",", "large", "pepper"]
        labels = ["QTY", "NAME", "PUNC", "UNIT", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="1",
                unit="large",
                text="1 large",
                confidence=0,
                starting_index=0,
            )
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_no_quantity(self, p):
        """
        Test that a single IngredientAmount object with no quantity and
        unit "bunch" is returned.
        """

        tokens = ["bunch", "of", "basil", "leaves"]
        labels = ["UNIT", "COMMENT", "NAME", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="", unit="bunch", text="bunch", confidence=0, starting_index=0
            )
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_imperial(self):
        """
        Test that imperial units are returned for 'cup'
        """
        p = PostProcessor("", [], [], [], imperial_units=True)
        tokens = ["About", "2", "cup", "flour"]
        labels = ["COMMENT", "QTY", "UNIT", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="2",
                unit=pint.Unit("imperial_cup"),
                text="2 cups",
                confidence=0,
                starting_index=1,
                APPROXIMATE=True,
            )
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_string_units(self):
        """
        Test that the returned unit is 'cups'
        """
        p = PostProcessor("", [], [], [], string_units=True)
        tokens = ["About", "2", "cup", "flour"]
        labels = ["COMMENT", "QTY", "UNIT", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="2",
                unit="cups",
                text="2 cups",
                confidence=0,
                starting_index=1,
                APPROXIMATE=True,
            )
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_approximate(self, p):
        """
        Test that a single IngredientAmount object with the APPROXIMATE flag set
        is returned
        """
        tokens = ["About", "2", "cup", "flour"]
        labels = ["COMMENT", "QTY", "UNIT", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="2",
                unit=pint.Unit("cup"),
                text="2 cups",
                confidence=0,
                starting_index=1,
                APPROXIMATE=True,
            )
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_singular(self, p):
        """
        Test that a single IngredientAmount object with the SINGULAR flag set
        is returned
        """
        tokens = ["2", "bananas", ",", "4", "ounce", "each"]
        labels = ["QTY", "NAME", "PUNC", "QTY", "UNIT", "COMMENT"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        p.consumed = [0, 1, 2, 3]

        expected = [
            create_ingredient_amount(
                quantity="2",
                unit="",
                text="2",
                confidence=0,
                starting_index=0,
            ),
            create_ingredient_amount(
                quantity="4",
                unit=pint.Unit("ounces"),
                text="4 ounces",
                confidence=0,
                starting_index=3,
                SINGULAR=True,
                APPROXIMATE=False,
            ),
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_singular_and_approximate(self, p):
        """
        Test that a single IngredientAmount object with the APPROXIMATE and
        SINGULAR flags set is returned
        """
        tokens = ["2", "bananas", ",", "each", "about", "4", "ounce"]
        labels = ["QTY", "NAME", "PUNC", "COMMENT", "COMMENT", "QTY", "UNIT"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="2",
                unit="",
                text="2",
                confidence=0,
                starting_index=0,
            ),
            create_ingredient_amount(
                quantity="4",
                unit=pint.Unit("ounces"),
                text="4 ounces",
                confidence=0,
                starting_index=5,
                SINGULAR=True,
                APPROXIMATE=True,
            ),
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_dozen(self, p):
        """
        Test that the token "dozen" is combined with the preceding QTY token in a
        single IngredientAmount object.
        """
        tokens = ["2", "dozen", "bananas", ",", "each", "about", "4", "ounce"]
        labels = ["QTY", "QTY", "NAME", "PUNC", "COMMENT", "COMMENT", "QTY", "UNIT"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="2 dozen",
                unit="",
                text="2 dozen",
                confidence=0,
                starting_index=0,
            ),
            create_ingredient_amount(
                quantity="4",
                unit=pint.Unit("ounces"),
                text="4 ounces",
                confidence=0,
                starting_index=6,
                SINGULAR=True,
                APPROXIMATE=True,
            ),
        ]

        assert p._fallback_pattern(idx, tokens, labels, scores) == expected

    def test_range(self, p):
        """
        Test that the range 1-2 is correctly parsed to set the RANGE flag and
        quantity_max fields in the IngredientAmount object
        """
        tokens = ["1-2", "tablespoons", "local", "honey"]
        labels = ["QTY", "UNIT", "NAME", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="1-2",
                unit=pint.Unit("tablespoon"),
                text="1-2 tablespoons",
                confidence=0,
                starting_index=0,
            ),
        ]

        actual = p._fallback_pattern(idx, tokens, labels, scores)
        assert actual == expected
        assert actual[0].RANGE
        assert actual[0].quantity == 1
        assert actual[0].quantity_max == 2

    def test_multiplier(self, p):
        """
        Test that the multiplier "1x" is correctly parsed to set the MULTIPLIER
        flag, quantity and quantity_max fields in the IngredientAmount object
        """
        tokens = ["1x", "tin", "condensed", "milk"]
        labels = ["QTY", "UNIT", "NAME", "NAME"]
        scores = [0] * len(tokens)
        idx = list(range(len(tokens)))

        expected = [
            create_ingredient_amount(
                quantity="1x",
                unit="tin",
                text="1x tin",
                confidence=0,
                starting_index=0,
            ),
        ]

        actual = p._fallback_pattern(idx, tokens, labels, scores)
        assert actual == expected
        assert actual[0].MULTIPLIER
        assert actual[0].quantity == 1
