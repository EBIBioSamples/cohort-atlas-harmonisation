import re

import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier

stop_words = stopwords.words('english')

train_df = pd.read_csv('../resources/standard_terms.csv')
test_df = pd.read_csv('../resources/data_dictionary_estbb.csv')

sw = stopwords.words('english')
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z?.!,¿]+", " ", text)
    text = [word.lower() for word in text.split() if word.lower() not in sw]
    text = [lemmatizer.lemmatize(word) for word in text]
    text = " ".join(text)
    return text


train_df['DESCRIPTION'] = train_df['DESCRIPTION'].fillna('')
# train_df['FEATURE'] = train_df.apply(lambda x: x['TERM'] + ' ' + x['DESCRIPTION'], axis=1)
train_df['FEATURE'] = train_df['TERM']
train_df['FEATURE'] = train_df['FEATURE'].apply(lambda x: clean_text(x))

test_df['DESCRIPTION'] = test_df['DESCRIPTION'].fillna('')
test_df['TERM'] = test_df.apply(lambda x: x['TERM'].replace('.', ' '), axis=1)
# test_df['FEATURE'] = test_df.apply(lambda x: x['TERM'] + ' ' + x['DESCRIPTION'], axis=1)
test_df['FEATURE'] = test_df['DESCRIPTION']
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

test_df.to_csv('../resources/results/mapping.csv', index=False)
