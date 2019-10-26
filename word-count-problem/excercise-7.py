import operator
import sys
import pprint

import common

DEFAULT_WORD = 'yes'


def get_first_arg():
    try:
        return sys.argv[1]
    except IndexError:
        return DEFAULT_WORD


def main():
    lines = tuple(common.read_lines_from_file("data/pride-and-prejudice.txt"))
    lines_per_chapter = common.split_lines_into_chapters(lines)
    words_per_chapter = [
        tuple(common.extract_words_from_lines(lines))
        for lines in lines_per_chapter
    ]

    checked_word = get_first_arg()

    weights_in_chapters = []
    for chapter_idx, words in enumerate(words_per_chapter, 1):
        weight_in_chapter = common.tf_idf_weights(checked_word, words,
                                                  words_per_chapter)
        weights_in_chapters.append(
            'chapter=%s,weight=%s,count=%s' %
            (chapter_idx, weight_in_chapter, words.count(checked_word)))

    pprint.pprint(sorted(weights_in_chapters, key=operator.itemgetter(1)))


if __name__ == "__main__":
    main()