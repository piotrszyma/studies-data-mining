import pathlib
import collections

import wordcloud

import common


def main():
    lines = tuple(common.read_lines_from_file("data/pride-and-prejudice.txt"))
    words = common.extract_words_from_lines(lines)
    words_count = collections.Counter(words)
    cloud = wordcloud.WordCloud(background_color="white", max_words=5000)
    cloud.generate_from_frequencies(words_count)
    pathlib.Path('data/clouds/ex5/').mkdir(exist_ok=True)
    cloud.to_file("data/clouds/ex5/cloud.png")


if __name__ == "__main__":
    main()