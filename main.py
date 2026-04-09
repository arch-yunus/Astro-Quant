import datetime
import pandas as pd
from src.data_ingestion.fetcher import DataFetcher
from src.astro_engine.engine import AstroEngine
from src.analyzer.correlation import AstroAnalyzer
from src.analyzer.backtester import AstroBacktester
from src.analyzer.optimizer import AstroOptimizer
from src.analyzer.signals import ConfluenceEngine
from src.visualizer.charts import AstroVisualizer
from src.infrastructure.notifier import DiscordNotifier

def main():
    print("--- [Astro-Quant: Otonom Gök-Finans Dashboard Başlatılıyor] ---")
    
    # 1. Altyapı Hazırlığı
    fetcher = DataFetcher()
    engine = AstroEngine()
    analyzer = AstroAnalyzer(engine)
    backtester = AstroBacktester()
    notifier = DiscordNotifier() # Webhook URL opsiyonel
    visualizer = AstroVisualizer()
    
    # Analiz edilecek varlıklar
    assets = ["BTC-USD", "ETH-USD", "GC=F"] # Bitcoin, Ethereum, Altın
    planets = ["Mercury", "Venus", "Mars"]
    
    reports = []
    
    for asset in assets:
        print(f"\n>>> Analiz Ediliyor: {asset}...")
        
        # 2. Veri Çekme ve Zenginleştirme
        df = fetcher.fetch_stock(symbol=asset, period="5y")
        df = fetcher.normalize_market_data(df)
        df_enriched = analyzer.enrich_with_astro(df, planets=planets)
        
        # 3. Optimizasyon (En İyi Gezegensel Etkiyi Bul)
        optimizer = AstroOptimizer(df, analyzer, backtester)
        best_retro_info = optimizer.optimize_retrograde_impact(planet="Mercury")
        print(f"   [Optimizasyon] En iyi Merkür stratejisi: {best_retro_info['best_mode']}")
        
        # 4. Confluence (Fikir Birliği) Sinyalleri
        confluence = ConfluenceEngine()
        df_enriched["sentiment_score"] = confluence.calculate_sentiment_score(df_enriched)
        df_enriched["signals"] = confluence.get_signal_zones(df_enriched, threshold=0.4)
        
        # 5. Backtest (Hibrit Confluence Stratejisi)
        # Sinyal: Sentiment > 0.4 ise AL
        df_enriched["final_signal"] = df_enriched["signals"] == 1
        results = backtester.run_backtest(df_enriched, signal_col="final_signal")
        metrics = backtester.calculate_performance_metrics(results)
        
        # 6. Bildirim ve Kayıt
        last_sentiment = results["sentiment_score"].iloc[-1]
        last_signal = "LONG" if results["signals"].iloc[-1] == 1 else "WAIT"
        
        print(f"   [Performans] Sharpe: {metrics['annualized_sharpe']:.2f} | Getiri: {metrics['total_return']:.2%}")
        notifier.send_trade_signal(asset, last_signal, last_sentiment)
        
        # 7. Görselleştirme (Her varlık için rapor)
        file_name = f"Astro_Quant_Dashboard_{asset.replace('=', '_')}.html"
        visualizer.plot_candlesticks_with_events(results, planet="Mercury", output_file=file_name)
        reports.append(file_name)
        
    print("\n--- [İşlem Tamamlandı] ---")
    print(f"Üretilen Raporlar: {', '.join(reports)}")
    print("Otonom sinyaller işlendi.")

if __name__ == "__main__":
    main()
