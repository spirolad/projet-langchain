# Cet outil simule un flux de données financières en temps réel (cours d'actions, cryptomonnaies). Il génère des variations aléatoires pour simuler le comportement réel des marchés.
import yfinance as yf

def recuperer_donnees_marche(symbole: str) -> str:
    """
    Récupère le cours réel, la variation et le volume via yfinance.
    """
    symbole = symbole.strip().upper()
    
    try:
        ticker = yf.Ticker(symbole)
        
        info = ticker.info
        
        if not info or 'regularMarketPrice' not in info:
            return f"Données indisponibles pour le symbole : '{symbole}'"

        prix_actuel = info.get('regularMarketPrice')
        prix_precedent = info.get('regularMarketPreviousClose')
        volume = info.get('regularMarketVolume', 0)
        devise = info.get('currency', '$')

        if prix_precedent:
            variation_pct = ((prix_actuel - prix_precedent) / prix_precedent) * 100
        else:
            variation_pct = 0.0

        tendance = '📈' if variation_pct >= 0 else '📉'
        
        return (f"{symbole} {tendance} : {prix_actuel:.2f} {devise} "
                f"({variation_pct:+.2f}%) | Vol: {volume:,}")

    except Exception as e:
        return f"Erreur lors de la récupération de '{symbole}' : {str(e)}"

def obtenir_cours_action(symbole: str) -> str:
    """Interface pour les actions."""

    return recuperer_donnees_marche(symbole)

def obtenir_cours_crypto(symbole: str) -> str:
    """Interface pour les cryptos."""
    s = symbole.upper()
    if not s.endswith("-USD"):
        s = f"{s}-USD"
    return recuperer_donnees_marche(s)

if __name__ == "__main__":
    print("=== Test obtenir_cours_action ===")
    for symbole in ["AAPL", "MSFT", "TSLA", "INCONNU"]:
        print(obtenir_cours_action(symbole))

    print("\n=== Test obtenir_cours_crypto ===")
    for symbole in ["BTC", "ETH", "SOL", "DOGE"]:
        print(obtenir_cours_crypto(symbole))