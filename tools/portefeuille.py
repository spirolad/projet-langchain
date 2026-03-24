# Permet de calculer le networth d'un portefeuille action

import yfinance as yf

def get_networth(portfolio_input: str):
    """
    input = SYMBOLE:QUANTITE|SYMBOLE:QUANTITE
    """
    stocks = portfolio_input.split('|')
    result = ""
    total_networth = 0
    
    for stock in stocks:
            symb, qty_str = stock.split(':')
            quantity = int(qty_str)
            
            ticker = yf.Ticker(symb)
            prix_actuel = ticker.info.get('regularMarketPrice')
            
            if prix_actuel is None:
                result += f"⚠️ {symb} : Impossible de récupérer le prix.\n"
                continue
                
            total_ligne = prix_actuel * quantity
            total_networth += total_ligne
            
            result += f"{symb} : {quantity} x {prix_actuel:.2f}$ = {total_ligne:.2f}$\n"
        
            
    result += "---------------------------\n"
    result += f"TOTAL NETWORTH = {total_networth:.2f}$"
    return result
