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
from src.analyzer.features import AstroFeatureEngineer
from src.analyzer.models import AstroPredictor

def main():
    print("--- [Astro-Quant: Otonom Gök-Finans & ML Dashboard] ---")
    
    # 1. Altyapı Hazırlığı
    fetcher = DataFetcher()
    engine = AstroEngine()
    analyzer = AstroAnalyzer(engine)
    backtester = AstroBacktester()
    visualizer = AstroVisualizer()
    fe = AstroFeatureEngineer()
    
    assets = ["BTC-USD", "GC=F"] # Bitcoin ve Altın
    planets = ["Mercury", "Venus", "Mars", "Jupiter", "Saturn"]
    
    for asset in assets:
        print(f"\n>>> Gelişmiş Analiz: {asset}...")
        
        # 2. Veri Çekme ve Zenginleştirme
        df = fetcher.fetch_stock(symbol=asset, period="10y") # ML için daha uzun veri
        df = fetcher.normalize_market_data(df)
        df_enriched = analyzer.enrich_with_astro(df, planets=planets)
        
        # 3. ML Öznitelik Mühendisliği (Astro-Feature Engineering)
        print(f"   [ML] Döngüsel öznitelikler üretiliyor (Sin/Cos)...")
        df_ml = fe.generate_ml_ready_set(df_enriched, planets=planets)
        
        # Kullanılacak öznitelik sütunları
        feature_cols = []
        for p in planets:
            feature_cols += [f"{p}_sin", f"{p}_cos", f"{p}_speed"]
        
        # 4. Tahminleme Modeli Eğitimi (Machine Learning)
        print(f"   [ML] Random Forest modeli eğitiliyor...")
        predictor = AstroPredictor()
        accuracy = predictor.train(df_ml, feature_cols)
        print(f"   [ML] Test Doğruluğu: {accuracy:.2%}")
        
        # Gelecek için tahmin (Son satır)
        last_features = df_ml[feature_cols].tail(1)
        pred_dict = predictor.predict_next(last_features)
        dir_text = "YUKARI" if pred_dict['direction'] == 1 else "AŞAĞI"
        print(f"   [ML] Yarın İçin Tahmin: {dir_text} (Olasılık: {pred_dict['probability_up']:.2%})")
        
        # 5. İstatistiksel Confluence & Backtest
        confluence = ConfluenceEngine()
        df_enriched["sentiment_score"] = confluence.calculate_sentiment_score(df_enriched)
        df_enriched["signals"] = confluence.get_signal_zones(df_enriched, threshold=0.4)
        
        df_enriched["final_signal"] = df_enriched["signals"] == 1
        results = backtester.run_backtest(df_enriched, signal_col="final_signal")
        metrics = backtester.calculate_performance_metrics(results)
        
        print(f"   [Backtest] Sharpe: {metrics['annualized_sharpe']:.2f} | Getiri: {metrics['total_return']:.2%}")
        
        # 6. Raporlama
        file_name = f"Astro_Quant_ML_Report_{asset.replace('-', '_')}.html"
        visualizer.plot_candlesticks_with_events(results, planet="Mercury", output_file=file_name)
    
    print("\n--- [Sistem İşlemi Tamamlandı] ---")
    print("Otonom ML analizi ve dokümantasyon hazırlandı.")

if __name__ == "__main__":
    main()
