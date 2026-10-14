from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from pymongo import MongoClient
from datetime import datetime

app = Flask(__name__)
analyzer = pipeline("sentiment-analysis",
                    model="distilbert-base-uncased-finetuned-sst-2-english")

# MongoDB is optional; the app still works without it
try:
    db = MongoClient("mongodb://localhost:27017")["sentiment"]["results"]
except Exception:
    db = None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    texts = request.json.get("texts", [])
    results = []
    for text in texts:
        out = analyzer(text[:512])[0]          # model input limit
        label = out["label"].lower()           # 'positive' / 'negative'
        score = round(out["score"], 3)
        if score < 0.6:                        # low confidence = neutral
            label = "neutral"
        record = {"text": text, "sentiment": label, "score": score,
                  "time": datetime.utcnow().isoformat()}
        if db is not None:
            db.insert_one(record.copy())
        results.append(record)
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
