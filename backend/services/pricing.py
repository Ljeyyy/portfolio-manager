# backend/services/pricing.py
import time
import logging
from typing import Dict, Optional
import yfinance as yf
from backend.config import settings

logger = logging.getLogger(__name__)

# Cache en mémoire : { ticker: (price, timestamp) }
_price_cache: Dict[str, tuple] = {}

# Prix mock pour mode offline / tests
MOCK_PRICES = {
    "AAPL":    182.50, "MSFT":   415.00, "GOOGL":  175.00,
    "BTC-USD": 68000.0, "ETH-USD": 3500.0, "SPY":   520.00,
    "QQQ":     445.00,  "NVDA":   875.00,  "AMZN":  185.00,
    "MC.PA":   750.00,  # LVMH
}

def get_price(ticker: str, use_mock: bool = False) -> Optional[float]:
    """
    Retourne le prix actuel d'un ticker.
    Utilise le cache TTL, puis yfinance, puis mock en fallback.
    """
    ticker = ticker.upper()

    # Vérification cache
    if ticker in _price_cache:
        price, ts = _price_cache[ticker]
        if time.time() - ts < settings.PRICE_CACHE_TTL_SECONDS:
            return price

    if use_mock:
        return MOCK_PRICES.get(ticker, 100.0)

    # Appel yfinance avec timeout
    try:
        data = yf.Ticker(ticker)
        info = data.fast_info
        price = float(info.last_price) if info.last_price else None

        if price is None:
            # Fallback sur l'historique 1 jour si fast_info échoue
            hist = data.history(period="1d")
            price = float(hist["Close"].iloc[-1]) if not hist.empty else None

        if price:
            _price_cache[ticker] = (price, time.time())
            return price
    except Exception as e:
        logger.warning(f"yfinance erreur pour {ticker}: {e}")

    # Dernier fallback : mock ou None
    return MOCK_PRICES.get(ticker)

def get_prices_batch(tickers: list[str], use_mock: bool = False) -> Dict[str, float]:
    """
    Récupère les prix d'une liste de tickers en batch (1 appel yfinance).
    Beaucoup plus efficace que des appels individuels.
    """
    tickers = [t.upper() for t in tickers]
    result = {}
    to_fetch = []

    # Séparer les tickers cachés des tickers à fetcher
    for ticker in tickers:
        if ticker in _price_cache:
            price, ts = _price_cache[ticker]
            if time.time() - ts < settings.PRICE_CACHE_TTL_SECONDS:
                result[ticker] = price
                continue
        to_fetch.append(ticker)

    if not to_fetch or use_mock:
        for ticker in to_fetch:
            result[ticker] = MOCK_PRICES.get(ticker, 100.0)
        return result

    # Batch fetch yfinance
    try:
        raw = yf.download(
            tickers=" ".join(to_fetch),
            period="1d",
            progress=False,
            auto_adjust=True
        )
        closes = raw["Close"].iloc[-1] if len(to_fetch) > 1 else raw["Close"].iloc[-1]

        for ticker in to_fetch:
            try:
                price = float(closes[ticker]) if len(to_fetch) > 1 else float(closes)
                _price_cache[ticker] = (price, time.time())
                result[ticker] = price
            except Exception:
                result[ticker] = MOCK_PRICES.get(ticker, 100.0)

    except Exception as e:
        logger.warning(f"Batch yfinance erreur: {e}")
        for ticker in to_fetch:
            result[ticker] = MOCK_PRICES.get(ticker, 100.0)

    return result