import streamlit as st
import pandas as pd
import datetime
from src.data_ingestion.fetcher import DataFetcher
from src.astro_engine.engine import AstroEngine
from src.analyzer.correlation import AstroAnalyzer
from src.analyzer.backtester import AstroBacktester
from src.analyzer.optimizer import AstroOptimizer
from src.analyzer.signals import ConfluenceEngine
from src.visualizer.charts import AstroVisualizer
from src.analyzer.features import AstroFeatureEngineer
from src.analyzer.models import AstroPredictor

# Page Configuration for "WOW" Factor
st.set_page_config(page_title="Astro-Quant Master Dashboard", layout="wide", page_icon="??")

# High-Density CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stMetric { background-color: #1a1c24; padding: 15px; border-radius: 10px; border: 1px solid #30333d; }
    .stPlotlyChart { border-radius: 10px; overflow: hidden; }
    </style>
""", unsafe_allow_html=True)

st.title("?? Astro-Quant: Otonom Gök-Finans Kontrol Paneli")
st.markdown("*Akademik İşletim Sistemi (AOS) & Medresetü’z-Zehra Vizyonu*")

# --- Sidebar: Configuration ---
st.sidebar.header("?? Sistem Yapılandırması")
asset = st.sidebar.selectbox("Analiz Edilecek Varlık", ["BTC-USD", "ETH-USD", "GC=F", "NQ=F"])
lookback = st.sidebar.slider("Geçmiş Veri (Yıl)", 1, 10, 5)
threshold = st.sidebar.slider("Confluence Eşiği (Threshold)", 0.1, 1.0, 0.4)

st.sidebar.divider()
st.sidebar.subheader("?? Gezegen Ağırlıkları (Confluence)")
w_merc = st.sidebar.slider("Merkür", 0.0, 1.0, 0.4)
w_venus = st.sidebar.slider("Venüs", 0.0, 1.0, 0.3)
w_mars = st.sidebar.slider("Mars", 0.0, 1.0, 0.2)

# --- Logic: Data Orchestration ---
@st.cache_data(ttl=3600)
def load_data(asset, period):
    fetcher = DataFetcher()
    df = fetcher.fetch_stock(symbol=asset, period=f"{period}y")
    return fetcher.normalize_market_data(df)

df = load_data(asset, lookback)

# Engine Initialization
engine = AstroEngine()
analyzer = AstroAnalyzer(engine)
backtester = AstroBacktester()
visualizer = AstroVisualizer()
fe = AstroFeatureEngineer()
predictor = AstroPredictor()

# Enrichment
planets = ["Mercury", "Venus", "Mars"]
df_enriched = analyzer.enrich_with_astro(df, planets=planets)

# Confluence Logic
confluence = ConfluenceEngine(weights={"Mercury": w_merc, "Venus": w_venus, "Mars": w_mars})
df_enriched["sentiment_score"] = confluence.calculate_sentiment_score(df_enriched)
df_enriched["signals"] = confluence.get_signal_zones(df_enriched, threshold=threshold)
df_enriched["final_signal"] = df_enriched["signals"] == 1

# Performance
results = backtester.run_backtest(df_enriched, signal_col="final_signal")
metrics = backtester.calculate_performance_metrics(results)

# --- UI: Metrics Row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Final Bakiye", f"${metrics['final_equity']:,.2f}")
col2.metric("Toplam Getiri", f"{metrics['total_return']:.2%}")
col3.metric("Sharpe Oranı", f"{metrics['annualized_sharpe']:.2f}")
col4.metric("Maksimum Kayıp", f"{metrics['max_drawdown']:.2%}")

# --- UI: Main Content ---
st.divider()

tab1, tab2, tab3 = st.tabs(["?? Teknik Analiz & Sinyaller", "?? Portföy Performansı", "?? ML Gelecek Tahmini"])

with tab1:
    fig_price = visualizer.plot_candlesticks_with_events(results, planet="Mercury")
    st.plotly_chart(fig_price, use_container_width=True)

with tab2:
    fig_perf = visualizer.plot_portfolio_performance(results)
    st.plotly_chart(fig_perf, use_container_width=True)

with tab3:
    st.subheader("?? Yapay Zeka (AI) Yön Tahmini")
    # Simple training for the demo context
    df_ml = fe.generate_ml_ready_set(df_enriched, planets=planets)
    feature_cols = [f"{p}_sin" for p in planets] + [f"{p}_cos" for p in planets]
    
    accuracy = predictor.train(df_ml, feature_cols)
    last_features = df_ml[feature_cols].tail(1)
    pred_dict = predictor.predict_next(last_features)
    
    c1, c2 = st.columns(2)
    c1.info(f"Yarın İçin Tahmin: **{'YUKARI' if pred_dict['direction'] == 1 else 'AŞAĞI'}**")
    c1.write(f"Tahmin Güveni (Probability): {pred_dict['probability_up']:.2%}")
    c2.write(f"Model Test Doğruluğu (Accuracy): {accuracy:.2%}")
    st.progress(accuracy)

st.success("Sistem Çalışıyor: Otonom gök-finans verileri gerçek zamanlı senkronize edildi.")
