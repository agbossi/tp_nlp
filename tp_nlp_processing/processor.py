import math
import os

import nltk as nltk
import spacy
import re
from nltk.corpus import stopwords
from pysentimiento import create_analyzer
from tp_nlp_processing import visualizer
from tp_nlp_app.models import Place, Summary
from sklearn.feature_extraction.text import TfidfVectorizer

nltk.download('punkt')
nlp = spacy.load('es_core_news_md')
stop_list = stopwords.words("spanish")


def generate_place_summary(place):
    reviews = place.review_set.all()
    reviews_amount = len(reviews)
    clean_reviews = remove_crap(reviews)
    statements = get_statements_from_reviews(clean_reviews)
    sentences_amount = len(statements)
    blacklisted_words = place.blacklistedword_set.all()
    stop_list.extend(list(map(lambda w: w.word, blacklisted_words)))
    sentiment_dataset = sentiment_analysis(statements)

    print('starting summary')
    for key, value in sentiment_dataset.items():
        sentiment_dataset[key] = normalize(value)
    place = generate_summary(sentiment_dataset, place)
    summary = Summary(place=place, good=place.good, bad=place.bad, neutral=place.neutral,
                      goodTokens=place.goodTokens, badTokens=place.badTokens,
                      neutralTokens=place.neutralTokens,
                      reviewsAmount=reviews_amount, sentencesAmount=sentences_amount)
    summary.save()
    print('summary generated')


def sentiment_analysis(statements):
    good_statements = []
    bad_statements = []
    neutral_statements = []
    sentiment_dataset = {'NEU': neutral_statements, 'POS': good_statements, 'NEG': bad_statements}
    analyzer = create_analyzer(task="sentiment", lang="es")

    predictions = analyzer.predict(statements)
    for prediction in predictions:
        sentiment_dataset[prediction.output].append(prediction.sentence)
    return sentiment_dataset


def get_statements_from_reviews(reviews):
    statements = []
    for review in reviews:
        words = nltk.sent_tokenize(review, language="spanish")
        for word in words:
            statements.append(word)
    return statements


def normalize(data):
    data = apply_transformation(data, remove_numbers)
    data = apply_transformation(data, remove_trailing_dots)
    data = apply_transformation(data, remove_stopwords)
    data = apply_transformation(data, remove_tildes)
    data = apply_transformation(data, lemmatize_statement)
    return data


def apply_transformation(statements, function):
    ret = []
    for statement in statements:
        result = function(statement)
        if result != '':
            ret.append(result)
    return ret


def remove_crap(reviews):
    char_to_replace = {',': '', '\a': '', '?': '', '\\': '',
                       '¦': '', '|': '', '(': '', ')': '',
                       '[': '', ']': '', '\r': '', '{': '',
                       '}': '', '¡': '', '!': '', '\t': '',
                       '/': '', ':': '', ';': '', '+': '',
                       '#': '', '-': '', '_': '', '%': '', '$': ''}
    return [review.text.translate(str.maketrans(char_to_replace)) for review in reviews]


def remove_trailing_dots(text):
    return text.replace(".", "")


def remove_tildes(text):
    text = re.sub("á", "a", text)
    text = re.sub("é", "e", text)
    text = re.sub("í", "i", text)
    text = re.sub("ó", "o", text)
    text = re.sub("ú", "u", text)
    return text


def remove_numbers(text):
    text = re.sub(r'\d+', '', text)
    return text


def lemmatize_statement(statement):
    doc = nlp(statement)
    return ' '.join([word.lemma_ for word in doc])


def remove_stopwords(statement):
    filtered_statement = []
    if len(statement.split(' ')) == 1:
        return ''
    for word in statement.split(' '):
        if word not in stop_list:
            filtered_statement.append(word.lower())
            filtered_statement.append(' ')
    filtered_statement.pop()
    return ''.join(filtered_statement)


def generate_summary(sentiment_dataset, place):
    base_path = os.path.dirname(os.path.abspath('tp_nlp_ui'))
    base_path += "/tp_nlp_ui/public/"
    place_path = 'summaries/' + place.placeId + '/'
    full_path = base_path + "/" + place_path
    fmt = '.png'
    if not os.path.exists(full_path):
        os.makedirs(full_path)

    place.good = ''.join(sentiment_dataset['POS'])
    sentiment_dataset['POS'] = place.good
    place.bad = ''.join(sentiment_dataset['NEG'])
    sentiment_dataset['NEG'] = place.bad
    place.neutral = ''.join(sentiment_dataset['NEU'])
    sentiment_dataset['NEU'] = place.neutral
    place.save()
    important_tokens = {}
    for key, value in sentiment_dataset.items():
        text = sentiment_dataset[key]
        visualizer.generate_wordcloud(text, stop_list, full_path + key + fmt)
        important_tokens[key] = count_vectorize(text)
    place.goodTokens = important_tokens['POS']
    place.badTokens = important_tokens['NEG']
    place.neutralTokens = important_tokens['NEU']
    return place


def count_vectorize(classified_reviews):
    text_in_list = [classified_reviews]
    tfidf = TfidfVectorizer(ngram_range=[1, 2], max_features=None)
    TNG_tfidf = tfidf.fit_transform(text_in_list)
    return collect_remarkable_tokens(tfidf.get_feature_names_out(), TNG_tfidf[0].data)


def collect_remarkable_tokens(tokens, frequencies):
    tokens_to_select = math.ceil(len(tokens) * 0.15)
    remarkable_tokens = ""
    token_frequency = dict(zip(tokens, frequencies))
    for token in sorted(token_frequency, key=token_frequency.get, reverse=True):
        remarkable_tokens += token
        remarkable_tokens += "|"
        tokens_to_select -= 1
        if tokens_to_select == 0:
            break

    remarkable_tokens = remarkable_tokens[:-1]
    return remarkable_tokens
