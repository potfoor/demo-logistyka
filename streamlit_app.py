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
ZALOGOWANY_UZYTKOWNIK = "Jan Kowalski"

# 3. BAZA DOSTAWCÓW
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

# 4. CSS DLA KARTY I PRZYCISKÓW
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; }
    
    /* Czerwony przycisk zastosuj */
    div[data-testid="column"] button[kind="primary"] {
        background-color: #ff4b4b !important;
        border: none !important;
        color: white !important;
    }

    /* Stylizacja Popovera - Karta */
    div[data-testid="stPopover"] > button {
        margin-top: 28px;
        height: 38px;
        width: 100%;
        border: 1px solid #d1d5db;
    }
    
    /* Mniejsza czcionka tabeli */
    [data-testid="stDataFrame"] { font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY
with st.sidebar:
    st.title("🚚 Logistyka App")
    st.write(f"Zalogowany: **{ZALOGOWANY_UZYTKOWNIK}**")
    st.divider()
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

# --- LOGIKA SESJI ---
if 'o_sel' not in st.session_state: st.session_state.o_sel = []
if 'd_sel' not in st.session_state: st.session_state.d_sel = "Wszyscy"

if menu_selected == 'Moje Dostawy':
    st.session_state.o_sel = [ZALOGOWANY_UZYTKOWNIK]
elif menu_selected == 'Wszystkie Dostawy':
    st.session_state.o_sel = []

dostawcy_filtered = dostawcy_base
if st.session_state.o_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in st.session_state.o_sel]
if st.session_state.d_sel != "Wszyscy":
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == st.session_state.d_sel]

# --- 7. AKTYWNI DOSTAWCY ---
st.write(f"**Aktywni Dostawcy:**")
tags_html = '<div class="tag-container">'
for d in dostawcy_filtered:
    kolor = osoby_kolory.get(d["opiekun"], "#cccccc")
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# --- 6. SEKCJA WYSZUKIWANIE I KARTA ---
st.header("🔍 Wyszukiwanie")
with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 3])
    with c1:
        st.session_state.d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base])
    
    with c2:
        # ROZBUDOWANY POP-UP KARTY
        with st.popover("📇 KARTA"):
            if st.session_state.d_sel != "Wszyscy":
                st.subheader(f"Karta: {st.session_state.d_sel}")
                st.divider()
                
                # Dane dostępowe
                st.write("**🔐 Dane Logowania**")
                st.text_input("URL Serwisu:", f"https://b2b.{st.session_state.d_sel.lower().replace(' ', '')}.com")
                col_k1, col_k2 = st.columns(2)
                col_k1.text_input("Login:", "admin_logistics")
                col_k2.text_input("Hasło:", "*******")
                
                # Kontakt
                st.divider()
                st.write("**👤 Kontakt i Typ**")
                st.text_input("Osoba kontaktowa:", "Jan Nowak")
                st.text_input("Email Price List:", "ceny@dostawca.pl")
                
                # Opcje serwisu
                st.multiselect("Dostępne systemy:", ["B2B", "Zam. Email", "EDI", "API"], default=["B2B", "Zam. Email"])
                
                if st.button("💾 Zapisz zmiany w karcie"):
                    st.success("Zapisano!")
            else:
                st.warning("Najpierw wybierz dostawcę")

    with c3:
        st.session_state.o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=st.session_state.o_sel)

    # Dalsza część formularza
    c4, c5, c6, c7 = st.columns([3, 3, 2, 2])
    with c4: st.text_input("Ticket:", placeholder="Nr ticketu...")
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

# --- 8. TABELA ---
st.write("---")
st.subheader(f"📊 Tabela: {menu_selected}")

wszystkie_kolumny = [
    "Lp.", "Dostawca", "Nr dostawy", "HWO", "Data aw. OD", "Data aw. DO", 
    "Priorytet", "Status", "Zakupy", "Kurier", "List", 
    "Brak AW", "Brak FV", "Cen", "New", "Waga", "Knt", "Pal", "Box", "Opiekun", "Aktualizacja"
]

selected_cols = st.multiselect("Pokaż kolumny:", wszystkie_kolumny, 
                              default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Zakupy", "Waga", "Opiekun", "Aktualizacja"])

raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1, "Dostawca": d["firma"], "Nr dostawy": f"{14+i}/26 🔗",
        "HWO": "12-03-2026", "Data aw. OD": "12-03-2026", "Data aw. DO": "",
        "Priorytet": "Normalny", "Status": "SKŁAD" if i % 3 == 0 else "Zamówione",
        "Zakupy": "OK", "Kurier": "Virtus Logistics", "List": "/", "Brak AW": "/", 
        "Brak FV": "Nie", "Cen": "Nie", "New": "Nie", "Waga": "150kg", "Knt": "/", 
        "Pal": "1", "Box": "2", "Opiekun": d["opiekun"], "Aktualizacja": "12-03-2026 13:42:56"
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
        }
    )
