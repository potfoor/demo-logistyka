import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
from datetime import datetime

# --- 1. KONFIGURACJA ---
st.set_page_config(layout="wide", page_title="System Logistyczny Pro", page_icon="🚚")

# --- 2. STAN SESJI (Dla kreatora i filtrów) ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'current_year' not in st.session_state: st.session_state.current_year = 26

# --- 3. DANE I KOLORY ---
osoby_kolory = {
    "Jan Kowalski": "#333333",
    "Anna Nowak": "#8db600",
    "Piotr Zieliński": "#ff5722",
    "Marek Woźniak": "#0288d1"
}
ZALOGOWANY_UZYTKOWNIK = "Jan Kowalski"

lista_firm = ["Samsung", "Toyota", "Coca-Cola", "Microsoft", "Nestlé", "Apple", "LG", "Sony", "Dell", "IKEA"]

# Generowanie bazy (Jan Kowalski ma większość)
raw_data = []
for i, firma in enumerate(lista_firm * 2):
    opiekun = "Jan Kowalski" if (i < 12 or i % 2 == 0) else "Anna Nowak"
    alert = "TAK" if opiekun == "Jan Kowalski" and i in [0, 3, 5, 8] else "Nie"
    raw_data.append({
        "Lp.": i + 1, "Dostawca": firma, "Nr dostawy": f"{100+i}/26 🔗",
        "HWO": "12-03-2026", "Data aw. OD": "14-03-2026", "Status": "Zamówione",
        "Zakupy": "OK", "Cen": alert, "Waga": f"{150+i}kg", "Pal": "1", "Box": "4",
        "Opiekun": opiekun, "Aktualizacja": "2026-03-14 22:00",
        "Data aw. DO": "", "Priorytet": "Normalny", "Kurier": "Virtus", "List": "/", 
        "Brak AW": "/", "Brak FV": "Nie", "New": "Nie", "Knt": "/"
    })
df = pd.DataFrame(raw_data)
alerty_jana = df[(df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK) & (df["Cen"] == "TAK")]

# --- 4. CSS ---
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; }
    div[data-testid="column"] button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stPopover"] > button { margin-top: 28px; height: 38px; width: 100%; border: 1px solid #d1d5db; }
    .alert-box { padding: 15px; background-color: #fff5f5; border-left: 5px solid #ff4b4b; border-radius: 5px; margin-bottom: 10px; }
    [data-testid="stDataFrame"] { font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. MODAL KREATORA NOWEGO ZAMÓWIENIA ---
@st.dialog("PROCES TWORZENIA NOWEGO ZAMÓWIENIA", width="large")
def modal_kreatora():
    sac.steps(items=[
        sac.StepsItem(title='Rodzaj'), sac.StepsItem(title='Dostawca'),
        sac.StepsItem(title='Metoda'), sac.StepsItem(title='Info'), sac.StepsItem(title='Finalizacja')
    ], index=st.session_state.step, color='#ff4b4b')
    
    st.divider()
    if st.session_state.step == 0:
        r = st.radio("Rodzaj:", ["Magazyn", "Pre-order"])
        if r == "Magazyn": st.selectbox("Typ:", ["Zapas", "Bieżące"])
    elif st.session_state.step == 1:
        st.selectbox("Dostawca:", lista_firm)
        st.text_input("Numer zamówienia:", f"1/{st.session_state.current_year}")
    elif st.session_state.step == 2:
        st.segmented(items=['Ręczna', 'Formatka', 'Automatyczna'], color='#ff4b4b')
        st.text_area("Dane zamówienia:")
    elif st.session_state.step == 3:
        st.selectbox("Status:", ["Oczekuje", "W trakcie"])
        st.text_input("Uwagi:")
    elif st.session_state.step == 4:
        st.success("Gotowe do finalizacji!")
        st.info("Status końcowy: W drodze (Awizacja)")

    st.divider()
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.session_state.step > 0:
            if st.button("⬅️ Wróć"): 
                st.session_state.step -= 1
                st.rerun()
    with c_nav2:
        if st.session_state.step < 4:
            if st.button("Dalej ➡️", type="primary"):
                st.session_state.step += 1
                st.rerun()
        else:
            if st.button("✅ Zakończ i Dodaj", type="primary"):
                st.session_state.step = 0
                st.rerun()

# --- 6. PANEL BOCZNY ---
with st.sidebar:
    st.title("🚚 Logistyka App")
    st.write(f"Zalogowany: **{ZALOGOWANY_UZYTKOWNIK}**")
    st.divider()
    menu = sac.tree(items=[
        sac.TreeItem('Dashboard', icon='speedometer2'),
        sac.TreeItem('Zamówienia', icon='box', children=[
            sac.TreeItem('Powiadomienia', icon='bell', tag=sac.Tag(str(len(alerty_jana)), color='red')),
            sac.TreeItem('Ticket', icon='ticket-perforated', children=[
                sac.TreeItem('Moje Dostawy', icon='person-check'),
                sac.TreeItem('Wszystkie Dostawy', icon='globe'),
            ]),
        ]),
    ], label='NAWIGACJA', open_all=True, size='sm')

# --- 7. WIDOKI ---
if menu == 'Powiadomienia':
    st.header("🔔 Powiadomienia")
    for _, r in alerty_jana.iterrows():
        st.markdown(f'<div class="alert-box"><b>⚠️ ALERT CENOWY: {r["Dostawca"]}</b> ({r["Nr dostawy"]})<br>Weryfikacja ceny wymagana.</div>', unsafe_allow_html=True)
else:
    # FILTROWANIE
    df_v = df.copy()
    if menu == 'Moje Dostawy': df_v = df[df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK]

    # TAGI
    st.write("**Aktywni Dostawcy:**")
    t_html = '<div class="tag-container">'
    for d_name in df_v["Dostawca"].unique():
        t_html += f'<span class="tag" style="background-color: {osoby_kolory.get(ZALOGOWANY_UZYTKOWNIK)};">{d_name}</span>'
    st.markdown(t_html + '</div>', unsafe_allow_html=True)

    # WYSZUKIWANIE + KARTA
    st.header("🔍 Wyszukiwanie")
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 3])
        with c1: d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + list(df_v["Dostawca"].unique()))
        with c2:
            with st.popover("📇 KARTA"):
                if d_sel != "Wszyscy":
                    st.subheader(f"Karta: {d_sel}")
                    st.text_input("URL B2B:", f"https://b2b.{d_sel.lower()}.com")
                    st.text_input("Login:", "jan.kowalski")
                    st.text_input("Hasło:", "****", type="password")
                    st.text_input("Email Price List:", "ceny@dostawca.pl")
                    if st.button("💾 Zapisz"): st.success("Zapisano")
                else: st.warning("Wybierz dostawcę")
        with c3: o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=[ZALOGOWANY_UZYTKOWNIK] if menu == 'Moje Dostawy' else [])

        st.columns(4)[0].text_input("Ticket:", placeholder="Nr...")
        st.divider()
        st.write("**Akcje Szybkie:**")
        sa1, sp1, sa2, sp2, sa3, sp3, sa4 = st.columns([1, 0.2, 1, 0.2, 1, 0.2, 1])
        with sa1: 
            if st.button("✨ Nowa dostawa", type="primary"): modal_kreatora()
        with sa2: st.button("➕ Dodaj Dostawcę")
        with sa3: st.button("🚛 Dodaj Przewoźnika")
        with sa4: st.button("🔄 Zamówienia Cykliczne")

    # ZARZĄDZANIE TABELĄ
    st.write("---")
    st.subheader("📊 Zarządzanie Tabelą")
    all_c = ["Lp.", "Dostawca", "Nr dostawy", "HWO", "Status", "Zakupy", "Cen", "Waga", "Pal", "Box", "Opiekun", "Aktualizacja"]
    sel_c = st.multiselect("Pokaż kolumny:", all_c, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Cen", "Opiekun"])

    # TABELA
    f_df = df_v.copy()
    if d_sel != "Wszyscy": f_df = f_df[f_df["Dostawca"] == d_sel]
    if o_sel: f_df = f_df[f_df["Opiekun"].isin(o_sel)]

    st.dataframe(
        f_df[sel_c].style.applymap(lambda x: 'background-color: #ffcccc' if x == "TAK" else '', subset=['Cen'] if 'Cen' in sel_c else []),
        use_container_width=True, hide_index=True
    )
