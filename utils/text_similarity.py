from nltk.corpus import stopwords
from unidecode import unidecode
import string
from nltk.tokenize import word_tokenize
import gensim.downloader as api
import numpy as np
from collections import Counter
import itertools
from sklearn.metrics.pairwise import cosine_similarity
from googletrans import Translator


def pre_process(corpus):
    # convert input corpus to lower case.
    corpus = corpus.lower()
    # collecting a list of stop words from nltk and punctuation form
    # string class and create single array.
    stopset = stopwords.words('english') + list(string.punctuation)
    # remove stop words and punctuations from string.
    # word_tokenize is used to tokenize the input corpus in word tokens.
    corpus = " ".join([i for i in word_tokenize(corpus) if i not in stopset])
    # remove non-ascii characters
    corpus = unidecode(corpus)
    return corpus


def map_word_frequency(document):
    return Counter(itertools.chain(*document))


def get_cosine_similarity(feature_vec_1, feature_vec_2):
    if np.isnan(feature_vec_1[0]) or np.isnan(feature_vec_2[0]):
        return 0

    return cosine_similarity(
        feature_vec_1.reshape(1, -1), feature_vec_2.reshape(1, -1)
    )[0][0]


class TextSimilarityEstimator(object):
    def __init__(self):
        self.word_emb_model = api.load('word2vec-google-news-300')
        self.translator = Translator()

    def translate(self, russian_string: str) -> str:
        """
        Translate russian sentence to english
        Args:
            russian_string: string with sentence in russian

        Returns:
            string with sentence in english
        """
        return self.translator.translate(text=russian_string, src='ru').text

    def get_sif_feature_vectors(
            self,
            sentence1, sentence2):
        sentence1 = [
            token
            for token in sentence1.split()
            if token in self.word_emb_model.wv.vocab
        ]
        sentence2 = [
            token
            for token in sentence2.split()
            if token in self.word_emb_model.wv.vocab
        ]

        word_counts = map_word_frequency((sentence1 + sentence2))
        embedding_size = 300  # size of vectore in word embeddings
        a = 0.001
        sentence_set = []
        for sentence in [sentence1, sentence2]:
            vs = np.zeros(embedding_size)
            sentence_length = len(sentence)
            for word in sentence:
                a_value = a / (a + word_counts[
                    word])  # smooth inverse frequency, SIF
                vs = np.add(
                    vs,
                    np.multiply(a_value, self.word_emb_model.wv[word])
                )  # vs += sif * word_vector
            vs = np.divide(vs, sentence_length)  # weighted average
            sentence_set.append(vs)
        return sentence_set

    def __call__(self, sentence1: str, sentence2: str, ru: bool = False):
        """
        Evaluate probability
        Args:
            sentence1: string with sentence
            sentence2: string with sentence
            ru: strings in russian

        Returns:
            Cos similarity of sentences vectors
        """
        s1, s2 = sentence1, sentence2
        if ru:
            s1, s2 = self.translate(s1), self.translate(s2)

        v1, v2 = self.get_sif_feature_vectors(
            pre_process(s1),
            pre_process(s2)
        )

        return get_cosine_similarity(v1, v2)
