from flask import Flask, request, jsonify, render_template
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    texts = request.json.get("texts", [])
    results = []
    for text in texts:
        score = analyzer.polarity_scores(text)["compound"]   # -1 (negative) to +1 (positive)
        if score >= 0.05:
            label = "positive"
        elif score <= -0.05:
            label = "negative"
        else:
            label = "neutral"
        results.append({"text": text, "sentiment": label, "score": round(score, 3)})
    return jsonify(results)

if __name__ == "__main__":
    app.run(debug=True)
