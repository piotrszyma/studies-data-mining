import pathlib
import collections
import random

import wordcloud

import common


def main():
    lines = common.read_lines_from_file("data/pride-and-prejudice.txt")
    words = tuple(common.extract_words_from_lines(lines))

    word_to_next_words = collections.defaultdict(list)

    for word, next_word in zip(words[:-1], words[1:]):
        word_to_next_words[word].append(next_word)

    word_to_most_common = {}

    for word, next_words in word_to_next_words.items():
        most_common = collections.Counter(next_words).most_common(5)
        word_to_most_common[word] = tuple(w[0] for w in most_common)

    sentence_len = 5
    next_word = random.choice(tuple(word_to_most_common))
    sentence = []

    for _ in range(sentence_len):
        sentence.append(next_word)
        next_word = random.choice(tuple(word_to_most_common[next_word]))

    print(' '.join(sentence).capitalize() + '.')


if __name__ == "__main__":
    main()