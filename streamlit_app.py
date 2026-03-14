import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. Konfiguracja strony
st.set_page_config(layout="wide", page_title="System Logistyczny Pro", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW
osoby_kolory = {
    "Jan Kowalski": "#333333",
    "Anna Nowak": "#8db600",
    "Piotr Zieliński": "#ff5722",
    "Marek Woźniak": "#0288d1"
}
ZALOGOWANY_UZYTKOWNIK = "Jan Kowalski"

# 3. BAZA DOSTAWCÓW
lista_firm = ["Samsung Electronics", "Toyota Motor Poland", "Coca-Cola HBC", "Microsoft", "Nestlé Polska", "Apple Poland"]
opiekunowie = list(osoby_kolory.keys())
dostawcy_base = [{"firma": nazwa, "opiekun": opiekunowie[i % len(opiekunowie)]} for i, nazwa in enumerate(lista_firm)]

# 4. CSS DLA STYLIZACJI
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; }
    div[data-testid="stPopover"] > button { margin-top: 28px; height: 38px; width: 100%; border: 1px solid #d1d5db; }
    </style>
""", unsafe_allow_html=True)

# --- 5. GENEROWANIE DANYCH (Z LOGIKĄ POWIADOMIEŃ) ---
raw_data = []
licznik_cen_alert = 0

for i, d in enumerate(dostawcy_base):
    # Symulacja: Jan Kowalski ma alerty cenowe w co drugiej swojej dostawie
    ma_alert_cenowy = "TAK" if d["opiekun"] == "Jan Kowalski" and i % 2 == 0 else "Nie"
    
    if ma_alert_cenowy == "TAK":
        licznik_cen_alert += 1
        
    raw_data.append({
        "Lp.": i + 1, "Dostawca": d["firma"], "Nr dostawy": f"{104+i}/26 🔗",
        "HWO": "12-03-2026", "Status": "Zamówione", "Zakupy": "OK",
        "Cen": ma_alert_cenowy, "Waga": "150kg", "Opiekun": d["opiekun"],
        "Aktualizacja": "12-03-2026 13:42:56"
    })

df = pd.DataFrame(raw_data)

# --- 6. PANEL BOCZNY Z DYNAMICZNYM POWIADOMIENIEM ---
with st.sidebar:
    st.title("🚚 Logistyka App")
    st.write(f"Zalogowany: **{ZALOGOWANY_UZYTKOWNIK}**")
    st.divider()
    
    menu_selected = sac.tree(
        items=[
            sac.TreeItem('Dashboard', icon='speedometer2'),
            sac.TreeItem('Zamówienia', icon='box', children=[
                # Dynamiczny Badge przy powiadomieniach
                sac.TreeItem('Powiadomienia', icon='bell', 
                             tag=sac.Tag(str(licznik_cen_alert), color='red') if licznik_cen_alert > 0 else None),
                sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                    sac.TreeItem('Moje Dostawy', icon='person-check'),
                    sac.TreeItem('Wszystkie Dostawy', icon='globe'),
                ]),
            ]),
        ], label='NAWIGACJA', open_all=True, size='sm'
    )

# --- 7. LOGIKA FILTROWANIA SESJI ---
if menu_selected == 'Moje Dostawy':
    st.session_state.o_sel = [ZALOGOWANY_UZYTKOWNIK]
elif menu_selected == 'Wszystkie Dostawy':
    st.session_state.o_sel = []

if 'o_sel' not in st.session_state: st.session_state.o_sel = []

df_filtered = df.copy()
if st.session_state.o_sel:
    df_filtered = df[df["Opiekun"].isin(st.session_state.o_sel)]

# --- 8. WIDOK GŁÓWNY ---
st.write(f"**Aktywni Dostawcy:**")
tags_html = '<div class="tag-container">'
for d in df_filtered["Dostawca"].unique():
    # Pobieramy kolor opiekuna dla danego dostawcy
    opiekun = df[df["Dostawca"] == d]["Opiekun"].values[0]
    kolor = osoby_kolory.get(opiekun, "#cccccc")
    tags_html += f'<span class="tag" style="background-color: {kolor};">{d}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

# Sekcja wyszukiwania (uproszczona dla czytelności przykładu)
st.header("🔍 Wyszukiwanie")
with st.container(border=True):
    c1, c2, c3 = st.columns([3, 1, 3])
    with c1: st.selectbox("Dostawca:", ["Wszyscy"] + list(df["Dostawca"].unique()))
    with c2: 
        with st.popover("📇 KARTA"):
            st.write("Szczegóły B2B / Kontakt")
    with c3: st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=st.session_state.o_sel)

# --- 9. TABELA Z KOLOROWANIEM KOMÓREK ---
st.write("---")
st.subheader(f"📊 Tabela: {menu_selected}")

# Funkcja do kolorowania kolumny 'Cen'
def style_price_alerts(val):
    color = '#ffcccc' if val == "TAK" else 'transparent'
    return f'background-color: {color}'

# Zastosowanie stylu do DataFrame
styled_df = df_filtered.style.applymap(style_price_alerts, subset=['Cen'])

st.dataframe(
    styled_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Lp.": st.column_config.Column(width=40),
        "Cen": st.column_config.TextColumn("Cen", help="Wyróżnienie na czerwono oznacza zmianę ceny!")
    }
)
