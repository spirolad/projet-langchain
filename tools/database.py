# Cet outil simule une base de données relationnelle contenant des informations sur les clients et les produits d'une PME. Il permet à l'agent de répondre à des questions du type : «Quel est le solde du compte de Marie Dupont ?» ou «Combien coûte le produit X ?»

import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """Établit la connexion à la base MySQL Docker."""
    return mysql.connector.connect(
        host='localhost',
        port=3306,
        database='db',
        user='user',
        password='password'
    )

def rechercher_client(query: str) -> str:
    """Recherche un client par nom ou par ID dans la DB."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM client WHERE id = %s OR name LIKE %s"
        cursor.execute(sql, (query.strip().upper(), f"%{query}%"))
        
        client = cursor.fetchone()
        if client:
            return (f"Client : {client['name']} | Solde : {client['balance']:.2f} € "
                    f"| Type de compte : {client['account_type']}")
        return f"Aucun client trouvé pour : '{query}'"
    
    except Error as e:
        return f"Erreur DB : {e}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def rechercher_produit(query: str) -> str:
    """Recherche un produit et calcule la TVA dynamiquement."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        sql = "SELECT * FROM product WHERE id = %s OR name LIKE %s"
        cursor.execute(sql, (query.strip().upper(), f"%{query}%"))
        
        produit = cursor.fetchone()
        if produit:
            prix_ht = produit['price']
            tva = prix_ht * 0.20
            prix_ttc = prix_ht + tva
            return (f"Produit : {produit['name']} | Prix HT : {prix_ht:.2f} € "
                    f"| TVA : {tva:.2f} € | Prix TTC : {prix_ttc:.2f} € | Stock : {produit['stock']}")
        return f"Aucun produit trouvé pour : '{query}'"
    
    except Error as e:
        return f"Erreur DB : {e}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()

def lister_tous_les_clients(query: str = "") -> str:
    """Retourne la liste complète de tous les clients depuis la DB."""
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        cursor.execute("SELECT id, name, account_type, balance FROM client")
        clients = cursor.fetchall()
        
        result = "Liste des clients (Base de données) :\n"
        for c in clients:
            result += f"  {c['id']} : {c['name']} | {c['account_type']} | Solde : {c['balance']:.2f} €\n"
        return result
    
    except Error as e:
        return f"Erreur DB : {e}"
    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
    
if __name__ == "__main__":
    print("=== Test rechercher_client ===")
    print(rechercher_client("Marie Dupont"))
    print(rechercher_client("C002"))
    print(rechercher_client("inconnu"))

    print("\n=== Test rechercher_produit ===")
    print(rechercher_produit("P001"))
    print(rechercher_produit("Souris"))
    print(rechercher_produit("inconnu"))

    print("\n=== Test lister_tous_les_clients ===")
    print(lister_tous_les_clients())