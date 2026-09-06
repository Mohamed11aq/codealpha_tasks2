# CodeAlpha_FAQChatbot

An FAQ chatbot built for the CodeAlpha Artificial Intelligence internship (Task 2).
It matches a user's question against a fixed set of FAQs using NLP preprocessing
and TF-IDF cosine similarity, and serves the result through a small chat interface.

## How it works

1. **FAQ data** — `faqs.json` holds a list of `{question, answer}` pairs (here, an
   online course platform's support FAQ — accounts, billing, courses, certificates).
2. **Preprocessing** — each question (and every incoming user message) is lowercased,
   stripped of punctuation, tokenized, cleaned of stopwords, and lemmatized using **NLTK**.
3. **Matching** — the cleaned FAQ questions are vectorized with **scikit-learn's**
   `TfidfVectorizer`. An incoming message is vectorized the same way, and **cosine
   similarity** finds the closest FAQ question.
4. **Response** — if the best match scores above a confidence threshold, its answer
   is returned; otherwise the bot admits it doesn't know rather than guessing.
5. **UI** — a simple chat window (Flask + vanilla JS) with a text input, a few
   suggested questions to try, and a typing indicator while the backend responds.

## Project structure

```
CodeAlpha_FAQChatbot/
├── app.py              # Flask app: preprocessing, TF-IDF matching, /chat endpoint
├── faqs.json           # FAQ dataset (edit this to change topic/product)
├── requirements.txt
├── templates/
│   └── index.html      # Chat UI markup
└── static/
    ├── style.css
    └── script.js        # Chat logic (send message, render replies)
```

## Running it locally

```bash
pip install -r requirements.txt
python app.py
```

Then open **http://127.0.0.1:5000** in your browser. The first run downloads a few
small NLTK data packages (stopwords, wordnet, punkt) automatically.

## Customizing it for a different topic

Replace the contents of `faqs.json` with your own `question`/`answer` pairs — the
preprocessing and matching logic works the same regardless of subject. You can also
tune `CONFIDENCE_THRESHOLD` in `app.py` to make the bot stricter or more lenient
about what counts as a good match.

## Built with

Python, Flask, NLTK, scikit-learn (TF-IDF + cosine similarity), HTML/CSS/JS.
