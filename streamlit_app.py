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

# 4. CSS DLA ZWARTEGO UKŁADU
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding: 10px 0; justify-content: flex-start; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 9px; color: white; font-weight: bold; text-transform: uppercase; white-space: nowrap; }
    .stSelectbox label, .stMultiSelect label, .stTextInput label { font-size: 13px !important; font-weight: bold !important; }
    /* Stylizacja przycisku popovera */
    div[data-testid="stPopover"] > button { border-radius: 5px; height: 38px; margin-top: 28px; width: 100%; }
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
        ],
        label='NAWIGACJA', open_all=True, size='sm'
    )

# --- UKŁAD GŁÓWNY ---
st.header("🔍 Wyszukiwanie")

# 6. FILTRY
with st.container(border=True):
    r1_col1, r1_col2, r1_col3, r1_col4, r1_col5 = st.columns([2, 0.6, 2, 1, 1.5])
    
    with r1_col1:
        dostawca_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base])
    
    with r1_col2:
        # KARTA DOSTAWCY JAKO POPOVER
        with st.popover("📇 Karta"):
            if dostawca_sel == "Wszyscy":
                st.warning("Wybierz dostawcę, aby edytować kartę.")
            else:
                st.subheader(f"Dane dostawcy: {dostawca_sel}")
                st.text_input("Osoba kontaktowa:", value="Jan Nowak")
                st.text_input("E-mail kontaktowy:", value="kontakt@firma.pl")
                st.divider()
                st.write("**Dostęp B2B**")
                st.text_input("URL Systemu:", value="https://b2b.firma.pl")
                st.text_input("Login:", value="user_demo")
                st.text_input("Hasło:", type="password", value="********")
                if st.button("💾 Zapisz dane karty", use_container_width=True):
                    st.success("Zapisano pomyślnie!")
    
    with r1_col3:
        odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))
    
    with r1_col4:
        st.write("**Statusy:**")
        otwarte = st.checkbox("Otwarte", value=True)
        zamkniete = st.checkbox("Zamknięte")
        
    with r1_col5:
        st.write("**Akcje:**")
        apply_btn = st.button("🚀 ZASTOSUJ FILTRY", type="primary", use_container_width=True)

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
m_col1, m_col2 = st.columns([3, 1])

with m_col1:
    all_columns = ["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny", "Zakupy", "Data Awizacji"]
    selected_cols = st.multiselect("Wybierz kolumny:", all_columns, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny"])

with m_col2:
    st.selectbox("Szablony widoku:", ["Standardowy", "Dla Magazynu", "Finansowy"])
    st.button("💾 Zapisz Szablon", use_container_width=True)

# 9. TABELA DANYCH
raw_table_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_table_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{i+102}/2024",
        "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"],
        "Zakupy": "Zatwierdzone",
        "Data Awizacji": "2024-03-25"
    })

if raw_table_data:
    df = pd.DataFrame(raw_table_data)
    st.dataframe(df[selected_cols], use_container_width=True, hide_index=True)
else:
    st.warning("Brak wyników dla wybranych kryteriów.")
