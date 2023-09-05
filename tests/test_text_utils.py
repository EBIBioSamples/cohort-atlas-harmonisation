from harmonise.text_utils import clean_text, tokenize_text
from assertpy import assert_that


def test_clean_text():
    text_to_clean = 'PersonPortrait.residencyCountry'
    cleaned_text = clean_text(text_to_clean)
    assert_that(cleaned_text).is_equal_to('personportrait.residencycountry')


def test_tokenize_text():
    text_to_clean = 'PersonPortrait.residencyCountry'
    cleaned_text = tokenize_text(text_to_clean)
    assert_that(cleaned_text).is_equal_to(['Person', 'Portrait', 'residency', 'Country'])
