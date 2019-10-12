import collections
import math
import string

from typing import Text, Sequence

from stemming.porter2 import stem
import wordcloud


TRANS_PUNCTUATION = str.maketrans({s: None for s in string.punctuation + "“”" + string.digits})

with open("stop_words.txt", "r") as f:
    STOP_WORDS = set(word.strip() for word in f.readlines())

def read_lines_from_file(filename: Text) -> Sequence[Text]:
    with open(filename, "r") as f:
        for line in f.readlines():
            yield line


def extract_distinct_words_from_lines(lines: Sequence[Text]) -> Sequence[Text]:
    for line in lines:
        line = line.translate(TRANS_PUNCTUATION)
        words = (word.strip() for word in line.split(" "))
        words = (word for word in words if word not in STOP_WORDS)
        words = (stem(word.lower()) for word in words)
        yield from words

# TODO: Try to replace with genexpr
def split_into_chapters(lines: Sequence[Text]) -> Sequence[Text]:
    group = []

    for line in lines:

        if line.startswith("Chapter") and group:
            yield group
            group = []

        group.append(line)

    if group:
        yield group


def tf(term: Text, document: Sequence[Text]) -> int:
    return document.count(term)


def inverse_tf(term: Text, documents: Sequence[Sequence[Text]]) -> float:
    docs_with_term = tuple(document for document in documents if term in document)
    number_of_docs_with_term = len(docs_with_term)
    return math.log(
        len(documents) / (1 + number_of_docs_with_term))


def tf_idf_weights(term: Text, 
                   document: Sequence[Text], 
                   documents: Sequence[Sequence[Text]]) -> float:
    return tf(term, document) * inverse_tf(term, documents)


def create_clouds_for_whole_document(lines):
    words = extract_distinct_words_from_lines(lines)
    words_count = collections.Counter(words)
    cloud = wordcloud.WordCloud(background_color="white", max_words=20000)
    cloud.generate_from_frequencies(words_count)
    cloud.to_file("clouds/all_words_cloud.png")



def create_clouds_for_chapters(chapter_lines):
    for chapter_idx, chapter_lines in enumerate(chapters_lines, 1):
        words = extract_distinct_words_from_lines(chapter_lines)
        words_count = collections.Counter(words)
        cloud = wordcloud.WordCloud(background_color="white", max_words=20000)
        cloud.generate_from_frequencies(words_count)
        cloud.to_file(f"clouds/counts/chapter_{chapter_idx}_cloud.png")


def create_weighted_clouds_for_chapters(chapter_lines):
    chapters_words = [
        tuple(extract_distinct_words_from_lines(chapter_lines))
        for chapter_lines in chapters_lines]

    for chapter_idx, words_in_chapter in enumerate(chapters_words, 1):
        words_in_chapter_weights = {}
        for word in set(words_in_chapter):
            words_in_chapter_weights[word] = (
                tf_idf_weights(word, words_in_chapter, chapters_words))

        cloud = wordcloud.WordCloud(background_color="white", max_words=20000)
        cloud.generate_from_frequencies(words_in_chapter_weights)
        cloud.to_file(f"clouds/tf_idf/chapter_{chapter_idx}_cloud.png")


def create_weighted_cloud_for_book():
    ...


def main():
    lines = tuple(read_lines_from_file("pride-and-prejudice.txt"))
    chapters_lines = split_into_chapters(lines)



    # create_weighted_clouds_for_chapters(chapters_lines)




if __name__ == "__main__":
    main()
