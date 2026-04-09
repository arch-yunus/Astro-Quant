import argparse
import sys
from main import main as run_demo
from src.data_ingestion.fetcher import DataFetcher
from src.astro_engine.engine import AstroEngine
from src.analyzer.correlation import AstroAnalyzer

def main():
    parser = argparse.ArgumentParser(description="?? Astro-Quant: Professional CLI Terminal")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: run (Runs the main demo)
    subparsers.add_parser("run", help="Run the full automated orchestration demo")

    # Command: analyze
    analyze_parser = subparsers.add_parser("analyze", help="Analyze asset for celestial impact")
    analyze_parser.add_argument("--asset", type=str, default="BTC-USD", help="Target asset symbol")
    analyze_parser.add_argument("--period", type=str, default="5y", help="Historical period")
    analyze_parser.add_argument("--planet", type=str, default="Mercury", help="Target planet")

    args = parser.parse_args()

    if args.command == "run":
        run_demo()
    elif args.command == "analyze":
        print(f"--- [Astro-Quant Center: {args.asset}] ---")
        fetcher = DataFetcher()
        engine = AstroEngine()
        analyzer = AstroAnalyzer(engine)
        
        df = fetcher.fetch_stock(symbol=args.asset, period=args.period)
        df = fetcher.normalize_market_data(df)
        df_enriched = analyzer.enrich_with_astro(df, planets=[args.planet])
        
        stats = analyzer.evaluate_performance(df_enriched, planet=args.planet)
        print(f"Planetary Impact ({args.planet}):")
        print(f"  Direct ROI: {stats['direct_return']:.2%}")
        print(f"  Retrograde ROI: {stats['retrograde_return']:.2%}")
        print(f"  Impact Coefficient: {stats['impact_coefficient']:.2f}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
