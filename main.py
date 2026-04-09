import datetime
import pandas as pd
from src.data_ingestion.fetcher import DataFetcher
from src.astro_engine.engine import AstroEngine
from src.analyzer.correlation import AstroAnalyzer
from src.analyzer.backtester import AstroBacktester
from src.visualizer.charts import AstroVisualizer

def main():
    print("--- [Astro-Quant: Gelişmiş Algoritmik Backtest Başlıyor] ---")
    
    # 1. Veri Ingestion
    # Bitcoin (BTC-USD) verisi çekiliyor - YFinance üzerinden geniş kapsamlı analiz için.
    fetcher = DataFetcher()
    print("Adım 1: Bitcoin (BTC-USD) tarihsel verileri çekiliyor...")
    df = fetcher.fetch_stock(symbol="BTC-USD", period="5y")
    df = fetcher.normalize_market_data(df)
    
    # 2. Astro Engine & Analiz
    engine = AstroEngine()
    analyzer = AstroAnalyzer(engine)
    
    print("Adım 2: Gök mekaniği verileri işleniyor (Merkür + Ay Fazı)...")
    # Merkür verilerini ekle
    df = analyzer.enrich_with_astro(df, planets=["Mercury"])
    
    # Ay fazı verilerini ekle (0-360 arası derece)
    df["lunar_phase"] = df["timestamp"].apply(lambda x: engine.get_lunar_phase(x))
    
    # 3. Hibrit Strateji Tanımlama (Signal Engineering)
    # Strateji: Merkür Retrosu YOKKEN ve Ay Büyürken (Waxing - 0 ile 180 arası) ALIM yap.
    print("Adım 3: Hibrit strateji sinyalleri üretiliyor...")
    df["signal"] = (df["Mercury_retrograde"] == False) & (df["lunar_phase"] < 180)
    
    # 4. Backtest Simülasyonu
    print("Adım 4: Portföy simülasyonu çalıştırılıyor...")
    backtester = AstroBacktester(initial_capital=10000.0, commission=0.001)
    results = backtester.run_backtest(df, signal_col="signal")
    
    # 5. Performans Ölçümü
    metrics = backtester.calculate_performance_metrics(results)
    print("\n--- Backtest Sonuçları ---")
    print(f"Başlangıç Sermayesi: $10,000.00")
    print(f"Final Bakiyesi: ${metrics['final_equity']:,.2f}")
    print(f"Toplam Getiri: {metrics['total_return']:.2%}")
    print(f"Sharpe Oranı: {metrics['annualized_sharpe']:.2f}")
    print(f"Maksimum Kayıp (Max Drawdown): {metrics['max_drawdown']:.2%}")
    
    # 6. Görsel Raporlama
    print("\nAdım 5: İnteraktif görsel raporlar üretiliyor...")
    visualizer = AstroVisualizer()
    
    # Fiyat ve Sinyal Grafiği
    visualizer.plot_candlesticks_with_events(results, planet="Mercury", 
                                            output_file="Advanced_Astro_Impact_Analysis.html")
    
    # Portföy Performans Grafiği
    visualizer.plot_portfolio_performance(results, 
                                         output_file="Astro_Portfolio_Performance.html")
    
    print("Done! Raporlar üretildi:")
    print("- Advanced_Astro_Impact_Analysis.html")
    print("- Astro_Portfolio_Performance.html")

if __name__ == "__main__":
    main()
