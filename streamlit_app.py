import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Zarządzania Dostawami", page_icon="📦")

# 2. CSS dla stylizacji wizualnej (kolory tagów i tabeli)
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 20px; }
    .tag { padding: 4px 10px; border-radius: 4px; font-size: 12px; color: white; font-weight: bold; }
    .stDataFrame { border: 1px solid #e6e9ef; border-radius: 5px; }
    [data-testid="stSidebar"] { background-color: #f0f2f6; }
    </style>
""", unsafe_allow_html=True)

# 3. PASEK BOCZNY - Drzewko menu
with st.sidebar:
    st.title("Panel Sterowania")
    
    # Drzewko menu (zamiast selectboxów)
    menu_selection = sac.tree(
        items=[
            sac.TreeItem('ZAMÓWIENIA', icon='box', children=[
                sac.TreeItem('Powiadomienia', icon='bell', children=[
                    sac.TreeItem('Aktywne'),
                ]),
                sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                    sac.TreeItem('Moje dostawy'),
                    sac.TreeItem('Wszystkie dostawy'),
                    sac.TreeItem('Odprawa celna'),
                    sac.TreeItem('Problemy dostaw'),
                ]),
                sac.TreeItem('Awizacja', icon='calendar-check', children=[
                    sac.TreeItem('Moje dostawy'),
                    sac.TreeItem('Kalendarz'),
                ]),
            ]),    
        ],
        label='NAWIGACJA',
        index=0,
        open_all=True,
        size='sm',
    )

# 4. GÓRNE TAGI
st.markdown("""
    <div class="tag-container">
        <span class="tag" style="background-color: #333;">#01 MEDIA</span>
        <span class="tag" style="background-color: #8db600;">2020 Supplies</span>
        <span class="tag" style="background-color: #8db600;">4Shooter</span>
        <span class="tag" style="background-color: #2e7d32;">5.11</span>
        <span class="tag" style="background-color: #ff5722;">ABEKOM</span>
        <span class="tag" style="background-color: #0288d1;">ABISAL</span>
        <span class="tag" style="background-color: #0097a7;">ABSOLUTUS</span>
        <span class="tag" style="background-color: #2e7d32;">ACCELENT</span>
        <span class="tag" style="background-color: #ff5722;">ACERBI</span>
        <span class="tag" style="background-color: #0288d1;">ACP sPORT</span>
        <span class="tag" style="background-color: #0097a7;">ACTION HOLSTERS</span>        
    </div>
""", unsafe_allow_html=True)

# 5. FILTRY
col_left, col_right = st.columns([1, 2])

with col_right:
    with st.expander("📂 Filtry - Wielowybór", expanded=True):
        f_row1 = st.columns(3)
        f_row1[0].selectbox("Zakładka:", ["Wszystkie", "Magazyn Główny", "Outlet"])
        f_row1[1].multiselect("Grupy:", ["Grupa A", "Grupa B", "Grupa C"])
        f_row1[2].selectbox("Typ PIM:", ["Dowolny", "Zdefiniowany"])
        
        f_row2 = st.columns(3)
        f_row2[0].text_input("Kod obcy:")
        f_row2[1].text_input("Nazwa produktu:")
        f_row2[2].date_input("Data odcięcia:")
        st.button("USTAWIENIA ZAAWANSOWANE", use_container_width=True)

# --- 6. TABELA DANYCH "MOJE DOSTAWY" ---
st.subheader(f"MOJE DOSTAWY - Widok: {menu_selection}")

# 1. Dane
df_data = pd.DataFrame([
    {"Lp.": 1, "Dostawca": "ASG", "Nr dostawy": "14/23", "Status": "BR", "Zakupy": "Brak danych", "Kolor": "#f8d7da"},
    {"Lp.": 2, "Dostawca": "BARREL OPTICS", "Nr dostawy": "1/24-sampl", "Status": "Zamówiono", "Zakupy": "Brak danych", "Kolor": "#ffffff"},
    {"Lp.": 3, "Dostawca": "WYDAWNICTWO X", "Nr dostawy": "7/24", "Status": "SKŁAD", "Zakupy": "W przygotowaniu", "Kolor": "#d4edda"},
    {"Lp.": 4, "Dostawca": "Darek", "Nr dostawy": "1/24", "Status": "Zrealizowane", "Zakupy": "Brak danych", "Kolor": "#ffffff"},
    {"Lp.": 5, "Dostawca": "ZIRI", "Nr dostawy": "4/24", "Status": "SKŁAD", "Zakupy": "Gotowy", "Kolor": "#d4edda"},
])

# 2. BEZPIECZNIEJSZA funkcja stylizująca
def style_row(row):
    # Używamy .get('Kolor') aby uniknąć błędu jeśli kolumna zostanie usunięta
    color = row.get('Kolor', '#ffffff') 
    # Generujemy listę stylów dla wszystkich kolumn w wierszu
    return ['background-color: ' + color] * len(row)

# 3. Nakładamy style na PEŁNY dataframe (nie usuwamy kolumny Kolor wcześniej!)
styled_df = df_data.style.apply(style_row, axis=1)

# 4. Wyświetlamy tabelę, ukrywając kolumnę technologiczną w ustawieniach widoku
st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Kolor": None  # Ta linijka ukrywa kolumnę z widoku użytkownika
    }
)

st.info(f"Podsumowanie: Znaleziono towary dla sekcji {menu_selection}")
```
