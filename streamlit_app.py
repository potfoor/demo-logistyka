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

# 3. ROZBUDOWANA BAZA DANYCH (Więcej dostaw dla Jana)
lista_firm = [
    "Samsung", "Toyota", "Coca-Cola", "Microsoft", "Nestlé", "Apple", "LG", "Sony", 
    "Dell", "IKEA", "Nike", "Adidas", "BMW", "Amazon", "DHL", "FedEx", "Pepsi", "Canon"
]

raw_data = []
for i, firma in enumerate(lista_firm):
    # Przypisujemy Jana Kowalskiego do większości dostaw (np. pierwsze 10 i co druga potem)
    if i < 10 or i % 2 == 0:
        opiekun = "Jan Kowalski"
    else:
        opiekun = list(osoby_kolory.keys())[i % 4]
        
    # Generujemy alerty cenowe dla Jana (np. 8 pozycji z alertem)
    ma_alert = "TAK" if opiekun == "Jan Kowalski" and i in [0, 2, 4, 5, 7, 8, 12, 14] else "Nie"
    
    raw_data.append({
        "Lp.": i + 1, "Dostawca": firma, "Nr dostawy": f"{100+i}/26 🔗",
        "HWO": "12-03-2026", "Data aw. OD": "14-03-2026", "Status": "Zamówione",
        "Zakupy": "OK", "Cen": ma_alert, "Waga": f"{100+i*5}kg", "Pal": "2", "Box": "5",
        "Opiekun": opiekun, "Aktualizacja": "2026-03-14 10:00"
    })

df = pd.DataFrame(raw_data)
alerty_jana = df[(df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK) & (df["Cen"] == "TAK")]
liczba_alertow = len(alerty_jana)

# 4. CSS
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; }
    div[data-testid="column"] button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    .alert-box { padding: 15px; background-color: #fff5f5; border-left: 5px solid #ff4b4b; border-radius: 5px; margin-bottom: 10px; }
    [data-testid="stDataFrame"] { font-size: 11px; }
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
    st.subheader(f"Alerty dla: {ZALOGOWANY_UZYTKOWNIK}")
    
    if not alerty_jana.empty:
        for _, row in alerty_jana.iterrows():
            st.markdown(f"""
                <div class="alert-box">
                    <strong style="color: #ff4b4b;">⚠️ ALERT CENOWY</strong><br>
                    Dostawca: <b>{row['Dostawca']}</b> | Nr dostawy: <b>{row['Nr dostawy']}</b><br>
                    <small>Wykryto zmianę ceny w systemie B2B. Wymagana weryfikacja zamówienia.</small>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.success("Brak nowych powiadomień.")

else:
    # --- WIDOK DLA MOJE / WSZYSTKIE DOSTAWY ---
    
    # Filtrowanie bazowe dla tagów
    df_display = df.copy()
    if menu_selected == 'Moje Dostawy':
        df_display = df[df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK]

    # Tagi na górze
    st.write(f"**Aktywni Dostawcy:**")
    tags_html = '<div class="tag-container">'
    for _, d in df_display.drop_duplicates('Dostawca').iterrows():
        kolor = osoby_kolory.get(d["Opiekun"], "#cccccc")
        tags_html += f'<span class="tag" style="background-color: {kolor};">{d["Dostawca"]}</span>'
    tags_html += '</div>'
    st.markdown(tags_html, unsafe_allow_html=True)

    # 6. PANEL WYSZUKIWANIA (Tylko tutaj!)
    st.header("🔍 Wyszukiwanie")
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 3])
        with c1:
            d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + list(df_display["Dostawca"].unique()))
        with c2:
            with st.popover("📇 KARTA"):
                st.write("**Dane B2B i Kontakt**")
                st.text_input("URL:", "https://b2b.portal.pl")
                st.text_input("Login:", "jan.k")
        with c3:
            o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), 
                                   default=[ZALOGOWANY_UZYTKOWNIK] if menu_selected == 'Moje Dostawy' else [])

        c4, c5, c6, c7 = st.columns([3, 3, 2, 2])
        with c4: st.text_input("Ticket:", placeholder="Nr ticketu...")
        with c5: st.multiselect("Flaga:", ["PILNE", "POWTÓRKA"])
        with c6:
            st.write("**Statusy:**")
            st.checkbox("Otwarte", value=True); st.checkbox("Zamknięte")
        with c7:
            st.write("**Akcje:**")
            st.button("🚀 ZASTOSUJ FILTRY", type="primary")

        st.write("---")
        st.write("**Akcje Szybkie:**")
        b1, b2, b3 = st.columns(3)
        b1.button("➕ Dodaj Dostawcę"); b2.button("🚛 Dodaj Przewoźnika"); b3.button("🔄 Zamówienia Cykliczne")

    # 7. TABELA
    st.write("---")
    st.subheader(f"📊 Tabela: {menu_selected}")
    
    # Finalne filtrowanie tabeli
    final_df = df_display.copy()
    if d_sel != "Wszyscy":
        final_df = final_df[final_df["Dostawca"] == d_sel]
    if o_sel:
        final_df = final_df[final_df["Opiekun"].isin(o_sel)]

    # Kolorowanie Cen
    def style_cen(val):
        return 'background-color: #ffcccc' if val == "TAK" else ''

    st.dataframe(
        final_df.style.applymap(style_cen, subset=['Cen']),
        use_container_width=True,
        hide_index=True,
        column_config={"Lp.": st.column_config.Column(width=40)}
    )
