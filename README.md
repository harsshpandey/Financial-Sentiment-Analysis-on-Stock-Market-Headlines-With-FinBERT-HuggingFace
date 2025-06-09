# Financial Sentiment Analysis on Stock Market Headlines 📈

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![HuggingFace](https://img.shields.io/badge/🤗-HuggingFace-yellow)](https://huggingface.co/)
[![FinBERT](https://img.shields.io/badge/Model-FinBERT-green)](https://huggingface.co/ProsusAI/finbert)

## 🎯 Project Overview

This project uses FinBERT and HuggingFace to analyze sentiment in stock market headlines and generate trading signals.

## 🚀 Features

- Real-time sentiment analysis of financial headlines
- Trading signal generation (BUY/SELL/HOLD)
- REST API for easy integration
- Batch processing support
- Webhook integration for TradingView
- Comprehensive logging and error handling

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)

## 💻 Usage

1. Clone the repository:
```bash
git clone https://github.com/yourusername/financial-sentiment-analysis.git
cd financial-sentiment-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the trading server:
```bash
python trading_server.py
```

The server will start at `http://localhost:8000`

## 📊 Example

```python
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")

# Example headline
headline = "Tesla reports record quarterly profits"

# Analyze sentiment
inputs = tokenizer(headline, return_tensors="pt", padding=True)
outputs = model(**inputs)
predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)

# Get sentiment
labels = ["positive", "negative", "neutral"]
sentiment = labels[predictions.argmax().item()]
```

## 📊 Example API Response

```json
{
    "status": "success",
    "data": {
        "timestamp": "2023-04-30T10:00:00Z",
        "symbol": "AAPL",
        "headline": "Apple Reports Record Q2 Revenue",
        "sentiment_scores": {
            "positive": 0.85,
            "negative": 0.05,
            "neutral": 0.10
        },
        "trading_signal": "BUY"
    }
}
```

## 📈 Results

The model analyzes financial headlines and provides:
- 📈 Positive: Bullish/optimistic sentiment (> 0.6 triggers BUY)
- 📉 Negative: Bearish/pessimistic sentiment (> 0.6 triggers SELL)
- ➖ Neutral: No clear sentiment direction (triggers HOLD)

Trading signals are automatically generated based on sentiment scores:
- BUY: When positive sentiment > 0.6
- SELL: When negative sentiment > 0.6
- HOLD: When no strong sentiment is detected

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📧 Contact

Your Name - [your-email@example.com](mailto:your-email@example.com)

Project Link: [https://github.com/[your-username]/Financial-Sentiment-Analysis](https://github.com/[your-username]/Financial-Sentiment-Analysis)

## 📄 Project Structure

```
financial-sentiment-analysis/
├── trading_server.py      # Main API server
├── main.ipynb            # Development and testing notebook
├── utils.py              # Utility functions
├── api_config.py         # API configuration
├── requirements.txt      # Project dependencies
└── README.md            # This file
```

## 🔍 Testing

Run the test script:
```bash
python test_api.py
```

## 📄 Acknowledgments

- FinBERT model by ProsusAI
- HuggingFace Transformers library
- FastAPI framework
