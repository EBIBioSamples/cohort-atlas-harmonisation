import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import TfidfVectorizer

from harmonise.text_utils import clean_text
from harmonise.annotator import Annotator

train_df = pd.read_csv('resources/standard_terms.csv')
# test_df = pd.read_csv('../resources/temp/data_dictionary_estbb.csv')


class AnnotatorTfidf(Annotator):
    def __init__(self):
        self.me = 'tfidf'
        self.tfidf_vectorizer, self.classifier = self.load_model()

    def annotate(self, test_dataframe):
        test_dataframe['name'] = test_dataframe.apply(lambda x: x['name'].replace('.', ' '), axis=1)
        # test_df['FEATURE'] = test_df.apply(lambda x: x['TERM'] + ' ' + x['DESCRIPTION'], axis=1)
        test_dataframe['FEATURE'] = test_dataframe['name']
        test_dataframe['FEATURE'] = test_dataframe['FEATURE'].apply(lambda x: clean_text(x))

        x_test = test_dataframe['FEATURE']
        tfidf_test_vectors = self.tfidf_vectorizer.transform(x_test)
        y_pred = self.classifier.predict(tfidf_test_vectors)
        test_dataframe["CLASS"] = y_pred

        return test_dataframe

    def load_model(self):
        train_df['DESCRIPTION'] = train_df['DESCRIPTION'].fillna('')
        # train_df['FEATURE'] = train_df.apply(lambda x: x['TERM'] + ' ' + x['DESCRIPTION'], axis=1)
        train_df['FEATURE'] = train_df['TERM']
        train_df['FEATURE'] = train_df['FEATURE'].apply(lambda x: clean_text(x))

        x_train = train_df['FEATURE']
        y_train = train_df['TERM']
        tfidf_vectorizer = TfidfVectorizer()
        tfidf_train_vectors = tfidf_vectorizer.fit_transform(x_train)
        classifier = RandomForestClassifier()
        classifier.fit(tfidf_train_vectors, y_train)

        return tfidf_vectorizer, classifier


def get_annotated_dataframe(filepath):
    test_df = pd.read_csv(filepath)

    train_df['DESCRIPTION'] = train_df['DESCRIPTION'].fillna('')
    # train_df['FEATURE'] = train_df.apply(lambda x: x['TERM'] + ' ' + x['DESCRIPTION'], axis=1)
    train_df['FEATURE'] = train_df['TERM']
    train_df['FEATURE'] = train_df['FEATURE'].apply(lambda x: clean_text(x))

    test_df['name'] = test_df.apply(lambda x: x['name'].replace('.', ' '), axis=1)
    # test_df['FEATURE'] = test_df.apply(lambda x: x['TERM'] + ' ' + x['DESCRIPTION'], axis=1)
    test_df['FEATURE'] = test_df['name']
    test_df['FEATURE'] = test_df['FEATURE'].apply(lambda x: clean_text(x))

    x_train = train_df['FEATURE']
    x_test = test_df['FEATURE']
    y_train = train_df['TERM']

    tfidf_vectorizer = TfidfVectorizer()
    tfidf_train_vectors = tfidf_vectorizer.fit_transform(x_train)
    tfidf_test_vectors = tfidf_vectorizer.transform(x_test)

    classifier = RandomForestClassifier()
    classifier.fit(tfidf_train_vectors, y_train)
    y_pred = classifier.predict(tfidf_test_vectors)

    test_df["CLASS"] = y_pred
    # test_df.to_csv('../resources/results/mapping.csv', index=False)

    return test_df
