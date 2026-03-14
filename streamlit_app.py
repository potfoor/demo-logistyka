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

# 3. NOWA LISTA FIRM
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
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding: 10px 0; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 9px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; }
    div[data-testid="stPopover"] > button { margin-top: 28px; border: 1px solid #d1d5db; height: 38px; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY
with st.sidebar:
    st.title("Panel Sterowania")
    menu_selection = sac.tree(
        items=[
            sac.TreeItem('Zamówienia', icon='box', children=[
                sac.TreeItem('Powiadomienia', icon='bell', children=[sac.TreeItem('Aktywne')]),
                sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                    sac.TreeItem('Moje Dostawy'), sac.TreeItem('Wszystkie Dostawy'),
                    sac.TreeItem('Odprawa Celna'), sac.TreeItem('Problemy Dostaw')
                ]),
                sac.TreeItem('Awizacja', icon='calendar-event', children=[sac.TreeItem('Kalendarz')]),
            ]),
        ], label='NAWIGACJA', open_all=True, size='sm'
    )

# 6. WYSZUKIWANIE
st.header("🔍 Wyszukiwanie")
with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 3])
    with c1:
        dostawca_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base])
    with c2:
        with st.popover("📇 Karta"):
            if dostawca_sel != "Wszyscy":
                st.write(f"**Karta: {dostawca_sel}**")
                st.text_input("Kontakt:", "Jan Nowak")
                st.text_input("B2B URL:", f"https://b2b.{dostawca_sel.lower().replace(' ', '')}.pl")
                st.button("💾 Zapisz")
            else: st.info("Wybierz firmę")
    with c3:
        odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))

    c4, c5, c6 = st.columns([3, 2, 2])
    with c4:
        st.text_input("Ticket:", placeholder="Nr ticketu...")
    with c5:
        st.write("**Statusy:**")
        st_col1, st_col2 = st.columns(2)
        st_col1.checkbox("Otwarte", value=True)
        st_col2.checkbox("Zamknięte")
    with c6:
        st.write("**Akcje:**")
        st.button("🚀 ZASTOSUJ FILTRY", type="primary")

# LOGIKA FILTRÓW
dostawcy_filtered = dostawcy_base
if odp_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in odp_sel]
if dostawca_sel != "Wszyscy":
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == dostawca_sel]

# 7. TAGI
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
    all_columns = ["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny", "Zakupy", "Data Awizacji"]
    selected_cols = st.multiselect("Kolumny:", all_columns, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny"])
with z2:
    st.selectbox("Szablony:", ["Standard", "Logistyka"])

# 9. TABELA Z SZTYWNYMI ODSTĘPAMI
raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1, 
        "Dostawca": d["firma"], 
        "Nr dostawy": f"{i+100}/24",
        "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"], 
        "Zakupy": "OK", 
        "Data Awizacji": "2024-03-20"
    })

if raw_data:
    df = pd.DataFrame(raw_data)
    
    # KONFIGURACJA SZTYWNYCH SZEROKOŚCI
    st.dataframe(
        df[selected_cols],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Lp.": st.column_config.Column(width="small", help="Numer porządkowy"),
            "Dostawca": st.column_config.Column(width="large"),
            "Nr dostawy": st.column_config.Column(width="medium"),
            "Status": st.column_config.Column(width="small"),
            "Odpowiedzialny": st.column_config.Column(width="medium"),
            "Zakupy": st.column_config.Column(width="small"),
            "Data Awizacji": st.column_config.Column(width="medium"),
        }
    )
