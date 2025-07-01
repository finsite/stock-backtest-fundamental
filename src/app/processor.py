"""
Processor module for stock-backtest-fundamental signal generation.

Validates incoming messages and computes a fundamental signal using
financial ratios and basic threshold logic.
"""

from typing import Any

from app.utils.setup_logger import setup_logger
from app.utils.types import ValidatedMessage
from app.utils.validate_data import validate_message_schema

logger = setup_logger(__name__)


def validate_input_message(message: dict[str, Any]) -> ValidatedMessage:
    """
    Validate the incoming raw message against the expected schema.

    Args:
        message (dict[str, Any]): The raw message payload.

    Returns:
        ValidatedMessage: A validated message object.

    Raises:
        ValueError: If the message format is invalid.
    """
    logger.debug("🔍 Validating message schema...")
    if not validate_message_schema(message):
        logger.error("❌ Invalid message schema: %s", message)
        raise ValueError("Invalid message format")
    return message  # type: ignore[return-value]


def compute_fundamental_signal(message: ValidatedMessage) -> dict[str, Any]:
    """
    Compute a fundamental signal from key financial metrics.

    Args:
        message (ValidatedMessage): The validated input data.

    Returns:
        dict[str, Any]: Enriched message with fundamental signal and score.
    """
    symbol = message.get("symbol", "UNKNOWN")
    eps = float(message.get("eps", 2.0))
    revenue_growth = float(message.get("revenue_growth", 0.05))
    debt_to_equity = float(message.get("debt_to_equity", 0.4))

    logger.info("📘 Computing fundamental signal for %s", symbol)

    score = eps + revenue_growth - debt_to_equity
    signal = "BUY" if score > 1.5 else "HOLD"

    result = {
        "fundamental_score": round(score, 4),
        "fundamental_signal": signal,
    }

    logger.debug("📈 Fundamental result for %s: %s", symbol, result)
    return {**message, **result}
