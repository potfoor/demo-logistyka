import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Zarządzania Dostawami")

# --- STYLE CSS (dla kolorowych przycisków i estetyki) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 5px; }
    .tag-container { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 20px; }
    .tag { padding: 4px 10px; border-radius: 4px; font-size: 12px; color: white; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- PASEK BOCZNY (Sidebar) ---
with st.sidebar:
    st.title("Panel Sterowania")
    
    # Główne drzewko "Zamówienia"
    with st.expander("📦 ZAMÓWIENIA", expanded=True):
        # Podkategorie jako rozwijane listy (tree-style)
        st.expander("🔔 Powiadomienia", ["Wszystkie", "Aktywne", "Archiwum"], key="sb_pow")
        st.expander("🎫 Ticket", ["Dodaj produkt", "Zestawy"], key="sb_tick")
        st.expander("📅 Awizacja", ["Ceny produktów", "Rodzaje cen"], key="sb_awiz")
    
    
# --- GÓRNE TAGI (Zakładki/Kategorie) ---
st.markdown("""
    <div class="tag-container">
        <span class="tag" style="background-color: #555;">#01 MEDIA</span>
        <span class="tag" style="background-color: #8db600;">#4F AW'23</span>
        <span class="tag" style="background-color: #8db600;">#4F AW'24</span>
        <span class="tag" style="background-color: #2e7d32;">#4F GR.F</span>
        <span class="tag" style="background-color: #ff5722;">#4SHOOTER</span>
        <span class="tag" style="background-color: #0288d1;">#A ZESTAWY</span>
    </div>
""", unsafe_allow_html=True)

# --- SEKCE FILTRÓW (Expander) ---
col_f1, col_f2 = st.columns([1, 2])

with col_f1:
    with st.expander("🔍 Filtry - Unikalne", expanded=True):
        st.text_input("SKU:")
        st.text_input("Kod:")
        st.checkbox("Pokaż warianty", value=True)
        c1, c2, c3 = st.columns(3)
        c1.button("Filtruj", type="primary")
        c2.button("Zakładkę")
        c3.button("Resetuj")

with col_f2:
    with st.expander("📂 Filtry - Wielowybór", expanded=True):
        f_c1, f_c2, f_c3 = st.columns(3)
        f_c1.selectbox("Zakładka:", ["Wybierz...", "Magazyn A", "Magazyn B"])
        f_c2.multiselect("Grupy:", ["Grupa 1", "Grupa 2"])
        f_c3.selectbox("Typ PIM:", ["Dowolny", "Zdefiniowany"])
        
        f_c4, f_c5, f_c6 = st.columns(3)
        f_c4.text_input("Nazwa:")
        f_c5.date_input("Odcięcie od:")
        f_c6.date_input("do:")
        st.button("FILTRUJ ZAAWANSOWANE")

# --- WYBÓR KOLUMN ---
with st.expander("📊 Wybierz kolumny tabeli"):
    st.multiselect("Kolumny towaru:", ["Kod", "EAN", "Waga", "Katalog"], default=["Kod", "EAN"])
    st.multiselect("Porównywarki:", ["Ceneo", "Google", "Empik"])

# --- TABELA DANYCH (Moje Dostawy) ---
st.subheader("MOJE DOSTAWY")

# Przykładowe dane odzwierciedlające zdjęcie
data = {
    "Lp.": [1, 2, 3, 4, 5],
    "Dostawca": ["ABC", "BARREL OPTICS", "WYDAWNICTWO X", "Darek", "ASG"],
    "Nr dostawy": ["14/23", "1/24-sampl", "7/24", "1/24", "13/20"],
    "Data": ["17-03-2024", "12-01-2024", "12-01-2024", "-", "05-03-2024"],
    "Priorytet": ["Normalny", "Normalny", "Normalny", "Normalny", "Normalny"],
    "Status": ["BR", "Zamówiono", "SKŁAD", "Zrealizowano", "BR"],
    "Zakupy": ["Brak danych", "Brak danych", "W przygotowaniu", "Brak danych", "Gotowy"]
}

df = pd.DataFrame(data)

# Wyświetlenie tabeli z interaktywnymi funkcjami
st.dataframe(df, use_container_width=True, hide_index=True)

# Pasek statusu na dole
st.info("Znaleziono towary: > 1000")
