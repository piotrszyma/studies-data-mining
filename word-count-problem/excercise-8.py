import pathlib
import collections

import wordcloud

import common


def main():
    lines = common.read_lines_from_file("data/pride-and-prejudice.txt")
    words = tuple(common.extract_words_from_lines(lines))

    word_to_next_words = collections.defaultdict(list)

    for word, next_word in zip(words[:-1], words[1:]):
        if len(word) == 1:
            import pdb
            pdb.set_trace()
        word_to_next_words[word].append(next_word)

    word_to_most_common = {}

    for word, next_words in word_to_next_words.items():
        most_common = collections.Counter(next_words).most_common()

        if len(most_common) < 5:
            print(most_common)
        else:
            word_to_most_common[word] = most_common

    import pdb
    pdb.set_trace()


if __name__ == "__main__":
    main()