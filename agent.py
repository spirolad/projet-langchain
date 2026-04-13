from langchain_classic.tools import Tool

from tools.database import rechercher_client, rechercher_produit
from tools.finance import obtenir_cours_action, obtenir_cours_crypto
from tools.calculs import calculer_interets_composes, calculer_marge, calculer_mensualite_pret, calculer_tva
from tools.api_publique import convertir_devise
from tools.texte import  extraire_mots_cles, formater_rapport, resumer_texte
from tools.recommandation import recommander_produits
from tools.portefeuille import get_networth
from tools.tavily import answer_open_question
from langchain_experimental.tools import PythonREPLTool

python_repl = PythonREPLTool()
python_repl.description = (
     'Exécute du code Python pour des calculs complexes ou traitements '
     'de données non couverts par les autres outils. '
     'Entrée : code Python valide sous forme de chaîne.'
)

tools =[
    # ── Outil 1 : Base de données ─────────────────────────────────────
    Tool(name='rechercher_client', func=rechercher_client,
         description='Recherche un client par nom ou ID (ex: C001). '
                     'Retourne solde, type de compte, historique achats.'),
    Tool(name='rechercher_produit', func=rechercher_produit,
         description='Recherche un produit par nom ou ID. '
                     'Retourne prix HT, TVA, prix TTC, stock.'),
    # ── Outil 2 : Données financières ─────────────────────────────────
    Tool(name='cours_action', func=obtenir_cours_action,
         description='Cours boursier d\'une action. '
                     'Entrée : symbole majuscule ex AAPL, MSFT, TSLA, LVMH, AIR.'),
    Tool(name='cours_crypto', func=obtenir_cours_crypto,
         description='Cours d\'une crypto. '
                     'Entrée : symbole ex BTC, ETH, SOL, BNB, DOGE.'),
    # ── Outil 3 : Calculs financiers ──────────────────────────────────
    Tool(name='calculer_tva', func=calculer_tva,
         description='Calcule TVA et prix TTC. Entrée : prix_ht,taux ex 100,20.'),
    Tool(name='calculer_interets', func=calculer_interets_composes,
         description='Intérêts composés. Entrée : capital,taux_annuel,années ex 10000,5,3.'),
    Tool(name='calculer_marge', func=calculer_marge,
         description='Marge commerciale. Entrée : prix_vente,cout_achat ex 150,80.'),
    Tool(name='calculer_mensualite', func=calculer_mensualite_pret,
         description='Mensualité prêt. Entrée : capital,taux_annuel,mois ex 200000,3.5,240.'),
    # ── Outil 4 : API publique ────────────────────────────────────────
    Tool(name='convertir_devise', func=convertir_devise,
         description='Conversion de devises en temps réel (API Frankfurter). '
                     'Entrée : montant,DEV_SOURCE,DEV_CIBLE ex 100,USD,EUR.'),
    # ── Outil 5 : Transformation de texte ────────────────────────────
    Tool(name='resumer_texte', func=resumer_texte,
         description='Résume un texte et donne des statistiques. Entrée : texte complet.'),
    Tool(name='formater_rapport', func=formater_rapport,
         description='Formate en rapport. Entrée : Cle1:Val1|Cle2:Val2.'),
    Tool(name='extraire_mots_cles', func=extraire_mots_cles,
         description='Extrait les mots-clés d\'un texte. Entrée : texte complet.'),
    # ── Outil 6 : Recommandation ─────────────────────────────────────
    Tool(name='recommander_produits', func=recommander_produits,
         description='Recommandations produits. '
                     'Entrée : budget,categorie,type_compte ex 300,Informatique,Premium. '
                     'Catégories : Informatique, Mobilier, Audio, Toutes. '
                     'Types : Standard, Premium, VIP.'),
     # ── Outil 7 : Portefeuille ─────────────────────────────────────
     Tool(name="portefeuille", func=get_networth,
          description='Calcul de la valeur cumule de plusieurs actions'
                      'Entree: SYMBOLE:QUANTITE|SYMBOLE:QUANTITE'
                      'Sortie: Format pour chaque action: symb quantity = total'
                      'Derniere ligne: Somme = total_prix'),
     # ── Outil 8 : Tavily ─────────────────────────────────────
     Tool(name="tavily", func=answer_open_question,
          description='Permet de répondre à des questions ouvertes comme'
                       'actualités financières, informations sur une entreprise, cours récents non'
                       'couverts par les autres outils.'),
     # ── Outil 9 : PythonREPLTool ─────────────────────────────────────
     python_repl
]

def creer_agent():
    """Crée et retourne un agent LangChain configuré."""
    from langchain_openai import ChatOpenAI
    from langchain_classic.agents import AgentExecutor, create_openai_tools_agent
    from langchain_classic.memory import ConversationBufferMemory
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    import os

    # Initialisation du LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,           # 0 = déterministe (résultats reproductibles)
        openai_api_key=os.getenv('OPENAI_API_KEY')
    )
    # Prompt chat-compatible pour OpenAI Tools + historique conversationnel.
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Tu es un assistant financier précis et concis. "
            "Utilise les outils quand nécessaire et réutilise l'historique de conversation."
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    # Mémoire courte conversationnelle partagée entre les tours.
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        input_key="input",
        output_key="output",
        return_messages=True,
    )

    # Création de l'agent avec la stratégie OpenAI Tools.
    agent = create_openai_tools_agent(llm=llm, tools=tools, prompt=prompt)

    # Création de l'exécuteur
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        memory=memory,
        verbose=True,            # Affiche le raisonnement étape par étape
        max_iterations=10,       # Évite les boucles infinies
        handle_parsing_errors=True
    )
    return agent_executor


def interroger_agent(agent, question: str):
    """Envoie une question à l'agent et affiche la réponse finale."""
    print(f"\n{'='*60}")
    print(f"Question : {question}")
    print('='*60)
    result = agent.invoke({"input": question})
    print(f"\nRéponse finale : {result['output']}")
    return result

