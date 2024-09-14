from ingredient_parser.en import PreProcessor
from ingredient_parser.en._foundationfoods import extract_foundation_foods


class Teste_extract_foundation_foods:
    def test_extract(self):
        p = PreProcessor("1 cup finely chopped red onion")
        tokens = p.tokenized_sentence
        features = p.sentence_features()
        labels = ["QTY", "UNIT", "PREP", "PREP", "NAME", "NAME"]

        assert extract_foundation_foods(tokens, labels, features) == ["red onion"]

    def test_no_FF_token(self):
        p = PreProcessor("1 cup finely chopped")
        tokens = p.tokenized_sentence
        features = p.sentence_features()
        labels = ["QTY", "UNIT", "PREP", "PREP"]

        assert extract_foundation_foods(tokens, labels, features) is None
