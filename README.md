# Astro-Quant: Kantitatif Gök-Finans Korelasyon Çerçevesi

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![Status: Academic Production](https://img.shields.io/badge/Status-Akademik_Üretim-green.svg)]()
[![Framework: Medresetü’z-Zehra](https://img.shields.io/badge/Framework-Medreset%C3%BC%E2%80%99z--Zehra-midnightblue.svg)]()

**Astro-Quant**, göksel mekanik (efemeris verileri, gezegen döngüleri, dizilimler) ile küresel finansal denge (kripto varlıklar, emtialar, hisse senetleri) arasındaki tarihsel ve algoritmik korelasyonları analiz etmek üzere tasarlanmış ileri düzey, yüksek yoğunluklu bir kantitatif araştırma çerçevesidir.

Klasik astronomik hesaplamalar ile modern finansal veri bilimi arasındaki boşluğu dolduran Astro-Quant, doğrusal olmayan piyasa iticilerini test etmek (backtesting) ve asimetrik algoritmik ticaret stratejileri geliştirmek için titiz bir matematiksel ortam sunar.

---

## 00. Felsefi Temel
Doğa bilimlerini mesleki uzmanlıkla bütünleştirmeyi hedefleyen **Medresetü’z-Zehra** vizyonu üzerine inşa edilen Astro-Quant, kozmosu devasa ve deterministik bir saat mekanizması olarak ele alır. Göksel mekanikteki makro döngülerin, küresel likidite havuzlarında öngörülebilir volatilite kümeleri veya trend dönüşleri olarak tezahür eden sistematik insan davranışlarını ölçeklenebilir düzeyde yansıttığı hipotezini savunur.

---

## 01. Çekirdek Mimari

Sistem, yüksek verimli veri işleme ve sinyal çıkarma işlemleri için modüler bir boru hattı (pipeline) olarak yapılandırılmıştır:

### A. Efemeris Vektör Uzayı Eşlemesi (`src/astro_engine`)
- **Hassas Hesaplama**: Yüksek hassasiyetli gezegen konumlandırması için standart efemeris kütüphaneleri (Swiss Ephemeris / PyEphem) entegrasyonu.
- **Harmonikler ve Açılar**: Zamansal bir vektör uzayına eşlenmiş majör ve minör açılar (Kavuşum, Karşıt, Üçgen, Kare) gerçek zamanlı hesaplanır.
- **Retrograd Dinamikleri**: Gezegenlerin geri hareketlerinin otomatik tespiti ve piyasa duyarlılığı üzerindeki etkisinin meta-veri olarak işlenmesi.

### B. Çok Kaynaklı Finansal Veri Çekimi (`src/data_ingestion`)
- **CEX/DEX Bağlantıları**: Binance, Kraken ve Web3 sağlayıcıları üzerinden merkeziyetsiz likidite havuzları için yerel destek.
- **Geleneksel Piyasalar**: Tarihsel hisse senedi ve emtia veri setleri için Yahoo Finance ve Alpha Vantage entegrasyonu.
- **Normalizasyon Motoru**: Eksik zaman serisi verilerinin onarılması ve zaman dilimi hizalamaları için sağlam veri hatları.

### C. Kantitatif Korelasyon Motoru (`src/analyzer`)
- **İstatistiksel Anlamlılık**: "Sahte korelasyonları" filtrelemek için p-değerleri ve güven aralıkları kullanılarak yapılan titiz hipotez testleri.
- **Volatilite Kümelenmesi**: Göksel olayların GARCH modelli volatilite değişimleri üzerindeki tetikleyici etkisinin analizi.
- **Makine Öğrenimi Hazırlığı**: Gezegensel boylam, enlem, hız ve faz gibi yüksek yoğunluklu özellik setlerinin doğrudan Scikit-Learn veya PyTorch hatlarına aktarımı.

---

## 02. Dizin İskeleti

```text
Astro-Quant/
├── src/                        # Çekirdek algoritmik motor
│   ├── astro_engine/           # Gök koordinatları ve açı hesaplamaları
│   ├── data_ingestion/         # API bağlantıları (Binance, YFinance, Web3)
│   ├── analyzer/               # Korelasyon matematiği ve sinyal mantığı
│   └── visualizer/             # Plotly/Matplotlib yüksek yoğunluklu grafikler
├── research/                   # Akademik derinlemesine incelemeler
│   ├── notebooks/              # Jupyter araştırma ortamları
│   └── papers/                 # Teknik teknik makaleler (LATEX)
├── infrastructure/             # Dağıtım ve yapılandırma
│   ├── api_secrets/            # Yönetilen kimlik bilgileri (yerel)
│   └── docker/                 # Konteynırlaştırma meta-verileri
├── docs/                       # Yüksek yoğunluklu teknik spesifikasyonlar
├── LICENSE                     # MIT Yönetişimi
└── README.md                   # Sistem Genel Bakışı
```

---

## 03. Mühendislik Kurulumu

### Ortam Başlatma
```bash
# Depoyu klonlayın
git clone https://github.com/arch-yunus/Astro-Quant.git
cd Astro-Quant

# Sanal araştırma ortamını oluşturun
python -m venv venv
source venv/bin/activate  # Linux/macOS
# .\venv\Scripts\Activate.ps1 # Windows

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### Yapılandırma (`infrastructure/.env`)
Güvenli API yönetimi için `.env` dosyası oluşturun:
```env
BINANCE_API_KEY=ANAHTARINIZ
BINANCE_API_SECRET=SIRRINIZ
SWISS_EPHE_PATH=/efemeris/yolu
```

---

## 04. Algoritmik Yürütme Akışı

**Örnek**: Merkür Retrosu ile BTC/USDT volatilitesi arasındaki 10 yıllık korelasyon analizi.

```python
from src.analyzer import AstroFinanceAnalyzer
from src.data_ingestion import CryptoFetcher

# 1. Yüksek Yoğunluklu Veri Çekimini Başlat
fetcher = CryptoFetcher(symbol="BTCUSDT", interval="1d", depth="10y")
df = fetcher.get_dataframe()

# 2. Korelasyon Analizini Düzenle
model = AstroFinanceAnalyzer(data=df)
signal_report = model.evaluate_event(
    planet="Mercury", 
    state="Retrograde", 
    metric="Volatility"
)

# 3. Analitik Çıktı Üret
print(f"Güven Seviyesi: {signal_report.p_value}")
print(f"Ortalama ROI Varyansı: {signal_report.avg_performance}")
model.plot_signals("Mercury_Retro_BTC_Correlation.html")
```

---

## 05. Araştırma Yol Haritası (Roadmap)

- [x] **Tier 0**: Çekirdek Efemeris Motoru ve DataFrame Normalizasyonu.
- [x] **Tier 1**: Temel Korelasyon Testleri (Açılar vs. Fiyat Hareketleri).
- [ ] **Tier 2**: Asimetrik Risk Modelli Gelişmiş Backtesting Motoru.
- [ ] **Tier 3**: Otonom Sinyal Üretimi (Webhook/Discord Entegrasyonu).
- [ ] **Tier 4**: DeFi Havuzlarında Ay Fazı Likidite Döngüleri Entegrasyonu.
- [ ] **Tier 5**: "Celestial Market Drivers" Veri Setinin Tam Akademik Yayını.

---

## 06. Yönetişim ve Akademik Katkı
Bu depo, profesyonel ve bilimsel olarak tarafsız bir platformdur. Katkıların yüksek yoğunluklu kodlama standartlarına uyması ve temel astronomik/finansal mantığın titizlikle belgelenmesi gerekmektedir.

**Sorumluluk Reddi**: Tüm analitik çıktılar araştırma ve eğitim amaçlıdır. Finansal piyasalar doğası gereği risklidir; göksel korelasyonlar yatırım tavsiyesi (YTD) teşkil etmez.

---
*Akademik İşletim Sistemi (AOS) vizyonu altında geliştirilmiştir.*
