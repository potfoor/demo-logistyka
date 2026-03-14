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

# 3. PEŁNA LISTA DOSTAWCÓW
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
    .tag-container { display: flex; flex-wrap: wrap; gap: 5px; margin-bottom: 20px; }
    .tag { padding: 4px 10px; border-radius: 4px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
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

# 6. SEKCJA WYSZUKIWANIA (FILTRY) - Przeniesiona wyżej, aby wpływać na tagi
st.subheader("🔍 Wyszukiwanie")
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        dostawca_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base])
        ticket_input = st.text_input("Ticket:", placeholder="Wpisz numer...")
    with col2:
        # KLUCZOWY FILTR: Odpowiedzialny
        odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))
    with col3:
        st.write("**Statusy:**")
        otwarte = st.checkbox("Otwarte", value=True)
        zamkniete = st.checkbox("Zamknięte")
    with col4:
        st.write("**Akcje:**")
        # Przycisk ZASTOSUJ teraz faktycznie filtruje
        apply_filter = st.button("🚀 FILTRUJ / ZASTOSUJ", type="primary", use_container_width=True)

# --- LOGIKA FILTROWANIA ---
dostawcy_filtered = dostawcy_base

# Jeśli wybrano osoby odpowiedzialne, filtrujemy listę
if odp_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in odp_sel]

# Dodatkowe filtrowanie po konkretnym dostawcy (selectbox)
if dostawca_sel != "Wszyscy":
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == dostawca_sel]

# 7. GENEROWANIE GÓRNYCH TAGÓW (Zależne od filtra)
st.write("**Aktywni Dostawcy:**")
tags_html = '<div class="tag-container">'
for d in dostawcy_filtered:
    kolor = osoby_kolory[d["opiekun"]]
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# 8. ZARZĄDZANIE TABELĄ
st.write("---")
st.subheader("📊 Zarządzanie Tabelą")
col_manage1, col_manage2 = st.columns([2, 1])

with col_manage1:
    all_columns = ["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny", "Zakupy", "Data Awizacji"]
    selected_cols = st.multiselect("Wybierz kolumny:", all_columns, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Odpowiedzialny"])

with col_manage2:
    st.selectbox("Szablony widoku:", ["Standardowy", "Dla Magazynu", "Finansowy"])
    st.button("💾 Zapisz Szablon", use_container_width=True)

# 9. TABELA DANYCH (Filtrowana)
raw_table_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_table_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{i+102}/2024",
        "Status": "SKŁAD" if i % 2 == 0 else "W DRODZE",
        "Odpowiedzialny": d["opiekun"],
        "Zakupy": "Zatwierdzone",
        "Data Awizacji": "2024-03-25",
        "color_hex": osoby_kolory[d["opiekun"]] 
    })

df = pd.DataFrame(raw_table_data)

def style_row(row):
    color = row["color_hex"]
    return [f'background-color: {color}; color: white;' for _ in row]

if not df.empty:
    st.dataframe(
        df[selected_cols + ["color_hex"]].style.apply(style_row, axis=1),
        use_container_width=True,
        hide_index=True,
        column_config={"color_hex": None}
    )
else:
    st.warning("Brak danych dla wybranych filtrów.")

st.info(f"Wyświetlono {len(dostawcy_filtered)} dostawców.")
