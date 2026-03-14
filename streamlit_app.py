import streamlit as st
import pandas as pd
import streamlit_antd_components as sac

# 1. KONFIGURACJA STRONY
st.set_page_config(layout="wide", page_title="System Logistyczny Pro", page_icon="🚚")

# 2. DEFINICJA OSÓB I KOLORÓW
osoby_kolory = {
    "Jan Kowalski": "#333333",
    "Anna Nowak": "#8db600",
    "Piotr Zieliński": "#ff5722",
    "Marek Woźniak": "#0288d1"
}
ZALOGOWANY_UZYTKOWNIK = "Jan Kowalski"

# 3. BAZA DANYCH
lista_firm = [
    "Samsung", "Toyota", "Coca-Cola", "Microsoft", "Nestlé", "Apple", "LG", "Sony", 
    "Dell", "IKEA", "Nike", "Adidas", "BMW", "Amazon", "DHL", "FedEx", "Pepsi", "Canon"
]

raw_data = []
for i, firma in enumerate(lista_firm):
    opiekun = "Jan Kowalski" if (i < 12 or i % 2 == 0) else list(osoby_kolory.keys())[i % 4]
    ma_alert = "TAK" if opiekun == "Jan Kowalski" and i in [0, 2, 5, 8, 10, 14] else "Nie"
    
    raw_data.append({
        "Lp.": i + 1, "Dostawca": firma, "Nr dostawy": f"{100+i}/26 🔗",
        "HWO": "12-03-2026", "Data aw. OD": "14-03-2026", "Data aw. DO": "", 
        "Priorytet": "Normalny", "Status": "Zamówione", "Zakupy": "OK", 
        "Kurier": "Virtus", "List": "/", "Brak AW": "/", "Brak FV": "Nie", 
        "Cen": ma_alert, "New": "Nie", "Waga": f"{150 + i}kg", "Knt": "/", 
        "Pal": "1", "Box": "4", "Opiekun": opiekun, "Aktualizacja": "2026-03-14 22:00"
    })

df = pd.DataFrame(raw_data)
alerty_jana = df[(df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK) & (df["Cen"] == "TAK")]
liczba_alertow = len(alerty_jana)

# 4. CSS DLA INTERFEJSU I ODSTĘPÓW 50PX
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    
    /* Stylizacja przycisków */
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; }
    div[data-testid="column"] button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    
    /* Kontener dla Szybkich Akcji z odstępem 50px */
    .szybkie-akcje-container {
        display: flex;
        gap: 50px !important;
        align-items: center;
    }
    .szybkie-akcje-container > div {
        flex: 1;
    }

    .alert-box { padding: 15px; background-color: #fff5f5; border-left: 5px solid #ff4b4b; border-radius: 5px; margin-bottom: 10px; }
    [data-testid="stDataFrame"] { font-size: 11px; }
    div[data-testid="stPopover"] > button { margin-top: 28px; height: 38px; width: 100%; border: 1px solid #d1d5db; }
    </style>
""", unsafe_allow_html=True)

# 5. PANEL BOCZNY
with st.sidebar:
    st.title("🚚 Logistyka App")
    st.write(f"Zalogowany: **{ZALOGOWANY_UZYTKOWNIK}**")
    st.divider()
    menu_selected = sac.tree(
        items=[
            sac.TreeItem('Dashboard', icon='speedometer2'),
            sac.TreeItem('Zamówienia', icon='box', children=[
                sac.TreeItem('Powiadomienia', icon='bell', tag=sac.Tag(str(liczba_alertow), color='red')),
                sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                    sac.TreeItem('Moje Dostawy', icon='person-check'),
                    sac.TreeItem('Wszystkie Dostawy', icon='globe'),
                ]),
            ]),
        ], label='NAWIGACJA', open_all=True, size='sm'
    )

# --- LOGIKA WYŚWIETLANIA ---

if menu_selected == 'Powiadomienia':
    st.header("🔔 Powiadomienia Systemowe")
    st.subheader(f"Alerty cenowe dla: {ZALOGOWANY_UZYTKOWNIK}")
    if not alerty_jana.empty:
        for _, row in alerty_jana.iterrows():
            st.markdown(f"""<div class="alert-box"><strong style="color: #ff4b4b;">⚠️ ALERT CENOWY</strong><br>Dostawca: <b>{row['Dostawca']}</b> | Nr dostawy: <b>{row['Nr dostawy']}</b><br><small>Wykryto niezgodność ceny w B2B.</small></div>""", unsafe_allow_html=True)
    else:
        st.success("Brak nowych powiadomień.")

else:
    # --- WIDOK DOSTAW ---
    df_display = df.copy()
    if menu_selected == 'Moje Dostawy':
        df_display = df[df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK]

    # TAGI NA GÓRZE
    st.write(f"**Aktywni Dostawcy:**")
    tags_html = '<div class="tag-container">'
    for _, d in df_display.drop_duplicates('Dostawca').iterrows():
        kolor = osoby_kolory.get(d["Opiekun"], "#cccccc")
        tags_html += f'<span class="tag" style="background-color: {kolor};">{d["Dostawca"]}</span>'
    tags_html += '</div>'
    st.markdown(tags_html, unsafe_allow_html=True)

    # 6. PANEL WYSZUKIWANIA
    st.header("🔍 Wyszukiwanie")
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 3])
        with c1:
            d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + list(df_display["Dostawca"].unique()))
        with c2:
            with st.popover("📇 KARTA"):
                if d_sel != "Wszyscy":
                    st.subheader(f"Karta: {d_sel}")
                    st.text_input("URL:", f"https://b2b.{d_sel.lower()}.com")
                    st.text_input("Login:", "jan_logistyk")
                    st.text_input("Hasło:", "********", type="password")
                else: st.warning("Wybierz dostawcę")
        with c3:
            o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=[ZALOGOWANY_UZYTKOWNIK] if menu_selected == 'Moje Dostawy' else [])

        c4, c5, c6, c7 = st.columns([3, 3, 2, 2])
        with c4: st.text_input("Ticket:", placeholder="Wpisz numer...")
        with c5: st.multiselect("Flaga:", ["PILNE", "POWTÓRKA"])
        with c6:
            st.write("**Statusy:**")
            st.checkbox("Otwarte", value=True); st.checkbox("Zamknięte")
        with c7:
            st.write("**Akcje:**")
            st.button("🚀 ZASTOSUJ FILTRY", type="primary")

        st.write("---")
        # SZYBKIE AKCJE Z ODSTĘPEM 50PX
        st.write("**Akcje Szybkie:**")
        # Tworzymy kontener z 4 kolumnami i CSS gap
        st.markdown('<div class="szybkie-akcje-container">', unsafe_allow_html=True)
        sa1, sa2, sa3, sa4 = st.columns(4)
        with sa1: st.button("✨ Nowa dostawa")
        with sa2: st.button("➕ Dodaj Dostawcę")
        with sa3: st.button("🚛 Dodaj Przewoźnika")
        with sa4: st.button("🔄 Zamówienia Cykliczne")
        st.markdown('</div>', unsafe_allow_html=True)

    # 7. ZARZĄDZANIE TABELĄ (Przywrócone nad tabelę)
    st.write("---")
    st.subheader("📊 Zarządzanie Tabelą")
    wszystkie_kolumny = ["Lp.", "Dostawca", "Nr dostawy", "HWO", "Data aw. OD", "Data aw. DO", "Priorytet", "Status", "Zakupy", "Kurier", "List", "Brak AW", "Brak FV", "Cen", "New", "Waga", "Knt", "Pal", "Box", "Opiekun", "Aktualizacja"]
    
    col_mgmt1, col_mgmt2 = st.columns([3, 1])
    with col_mgmt1:
        selected_cols = st.multiselect("Pokaż kolumny:", wszystkie_kolumny, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Cen", "Waga", "Opiekun"])
    with col_mgmt2:
        st.selectbox("Widok:", ["Standardowy", "Pełny Logistyczny"])

    # 8. TABELA
    final_df = df_display.copy()
    if d_sel != "Wszyscy": final_df = final_df[final_df["Dostawca"] == d_sel]
    if o_sel: final_df = final_df[final_df["Opiekun"].isin(o_sel)]

    st.dataframe(
        final_df[selected_cols].style.applymap(lambda x: 'background-color: #ffcccc' if x == "TAK" else '', subset=['Cen'] if 'Cen' in selected_cols else []),
        use_container_width=True,
        hide_index=True,
        column_config={"Lp.": st.column_config.Column(width=40)}
    )
