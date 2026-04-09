# Astro-Quant: API Reference

This document provides a high-density reference for the core modules of the Astro-Quant framework.

## 1. Astro Engine (`src.astro_engine.engine`)
- **`AstroEngine(ephe_path=None)`**: Main entry point for celestial mechanics.
- **`get_planetary_data(dt, planet)`**: Returns longitude, latitude, and speed.
- **`get_lunar_phase(dt)`**: Returns Moon phase [0, 360].
- **`get_active_aspects(dt, planets, orb=8.0)`**: Scans for active major aspects.

## 2. Ingestion (`src.data_ingestion.fetcher`)
- **`DataFetcher(exchange_id='binance')`**: Multi-source data ingestion.
- **`fetch_crypto(symbol, timeframe, start_date)`**: Fetches OHLCV from CCXT.
- **`fetch_stock(symbol, period='10y')`**: Fetches historical data from YFinance.

## 3. Analysis & Strategy (`src.analyzer`)
### 3.1 `AstroAnalyzer`
- **`enrich_with_astro(df, planets)`**: Merges financial and celestial data.
- **`evaluate_performance(df, planet)`**: Statistical breakdown of returns.

### 3.2 `AstroBacktester`
- **`run_backtest(df, signal_col)`**: Simulates trades with fees.
- **`calculate_performance_metrics(results)`**: Sharpe, Drawdown, ROI.

### 3.3 `AstroPredictor` (ML)
- **`train(df, feature_cols)`**: Trains a Random Forest on celestial features.
- **`predict_next(current_features)`**: Predicts next-day direction probability.

## 4. Visualization (`src.visualizer.charts`)
- **`plot_candlesticks_with_events(df, planet)`**: Candlestick with retro markers.
- **`plot_portfolio_performance(df)`**: Equity and Daily ROI graphs.

---
*AOS Technical Documentation*
