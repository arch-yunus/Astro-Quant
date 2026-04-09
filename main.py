import datetime
from src.data_ingestion.fetcher import DataFetcher
from src.astro_engine.engine import AstroEngine
from src.analyzer.correlation import AstroAnalyzer
from src.visualizer.charts import AstroVisualizer
import os

def main():
    print("--- [Astro-Quant: Veri Analizi Başlıyor] ---")
    
    # 1. Veri Ingestion (Finansal Veri Çekimi)
    # Altın (GC=F) verisi çekiliyor - Güvenli liman varlığı olarak seçilmiştir.
    fetcher = DataFetcher()
    print("Adım 1: Altın (Gold Futures) tarihsel verileri çekiliyor...")
    df = fetcher.fetch_stock(symbol="GC=F", period="5y")
    df = fetcher.normalize_market_data(df)
    
    # 2. Astro Engine Başlatma
    # Gezegensel konumlar ve retrograd hareketleri hesaplayan motor.
    print("Adım 2: Gök mekaniği motoru başlatılıyor (Swiss Ephemeris)...")
    engine = AstroEngine()
    
    # 3. Veri Analizi ve Zenginleştirme
    # Finansal verilere Merkür retrograd durumu ekleniyor.
    print("Adım 3: Merkür döngüleri ile fiyat verileri eşleniyor (Zenginleştirme)...")
    analyzer = AstroAnalyzer(engine)
    enriched_df = analyzer.enrich_with_astro(df, planets=["Mercury"])
    
    # 4. İstatistiksel Rapor Üretimi
    print("Adım 4: İstatistiksel korelasyon raporu çıkarılıyor...")
    summary = analyzer.generate_report_summary(enriched_df, planet="Mercury")
    print(summary)
    
    # 5. Görselleştirme (Plotly HTML Raporu)
    print("Adım 5: İnteraktif görsel rapor üretiliyor...")
    visualizer = AstroVisualizer()
    visualizer.plot_candlesticks_with_events(
        enriched_df, 
        planet="Mercury", 
        output_file="Mercury_Retro_Impact_Report.html"
    )
    
    print("Done! 'Mercury_Retro_Impact_Report.html' dosyası üretildi.")

if __name__ == "__main__":
    main()
