# AI-Based Sentiment Analyzer

A Flask web app that reads product reviews and labels each one as positive, negative or neutral, using a pre-trained Hugging Face transformer model.

## Technologies
- Python, Flask
- Hugging Face Transformers (DistilBERT SST-2)
- MongoDB (optional, for storing results)

## Setup
pip install -r requirements.txt
python app.py

Open http://127.0.0.1:5000, type one review per line, and click Analyze.

## Features
- Sentiment score for each review
- Neutral label for low-confidence results
- Results saved to MongoDB when it is running
