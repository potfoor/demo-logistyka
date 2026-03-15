import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
from datetime import datetime

# --- 1. KONFIGURACJA ---
st.set_page_config(layout="wide", page_title="System Logistyczny Pro", page_icon="🚚")

# --- 2. STAN SESJI ---
if 'step' not in st.session_state: st.session_state.step = 0
if 'current_year' not in st.session_state: st.session_state.current_year = 26

# --- 3. DANE ---
osoby_kolory = {"Jan Kowalski": "#333333", "Anna Nowak": "#8db600", "Piotr Zieliński": "#ff5722"}
ZALOGOWANY_UZYTKOWNIK = "Jan Kowalski"
lista_firm = ["Samsung", "Toyota", "Coca-Cola", "Microsoft", "Nestlé", "Apple", "LG", "Sony", "Dell", "IKEA"]
WSZYSTKIE_KOLUMNY = ["Lp.", "Dostawca", "Nr dostawy", "HWO", "Status", "Zakupy", "Cen", "Waga", "Pal", "Box", "Opiekun", "Aktualizacja"]

raw_data = []
for i, firma in enumerate(lista_firm * 3):
    opiekun = list(osoby_kolory.keys())[i % 3]
    alert = "TAK" if i in [1, 4, 10] else "Nie"
    raw_data.append({
        "Lp.": i + 1, "Dostawca": firma, "Nr dostawy": f"{100+i}/26 🔗",
        "HWO": "12-03-2026", "Status": "Zamówione", "Cen": alert, 
        "Waga": f"{100+i}kg", "Pal": "1", "Box": "4", "Opiekun": opiekun,
        "Aktualizacja": "2026-03-14 22:45", "Zakupy": "OK"
    })
df = pd.DataFrame(raw_data)
alerty_jana = df[(df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK) & (df["Cen"] == "TAK")]

# --- 4. CSS (Zagęszczenie przycisków i Karta) ---
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; }
    div[data-testid="column"] button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    
    /* Popover i Karta */
    div[data-testid="stPopover"] > button { margin-top: 28px; height: 38px; width: 100%; border: 1px solid #d1d5db; background-color: #f8f9fa; }
    [data-testid="stPopoverContent"] { width: 500px !important; } 
    
    /* Zagęszczenie kolumn dla przycisków */
    [data-testid="stHorizontalBlock"] { gap: 10px !important; }
    
    .alert-box { padding: 15px; background-color: #fff5f5; border-left: 5px solid #ff4b4b; border-radius: 5px; margin-bottom: 10px; }
    [data-testid="stDataFrame"] { font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. MODAL KREATORA ---
@st.dialog("PROCES TWORZENIA NOWEGO ZAMÓWIENIA", width="large")
def modal_kreatora():
    sac.steps(items=[sac.StepsItem(title='Rodzaj'), sac.StepsItem(title='Dostawca'), sac.StepsItem(title='Metoda'), sac.StepsItem(title='Info'), sac.StepsItem(title='Finalizacja')], index=st.session_state.step, color='#ff4b4b')
    st.divider()
    if st.session_state.step == 0:
        r = st.radio("Rodzaj:", ["Magazyn", "Pre-order"], horizontal=True)
        if r == "Magazyn": st.selectbox("Cel:", ["Zapas", "Bieżące"])
    elif st.session_state.step == 1:
        st.selectbox("Dostawca:", lista_firm)
        st.text_input("Numer zamówienia:", f"1/{st.session_state.current_year}")
    elif st.session_state.step == 2:
        sac.segmented(items=[sac.SegmentedItem(label='Ręczna'), sac.SegmentedItem(label='Formatka'), sac.SegmentedItem(label='Automatyczna')], color='#ff4b4b', align='center')
        st.text_area("Wklej treść zamówienia:")
    elif st.session_state.step == 3:
        c1, c2 = st.columns(2); c1.selectbox("Status:", ["Oczekuje", "W trakcie"]); c2.text_input("Odpowiedzialny:", value=ZALOGOWANY_UZYTKOWNIK); st.text_area("Uwagi:")
    elif st.session_state.step == 4:
        st.success("Gotowe!"); st.write("Status: **W drodze**")
    st.divider()
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.session_state.step > 0:
            if st.button("⬅️ Wróć", key="back_modal"): st.session_state.step -= 1; st.rerun()
    with c_nav2:
        if st.session_state.step < 4:
            if st.button("Dalej ➡️", type="primary", key="next_modal"): st.session_state.step += 1; st.rerun()
        else:
            if st.button("✅ Zakończ i Dodaj", type="primary", key="finish_modal"): st.session_state.step = 0; st.rerun()

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
            sac.TreeItem('Awizacja', icon='calendar-event', children=[
                sac.TreeItem('Moje Awizacje', icon='person-check'),
                sac.TreeItem('Kalendarz', icon='calendar3'),
            ]),
        ]),
    ], label='NAWIGACJA', open_all=True, size='sm')

# --- 7. WIDOKI ---
if menu == 'Powiadomienia':
    st.header("🔔 Powiadomienia")
    for _, r in alerty_jana.iterrows():
        st.markdown(f'<div class="alert-box"><b>⚠️ ALERT CENOWY: {r["Dostawca"]}</b><br>Weryfikacja ceny dla {r["Nr dostawy"]}.</div>', unsafe_allow_html=True)
else:
    df_v = df.copy()
    if menu in ['Moje Dostawy', 'Moje Awizacje']: 
        df_v = df[df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK]

    st.write("**Aktywni Dostawcy:**")
    t_html = '<div class="tag-container">'
    for d_name in df_v["Dostawca"].unique():
        t_html += f'<span class="tag" style="background-color: {osoby_kolory.get(ZALOGOWANY_UZYTKOWNIK, "#333")};">{d_name}</span>'
    st.markdown(t_html + '</div>', unsafe_allow_html=True)

    st.header("🔍 Wyszukiwanie")
    # GŁÓWNY KONTENER FILTRÓW
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 3])
        with c1: 
            d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + list(df_v["Dostawca"].unique()))
        with c2:
            with st.popover("📇 KARTA"):
                if d_sel != "Wszyscy":
                    st.subheader(f"Karta: {d_sel}")
                    st.text_input("URL Serwisu:", f"https://portal-b2b.{d_sel.lower()}.com")
                    ck1, ck2 = st.columns(2); ck1.text_input("Login:", "jan.logistyka"); ck2.text_input("Hasło:", "****", type="password")
                    st.text_input("Osoba kontaktowa:", "Marek Nowak"); st.text_input("Email Price List:", "ceny@dostawca.pl")
                    if st.button("💾 Zapisz"): st.success("Zapisano")
                else: st.warning("Wybierz dostawcę")
        with c3:
            default_ops = [] if menu == 'Wszystkie Dostawy' else [ZALOGOWANY_UZYTKOWNIK]
            o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=default_ops)

        st.columns(4)[0].text_input("Ticket:", placeholder="Nr...")
        
        st.divider()
        st.write("**Akcje Szybkie:**")
        # PRZYCISKI BLISKO SIEBIE (Małe wagi kolumn + brak pustych separatorów)
        sa1, sa2, sa3, sa4, sa_spacer = st.columns([1.2, 1.2, 1.2, 1.4, 4])
        with sa1:
            if st.button("✨ Nowa dostawa", type="primary", use_container_width=True): modal_kreatora()
        with sa2: st.button("➕ Dodaj Dostawcę", use_container_width=True)
        with sa3: st.button("🚛 Dodaj Przewoźnika", use_container_width=True)
        with sa4: st.button("🔄 Zamówienia Cykliczne", use_container_width=True)

    # ZARZĄDZANIE TABELĄ (Poza kontenerem wyszukiwania dla przejrzystości)
    st.write("---")
    st.subheader("📊 Zarządzanie Tabelą")
    with st.container(border=True):
        cm1, cm2 = st.columns([3, 1])
        with cm1:
            def_cols = WSZYSTKIE_KOLUMNY if menu == 'Wszystkie Dostawy' else ["Lp.", "Dostawca", "Nr dostawy", "Status", "Cen", "Opiekun"]
            selected_cols = st.multiselect("Pokaż kolumny:", WSZYSTKIE_KOLUMNY, default=def_cols)
        with cm2: 
            st.selectbox("Widok:", ["Standardowy", "Pełny"])

    # FINALNE FILTROWANIE I WYŚWIETLANIE
    f_df = df_v.copy()
    if d_sel != "Wszyscy": f_df = f_df[f_df["Dostawca"] == d_sel]
    if o_sel: f_df = f_df[f_df["Opiekun"].isin(o_sel)]

    st.dataframe(
        f_df[selected_cols].style.applymap(lambda x: 'background-color: #ffcccc' if x == "TAK" else '', subset=['Cen'] if 'Cen' in selected_cols else []),
        use_container_width=True, hide_index=True
    )
