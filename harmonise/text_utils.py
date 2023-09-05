import re
import wordninja

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stop_words = stopwords.words('english')
lemmatizer = WordNetLemmatizer()


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z?.!,¿]+", " ", text)
    text = [word.lower() for word in text.split() if word.lower() not in stop_words]
    text = [lemmatizer.lemmatize(word) for word in text]
    text = " ".join(text)
    return text


def tokenize_text(text):
    return wordninja.split(text)
