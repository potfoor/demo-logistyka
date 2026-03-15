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

# Budowa bazy danych
raw_data = []
for i, firma in enumerate(lista_firm * 3):
    opiekun = "Jan Kowalski" if (i < 15 or i % 2 == 0) else "Anna Nowak"
    alert = "TAK" if opiekun == "Jan Kowalski" and i in [1, 4, 7, 10, 14] else "Nie"
    raw_data.append({
        "Lp.": i + 1, "Dostawca": firma, "Nr dostawy": f"{100+i}/26 🔗",
        "HWO": "12-03-2026", "Status": "Zamówione", "Cen": alert, 
        "Waga": f"{100+i}kg", "Pal": "1", "Box": "4", "Opiekun": opiekun,
        "Aktualizacja": "2026-03-14 22:45", "Zakupy": "OK"
    })
df = pd.DataFrame(raw_data)
alerty_jana = df[(df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK) & (df["Cen"] == "TAK")]

# --- 4. CSS (Rozszerzona karta i odstępy) ---
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; }
    div[data-testid="column"] button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    
    /* POWIĘKSZONY POPOVER KARTY */
    div[data-testid="stPopover"] > button { margin-top: 28px; height: 38px; width: 100%; border: 1px solid #d1d5db; background-color: #f8f9fa; }
    [data-testid="stPopoverContent"] { width: 450px !important; } /* Szerokość karty */
    
    .alert-box { padding: 15px; background-color: #fff5f5; border-left: 5px solid #ff4b4b; border-radius: 5px; margin-bottom: 10px; }
    [data-testid="stDataFrame"] { font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# --- 5. MODAL KREATORA (NAPRAWIONY) ---
@st.dialog("PROCES TWORZENIA NOWEGO ZAMÓWIENIA", width="large")
def modal_kreatora():
    # Używamy sac.steps, a nie st.steps
    sac.steps(items=[
        sac.StepsItem(title='Rodzaj'), sac.StepsItem(title='Dostawca'),
        sac.StepsItem(title='Metoda'), sac.StepsItem(title='Info'), sac.StepsItem(title='Finalizacja')
    ], index=st.session_state.step, color='#ff4b4b')
    
    st.divider()
    
    if st.session_state.step == 0:
        r = st.radio("Rodzaj:", ["Magazyn", "Pre-order"], horizontal=True)
        if r == "Magazyn": 
            st.selectbox("Cel:", ["Zapas", "Bieżące"])
            
    elif st.session_state.step == 1:
        st.selectbox("Dostawca:", lista_firm)
        # Numer zamówienia z możliwością edycji
        st.text_input("Numer zamówienia:", f"1/{st.session_state.current_year}")
        
    elif st.session_state.step == 2:
        # TUTAJ BYŁ BŁĄD: Musi być sac.segmented zamiast st.segmented
        sac.segmented(
            items=[
                sac.SegmentedItem(label='Ręczna'),
                sac.SegmentedItem(label='Formatka'),
                sac.SegmentedItem(label='Automatyczna'),
            ], color='#ff4b4b', align='center'
        )
        st.text_area("Wklej treść zamówienia lub listę pozycji:")
        
    elif st.session_state.step == 3:
        col_s1, col_s2 = st.columns(2)
        col_s1.selectbox("Status:", ["Oczekuje", "W trakcie kompletowania"])
        col_s2.text_input("Osoba odpowiedzialna:", value=ZALOGOWANY_UZYTKOWNIK)
        st.text_area("Uwagi ogólne do ticketu:")
        
    elif st.session_state.step == 4:
        st.success("Wszystkie dane zostały uzupełnione!")
        st.markdown("### Podsumowanie:")
        st.write("- Status: **W drodze**")
        st.write("- Powiadomienie: **Wysłane do dostawcy**")
        st.checkbox("Potwierdzam poprawność danych", value=True)

    st.divider()
    
    # Nawigacja - przyciski na dole pop-upa
    c_nav1, c_nav2 = st.columns([1, 1])
    with c_nav1:
        if st.session_state.step > 0:
            # Używamy st.button z unikalnym key, żeby uniknąć konfliktów
            if st.button("⬅️ Wróć", key="btn_prev"): 
                st.session_state.step -= 1
                st.rerun() # Odświeża modal, by pokazać poprzedni krok
                
    with c_nav2:
        if st.session_state.step < 4:
            if st.button("Dalej ➡️", type="primary", key="btn_next"):
                st.session_state.step += 1
                st.rerun() # Odświeża modal, by pokazać kolejny krok
        else:
            if st.button("✅ Zakończ i Dodaj", type="primary", key="btn_finish"):
                # Resetujemy proces dla następnego razu
                st.session_state.step = 0
                st.toast("Zamówienie zostało pomyślnie utworzone!")
                # Tutaj nie robimy rerun, aby zamknąć dialog po zakończeniu

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
            sac.TreeItem('Awizacja', icon='ticket-perforated', children=[
                sac.TreeItem('Moje Dostawy', icon='person-check'),
                sac.TreeItem('Kalendarz', icon='globe'),
            ]),
        ]),
    ], label='NAWIGACJA', open_all=True, size='sm')

# --- 7. WIDOKI ---
if menu == 'Powiadomienia':
    st.header("🔔 Powiadomienia")
    for _, r in alerty_jana.iterrows():
        st.markdown(f'<div class="alert-box"><b>⚠️ ALERT CENOWY: {r["Dostawca"]}</b><br>Weryfikacja ceny wymagana dla dostawy {r["Nr dostawy"]}.</div>', unsafe_allow_html=True)
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

    # WYSZUKIWANIE + ROZBUDOWANA KARTA
    st.header("🔍 Wyszukiwanie")
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 3])
        with c1: d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + list(df_v["Dostawca"].unique()))
        with c2:
            with st.popover("📇 KARTA"):
                if d_sel != "Wszyscy":
                    st.subheader(f"Karta Kontrahenta: {d_sel}")
                    st.divider()
                    st.write("**🔐 Dane Logowania B2B**")
                    st.text_input("URL Serwisu:", f"https://portal-b2b.{d_sel.lower()}.com")
                    ck1, ck2 = st.columns(2)
                    ck1.text_input("Login:", "jan.logistyka")
                    ck2.text_input("Hasło:", "********", type="password")
                    
                    st.divider()
                    st.write("**👤 Kontakt i Cenniki**")
                    st.text_input("Osoba kontaktowa:", "Marek Nowak")
                    st.text_input("Email Price List:", "ceny@dostawca.pl")
                    
                    st.divider()
                    st.write("**⚙️ Konfiguracja**")
                    st.multiselect("Metody zamówień:", ["B2B", "Email", "EDI", "API"], default=["B2B", "Email"])
                    st.checkbox("Automatyczne potwierdzenia")
                    
                    if st.button("💾 Zastosuj zmiany w karcie"): st.success("Dane karty zapisane.")
                else: 
                    st.warning("Wybierz dostawcę, aby edytować kartę.")
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

    # ZARZĄDZANIE TABELĄ (PRZYWRÓCONE)
    st.write("---")
    st.subheader("📊 Zarządzanie Tabelą")
    with st.container(border=True):
        cm1, cm2 = st.columns([3, 1])
        with cm1:
            all_cols = ["Lp.", "Dostawca", "Nr dostawy", "HWO", "Status", "Zakupy", "Cen", "Waga", "Pal", "Box", "Opiekun", "Aktualizacja"]
            selected_cols = st.multiselect("Widoczne kolumny:", all_cols, default=["Lp.", "Dostawca", "Nr dostawy", "Status", "Cen", "Waga", "Opiekun"])
        with cm2:
            st.selectbox("Szablon widoku:", ["Standardowy", "Księgowy", "Logistyczny"])

    # TABELA
    f_df = df_v.copy()
    if d_sel != "Wszyscy": f_df = f_df[f_df["Dostawca"] == d_sel]
    if o_sel: f_df = f_df[f_df["Opiekun"].isin(o_sel)]

    st.dataframe(
        f_df[selected_cols].style.applymap(lambda x: 'background-color: #ffcccc' if x == "TAK" else '', subset=['Cen'] if 'Cen' in selected_cols else []),
        use_container_width=True, hide_index=True
    )
