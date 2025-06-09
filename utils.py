import logging
import sys
from typing import Dict, Any
from datetime import datetime
import json
from fastapi import HTTPException

# Configure logging
def setup_logging(log_file: str = "sentiment_trading.log", log_level: str = "INFO") -> logging.Logger:
    """Set up logging configuration."""
    logger = logging.getLogger("sentiment_trading")
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Create handlers
    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler(sys.stdout)
    
    # Create formatters and add it to handlers
    log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(log_format)
    console_handler.setFormatter(log_format)
    
    # Add handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    return logger

# Initialize logger
logger = setup_logging()

class SentimentAnalysisError(Exception):
    """Custom exception for sentiment analysis errors."""
    pass

class TradingError(Exception):
    """Custom exception for trading-related errors."""
    pass

def validate_webhook_data(data: Dict[str, Any]) -> None:
    """Validate incoming webhook data."""
    required_fields = ["headline", "symbol", "timestamp"]
    
    for field in required_fields:
        if field not in data:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required field: {field}"
            )
    
    try:
        datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid timestamp format"
        )

def format_trading_signal(sentiment_scores: Dict[str, float], threshold: float = 0.6) -> str:
    """Format trading signal based on sentiment scores."""
    if sentiment_scores["positive"] > threshold:
        return "BUY"
    elif sentiment_scores["negative"] > threshold:
        return "SELL"
    return "HOLD"

def log_trading_decision(symbol: str, headline: str, sentiment_scores: Dict[str, float], signal: str) -> None:
    """Log trading decision with all relevant information."""
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "symbol": symbol,
        "headline": headline,
        "sentiment_scores": sentiment_scores,
        "trading_signal": signal
    }
    logger.info(f"Trading Decision: {json.dumps(log_data)}")

def handle_error(error: Exception, context: str) -> Dict[str, Any]:
    """Handle and log errors with context."""
    error_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "error_type": type(error).__name__,
        "error_message": str(error),
        "context": context
    }
    logger.error(f"Error occurred: {json.dumps(error_data)}")
    return error_data 