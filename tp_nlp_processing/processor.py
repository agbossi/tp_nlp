import os

import nltk as nltk
import spacy
import re
from nltk.corpus import stopwords
from pysentimiento import SentimentAnalyzer
from tp_nlp_processing import visualizer
from tp_nlp_app.models import Place
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

nltk.download('punkt')
nlp = spacy.load(r'/home/abossi/anaconda3/lib/python3.7/site-packages/es_core_news_md/es_core_news_md-3.4.0')


def generate_place_summary(place):
    reviews = place.review_set.all()
    clean_reviews = remove_crap(reviews)
    statements = get_statements_from_reviews(clean_reviews)
    sentiment_dataset = sentiment_analysis(statements)

    for key, value in sentiment_dataset.items():
        sentiment_dataset[key] = normalize(value)
    generate_summary(sentiment_dataset, place)


def sentiment_analysis(statements):
    good_statements = []
    bad_statements = []
    neutral_statements = []
    sentiment_dataset = {'NEU': neutral_statements, 'POS': good_statements, 'NEG': bad_statements}
    analyzer = SentimentAnalyzer(lang="es")

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
    stop_list = stopwords.words("spanish")
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
    base_path = os.path.dirname(os.path.abspath('summaries'))
    place_path = 'summaries/' + place.placeId + '/'
    full_path = base_path + "/" + place_path
    fmt = '.png'
    os.mkdir(full_path)

    place.good = ''.join(sentiment_dataset['POS'])
    sentiment_dataset['POS'] = place.good
    place.bad = ''.join(sentiment_dataset['NEG'])
    sentiment_dataset['NEG'] = place.bad
    place.neutral = ''.join(sentiment_dataset['NEU'])
    sentiment_dataset['NEU'] = place.neutral
    place.save()
    for key, value in sentiment_dataset.items():
        text = sentiment_dataset[key]
        visualizer.generate_wordcloud(text, full_path + key + fmt)

# primeros 15 de clase
def count_vectorize(classified_reviews):
    cv = CountVectorizer(ngram_range=[1, 2], max_df=0.8, min_df=2, max_features=None, stop_words=None)

    TNG_cv = cv.fit_transform(classified_reviews)
