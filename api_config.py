from fastapi.openapi.utils import get_openapi
from fastapi import FastAPI

def custom_openapi(app: FastAPI):
    """Custom OpenAPI schema configuration."""
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Financial Sentiment Analysis API",
        version="1.0.0",
        description="""
        API for analyzing financial sentiment in stock market headlines using FinBERT.
        
        ## Features
        * Sentiment analysis of financial headlines
        * Real-time trading signals
        * Webhook integration with TradingView
        
        ## Endpoints
        * `/webhook` - TradingView webhook endpoint
        * `/analyze` - Manual sentiment analysis endpoint
        * `/health` - Health check endpoint
        """,
        routes=app.routes,
    )

    # Add security scheme
    openapi_schema["components"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    }

    app.openapi_schema = openapi_schema
    return app.openapi_schema

# API Tags
TAGS_METADATA = [
    {
        "name": "sentiment",
        "description": "Sentiment analysis operations",
    },
    {
        "name": "trading",
        "description": "Trading signal operations",
    },
    {
        "name": "health",
        "description": "Health check operations",
    },
]

# API Response Models
RESPONSE_MODELS = {
    "SentimentResponse": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "data": {
                "type": "object",
                "properties": {
                    "timestamp": {"type": "string", "format": "date-time"},
                    "symbol": {"type": "string"},
                    "headline": {"type": "string"},
                    "sentiment_scores": {
                        "type": "object",
                        "properties": {
                            "positive": {"type": "number"},
                            "negative": {"type": "number"},
                            "neutral": {"type": "number"},
                        },
                    },
                    "trading_signal": {"type": "string", "enum": ["BUY", "SELL", "HOLD"]},
                },
            },
        },
    },
    "ErrorResponse": {
        "type": "object",
        "properties": {
            "status": {"type": "string"},
            "error": {
                "type": "object",
                "properties": {
                    "code": {"type": "integer"},
                    "message": {"type": "string"},
                },
            },
        },
    },
} 