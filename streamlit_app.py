import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny Pro", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW
osoby_kolory = {
    "Jan Kowalski": "#333333",
    "Anna Nowak": "#8db600",
    "Piotr Zieliński": "#ff5722",
    "Marek Woźniak": "#0288d1"
}

# Symulacja zalogowanego użytkownika
ZALOGOWANY_UZYTKOWNIK = "Jan Kowalski"

# 3. BAZA DOSTAWCÓW (Twoja lista 30 firm)
lista_firm = [
    "Samsung Electronics", "Toyota Motor Poland", "Coca-Cola HBC", "Microsoft",
    "Nestlé Polska", "Apple Poland", "Grupa Azoty", "Volkswagen Group",
    "Procter & Gamble", "Siemens", "Philips Lighting", "Robert Bosch",
    "L'Oréal Polska", "PepsiCo", "Unilever", "ABB Sp. z o.o.", "Danone",
    "IKEA Retail", "Bridgestone", "Dell Technologies", "BASF Polska",
    "Michelin", "Saint-Gobain", "Continental", "Sony Interactive",
    "Huawei Polska", "Goodyear", "Henkel Polska", "LG Electronics", "Castorama Polska"
]

opiekunowie = list(osoby_kolory.keys())
dostawcy_base = [
    {"firma": nazwa, "opiekun": opiekunowie[i % len(opiekunowie)]}
    for i, nazwa in enumerate(lista_firm)
]

# 4. CSS
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; }
    div[data-testid="column"] button[kind="primary"] { background-color: #ff4b4b !important; border: none !important; color: white !important; }
    [data-testid="stDataFrame"] { font-size: 11px; }
    div[data-testid="stPopover"] > button { margin-top: 28px; height: 38px; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY I LOGIKA NAWIGACJI
with st.sidebar:
    st.title("🚚 Logistyka App")
    st.write(f"Zalogowany: **{ZALOGOWANY_UZYTKOWNIK}**")
    st.divider()
    
    # Menu boczne
    menu_selected = sac.tree(
        items=[
            sac.TreeItem('Dashboard', icon='speedometer2'),
            sac.TreeItem('Zamówienia', icon='box', children=[
                sac.TreeItem('Powiadomienia', icon='bell'),
                sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                    sac.TreeItem('Moje Dostawy', icon='person-check'),
                    sac.TreeItem('Wszystkie Dostawy', icon='globe'),
                ]),
                sac.TreeItem('Awizacja', icon='calendar-event'),
            ]),
        ], label='NAWIGACJA', open_all=True, size='sm'
    )

# --- LOGIKA FILTROWANIA NA PODSTAWIE PANELU BOCZNEGO ---
# Jeśli wybrano "Moje Dostawy", wymuś filtr na zalogowanego użytkownika
if menu_selected == 'Moje Dostawy':
    st.session_state.o_sel = [ZALOGOWANY_UZYTKOWNIK]
    st.session_state.d_sel = "Wszyscy"
elif menu_selected == 'Wszystkie Dostawy':
    st.session_state.o_sel = [] # Reset filtrów
    st.session_state.d_sel = "Wszyscy"

# Inicjalizacja stanów dla selectboxów, jeśli nie istnieją
if 'o_sel' not in st.session_state: st.session_state.o_sel = []
if 'd_sel' not in st.session_state: st.session_state.d_sel = "Wszyscy"

# Zastosowanie filtrów do danych
dostawcy_filtered = dostawcy_base
if st.session_state.o_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in st.session_state.o_sel]
if st.session_state.d_sel != "Wszyscy":
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == st.session_state.d_sel]

# --- 6. AKTYWNI DOSTAWCY (GÓRA) ---
st.write(f"**Aktywni Dostawcy ({'MOJE' if menu_selected == 'Moje Dostawy' else 'WSZYSTKIE'}):**")
tags_html = '<div class="tag-container">'
for d in dostawcy_filtered:
    kolor = osoby_kolory.get(d["opiekun"], "#cccccc")
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# --- 7. SEKCJA WYSZUKIWANIE ---
st.header("🔍 Wyszukiwanie")
with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 3])
    with c1:
        # Selectbox reaguje na st.session_state zmieniany przez menu boczne
        st.session_state.d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base], 
                                              index=0 if st.session_state.d_sel == "Wszyscy" else [d["firma"] for d in dostawcy_base].index(st.session_state.d_sel)+1)
    with c2:
        with st.popover("📇 Karta"): st.write("Dane kontaktowe")
    with c3:
        # Multiselect reaguje na kliknięcie w "Moje Dostawy"
        st.session_state.o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=st.session_state.o_sel)

    c4, c5, c6, c7 = st.columns([3, 3, 2, 2])
    with c4: st.text_input("Ticket:", placeholder="Wpisz numer...")
    with c5: st.multiselect("Flaga:", ["PILNE", "POWTÓRKA"])
    with c6:
        st.write("**Statusy:**")
        st.checkbox("Otwarte", value=True)
        st.checkbox("Zamknięte")
    with c7:
        st.write("**Akcje:**")
        st.button("🚀 ZASTOSUJ FILTRY", type="primary")

    st.write("---")
    st.write("**Akcje Szybkie:**")
    b1, b2, b3 = st.columns(3)
    b1.button("➕ Dodaj Dostawcę")
    b2.button("🚛 Dodaj Przewoźnika")
    b3.button("🔄 Zamówienia Cykliczne")

# --- 8. ZARZĄDZANIE TABELĄ I TABELA ---
st.write("---")
st.subheader(f"📊 Tabela Dostaw: {menu_selected if menu_selected else 'Dashboard'}")

wszystkie_kolumny = ["Lp.", "Dostawca", "Nr dostawy", "HWO", "Data aw. OD", "Status", "Zakupy", "Waga", "Opiekun", "Aktualizacja"]
selected_cols = st.multiselect("Pokaż kolumny:", wszystkie_kolumny, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Opiekun"])

raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{100+i}/26",
        "HWO": "12-03-2026",
        "Data aw. OD": "12-03-2026",
        "Status": "SKŁAD" if i % 2 == 0 else "Zamówione",
        "Zakupy": "OK",
        "Waga": "200kg",
        "Opiekun": d["opiekun"],
        "Aktualizacja": "2026-03-14"
    })

if raw_data:
    df = pd.DataFrame(raw_data)
    st.dataframe(df[selected_cols], use_container_width=True, hide_index=True)
else:
    st.warning("Brak dostaw przypisanych do Twojego konta.")

# 9. GENEROWANIE DANYCH (Pełne 21 kolumn jak na wzorze)
raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{14+i}/26 🔗",
        "HWO": "12-03-2026",
        "Data aw. OD": "12-03-2026",
        "Data aw. DO": "",
        "Priorytet": "Normalny",
        "Status": "SKŁAD" if i == 2 else "Zamówione",
        "Zakupy": "W przygotowaniu" if i == 2 else "Brak danych",
        "Kurier": "Virtus Logistics",
        "List": "/",
        "Brak AW": "/",
        "Brak FV": "Nie",
        "Cen": "Nie",
        "New": "Tak" if i == 2 else "Nie",
        "Waga": "150kg",
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
            "Dostawca": st.column_config.Column(width=200),
            "Nr dostawy": st.column_config.Column(width=130),
            "Status": st.column_config.Column(width=100),
            "Waga": st.column_config.Column(width=70),
            "Pal": st.column_config.Column(width=45),
            "Box": st.column_config.Column(width=45),
            "Aktualizacja": st.column_config.Column(width=160),
        }
    )
