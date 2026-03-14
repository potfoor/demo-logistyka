import streamlit as st
import pandas as pd

# Konfiguracja strony
st.set_page_config(layout="wide", page_title="Panel Logistyczny")

# --- CUSTOM CSS (Stylizacja wizualna) ---
st.markdown("""
    <style>
    /* Główny tło i fonty */
    .stApp { background-color: #f8f9fa; }
    
    /* Stylizacja górnych tagów */
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 15px; }
    .tag { padding: 2px 8px; border-radius: 3px; font-size: 11px; color: white; font-weight: 600; text-transform: uppercase; }
    
    /* Stylizacja nagłówków sekcji */
    .section-header { 
        background-color: #f1f1f1; 
        padding: 5px 10px; 
        border-radius: 5px 5px 0 0; 
        border-bottom: 2px solid #ddd;
        font-weight: bold; font-size: 14px;
        margin-top: 10px;
    }
    
    /* Kolory statusów w tabeli (symulacja) */
    .status-br { background-color: #d4edda; color: #155724; padding: 3px; border-radius: 3px; }
    .status-missing { background-color: #f8d7da; color: #721c24; padding: 3px; border-radius: 3px; }
    
    /* Pasek boczny - ikony i tekst */
    .css-1d391kg { background-color: #ffffff; }
    </style>
""", unsafe_allow_html=True)

# --- SIDEBAR (Menu boczne z ikonami) ---
with st.sidebar:
    st.markdown("### 🖥️ Maszynoplik")
    st.markdown("---")
    st.write("🔍 **Filtry produktów**")
    st.write("⚙️ **Operacje**")
    st.write("➕ **Dodawanie towarów**")
    st.write("📦 **Zestawy produktów**")
    st.markdown("---")
    st.write("💰 **CenoPlik**")
    st.write("📊 **Ceny produktów**")
    st.write("📑 **Rodzaje cen**")
    st.markdown("---")
    st.write("📥 **Import**")
    st.write("📋 **Kolejka importów**")

# --- GÓRNE MENU (Kolorowe Tagi) ---
tags_html = """
<div class="tag-container">
    <span class="tag" style="background-color: #333;">#01 MEDIA</span>
    <span class="tag" style="background-color: #93c47d;">#4F AW'23</span>
    <span class="tag" style="background-color: #6aa84f;">#4F AW'24</span>
    <span class="tag" style="background-color: #38761d;">#4F GR.F</span>
    <span class="tag" style="background-color: #e06666;">#4SHOOTER</span>
    <span class="tag" style="background-color: #3d85c6;">#A ZESTAWY</span>
    <span class="tag" style="background-color: #45818e;">#ABISAL</span>
</div>
"""
st.markdown(tags_html, unsafe_allow_html=True)

# --- SEKCE FILTRÓW (Układ kolumnowy) ---
c1, c2 = st.columns([1, 2.5])

with c1:
    st.markdown('<div class="section-header">Filtry - Unikalne</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.text_input("SKU:", placeholder="Wpisz SKU...")
        st.checkbox("Pokaż warianty", value=True)
        btn_cols = st.columns(3)
        btn_cols[0].button("🔵 FILTRUJ")
        btn_cols[1].button("📂 ZAKŁADKĘ")
        btn_cols[2].button("🔄")

with c2:
    st.markdown('<div class="section-header">Filtry - Wielowybór</div>', unsafe_allow_html=True)
    with st.container(border=True):
        f_row1 = st.columns(3)
        f_row1[0].selectbox("Zakładka:", ["Wszystkie", "Magazyn", "Outlet"])
        f_row1[1].multiselect("Grupy:", ["Grupa A", "Grupa B"], default=[])
        f_row1[2].selectbox("Typ PIM:", ["Dowolny", "Zdefiniowany"])
        
        f_row2 = st.columns(3)
        f_row2[0].text_input("Kod obcy:")
        f_row2[1].text_input("Marka:")
        f_row2[2].date_input("Odcięcie:")
        st.button("⚙️ ZAAWANSOWANE")

# --- TABELA "MOJE DOSTAWY" ---
