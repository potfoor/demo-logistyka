import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny - Demo", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW
osoby_kolory = {
    "Jan Kowalski": "#333333",      # Ciemny szary
    "Anna Nowak": "#8db600",        # Oliwkowy
    "Piotr Zieliński": "#ff5722",    # Pomarańczowy
    "Marek Woźniak": "#0288d1"       # Niebieski
}

# 3. LISTA DOSTAWCÓW (Twoja pełna lista)
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

# 4. CSS DLA STYLIZACJI
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 20px; }
    .tag { padding: 4px 10px; border-radius: 4px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { border-radius: 5px; }
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

# 6. GENEROWANIE GÓRNYCH TAGÓW (Kolory opiekunów)
tags_html = '<div class="tag-container">'
for d in dostawcy_data:
    kolor = osoby_kolory[d["opiekun"]]
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# 7. SEKCJA WYSZUKIWANIA (FILTRY)
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
        st.button("🔁 Zamówienia Cykliczne", use_container_width=True)

# 8. PRZYWRÓCONA SEKCJA: ZARZĄDZANIE TABELĄ
st.write("---")
st.subheader("📊 Zarządzanie Tabelą")

col_manage1, col_manage2 = st.columns([2, 1])

with col_manage1:
    all_columns = ["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny", "Zakupy", "Data Awizacji", "Priorytet"]
    # Mechanizm wyboru kolumn
    selected_cols = st.multiselect("Wybierz kolumny tabeli:", all_columns, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny"])
    if st.button("✅ Zastosuj", type="primary"):
        st.toast("Widok tabeli został zaktualizowany!")

with col_manage2:
    # Szablony i przyciski akcji
    st.selectbox("Szablony widoku:", ["Standardowy", "Dla Magazynu", "Finansowy", "Moje ulubione"])
    c_btn1, c_btn2 = st.columns(2)
    c_btn1.button("💾 Zapisz", use_container_width=True)
    c_btn2.button("↕️ Kolejność", use_container_width=True)

# 9. TABELA DANYCH
st.write("---")
raw_table_data = []
for i, d in enumerate(dostawcy_data):
    raw_table_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{i+100}/2024",
        "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"],
        "Zakupy": "Gotowy",
        "Data Awizacji": "2024-03-20",
        "Priorytet": "Normalny",
        "color_hex": osoby_kolory[d["opiekun"]] 
    })

df = pd.DataFrame(raw_table_data)

# Funkcja stylizująca wiersze na podstawie koloru opiekuna
def style_row(row):
    color = row["color_hex"]
    return [f'background-color: {color}; color: white;' for _ in row]

# Wyświetlanie z zachowaniem dynamicznych kolumn
st.dataframe(
    df[selected_cols + ["color_hex"]].style.apply(style_row, axis=1),
    use_container_width=True,
    hide_index=True,
    column_config={"color_hex": None} # Ukrycie kolumny technicznej
)

st.info(f"Podsumowanie: Widok zawiera towary przypisane do sekcji {menu_selection}")
