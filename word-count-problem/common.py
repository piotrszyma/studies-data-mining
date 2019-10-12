import math
import string
from typing import Sequence, Text

from stemming.porter2 import stem

with open("data/stop-words.txt", "r") as f:
    STOP_WORDS = set(word.strip() for word in f.readlines())


def read_lines_from_file(filename: Text) -> Sequence[Text]:
    with open(filename, "r") as f:
        for line in f.readlines():
            yield line


TRANS_PUNCTUATION = str.maketrans(
    {s: None
     for s in string.punctuation + "“”" + string.digits})


def extract_words_from_lines(lines: Sequence[Text]) -> Sequence[Text]:
    for line in lines:
        line = line.translate(TRANS_PUNCTUATION)
        words = (word.strip() for word in line.split(" "))
        words = (word for word in words if word not in STOP_WORDS)
        words = (stem(word.lower()) for word in words)
        yield from words


# TODO: Try to replace with genexpr
def split_lines_into_chapters(lines: Sequence[Text]) -> Sequence[Text]:
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
    docs_with_term = tuple(document for document in documents
                           if term in document)
    number_of_docs_with_term = len(docs_with_term)
    return math.log(len(documents) / (1 + number_of_docs_with_term))


def tf_idf_weights(term: Text, document: Sequence[Text],
                   documents: Sequence[Sequence[Text]]) -> float:
    return tf(term, document) * inverse_tf(term, documents)
