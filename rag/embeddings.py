from sklearn.feature_extraction.text import TfidfVectorizer

def fit_text_vectors(texts: list[str]):
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(texts) if texts else None
    return vectorizer, matrix
