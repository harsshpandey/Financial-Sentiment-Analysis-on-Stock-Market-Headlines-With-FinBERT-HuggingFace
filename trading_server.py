from fastapi import FastAPI, HTTPException, Request, Depends
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import uvicorn
from typing import Dict, Any
import json
from datetime import datetime
from utils import (
    setup_logging,
    validate_webhook_data,
    format_trading_signal,
    log_trading_decision,
    handle_error,
    SentimentAnalysisError,
    TradingError,
    logger
)
from api_config import custom_openapi, TAGS_METADATA, RESPONSE_MODELS
from pydantic import BaseModel

# Initialize FastAPI app with custom configuration
app = FastAPI(
    title="Financial Sentiment Trading API",
    description="API for analyzing financial sentiment in stock market headlines using FinBERT",
    version="1.0.0",
    openapi_tags=TAGS_METADATA
)

# Set custom OpenAPI schema
app.openapi = lambda: custom_openapi(app)

# Global variables for model and tokenizer
model = None
tokenizer = None

# Pydantic models for request/response validation
class WebhookPayload(BaseModel):
    headline: str
    symbol: str
    timestamp: str

class SentimentRequest(BaseModel):
    headline: str

class BatchSentimentRequest(BaseModel):
    headlines: list[str]

@app.on_event("startup")
async def startup_event():
    """Initialize the model and tokenizer when the server starts"""
    global model, tokenizer
    try:
        model = AutoModelForSequenceClassification.from_pretrained("ProsusAI/finbert")
        tokenizer = AutoTokenizer.from_pretrained("ProsusAI/finbert")
        model.eval()
        logger.info("Model and tokenizer initialized successfully")
    except Exception as e:
        error_data = handle_error(e, "Model initialization")
        raise HTTPException(status_code=500, detail=error_data)

def analyze_sentiment(headline: str) -> Dict[str, float]:
    """Analyze the sentiment of a financial headline using FinBERT"""
    try:
        inputs = tokenizer(headline, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = model(**inputs)
        
        probabilities = torch.nn.functional.softmax(outputs.logits, dim=-1)
        return {
            "positive": float(probabilities[0][0]),
            "negative": float(probabilities[0][1]),
            "neutral": float(probabilities[0][2])
        }
    except Exception as e:
        error_data = handle_error(e, "Sentiment analysis")
        raise SentimentAnalysisError(str(error_data))

@app.get("/", tags=["health"])
async def root():
    """Root endpoint"""
    return {"message": "Financial Sentiment Trading API is running"}

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    try:
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "model_loaded": model is not None and tokenizer is not None
        }
    except Exception as e:
        error_data = handle_error(e, "Health check")
        raise HTTPException(status_code=500, detail=error_data)

@app.post("/analyze", tags=["sentiment"])
async def analyze_headline(request: SentimentRequest):
    """Analyze sentiment of a single headline"""
    try:
        sentiment_scores = analyze_sentiment(request.headline)
        trading_signal = format_trading_signal(sentiment_scores)
        
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "headline": request.headline,
            "sentiment_scores": sentiment_scores,
            "trading_signal": trading_signal
        }
        
        log_trading_decision("N/A", request.headline, sentiment_scores, trading_signal)
        return {"status": "success", "data": result}
        
    except Exception as e:
        error_data = handle_error(e, "Headline analysis")
        raise HTTPException(status_code=500, detail=error_data)

@app.post("/analyze-batch", tags=["sentiment"])
async def analyze_batch_headlines(request: BatchSentimentRequest):
    """Analyze sentiment of multiple headlines"""
    try:
        results = []
        for headline in request.headlines:
            sentiment_scores = analyze_sentiment(headline)
            trading_signal = format_trading_signal(sentiment_scores)
            
            result = {
                "timestamp": datetime.utcnow().isoformat(),
                "headline": headline,
                "sentiment_scores": sentiment_scores,
                "trading_signal": trading_signal
            }
            results.append(result)
            log_trading_decision("N/A", headline, sentiment_scores, trading_signal)
        
        return {"status": "success", "data": results}
        
    except Exception as e:
        error_data = handle_error(e, "Batch headline analysis")
        raise HTTPException(status_code=500, detail=error_data)

@app.post("/webhook", tags=["trading"])
async def tradingview_webhook(payload: WebhookPayload):
    """Handle incoming webhooks from TradingView"""
    try:
        # Validate payload using our utility function
        validate_webhook_data(payload.dict())
        
        # Analyze sentiment
        sentiment_scores = analyze_sentiment(payload.headline)
        trading_signal = format_trading_signal(sentiment_scores)
        
        # Prepare response
        analysis_result = {
            "timestamp": payload.timestamp,
            "symbol": payload.symbol,
            "headline": payload.headline,
            "sentiment_scores": sentiment_scores,
            "trading_signal": trading_signal
        }
        
        # Log the trading decision
        log_trading_decision(payload.symbol, payload.headline, sentiment_scores, trading_signal)
        
        return {"status": "success", "data": analysis_result}
        
    except HTTPException:
        raise
    except Exception as e:
        error_data = handle_error(e, "Webhook processing")
        raise HTTPException(status_code=500, detail=error_data)

if __name__ == "__main__":
    uvicorn.run(
        "trading_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
