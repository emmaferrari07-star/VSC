# --- 1. IMPORTAZIONE DI CODICI PRECOMPILATI FUNZIONALI ---
import streamlit as st                  # framework che traduce il codice in web app
import pandas as pd                     # libreria per analisi, manipolazione, pulizia dati (usata per file xlsx in cacciatore.py) 
import os                               # carica l'Operating System per gestire directory e path 
import google.generativeai as genai     # modello di intelligenza artificale generativa utilizzato 
from PIL import Image                   # importazione dell'immagina utilizzata 
import cacciatore                       # collega app.py a cacciatore.py 
from gnews import GNews                 # permette il reperimento dalle notizie Google News 



# --- 2. DEFINIZIONE REPERIMENTO ULTIME NOTIZIE DA GOOGLE NEWS ---
def esegui_cacciatore(tema):                                                            # all'interno del termine "tema" stanno le sezioni dell'app
    google_news = GNews(language='it', country='IT', period='7d', max_results=10)       # criteri di selezione delle notizie
    notizie = google_news.get_news(tema)                                                # reperisce le notizie e le salva come un pacchetto disordinato di "notizie" (contiene link, date...)
    df = pd.DataFrame(notizie)                                                          # Pandas trasforma il pacchetto in un file excel ordinato
    df.to_excel(f"Risultati/{tema}.xlsx", index=False)                                  # salva la tabella excel sul mio computer
    return True                                                                         # fa attivamente ricaricare l'interfaccia con i nuovi dati



# --- 3. CONFIGURAZIONE PAGINA ---
st.set_page_config(page_title="Cacciatore", layout="wide")



# --- 4. LAYER DI STILE (CSS) ---
def load_custom_style():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        
        .main { background-color: #ffffff; color: #000000; }
        
        .nav-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            border-bottom: 1px solid #eeeeee;
            font-family: 'Inter', sans-serif;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-size: 0.8rem;
        }

        /* HEADLINE CHE NON VA A CAPO */
        .headline {
            font-family: 'Georgia', serif;
            font-size: 5vw; 
            line-height: 0.8;
            margin-bottom: 1rem;
            text-transform: uppercase;
            font-weight: 900;
            white-space: nowrap; /* Non va a capo */
            overflow: hidden;    /* Non esce dallo schermo */
            display: block;
            width: 100%;         /* Si adatta al contenitore */
        }

        .subheadline {
            font-size: 1.1rem;
            font-weight: bold;
            text-transform: uppercase;
            font-family: 'Inter', sans-serif;
        }

        .body-text {
            font-size: 0.9rem;
            color: #666666;
            font-family: 'Inter', sans-serif;
        }

        /* NASCONDI IL BOTTONE STANDARD DELLA SIDEBAR (lo attiviamo noi col menu) */
        [data-testid="stSidebarNav"] {display: none;}
        </style>
    """, unsafe_allow_html=True)
load_custom_style()



# --- 5. LOGICA DI NAVIGAZIONE E HERO ---

# Header 
st.markdown("""
    <div class="nav-container">
        <div class="logo-text">CACCIATORE</div>
    </div>
""", unsafe_allow_html=True)

# Layout Hero
col_text, col_spacer = st.columns([2, 1])

with col_text:
    st.markdown('<div class="hero-container">', unsafe_allow_html=True)
    # La headline ora reagisce al restringimento della colonna
    st.markdown('<div class="headline">CACCIATORE</div>', unsafe_allow_html=True)
    st.markdown('<div class="subheadline">Dashboard di analisi di intelligence e IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="body-text">Consulta e compara le ultime notizie del giorno.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Visualizzazione Immagine Hero
if os.path.exists("hero_image.jpeg"):
    image = Image.open("hero_image.jpeg")
    st.image(image, use_container_width=True)
else:
    st.warning("Assicurati di avere 'hero_image.jpeg' nella cartella del progetto.")

st.divider()



# --- 6. SIDEBAR (HOME) ---

st.sidebar.title("HOME")
tema = st.sidebar.selectbox(
    "Scegli il tema che vuoi approfondire:", 
    ["Geopolitica", "Letteratura", "Arte", "Scienze"]
)
# Definizione del percorso del file subito dopo la scelta del tema
percorso_file = f"Risultati/{tema}.xlsx"

if st.sidebar.button("🚀 Aggiorna Notizie Ora"):
    with st.spinner(f"Il cacciatore sta cercando notizie su: {tema}..."):
        if esegui_cacciatore(tema): 
            st.sidebar.success("Aggiornamento completato!")
            st.rerun()



# --- 7. CONFIGURAZIONE CHIAVE API DI GOOGLE GEMINI ---

API_KEY = "AIzaSyAYT0Y3ZvT6Oqz4rX-hWNvRPg19ZApjAGo" 
genai.configure(api_key=API_KEY)



# --- 8. CONFIGURAZIONE MODELLO CON AUTO-DIAGNOSI ---
try:
    # 1. Elenco di tutti i modelli disponibili per il mio account
    modelli_disponibili = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    
    if modelli_disponibili:
        # Puliamo i nomi (spesso arrivano come 'models/gemini-1.5-flash')
        scelta = modelli_disponibili[0] # Prende il primo della lista (il più compatibile)
        model = genai.GenerativeModel(scelta)
        print(f"✅ Modello selezionato automaticamente: {scelta}")
    else:
        model = genai.GenerativeModel('gemini-pro') # Ultima spiaggia
except Exception as e:
    st.error(f"Errore nella lista modelli: {e}")
    model = genai.GenerativeModel('gemini-pro')



# --- 9. FUNZIONI DI SUPPORTO ---
# Esecuzione reperimento ultime notizie da Google News
def render_news_section(nome_sezione, anchor_id):
    if st.button(f"Aggiorna {nome_sezione}", key=f"btn_{anchor_id}"):
        with st.spinner(f"Cacciando {nome_sezione}..."):
            esegui_cacciatore(nome_sezione) 
            st.rerun()

def genera_analisi_ai(titolo, fonte, data):
    prompt = f"Analizza sinteticamente questa notizia di intelligence: {titolo} (Fonte: {fonte})."
    try:
        # Forziamo l'invio al modello caricato
        response = model.generate_content(prompt)
        # Alcune versioni della libreria richiedono .text, altre hanno strutture diverse
        if hasattr(response, 'text'):
            return response.text
        else:
            return "L'AI ha risposto ma il formato non è leggibile."
    except Exception as e:
        return f"Errore tecnico: {str(e)}"




# --- 10. INTERFACCIA SIDEBAR ---

st.sidebar.divider()
st.sidebar.info("L'analisi AI utilizza Google Gemini per riassumere i contenuti estratti.")



# --- 11. AREA PRINCIPALE (DASHBOARD) ---

st.title("🕵️‍♀️ Intelligence & AI Analysis Dashboard")
st.markdown(f"Stai analizzando il settore: **{tema}**")
st.divider()

if os.path.exists(percorso_file):
    try:
        df = pd.read_excel(percorso_file)
        
        if df.empty:
            st.warning("Il file esiste ma non contiene notizie.")
        else:
            # Layout per ogni notizia
            for index, row in df.iterrows():
                # Gestione sicura della fonte
                p = row.get('publisher', 'Fonte Sconosciuta')
                nome_fonte = p.get('title', 'Fonte Sconosciuta') if isinstance(p, dict) else str(p)
                data_notizia = row.get('published date', 'N/D')
                
                with st.expander(f"📌 {row['title']}"):
                    col1, col2 = st.columns([0.6, 0.4])
                    
                    with col1:
                        st.write(f"**Fonte:** {nome_fonte}")
                        st.write(f"**Data:** {data_notizia}")
                        st.link_button("Leggi Articolo Originale", row['url'])
                    
                    with col2:
                        # Tasto per analisi AI singola
                        if st.button(f"🧠 Analizza con AI", key=f"btn_{index}"):
                            with st.status("L'AI sta leggendo..."):
                                analisi = genera_analisi_ai(row['title'], nome_fonte, data_notizia)
                                st.markdown("### Analisi dell'Esperto")
                                st.info(analisi)
                                
    except Exception as e:
        st.error(f"Errore critico nella lettura dei dati: {e}")
else:
    st.info(f"Nessun dato locale trovato per **{tema}**.")
    st.write("Usa il tasto nella barra laterale per scaricare le prime notizie.")




# --- 12. REPORT COMPARATIVO (EXTRA) ---
if os.path.exists(percorso_file) and not df.empty:
    st.divider()
    if st.button("📊 Genera Report Comparativo dell'intera sezione"):
        with st.spinner("Analizzando i pattern comuni..."):
            titoli = "\n".join(df['title'].astype(str).tolist()[:10]) # Analizziamo le prime 10
            prompt_comp = f"Confronta queste notizie e individua i 3 temi caldi del momento per il settore {tema}:\n{titoli}"
            try:
                report = model.generate_content(prompt_comp)
                st.subheader("📈 Trend e Pattern Individuati")
                st.success(report.text)
            except Exception as e:
                st.error(f"Errore nel report: {e}")