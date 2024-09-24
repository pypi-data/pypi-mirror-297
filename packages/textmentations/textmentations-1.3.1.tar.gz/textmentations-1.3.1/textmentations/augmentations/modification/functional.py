from __future__ import annotations

import itertools
import math
import random

import numpy as np

from textmentations.augmentations.utils import SPACE, _squeeze_first, autopsy_sentence, autopsy_text, pass_empty_text
from textmentations.corpora.types import Corpus, Sentence, Text, Word
from textmentations.corpora.utils import get_random_synonym, is_stopword


@pass_empty_text
def delete_words(text: Text, deletion_prob: float, min_words_per_sentence: float | int) -> Text:
    """Randomly deletes words in the text.

    Args:
        text: The input text.
        deletion_prob: The probability of deleting a word.
        min_words_per_sentence:
            If a `float`, it is the minimum proportion of words to retain in each sentence.
            If an `int`, it is the minimum number of words in each sentence.

    Returns:
        A text with randomly deleted words.

    Examples:
        >>> import textmentations.augmentations.modification.functional as fm
        >>> text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
        >>> deletion_prob = 0.1
        >>> min_words_per_sentence = 0.8
        >>> augmented_text = fm.delete_words(text, deletion_prob, min_words_per_sentence)
    """
    return _delete_words(text, deletion_prob, min_words_per_sentence)


@autopsy_text
def _delete_words(
    sentences: list[Sentence],
    deletion_prob: float,
    min_words_per_sentence: float | int,
) -> list[Sentence]:
    """Randomly deletes words in each sentence."""
    return [
        augmented_sentence
        for sentence in sentences
        if (augmented_sentence := _delete_words_in_sentence(sentence, deletion_prob, min_words_per_sentence))
    ]


@autopsy_sentence
def _delete_words_in_sentence(words: list[Word], deletion_prob: float, min_words: float | int) -> list[Word]:
    """Randomly deletes words in the list of words."""
    return _delete_strings(words, deletion_prob, min_words)


def _delete_strings(strings: list[Corpus], deletion_prob: float, min_strings: float | int) -> list[Corpus]:
    """Randomly deletes strings in the list of strings."""
    num_strings = len(strings)
    min_strings = math.ceil(num_strings * min_strings) if isinstance(min_strings, float) else min_strings
    if num_strings <= min_strings:
        return strings
    indices_to_retain = set()
    num_possible_deletions = num_strings - min_strings
    shuffled_indices = np.random.permutation(num_strings).tolist()
    for index in shuffled_indices:
        if random.random() < deletion_prob and num_possible_deletions > 0:
            num_possible_deletions -= 1
            continue
        indices_to_retain.add(index)
    augmented_strings = [string for index, string in enumerate(strings) if index in indices_to_retain]
    return augmented_strings


@pass_empty_text
def delete_sentences(text: Text, deletion_prob: float, min_sentences: float | int) -> Text:
    """Randomly deletes sentences in the text.

    Args:
        text: The input text.
        deletion_prob: The probability of deleting a sentence.
        min_sentences:
            If a `float`, it is the minimum proportion of sentences to retain in the text.
            If an `int`, it is the minimum number of sentences in the text.

    Returns:
        A text with randomly deleted sentences.

    Examples:
        >>> import textmentations.augmentations.modification.functional as fm
        >>> text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
        >>> deletion_prob = 0.05
        >>> min_sentences = 0.9
        >>> augmented_text = fm.delete_sentences(text, deletion_prob, min_sentences)
    """
    return _delete_sentences(text, deletion_prob, min_sentences)


@autopsy_text
def _delete_sentences(
    sentences: list[Sentence],
    deletion_prob: float,
    min_sentences: float | int,
) -> list[Sentence]:
    """Randomly deletes sentences in the list of sentences."""
    return _delete_strings(sentences, deletion_prob, min_sentences)


@pass_empty_text
def insert_synonyms(text: Text, insertion_prob: float, n_times: int) -> Text:
    """Repeats n times the task of randomly inserting synonyms of words that are not stopwords in the text.

    Args:
        text: The input text.
        insertion_prob: The probability of inserting a synonym.
        n_times: The number of times to repeat the synonym-insertion process.

    Returns:
        A text with randomly inserted synonyms.

    Examples:
        >>> import textmentations.augmentations.modification.functional as fm
        >>> text = "물 한 잔만 주세요."
        >>> insertion_prob = 0.2
        >>> n_times = 1
        >>> augmented_text = fm.insert_synonyms(text, insertion_prob, n_times)
    """
    return _insert_synonyms(text, insertion_prob, n_times)


@autopsy_text
def _insert_synonyms(sentences: list[Sentence], insertion_prob: float, n_times: int) -> list[Sentence]:
    """Repeats n times the task of randomly inserting synonyms of words that are not stopwords in each sentence."""
    return [_insert_synonyms_in_sentence(sentence, insertion_prob, n_times) for sentence in sentences]


@autopsy_sentence
def _insert_synonyms_in_sentence(words: list[Word], insertion_prob: float, n_times: int) -> list[Word]:
    """Repeats n times the task of randomly inserting synonyms of words that are not stopwords in the list of words."""
    for _ in range(n_times):
        words = _insert_synonyms_in_words(words, insertion_prob)
    return words


def _insert_synonyms_in_words(
    words: list[Word],
    insertion_prob: float,
) -> list[Word]:
    """Randomly inserts synonyms of words that are not stopwords in the list of words."""
    num_words = len(words)
    augmented_words = [[word] for word in words]
    shuffled_indices = np.random.permutation(num_words).tolist()
    for index in shuffled_indices:
        word = words[index]
        if is_stopword(word) or random.random() >= insertion_prob:
            continue
        synonym = get_random_synonym(word)
        if synonym == word:
            continue
        insertion_index = random.randrange(0, num_words)
        augmented_words[insertion_index].append(synonym)
    return [*itertools.chain(*augmented_words)]  # flatten the list of lists


@pass_empty_text
def insert_punctuation(text: Text, insertion_prob: float, punctuation: tuple[str, ...]) -> Text:
    """Randomly inserts punctuation in the text.

    Args:
        text: The input text.
        insertion_prob: The probability of inserting a punctuation mark.
        punctuation: Punctuation to be inserted at random.

    Returns:
        A text with randomly inserted punctuation.

    Examples:
        >>> import textmentations.augmentations.modification.functional as fm
        >>> text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
        >>> insertion_prob = 0.2
        >>> punctuation = (".", ";", "?", ":", "!", ",")
        >>> augmented_text = fm.insert_punctuation(text, insertion_prob, punctuation)
    """
    return _insert_punctuation(text, insertion_prob, punctuation)


@autopsy_text
def _insert_punctuation(
    sentences: list[Sentence],
    insertion_prob: float,
    punctuation: tuple[str, ...],
) -> list[Sentence]:
    """Randomly inserts punctuation in each sentence."""
    return [_insert_punctuation_in_sentence(sentence, insertion_prob, punctuation) for sentence in sentences]


@autopsy_sentence
def _insert_punctuation_in_sentence(
    words: list[Word],
    insertion_prob: float,
    punctuation: tuple[str, ...],
) -> list[Word]:
    """Randomly inserts punctuation in the list of words."""
    return [_insert_punctuation_mark_into_word(word, insertion_prob, punctuation) for word in words]


def _insert_punctuation_mark_into_word(word: Word, insertion_prob: float, punctuation: tuple[str, ...]) -> Word:
    """Randomly inserts a punctuation mark at the beginning of a word."""
    if random.random() < insertion_prob:
        punctuation_mark = random.choice(punctuation)
        word_with_punctuation_mark = SPACE.join([punctuation_mark, word])
        return word_with_punctuation_mark
    return word


@pass_empty_text
def replace_synonyms(text: Text, replacement_prob: float) -> Text:
    """Randomly replaces words that are not stopwords in the text with synonyms.

    Args:
        text: The input text.
        replacement_prob: The probability of replacing a word with a synonym.

    Returns:
        A text with random words replaced by synonyms.

    Examples:
        >>> import textmentations.augmentations.modification.functional as fm
        >>> text = "물 한 잔만 주세요."
        >>> replacement_prob = 0.2
        >>> augmented_text = fm.replace_synonyms(text, replacement_prob)
    """
    return _replace_synonyms(text, replacement_prob)


@autopsy_text
def _replace_synonyms(sentences: list[Sentence], replacement_prob: float) -> list[Sentence]:
    """Randomly replaces words that are not stopwords in each sentence with synonyms."""
    return [_replace_synonyms_in_sentence(sentence, replacement_prob) for sentence in sentences]


@autopsy_sentence
def _replace_synonyms_in_sentence(words: list[Word], replacement_prob: float) -> list[Word]:
    """Randomly replaces words that are not stopwords in the list of words with synonyms."""
    return [_replace_word_with_synonym(word, replacement_prob) for word in words]


def _replace_word_with_synonym(word: Word, replacement_prob: float) -> Word:
    """Randomly replaces word that is not stopword with synonym."""
    if not is_stopword(word) and random.random() < replacement_prob:
        synonym = get_random_synonym(word)
        return synonym
    return word


@pass_empty_text
def swap_words(text: Text, alpha: float | int) -> Text:
    """Repeats n times the task of randomly swapping two words in a randomly selected sentence from the text.

    Args:
        text: The input text.
        alpha:
            If a `float`, it is the number of times to repeat the process is calculated as `N = alpha * L`,
            where `L` is the length of the text.
            If an `int`, it is the number of times to repeat the process.

    Returns:
        A text with randomly shuffled words each sentence.

    Examples:
        >>> import textmentations.augmentations.modification.functional as fm
        >>> text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
        >>> alpha = 0.1
        >>> augmented_text = fm.swap_words(text, alpha)
    """
    n_times = math.ceil(len(text) * alpha) if isinstance(alpha, float) else alpha
    return _swap_words(text, n_times)


@autopsy_text
def _swap_words(sentences: list[Sentence], n_times: int) -> list[Sentence]:
    """Repeats n times the task of randomly swapping two words in a randomly selected sentence."""
    num_sentences = len(sentences)
    sentence_lengths = [*map(len, sentences)]
    for _ in range(n_times):
        indices = random.choices(range(num_sentences), weights=sentence_lengths, k=1)
        index = _squeeze_first(indices)
        sentences[index] = _swap_two_words_in_sentence(sentences[index])
    return sentences


@autopsy_sentence
def _swap_two_words_in_sentence(words: list[Word]) -> list[Word]:
    """Randomly swaps two words in the list of words."""
    return _swap_two_strings(words)


def _swap_two_strings(strings: list[Corpus]) -> list[Corpus]:
    """Randomly swaps two strings in the list of strings."""
    num_strings = len(strings)
    if num_strings >= 2:
        index1, index2 = random.sample(range(num_strings), k=2)
        strings[index1], strings[index2] = strings[index2], strings[index1]
    return strings


@pass_empty_text
def swap_sentences(text: Text, n_times: int) -> Text:
    """Repeats n times the task of randomly swapping two sentences in the text.

    Args:
        text: The input text.
        n_times: The number of times to repeat the process.

    Returns:
        A text with randomly shuffled sentences.

    Examples:
        >>> import textmentations.augmentations.modification.functional as fm
        >>> text = "짜장면을 맛있게 먹었다. 짬뽕도 맛있게 먹었다. 짬짜면도 먹고 싶었다."
        >>> n_times = 1
        >>> augmented_text = fm.swap_sentences(text, n_times)
    """
    return _swap_sentences(text, n_times)


@autopsy_text
def _swap_sentences(sentences: list[Sentence], n_times: int) -> list[Sentence]:
    """Repeats n times the task of randomly swapping two sentences in the list of sentences."""
    for _ in range(n_times):
        sentences = _swap_two_strings(sentences)
    return sentences
