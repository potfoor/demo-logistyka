import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny - Demo", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW
osoby_kolory = {
    "Jan Kowalski": "#333333",
    "Anna Nowak": "#8db600",
    "Piotr Zieliński": "#ff5722",
    "Marek Woźniak": "#0288d1"
}

# 3. BAZA DOSTAWCÓW (Firmy z Twojej listy)
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

# 4. CSS DLA IDEALNEGO UKŁADU
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding: 10px 0; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 9px; color: white; font-weight: bold; text-transform: uppercase; }
    
    /* Stylizacja przycisków w sekcji Akcje Szybkie */
    .stButton > button { 
        width: 100%; 
        border-radius: 5px; 
        height: 38px;
        background-color: #f8f9fa;
        border: 1px solid #dee2e6;
        color: #212529;
    }
    .stButton > button:hover { border-color: #ff4b4b; color: #ff4b4b; }
    
    /* Przycisk Zastosuj Filtry */
    div[data-testid="column"]:nth-of-type(4) .stButton > button {
        background-color: #ff4b4b;
        color: white;
        border: none;
        font-weight: bold;
    }
    
    /* Popover Karta */
    div[data-testid="stPopover"] > button { 
        margin-top: 28px; 
        border: 1px solid #d1d5db; 
        height: 38px; 
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY
with st.sidebar:
    st.title("Panel Sterowania")
    sac.tree(
        items=[
            sac.TreeItem('Zamówienia', icon='box', children=[
                sac.TreeItem('Powiadomienia', icon='bell'),
                sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                    sac.TreeItem('Moje Dostawy'), sac.TreeItem('Wszystkie Dostawy')
                ]),
                sac.TreeItem('Awizacja', icon='calendar-event'),
            ]),
        ], label='NAWIGACJA', open_all=True, size='sm'
    )

# 6. SEKCJA WYSZUKIWANIE (Zgodnie z wymaganiami)
st.header("🔍 Wyszukiwanie")

with st.container(border=True):
    # Rząd 1: Filtry główne
    col1, col2, col3 = st.columns([3, 1, 3])
    with col1:
        dostawca_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base])
    with col2:
        with st.popover("📇 Karta"):
            if dostawca_sel != "Wszyscy":
                st.write(f"**{dostawca_sel}**")
                st.text_input("Kontakt:", "Jan Nowak")
                st.button("Zapisz dane")
            else: st.info("Wybierz firmę")
    with col3:
        odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))

    # Rząd 2: Ticket, Flaga i Akcje
    col4, col5, col6, col7 = st.columns([3, 3, 2, 2])
    with col4:
        ticket_input = st.text_input("Ticket:", placeholder="Wpisz numer...")
    with col5:
        flaga_sel = st.multiselect("Flaga:", ["PILNE", "POWTÓRKA", "REKLAMACJA", "OPÓŹNIONE"])
    with col6:
        st.write("**Statusy:**")
        otwarte = st.checkbox("Otwarte", value=True)
        zamkniete = st.checkbox("Zamknięte")
    with col7:
        st.write("**Akcje:**")
        st.button("🚀 ZASTOSUJ FILTRY")

    st.write("---")
    
    # Rząd 3: Akcje Szybkie (Przyciski, o które prosiłeś)
    st.write("**Akcje Szybkie:**")
    btn_col1, btn_col2, btn_col3 = st.columns(3)
    with btn_col1:
        st.button("➕ Dodaj Dostawcę")
    with btn_col2:
        st.button("🚛 Dodaj Przewoźnika")
    with btn_col3:
        st.button("🔄 Zamówienia Cykliczne")

# --- LOGIKA FILTROWANIA ---
dostawcy_filtered = dostawcy_base
if odp_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in odp_sel]
if dostawca_sel != "Wszyscy":
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == dostawca_sel]

# 7. TAGI DOSTAWCÓW
st.write(f"**Aktywni Dostawcy (Kolor wg Opiekuna):**")
tags_html = '<div class="tag-container">'
for d in dostawcy_filtered:
    kolor = osoby_kolory[d["opiekun"]]
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# 8. ZARZĄDZANIE TABELĄ
st.write("---")
st.subheader("📊 Zarządzanie Tabelą")
z1, z2 = st.columns([3, 1])
with z1:
    all_columns = ["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny", "Zakupy"]
    selected_cols = st.multiselect("Wybierz kolumny tabeli:", all_columns, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny"])
with z2:
    st.selectbox("Szablony widoku:", ["Standardowy", "Magazyn", "Finanse"])
    st.button("💾 Zapisz Szablon")

# 9. TABELA (Sztywne odstępy jak na wzorze)
raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1, 
        "Dostawca": d["firma"], 
        "Nr dostawy": f"{102 + i}/2024",
        "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"], 
        "Zakupy": "OK"
    })

if raw_data:
    df = pd.DataFrame(raw_data)
    st.dataframe(
        df[selected_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Lp.": st.column_config.Column(width=45),
            "Dostawca": st.column_config.Column(width="large"),
            "Nr dostawy": st.column_config.Column(width="medium"),
            "Status": st.column_config.Column(width="small"),
            "Odpowiedzialny": st.column_config.Column(width="medium"),
            "Zakupy": st.column_config.Column(width="small"),
        }
    )
