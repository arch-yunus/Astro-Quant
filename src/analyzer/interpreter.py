import json
from typing import Dict, Any, Optional

class AstroInterpreter:
    """
    High-density AI-driven interpreter for Astro-Quant results.
    Generates professional academic narratives in Turkish (AOS Standard).
    """

    def __init__(self):
        pass

    def generate_prompt_for_llm(self, metrics: Dict[str, Any], asset: str) -> str:
        """
        Generates a structured prompt that can be sent to an LLM (GPT-4, etc.)
        for professional interpretation.
        """
        prompt = f"""
AKTÖR: Astro-Quant Akademik Analist (Medresetü’z-Zehra AOS Standardı)
GÖREV: Aşağıdaki kantitatif verileri profesyonel, bilimsel ve teknik bir dille yorumla.
VARLIK: {asset}
VERİLER:
- Toplam Getiri: {metrics.get('total_return', 0):.2%}
- Sharpe Oranı: {metrics.get('annualized_sharpe', 0):.2f}
- Maksimum Kayıp: {metrics.get('max_drawdown', 0):.2%}
- Sinyal Sentimenti: {metrics.get('sentiment', 0):.2f}

ANALİZ FORMATI: 
1. Fenomenolojik ve Matematiksel Tespitler.
2. Kozmik Döngülerin Piyasa Likiditesi Üzerindeki Makro Etkisi.
3. Akademik Sonuç ve Stratejik Öngörü.
Lisan: Profesyonel Türkçe.
"""
        return prompt

    def generate_static_narrative(self, metrics: Dict[str, Any], asset: str) -> str:
        """
        Generates a predefined high-density narrative for environments without LLM access.
        """
        roi = metrics.get('total_return', 0)
        sharpe = metrics.get('annualized_sharpe', 0)
        
        narrative = f"""
{asset} üzerine yapılan otonom gök-finans analizi sonucunda, {roi:.2%} oranında bir toplam getiri ve {sharpe:.2f} Sharpe rasyosu ile yüksek yoğunluklu bir korelasyon tespit edilmiştir. 
Akademik İşletim Sistemi (AOS) çerçevesinde, bu veriler gezegensel fazların piyasa volatilitesi üzerindeki deterministik etkilerini 
doğrular niteliktedir. Medresetü’z-Zehra vizyonuyla uyumlu olarak, doğa yasalarının finansal döngülerle entegrasyonu operasyonel başarısını kanıtlamıştır.
"""
        return narrative
