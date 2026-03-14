import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny - Full Data", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW (Bez zmian)
osoby_kolory = {
    "Jan Kowalski": "#333333",
    "Anna Nowak": "#8db600",
    "Piotr Zieliński": "#ff5722",
    "Marek Woźniak": "#0288d1"
}

# 3. BAZA DOSTAWCÓW (Twoja pierwotna lista - bez zmian)
lista_firm = [
    "Samsung Electronics", "Toyota Motor Poland", "Coca-Cola HBC", "Microsoft",
    "Nestlé Polska", "Apple Poland", "Grupa Azoty", "Volkswagen Group",
    "Procter & Gamble", "Siemens", "Philips Lighting", "Robert Bosch",
    "L'Oréal Polska", "PepsiCo", "Unilever", "ABB Sp. z o.o.", "Danone",
    "IKEA Retail", "Bridgestone", "Dell Technologies", "BASF Polska",
    "Michelin", "Saint-Gobain", "Continental", "Sony Interactive",
    "Huawei Polska", "Goodyear", "Henkel Polska", "LG Electronics", "Castorama Polska"
]

opiekunowie = list(osoby_kolory.keys())
dostawcy_base = [
    {"firma": nazwa, "opiekun": opiekunowie[i % len(opiekunowie)]}
    for i, nazwa in enumerate(lista_firm)
]

# 4. CSS DLA TABELI I TAGÓW
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; }
    [data-testid="stDataFrame"] { font-size: 11px; } /* Mniejsza czcionka dla wielu kolumn */
    </style>
""", unsafe_allow_html=True)

# --- LOGIKA FILTROWANIA (Musi być przed tagami) ---
if 'dostawca_sel' not in st.session_state: st.session_state.dostawca_sel = "Wszyscy"
if 'odp_sel' not in st.session_state: st.session_state.odp_sel = []

dostawcy_filtered = dostawcy_base
if st.session_state.odp_sel:
    dostawcy_filtered = [d for d in dostawcy_base if d["opiekun"] in st.session_state.odp_sel]
if st.session_state.dostawca_sel != "Wszyscy":
    dostawcy_filtered = [d for d in dostawcy_filtered if d["firma"] == st.session_state.dostawca_sel]

# --- 7. AKTYWNI DOSTAWCY (NA SAMEJ GÓRZE) ---
st.write(f"**Aktywni Dostawcy (Kolor wg Opiekuna):**")
tags_html = '<div class="tag-container">'
for d in dostawcy_filtered:
    kolor = osoby_kolory.get(d["opiekun"], "#cccccc")
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d["firma"]}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# 6. SEKCJA WYSZUKIWANIE
st.header("🔍 Wyszukiwanie")
with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 3])
    with c1:
        st.session_state.dostawca_sel = st.selectbox("Dostawca:", ["Wszyscy"] + [d["firma"] for d in dostawcy_base])
    with c2:
        with st.popover("📇 Karta"): st.write("Dane dostawcy")
    with c3:
        st.session_state.odp_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()))

    c4, c5, c6, c7 = st.columns([3, 3, 2, 2])
    with c4: st.text_input("Ticket:", placeholder="Nr ticketu...")
    with c5: st.multiselect("Flaga:", ["PILNE", "POWTÓRKA"])
    with c6:
        st.write("**Statusy:**")
        st.checkbox("Otwarte", value=True)
        st.checkbox("Zamknięte")
    with c7:
        st.write("**Akcje:**")
        st.button("🚀 ZASTOSUJ FILTRY", type="primary")

    st.write("---")
    st.write("**Akcje Szybkie:**")
    b1, b2, b3 = st.columns(3)
    b1.button("➕ Dodaj Dostawcę")
    b2.button("🚛 Dodaj Przewoźnika")
    b3.button("🔄 Zamówienia Cykliczne")

# 8. ZARZĄDZANIE TABELĄ (Wszystkie kolumny ze screenshotu)
st.write("---")
st.subheader("📊 Zarządzanie Tabelą")

wszystkie_kolumny = [
    "Lp.", "Dostawca", "Nr dostawy", "HWO", "Data aw. OD", "Data aw. DO", 
    "Priorytet", "Status", "Zakupy", "Kurier", "List", 
    "Brak AW", "Brak FV", "Cen", "New", "Waga", "Knt", "Pal", "Box", "Opiekun", "Aktualizacja"
]

selected_cols = st.multiselect("Wybierz kolumny:", wszystkie_kolumny, 
                              default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Zakupy", "Waga", "Opiekun", "Aktualizacja"])

# 9. GENEROWANIE DANYCH (Uzupełnienie jak na wzorze)
raw_data = []
for i, d in enumerate(dostawcy_filtered):
    raw_data.append({
        "Lp.": i + 1,
        "Dostawca": d["firma"],
        "Nr dostawy": f"{14+i}/26 sample 🔗",
        "HWO": "12-03-2026" if i % 2 == 0 else "",
        "Data aw. OD": "12-03-2026" if i % 2 == 0 else "",
        "Data aw. DO": "",
        "Priorytet": "Normalny",
        "Status": "SKŁAD" if i == 2 else ("Zamówione" if i % 2 != 0 else "BR"),
        "Zakupy": "W przygotowaniu" if i == 2 else "Brak danych",
        "Kurier": "Virtus Logistics" if i % 2 == 0 else "",
        "List": "",
        "Brak AW": "/",
        "Brak FV": "Nie",
        "Cen": "Nie",
        "New": "Tak" if i == 2 else "Nie",
        "Waga": "150kg" if i % 2 == 0 else "",
        "Knt": "/",
        "Pal": "1" if i % 2 == 0 else "",
        "Box": "2" if i % 2 == 0 else "1",
        "Opiekun": d["opiekun"],
        "Aktualizacja": "12-03-2026 13:42:56"
    })

df = pd.DataFrame(raw_data)

st.dataframe(
    df[selected_cols],
    use_container_width=True,
    hide_index=True,
    column_config={
        "Lp.": st.column_config.Column(width=40),
        "Dostawca": st.column_config.Column(width=200),
        "Nr dostawy": st.column_config.Column(width=150),
        "Status": st.column_config.Column(width=100),
        "Zakupy": st.column_config.Column(width=150),
        "Waga": st.column_config.Column(width=70),
        "Opiekun": st.column_config.Column(width=150),
        "Aktualizacja": st.column_config.Column(width=160),
    }
)
