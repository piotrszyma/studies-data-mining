import collections
import pathlib

import wordcloud

import common


def main():
    lines = tuple(common.read_lines_from_file("data/pride-and-prejudice.txt"))

    lines_per_chapter = common.split_lines_into_chapters(lines)

    words_per_chapter = [
        tuple(common.extract_words_from_lines(lines))
        for lines in lines_per_chapter
    ]

    # For each document separately build a word cloud
    # using obtained tf-idf weights.
    for chapter_idx, words in enumerate(words_per_chapter, 1):
        distinct_words = set(words)
        words_weights = {
            word: common.tf_idf_weights(word, words, words_per_chapter)
            for word in distinct_words
        }
        cloud = wordcloud.WordCloud(background_color="white", max_words=5000)
        cloud.generate_from_frequencies(words_weights)
        pathlib.Path('data/clouds/ex6/').mkdir(exist_ok=True)
        cloud.to_file(f"data/clouds/ex6/chapter-{chapter_idx}.png")

    # Build a word cloud based on tf-idf weights for the entire book.
    all_words = tuple(common.extract_words_from_lines(lines))
    distinct_words = set(all_words)
    words_weights = {
        word: common.tf_idf_weights(word, all_words, [all_words])
        for word in distinct_words
    }
    cloud = wordcloud.WordCloud(background_color="white", max_words=5000)
    cloud.generate_from_frequencies(words_weights)
    pathlib.Path('data/clouds/ex6/').mkdir(exist_ok=True)
    cloud.to_file(f"data/clouds/ex6/whole-book.png")


if __name__ == "__main__":
    main()
