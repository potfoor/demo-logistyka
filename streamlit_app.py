import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny Pro", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW
osoby_kolory = {
    "Maciej Podwórny": "#333333",
    "Jan Kowalski": "#8db600",
    "Anna Nowak": "#ff5722",
    "Piotr Zieliński": "#0288d1",
    "Marek Woźniak": "#722ed1"
}

# 3. BAZA DOSTAWCÓW (Zgodnie z Twoimi nazwami)
lista_firm = [
    "ASG", "BARRIDE OPTICS", "WYDAWNICTWO Y", "Protek", "ZIBI", "ABEKOM", 
    "ABISAL", "ACCELENT", "Samsung Electronics", "Toyota Motor Poland"
]
opiekunowie = list(osoby_kolory.keys())
dostawcy_base = [
    {"firma": nazwa, "opiekun": "Maciej Podwórny" if i < 4 else opiekunowie[i % len(opiekunowie)]}
    for i, nazwa in enumerate(lista_firm)
]

# 4. CSS DLA IDEALNEGO DOPASOWANIA
st.markdown("""
    <style>
    /* Kontener tagów na samej górze */
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    
    /* Przyciski Akcji */
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; font-weight: 500; }
    
    /* Przycisk Zastosuj Filtry - Czerwony */
    div[data-testid="column"] button[kind="primary"] {
        background-color: #ff4b4b !important;
        border: none !important;
    }

    /* Stylizacja tabeli - mniejsza czcionka dla wielu kolumn */
    [data-testid="stDataFrame"] { font-size: 12px; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY
with st.sidebar:
    st.title("Panel Sterowania")
    sac.tree(items=[sac.TreeItem('Zamówienia', icon='box', children=[sac.TreeItem('Wszystkie Dostawy')])], open_all=True)

# --- LOGIKA FILTROWANIA (Musi być przed wyświetlaniem tagów) ---
# Inicjalizacja stanów dla filtrów, aby tagi na górze reagowały natychmiast
if 'odp_sel' not in st.session_state: st.session_state.odp_sel = []
if 'dostawca_sel' not in st.session_state: st.session_state.dostawca_sel = "Wszyscy"

dostawcy_filtered = dostawcy_base
if st.session_state.odp_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in st.session_state.odp_sel]
if st.session_state.dostawca_sel != "Wszyscy":
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == st.session_state.dostawca_sel]

# --- 7. AKTYWNI DOSTAWCY (TERAZ NA SAMEJ GÓRZE) ---
st.write(f"**Aktywni Dostawcy (Kolor wg Opiekuna):**")
tags_html = '<div class="tag-container">'
for d in dostawcy_filtered:
    kolor = osoby_kolory.get(d["opiekun"], "#cccccc")
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# 6. SEKCJA WYSZUKIWANIE
st.header("🔍 Wyszukiwanie")
with st.container(border=True):
    # Rząd 1
    col1, col2, col3 = st.columns([3, 1, 3])
    with col1:
        st.session_state.dostawca_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base])
    with col2:
        with st.popover("📇 Karta"):
            st.info("Dane kontaktowe dostawcy")
    with col3:
        st.session_state.odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))

    # Rząd 2
    c4, c5, c6, c7 = st.columns([3, 3, 2, 2])
    with c4:
        st.text_input("Ticket:", placeholder="Wpisz numer...")
    with c5:
        st.multiselect("Flaga:", ["PILNE", "POWTÓRKA", "OPÓŹNIONE"])
    with c6:
        st.write("**Statusy:**")
        st.checkbox("Otwarte", value=True)
        st.checkbox("Zamknięte")
    with c7:
        st.write("**Akcje:**")
        st.button("🚀 ZASTOSUJ FILTRY", type="primary")

    st.write("---")
    # Rząd 3: Akcje Szybkie
    st.write("**Akcje Szybkie:**")
    b1, b2, b3 = st.columns(3)
    b1.button("➕ Dodaj Dostawcę")
    b2.button("🚛 Dodaj Przewoźnika")
    b3.button("🔄 Zamówienia Cykliczne")

# 8. ZARZĄDZANIE TABELĄ
st.write("---")
st.subheader("📊 Zarządzanie Tabelą")
z1, z2 = st.columns([3, 1])

wszystkie_kolumny = [
    "Lp.", "Dostawca", "Nr dostawy", "HWO", "Data aw. OD", "Data aw. DO", 
    "Priorytet", "Status", "Zakupy", "Kurier", "List", 
    "Brak AW", "Brak FV", "Cen", "New", "Waga", "Knt", "Pal", "Box", "Opiekun", "Aktualizacja"
]

with z1:
    selected_cols = st.multiselect("Wybierz kolumny:", wszystkie_kolumny, 
                                  default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Zakupy", "Waga", "Opiekun"])
with z2:
    st.selectbox("Szablony widoku:", ["Standardowy", "Logistyka"])
    st.button("💾 Zapisz Szablon")

# 9. TABELA Z PEŁNYMI DANYMI (Zgodnie z Twoim ostatnim screenshotem)
raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{14+i}/26",
        "HWO": "12-03-2026",
        "Data aw. OD": "12-03-2026",
        "Data aw. DO": "",
        "Priorytet": "Normalny",
        "Status": "SKŁAD" if i % 2 == 0 else "Zamówione",
        "Zakupy": "W przygotowaniu" if i % 3 == 0 else "Brak danych",
        "Kurier": "Virtus Logistics",
        "List": "/",
        "Brak AW": "/",
        "Brak FV": "Nie",
        "Cen": "Nie",
        "New": "Nie",
        "Waga": f"{100 + i*10}kg",
        "Knt": "/",
        "Pal": "1",
        "Box": "2",
        "Opiekun": d["opiekun"],
        "Aktualizacja": "12-03-2026 13:42:56"
    })

if raw_data:
    df = pd.DataFrame(raw_data)
    st.dataframe(
        df[selected_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Lp.": st.column_config.Column(width=40),
            "Dostawca": st.column_config.Column(width=180),
            "Nr dostawy": st.column_config.Column(width=100),
            "Status": st.column_config.Column(width=100),
            "Waga": st.column_config.Column(width=70),
            "Pal": st.column_config.Column(width=45),
            "Box": st.column_config.Column(width=45),
            "Aktualizacja": st.column_config.Column(width=160),
        }
    )
