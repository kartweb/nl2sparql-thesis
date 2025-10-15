from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))

def tokenize(text):
    return text.split()

def remove_stop_words(tokens):
    return [word for word in tokens if word not in stop_words]