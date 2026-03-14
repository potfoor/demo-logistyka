import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny - Demo", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW (Słownik pomocniczy)
osoby_kolory = {
    "Jan Kowalski": "#333333",      # Ciemny szary
    "Anna Nowak": "#8db600",        # Oliwkowy
    "Piotr Zieliński": "#ff5722",    # Pomarańczowy
    "Marek Woźniak": "#0288d1"       # Niebieski
}

# 3. LISTA DOSTAWCÓW Z PRZYPISANIEM
dostawcy_data = [
    {"firma": "Logistics Hub Sp. z o.o.", "opiekun": "Jan Kowalski"},
    {"firma": "Trans-Port Solutions", "opiekun": "Anna Nowak"},
    {"firma": "Global Cargo Express", "opiekun": "Piotr Zieliński"},
    {"firma": "Euro-Spedycja S.A.", "opiekun": "Marek Woźniak"},
    {"firma": "Baltic Freight Systems", "opiekun": "Jan Kowalski"},
    {"firma": "Rapid Delivery Service", "opiekun": "Anna Nowak"},
    {"firma": "Pol-Express Logistics", "opiekun": "Piotr Zieliński"},
    {"firma": "Customs Clearance Pro", "opiekun": "Marek Woźniak"},
    {"firma": "Trade & Ship Co.", "opiekun": "Jan Kowalski"},
    {"firma": "Fast Track Forwarding", "opiekun": "Anna Nowak"},
    {"firma": "Mega-Trans International", "opiekun": "Piotr Zieliński"},
    {"firma": "Eco-Logistyka", "opiekun": "Marek Woźniak"},
    {"firma": "Sky Cargo Group", "opiekun": "Jan Kowalski"},
    {"firma": "Smart Warehouse Sp. z o.o.", "opiekun": "Anna Nowak"},
    {"firma": "Ocean-Way Shipping", "opiekun": "Piotr Zieliński"},
    {"firma": "Direct Trucking Poland", "opiekun": "Marek Woźniak"},
    {"firma": "Prime Supply Chain", "opiekun": "Jan Kowalski"},
    {"firma": "Nord-Express Logistyka", "opiekun": "Anna Nowak"},
    {"firma": "Inter-Global Transit", "opiekun": "Piotr Zieliński"},
    {"firma": "Best Way Spedycja", "opiekun": "Marek Woźniak"},
    {"firma": "Cargo Master Group", "opiekun": "Jan Kowalski"},
    {"firma": "Elite Freight Services", "opiekun": "Anna Nowak"},
    {"firma": "Road-Runner Transport", "opiekun": "Piotr Zieliński"},
    {"firma": "Blue Water Logistics", "opiekun": "Marek Woźniak"},
    {"firma": "National Cargo Network", "opiekun": "Jan Kowalski"},
    {"firma": "Flexi-Trans S.A.", "opiekun": "Anna Nowak"},
    {"firma": "Iron-Way Rail Freight", "opiekun": "Piotr Zieliński"},
    {"firma": "Advanced Logistics Lab", "opiekun": "Marek Woźniak"},
    {"firma": "Horizon Forwarding", "opiekun": "Jan Kowalski"},
    {"firma": "Master-Supply Solutions", "opiekun": "Anna Nowak"}
]

# 4. CSS DLA TAGÓW
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 20px; }
    .tag { padding: 4px 10px; border-radius: 4px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY (Drzewko)
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
        ],
        label='NAWIGACJA', open_all=True, size='sm'
    )

# 6. GENEROWANIE GÓRNYCH TAGÓW (Z kolorami opiekunów)
tags_html = '<div class="tag-container">'
for d in dostawcy_data:
    kolor = osoby_kolory[d["opiekun"]]
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# 7. SEKCJA WYSZUKIWANIA
st.subheader("🔍 Wyszukiwanie")
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lista_nazw = [d["firma"] for d in dostawcy_data]
        dostawca_sel = st.selectbox("Dostawca:", ["Wszyscy"] + lista_nazw)
        ticket = st.text_input("Ticket:", placeholder="Wpisz numer...")
    with col2:
        odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))
        flaga = st.multiselect("Flaga:", ["Import", "Krajowe", "Pilne"])
    with col3:
        st.write("**Statusy:**")
        st.checkbox("Otwarte", value=True)
        st.checkbox("Zamknięte")
    with col4:
        st.write("**Akcje Szybkie:**")
        st.button("➕ Dodaj Dostawcę", use_container_width=True)
        st.button("🚛 Dodaj Przewoźnika", use_container_width=True)

# 8. ZARZĄDZANIE TABELĄ
st.write("---")
all_columns = ["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny", "Zakupy"]
selected_cols = st.multiselect("Wybierz kolumny tabeli:", all_columns, default=all_columns)

# 9. DANE DO TABELI (Generowane na podstawie listy dostawców)
raw_table_data = []
for i, d in enumerate(dostawcy_data[:10]): # Pokazujemy pierwsze 10 dla przejrzystości demo
    raw_table_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{i+100}/2024",
        "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"],
        "Zakupy": "Gotowy",
        "color": osoby_kolory[d["opiekun"]] # Kolor wiersza taki sam jak tagu
    })

df = pd.DataFrame(raw_table_data)

# Stylizacja wierszy
def style_row(row):
    return [f'background-color: {row["color"]}; color: white;' if row["color"] != "#ffffff" else '' for _ in row]

st.dataframe(
    df[selected_cols + ["color"]].style.apply(style_row, axis=1),
    use_container_width=True,
    hide_index=True,
    column_config={"color": None}
)

st.info(f"💡 Kolory tagów i wierszy odpowiadają przypisanym osobom: " + 
        ", ".join([f"{k} ({v})" for k, v in osoby_kolory.items()]))
