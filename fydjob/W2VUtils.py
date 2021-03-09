
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import string


def to_lower(text):
    return text.lower()


def remove_number(text):
    text = ''.join(word for word in text if not word.isdigit())

    return text


def remove_punctuation_mod(text):

    punct = string.punctuation.replace(".","")
    for punctuation in punct:
        text = text.replace(punctuation, '')

    return text


def remove_stopwords(text):

    stop_words = set(stopwords.words('english'))
    new_text = []
    for sent in text:
        sent = word_tokenize(sent)
        sent = [w for w in sent if w not in stop_words and w not in string.punctuation and w]
        new_text.append(sent)
    return new_text


def lemmatize_words(text):

    lemmatizer = WordNetLemmatizer()
    for sentence in text:
        for word in sentence:
            word = lemmatizer.lemmatize(word)

    return text
