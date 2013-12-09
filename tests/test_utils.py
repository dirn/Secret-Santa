"""Tests for xmas.utils."""

from xmas import utils


def test_slugify():
    """Test `slugify()`."""
    expected = 'slug'
    actual = utils.slugify('SLUG')
    assert actual == expected

    expected = 'slug'
    actual = utils.slugify('slug')
    assert actual == expected

    expected = 'slug'
    actual = utils.slugify('Slug')
    assert actual == expected

    expected = 'slug'
    actual = utils.slugify('sLuG')
    assert actual == expected

    expected = 'two-words'
    actual = utils.slugify('Two Words')
    assert actual == expected

def test_slugify_edges():
    """Test `slugify()` for some edge cases."""
    expected = 'before'
    actual = utils.slugify(' before')
    assert actual == expected

    expected = 'after'
    actual = utils.slugify('after ')
    assert actual == expected

    expected = 'repeated-repeated'
    actual = utils.slugify('repeated .,!& repeated')
    assert actual == expected

    expected = 'a-sentence-with-punctuation'
    actual = utils.slugify('A sentence, with punctuation.')
    assert actual == expected
