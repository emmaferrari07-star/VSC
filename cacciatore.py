import pandas as pd
from gnews import GNews
import os
import sys # Fondamentale per ricevere ordini dall'app

def avvia_ricerca(tema):
    # Configurazione
    google_news = GNews(language='it', country='IT', max_results=10)
    notizie = google_news.get_news(tema)
    
    if notizie:
        df = pd.DataFrame(notizie)
        if not os.path.exists('Risultati'):
            os.makedirs('Risultati')
        
        # SALVATAGGIO DINAMICO: Il nome del file deve essere uguale al tema
        nome_file = f"Risultati/{tema}.xlsx"
        df.to_excel(nome_file, index=False)
        print(f"✅ Creato file: {nome_file}")
    else:
        print("❌ Nessuna notizia trovata.")

if __name__ == "__main__":
    # Se l'app gli passa un tema, usa quello. Altrimenti usa Geopolitica.
    argomento = sys.argv[1] if len(sys.argv) > 1 else "Geopolitica"
    avvia_ricerca(argomento)