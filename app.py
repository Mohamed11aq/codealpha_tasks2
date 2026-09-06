"""
CodeAlpha AI Internship — Task 2: Chatbot for FAQs
Matches a user's question against a set of FAQs using NLTK preprocessing
and scikit-learn's TF-IDF + cosine similarity, then serves a small chat UI.
"""

import json
import re

from flask import Flask, jsonify, render_template, request

import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------------------
# One-time NLTK data setup (safe to run every start; skips if already present)
# ---------------------------------------------------------------------------
_REQUIRED_NLTK_DATA = {
    "punkt_tab": "tokenizers/punkt_tab",
    "stopwords": "corpora/stopwords",
    "wordnet": "corpora/wordnet",
    "omw-1.4": "corpora/omw-1.4",
}
for package, path in _REQUIRED_NLTK_DATA.items():
    try:
        nltk.data.find(path)
    except LookupError:
        nltk.download(package, quiet=True)

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# ---------------------------------------------------------------------------
# Load FAQ data and build the TF-IDF index once at startup
# ---------------------------------------------------------------------------
with open("faqs.json", "r", encoding="utf-8") as f:
    FAQS = json.load(f)

questions = [item["question"] for item in FAQS]
answers = [item["answer"] for item in FAQS]


def preprocess(text: str) -> str:
    """Lowercase, strip punctuation, tokenize, remove stopwords, lemmatize."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    tokens = nltk.word_tokenize(text)
    tokens = [
        lemmatizer.lemmatize(token)
        for token in tokens
        if token.strip() and token not in stop_words
    ]
    return " ".join(tokens)


processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()
faq_matrix = vectorizer.fit_transform(processed_questions)

# Below this similarity score, the bot admits it doesn't know rather than
# guessing at the closest (but irrelevant) FAQ.
CONFIDENCE_THRESHOLD = 0.25


def get_best_answer(user_message: str):
    processed = preprocess(user_message)
    if not processed.strip():
        return (
            "Could you rephrase that? I didn't catch a real question there.",
            0.0,
        )

    user_vector = vectorizer.transform([processed])
    similarities = cosine_similarity(user_vector, faq_matrix)[0]
    best_index = int(similarities.argmax())
    best_score = float(similarities[best_index])

    if best_score < CONFIDENCE_THRESHOLD:
        return (
            "I'm not sure about that one yet. Try rephrasing, or ask about "
            "something else from our FAQ.",
            best_score,
        )
    return answers[best_index], best_score


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_message = (data.get("message") or "").strip()

    if not user_message:
        return jsonify(
            {"answer": "Type a question and I'll do my best to answer it.", "confidence": 0.0}
        )

    answer, confidence = get_best_answer(user_message)
    return jsonify({"answer": answer, "confidence": round(confidence, 2)})


import os

if name == "main":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
