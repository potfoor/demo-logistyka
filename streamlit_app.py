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

# 4. CSS DLA CZYTELNOŚCI
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding: 10px 0; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 9px; color: white; font-weight: bold; text-transform: uppercase; }
    div[data-testid="stPopover"] > button { margin-top: 28px; width: 100%; border: 1px solid #d1d5db; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY (Drzewko - uproszczone do list, by uniknąć błędów)
with st.sidebar:
    st.title("Panel Sterowania")
    sac.tree(
        items=[
            {'label': 'Zamówienia', 'icon': 'box', 'children': [
                {'label': 'Powiadomienia', 'icon': 'bell'},
                {'label': 'Ticket', 'icon': 'ticket-perforated'},
            ]},
        ], label='NAWIGACJA', open_all=True
    )

# 6. WYSZUKIWANIE
st.header("🔍 Wyszukiwanie")

with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 3])
    
    with c1:
        # ROZWIĄZANIE PROBLEMU: Standardowy selectbox z dodanymi ikonami (emoji)
        opcje_dostawcow = ["Wszyscy"] + [f"📇 {d['firma']}" for d in dostawcy_base]
        wybrany_element = st.selectbox("Dostawca:", opcje_dostawcow)
        
        # Oczyszczamy nazwę z ikony do logiki filtrów
        dostawca_sel = wybrany_element.replace("📇 ", "") if wybrany_element != "Wszyscy" else "Wszyscy"
    
    with c2:
        # KARTA DOSTAWCY
        with st.popover("📇 Karta"):
            if dostawca_sel != "Wszyscy":
                st.subheader(f"Dane: {dostawca_sel}")
                st.text_input("Kontakt:", "Jan Kowalski")
                st.text_input("B2B URL:", "https://system.b2b.pl")
                st.text_input("Hasło:", type="password", value="demo123")
                st.button("Zapisz")
            else:
                st.info("Wybierz firmę")

    with c3:
        odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))

    c4, c5, c6 = st.columns([3, 2, 2])
    with c4:
        st.text_input("Ticket:", placeholder="Nr ticketu...")
    with c5:
        st.write("**Statusy:**")
        st_c1, st_c2 = st.columns(2)
        st_c1.checkbox("Otwarte", value=True)
        st_c2.checkbox("Zamknięte")
    with c6:
        st.write("**Akcje:**")
        st.button("🚀 ZASTOSUJ FILTRY", type="primary")

# LOGIKA FILTROWANIA
dostawcy_filtered = dostawcy_base
if odp_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in odp_sel]
if dostawca_sel != "Wszyscy":
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
    wybrane_kolumny = st.multiselect("Kolumny:", ["Lp.", "Dostawca", "Status", "Odpowiedzialny", "Zakupy"], default=["Lp.", "Dostawca", "Status", "Odpowiedzialny"])
with z2:
    st.selectbox("Szablony:", ["Standard", "Logistyka"])
    st.button("💾 Zapisz")

# 9. TABELA
raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1, "Dostawca": d["firma"], "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"], "Zakupy": "OK"
    })

if raw_data:
    st.dataframe(pd.DataFrame(raw_data)[wybrane_kolumny], use_container_width=True, hide_index=True)
