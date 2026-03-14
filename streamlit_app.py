import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny - Demo", page_icon="🚚")

# 2. CSS dla wyglądu (Tagi i przyciski)
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 20px; }
    .tag { padding: 4px 10px; border-radius: 4px; font-size: 11px; color: white; font-weight: bold; }
    div.stButton > button:first-child { background-color: #f0f2f6; border: 1px solid #d1d5db; }
    .main-btn > div > button { background-color: #007bff !important; color: white !important; }
    </style>
""", unsafe_allow_html=True)

# 3. PANEL BOCZNY (Drzewko)
with st.sidebar:
    st.title("Panel Sterowania")
    
    menu_selection = sac.tree(
        items=[
            sac.TreeItem('Zamówienia', icon='box', children=[
                sac.TreeItem('Powiadomienia', icon='bell', children=[
                    sac.TreeItem('Aktywne'),
                ]),
                sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                    sac.TreeItem('Moje Dostawy'),
                    sac.TreeItem('Wszystkie Dostawy'),
                    sac.TreeItem('Odprawa Celna'),
                    sac.TreeItem('Problemy Dostaw'),
                ]),
                sac.TreeItem('Awizacja', icon='calendar-event', children=[
                    sac.TreeItem('Kalendarz'),
                ]),
            ]),
        ],
        label='NAWIGACJA',
        open_all=True,
        size='sm',
    )

# 4. GÓRNE TAGI (Wizualizacja kategorii)
st.markdown("""
    <div class="tag-container">
        <span class="tag" style="background-color: #333;">#01 MEDIA</span>
        <span class="tag" style="background-color: #8db600;">2020 SUPPLIES</span>
        <span class="tag" style="background-color: #ff5722;">ABEKOM</span>
        <span class="tag" style="background-color: #0288d1;">ABISAL</span>
        <span class="tag" style="background-color: #0097a7;">ACCELENT</span>
    </div>
""", unsafe_allow_html=True)

# 5. SEKCJA WYSZUKIWANIA (FILTRY)
st.subheader("🔍 Wyszukiwanie")
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        dostawca = st.selectbox("Dostawca:", ["Wszyscy", "ASG", "ZIBI", "Barrel Optics", "Wydawnictwo X", "ZIRI"])
        ticket = st.text_input("Ticket:", placeholder="Wpisz numer...")
    
    with col2:
        odpowiedzialny = st.multiselect("Odpowiedzialny:", ["Jan Kowalski", "Anna Nowak", "Piotr Zieliński", "Marek Woźniak"])
        flaga = st.multiselect("Flaga:", ["Priorytet", "Import", "Krajowe", "Reklamacja"])
        
    with col3:
        st.write("**Statusy:**")
        otwarte = st.checkbox("Otwarte", value=True)
        zamkniete = st.checkbox("Zamknięte", value=False)
        
    with col4:
        st.write("**Akcje Szybkie:**")
        st.button("➕ Dodaj Dostawcę", use_container_width=True)
        st.button("🚛 Dodaj Przewoźnika", use_container_width=True)
        st.button("🔁 Zamówienia Cykliczne", use_container_width=True)

# 6. ZARZĄDZANIE TABELĄ
st.write("---")
st.subheader("📊 Zarządzanie Tabelą")

col_manage1, col_manage2 = st.columns([2, 1])

with col_manage1:
    all_columns = ["Lp.", "Dostawca", "Nr dostawy", "Status", "Zakupy", "Data Awizacji", "Odpowiedzialny", "Priorytet"]
    selected_cols = st.multiselect("Wybierz kolumny tabeli:", all_columns, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Zakupy"])
    if st.button("✅ Zastosuj", type="primary"):
        st.toast("Widok tabeli został zaktualizowany!")

with col_manage2:
    st.selectbox("Szablony widoku:", ["Standardowy", "Dla Magazynu", "Finansowy", "Moje ulubione"])
    c_btn1, c_btn2 = st.columns(2)
    c_btn1.button("💾 Zapisz", use_container_width=True)
    c_btn2.button("↕️ Kolejność", use_container_width=True)

# 7. WYŚWIETLANIE TABELI (Z reagowaniem na wybrane kolumny)
# Dane demo
raw_data = [
    {"Lp.": 1, "Dostawca": "ASG", "Nr dostawy": "14/23", "Status": "BR", "Zakupy": "Brak danych", "Data Awizacji": "2024-03-15", "Odpowiedzialny": "Jan Kowalski", "Priorytet": "Wysoki", "color": "#f8d7da"},
    {"Lp.": 2, "Dostawca": "BARREL OPTICS", "Nr dostawy": "1/24", "Status": "Zamówiono", "Zakupy": "Brak danych", "Data Awizacji": "2024-03-20", "Odpowiedzialny": "Anna Nowak", "Priorytet": "Normalny", "color": "#ffffff"},
    {"Lp.": 3, "Dostawca": "ZIBI", "Nr dostawy": "7/24", "Status": "SKŁAD", "Zakupy": "W przygotowaniu", "Data Awizacji": "2024-03-12", "Odpowiedzialny": "Jan Kowalski", "Priorytet": "Niski", "color": "#d4edda"},
    {"Lp.": 4, "Dostawca": "ZIRI", "Nr dostawy": "4/24", "Status": "SKŁAD", "Zakupy": "Gotowy", "Data Awizacji": "2024-03-18", "Odpowiedzialny": "Piotr Zieliński", "Priorytet": "Wysoki", "color": "#d4edda"},
]

df = pd.DataFrame(raw_data)

# Filtrowanie kolumn na podstawie wyboru użytkownika
display_df = df[selected_cols + ["color"]]

def style_row(row):
    return [f'background-color: {row["color"]}' for _ in row]

st.dataframe(
    display_df.style.apply(style_row, axis=1),
    use_container_width=True,
    hide_index=True,
    column_config={"color": None}
)

# 8. KOLEJNOŚĆ KOLUMN (Demo Drag & Drop / Reorder)
with st.expander("🔄 Zmień kolejność kolumn (Widok poglądowy)"):
    st.info("W pełnej wersji możesz przeciągać kolumny poniżej:")
    st.data_editor(pd.DataFrame({"Kolejność": range(1, len(selected_cols)+1), "Kolumna": selected_cols}), 
                   use_container_width=True, hide_index=True)
