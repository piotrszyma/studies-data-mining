import collections
import math
import string

from typing import Text, Sequence

from stemming.porter2 import stem
import wordcloud

import common


def create_clouds_for_whole_document(lines):
    words = common.extract_words_from_lines(lines)
    words_count = collections.Counter(words)
    cloud = wordcloud.WordCloud(background_color="white", max_words=20000)
    cloud.generate_from_frequencies(words_count)
    cloud.to_file("clouds/all_words_cloud.png")


def create_clouds_for_chapters(chapter_lines):
    for chapter_idx, chapter_lines in enumerate(chapters_lines, 1):
        words = common.extract_words_from_lines(chapter_lines)
        words_count = collections.Counter(words)
        cloud = wordcloud.WordCloud(background_color="white", max_words=20000)
        cloud.generate_from_frequencies(words_count)
        cloud.to_file(f"clouds/counts/chapter_{chapter_idx}_cloud.png")


def create_weighted_clouds_for_chapters(chapter_lines):
    chapters_words = [
        tuple(common.extract_words_from_lines(chapter_lines))
        for chapter_lines in chapters_lines
    ]

    for chapter_idx, words_in_chapter in enumerate(chapters_words, 1):
        words_in_chapter_weights = {}
        for word in set(words_in_chapter):
            words_in_chapter_weights[word] = (tf_idf_weights(
                word, words_in_chapter, chapters_words))

        cloud = wordcloud.WordCloud(background_color="white", max_words=20000)
        cloud.generate_from_frequencies(words_in_chapter_weights)
        cloud.to_file(f"clouds/tf_idf/chapter_{chapter_idx}_cloud.png")


def create_weighted_cloud_for_book():
    ...


def main():
    lines = tuple(common.read_lines_from_file("data/pride-and-prejudice.txt"))


if __name__ == "__main__":
    main()
