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

# 3. BAZA DOSTAWCÓW
dostawcy_base = [
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

# 4. CSS
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding: 10px 0; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 9px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; }
    div[data-testid="stPopover"] > button { margin-top: 28px; border: 1px solid #d1d5db; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY (Drzewko)
with st.sidebar:
    st.title("Panel Sterowania")
    # Używamy prostszej listy słowników dla drzewka (bardziej kompatybilne)
    menu_selection = sac.tree(
        items=[
            {'label': 'Zamówienia', 'icon': 'box', 'children': [
                {'label': 'Powiadomienia', 'icon': 'bell'},
                {'label': 'Ticket', 'icon': 'ticket-perforated', 'children': [
                    {'label': 'Moje Dostawy'}, {'label': 'Wszystkie Dostawy'}
                ]},
            ]},
        ], label='NAWIGACJA', open_all=True, size='sm'
    )

# 6. WYSZUKIWANIE
st.header("🔍 Wyszukiwanie")

with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 3])
    
    with c1:
        # BEZPIECZNA WERSJA: Przekazujemy listę nazw zamiast obiektów CascaderItem
        # Dodajemy ikonę karty jako tekstową atrapę obok nazwy firmy
        lista_dostawcow_z_ikonami = [f"📇 {d['firma']}" for d in dostawcy_base]
        dostawca_wybrany_raw = sac.cascader(
            label='Dostawca:',
            items=lista_dostawcow_z_ikonami,
            placeholder='Wybierz dostawcę...',
            search=True,
            clearable=True,
            size='sm'
        )
        # Oczyszczamy nazwę z ikony do filtrowania
        dostawca_sel = dostawca_wybrany_raw.replace("📇 ", "") if dostawca_wybrany_raw else None
    
    with c2:
        with st.popover("📇 Karta"):
            if dostawca_sel:
                st.subheader(f"Szczegóły: {dostawca_sel}")
                st.text_input("Osoba kontaktowa:", "Jan Nowak")
                st.text_input("B2B URL:", "https://b2b.logistyka.pl")
                st.button("💾 Zapisz dane")
            else:
                st.info("Wybierz dostawcę.")

    with c3:
        odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))

    c4, c5, c6 = st.columns([3, 2, 2])
    with c4:
        ticket_input = st.text_input("Ticket:", placeholder="Wpisz nr ticketu...")
    with c5:
        st.write("**Statusy:**")
        st_col1, st_col2 = st.columns(2)
        otwarte = st_col1.checkbox("Otwarte", value=True)
        zamkniete = st_col2.checkbox("Zamknięte")
    with c6:
        st.write("**Akcje:**")
        apply_btn = st.button("🚀 ZASTOSUJ FILTRY", type="primary")

# LOGIKA FILTROWANIA
dostawcy_filtered = dostawcy_base
if odp_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in odp_sel]
if dostawca_sel:
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == dostawca_sel]

# 7. TAGI
st.write(f"**Aktywni Dostawcy ({len(dostawcy_filtered)}):**")
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
    selected_cols = st.multiselect("Kolumny:", all_columns, default=["Lp.", "Dostawca", "Status", "Odpowiedzialny"])

with z2:
    st.selectbox("Szablony:", ["Standard", "Magazyn"])
    st.button("💾 Zapisz")

# 9. TABELA
raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{i+102}/2024",
        "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"],
        "Zakupy": "OK"
    })

if raw_data:
    df = pd.DataFrame(raw_data)
    st.dataframe(df[selected_cols], use_container_width=True, hide_index=True)
