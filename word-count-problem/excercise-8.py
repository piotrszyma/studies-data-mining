import collections
import pathlib
import random
import sys

import wordcloud

import common

MIN_SEN_LEN = 4
MAX_SEN_LEN = 7


def get_random_sentence(word_to_most_common):
    sentence_len = random.randint(MIN_SEN_LEN, MAX_SEN_LEN)
    next_word = random.choice(tuple(word_to_most_common))
    sentence = []

    for _ in range(sentence_len):
        sentence.append(next_word)
        next_word = random.choice(tuple(word_to_most_common[next_word]))

    return ' '.join(sentence).capitalize() + '.'


def read_no_sentences_from_argv():
    try:
        return int(sys.argv[1])
    except (ValueError, IndexError):
        return None


def main():
    no_sentences = read_no_sentences_from_argv() or 1

    lines = common.read_lines_from_file("data/pride-and-prejudice.txt")
    words = tuple(common.extract_words_from_lines(lines))

    word_to_next_words = collections.defaultdict(list)

    for word, next_word in zip(words[:-1], words[1:]):
        word_to_next_words[word].append(next_word)

    word_to_most_common = {}

    for word, next_words in word_to_next_words.items():
        most_common = collections.Counter(next_words).most_common(5)
        word_to_most_common[word] = tuple(w[0] for w in most_common)

    for _ in range(no_sentences):
        print(get_random_sentence(word_to_most_common))


if __name__ == "__main__":
    main()