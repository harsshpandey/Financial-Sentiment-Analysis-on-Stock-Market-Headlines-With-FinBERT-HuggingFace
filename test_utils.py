import pytest
from datetime import datetime
from fastapi import HTTPException
from utils import (
    validate_webhook_data,
    format_trading_signal,
    log_trading_decision,
    handle_error,
    SentimentAnalysisError,
    TradingError
)

def test_validate_webhook_data_valid():
    """Test webhook data validation with valid data."""
    valid_data = {
        "headline": "Test headline",
        "symbol": "AAPL",
        "timestamp": datetime.utcnow().isoformat()
    }
    validate_webhook_data(valid_data)  # Should not raise any exception

def test_validate_webhook_data_missing_field():
    """Test webhook data validation with missing field."""
    invalid_data = {
        "headline": "Test headline",
        "symbol": "AAPL"
    }
    with pytest.raises(HTTPException) as exc_info:
        validate_webhook_data(invalid_data)
    assert exc_info.value.status_code == 400
    assert "Missing required field" in str(exc_info.value.detail)

def test_validate_webhook_data_invalid_timestamp():
    """Test webhook data validation with invalid timestamp."""
    invalid_data = {
        "headline": "Test headline",
        "symbol": "AAPL",
        "timestamp": "invalid-timestamp"
    }
    with pytest.raises(HTTPException) as exc_info:
        validate_webhook_data(invalid_data)
    assert exc_info.value.status_code == 400
    assert "Invalid timestamp format" in str(exc_info.value.detail)

def test_format_trading_signal():
    """Test trading signal formatting."""
    # Test BUY signal
    buy_scores = {"positive": 0.8, "negative": 0.1, "neutral": 0.1}
    assert format_trading_signal(buy_scores) == "BUY"

    # Test SELL signal
    sell_scores = {"positive": 0.1, "negative": 0.8, "neutral": 0.1}
    assert format_trading_signal(sell_scores) == "SELL"

    # Test HOLD signal
    hold_scores = {"positive": 0.4, "negative": 0.3, "neutral": 0.3}
    assert format_trading_signal(hold_scores) == "HOLD"

def test_handle_error():
    """Test error handling."""
    error = ValueError("Test error")
    context = "Test context"
    error_data = handle_error(error, context)
    
    assert "timestamp" in error_data
    assert error_data["error_type"] == "ValueError"
    assert error_data["error_message"] == "Test error"
    assert error_data["context"] == "Test context"

def test_custom_exceptions():
    """Test custom exceptions."""
    with pytest.raises(SentimentAnalysisError):
        raise SentimentAnalysisError("Test sentiment error")
    
    with pytest.raises(TradingError):
        raise TradingError("Test trading error") 