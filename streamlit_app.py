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
    alert = "TAK" if (opiekun == ZALOGOWANY_UZYTKOWNIK and i % 4 == 0) else "Nie"
    raw_data.append({
        "Lp.": i + 1, "Dostawca": firma, "Nr dostawy": f"{100+i}/26 🔗",
        "HWO": "12-03-2026", "Status": "Zamówione", "Cen": alert,
        "Waga": f"{100+i}kg", "Pal": "1", "Box": "4", "Opiekun": opiekun,
        "Aktualizacja": "2026-03-14 22:45", "Zakupy": "OK"
    })
df = pd.DataFrame(raw_data)
alerty_uzytkownika = df[(df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK) & (df["Cen"] == "TAK")]

# --- 4. CSS ---
st.markdown("""
    <style>
    .tag-container { display: flex; flex-wrap: wrap; gap: 4px; padding-bottom: 20px; }
    .tag { padding: 3px 8px; border-radius: 3px; font-size: 10px; color: white; font-weight: bold; text-transform: uppercase; }
    .stButton > button { width: 100%; height: 38px; border-radius: 4px; }
    div[data-testid="column"] button[kind="primary"] { background-color: #ff4b4b !important; color: white !important; }
    div[data-testid="stPopover"] > button { margin-top: 28px; height: 38px; width: 100%; border: 1px solid #d1d5db; background-color: #f8f9fa; }
    [data-testid="stPopoverContent"] { width: 600px !important; }
    .alert-card { padding: 20px; background-color: #fff5f5; border-left: 6px solid #ff4b4b; border-radius: 8px; margin-bottom: 15px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    [data-testid="stHorizontalBlock"] { gap: 10px !important; }
    [data-testid="stDataFrame"] { font-size: 11px; }
    </style>
""", unsafe_allow_html=True)

# --- HELPERY ---
def generuj_numer_dostawy_podrzednej(numer_glowny: str, lista_istniejacych: list) -> str:
    czesci = [t for t in lista_istniejacych if t.startswith(numer_glowny)]
    return f"{numer_glowny} cz.{len(czesci) + 1}"

def znajdz_nowe_eany(eany_z_dostawy: list, eany_w_cp: set) -> list:
    return [e for e in eany_z_dostawy if e not in eany_w_cp]

def init_kreator_state():
    defaults = {
        "step": 0,
        "rodzaj": "Magazyn",
        "cel": "Zapas",
        "dostawca": "",
        "numer_zamowienia": "",
        "status": "Oczekuje",
        "odpowiedzialny": "",
        "uwagi": "",
        "metoda": "Ręczna",
        "tresc_zamowienia": "",
        "liczba_ticketow": 1,
        "awizacja_glowna": "",
        "eany_input": "",
        "nowe_eany_wykryte": [],
        "nowosci_w_dostawie": False,
        "szukaj_tytul": "",
        "szukaj_tresc": "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

# --- 5. MODAL KREATORA (3 KROKI) ---
@st.dialog("PROCES TWORZENIA NOWEGO ZAMÓWIENIA", width="large")
def modal_kreatora():
    init_kreator_state()

    sac.steps(
        items=[
            sac.StepsItem(title='Rodzaj / Dostawca / Info'),
            sac.StepsItem(title='Metoda zamówienia'),
            sac.StepsItem(title='Finalizacja'),
        ],
        index=st.session_state.step,
        color='#ff4b4b',
    )
    st.divider()

    # KROK 1
    if st.session_state.step == 0:
        col_l, col_r = st.columns(2)

        with col_l:
            st.subheader("Rodzaj zamówienia")
            rodzaj_opcje = ["Magazyn", "Pre-order", ]
            st.session_state.rodzaj = st.radio(
                "Rodzaj:",
                rodzaj_opcje,
                horizontal=True,
                index=rodzaj_opcje.index(st.session_state.rodzaj),
            )
            opcje_celu = ["Bieżące", "Zapas", "Integracja", "Special (?)"]
            if st.session_state.rodzaj == "Magazyn":
                idx_cel = opcje_celu.index(st.session_state.cel) if st.session_state.cel in opcje_celu else 0
                st.session_state.cel = st.selectbox("Cel zamówienia:", opcje_celu, index=idx_cel)

        with col_r:
            st.subheader("Dostawca")
            idx_firma = lista_firm.index(st.session_state.dostawca) if st.session_state.dostawca in lista_firm else 0
            st.session_state.dostawca = st.selectbox("Dostawca:", lista_firm, index=idx_firma)
            st.session_state.numer_zamowienia = st.text_input(
                "Numer zamówienia:",
                value=st.session_state.numer_zamowienia or f"1/{st.session_state.current_year}",
            )
            if st.session_state.rodzaj == "Pre-order":
                st.info(
                    f"Dostawy podrzędne będą numerowane automatycznie: "
                    f"**{st.session_state.numer_zamowienia} cz.1**, cz.2 itd.",
                    icon="ℹ️",
                )

        st.divider()
        st.subheader("Informacje dodatkowe")
        col_s, col_o = st.columns(2)
        with col_s:
            st.session_state.status = st.selectbox(
                "Status:",
                ["Oczekuje", "W trakcie"],
                index=["Oczekuje", "W trakcie"].index(st.session_state.status),
            )
        with col_o:
            st.session_state.odpowiedzialny = st.text_input(
                "Odpowiedzialny:",
                value=st.session_state.odpowiedzialny or ZALOGOWANY_UZYTKOWNIK,
            )
        st.session_state.uwagi = st.text_area("Uwagi:", value=st.session_state.uwagi)

        st.divider()
        st.subheader("Liczba ticketów")
        st.session_state.liczba_ticketow = st.number_input(
            "Ile ticketów utworzyć naraz?",
            min_value=1, max_value=20,
            value=st.session_state.liczba_ticketow,
            help="Pozwala jednorazowo dodać wiele ticketów.",
        )
        if st.session_state.liczba_ticketow > 1:
            st.warning(
                f"Zostanie utworzonych **{st.session_state.liczba_ticketow}** ticketów "
                f"z automatyczną numeracją (cz.1 \u2026 cz.{st.session_state.liczba_ticketow}).",
                icon="⚠️",
            )

    # KROK 2
    elif st.session_state.step == 1:
        st.subheader("Metoda zamówienia")
        metody = ['Ręczna', 'Formatka', 'Automatyczna']
        st.session_state.metoda = sac.segmented(
            items=[sac.SegmentedItem(label=m) for m in metody],
            value=st.session_state.metoda,
            color='#ff4b4b',
            align='center',
        )
        st.divider()
        if st.session_state.metoda == "Ręczna":
            st.session_state.tresc_zamowienia = st.text_area(
                "Wklej treść zamówienia:",
                value=st.session_state.tresc_zamowienia,
                height=200,
            )
        elif st.session_state.metoda == "Formatka":
            st.info("Uzupełnij formularz formatki poniżej.")
            st.session_state.tresc_zamowienia = st.text_area(
                "Treść wg formatki:",
                value=st.session_state.tresc_zamowienia,
                height=200,
            )
        elif st.session_state.metoda == "Automatyczna":
            st.info("System wygeneruje zamówienie automatycznie na podstawie stanów magazynowych.")

        st.divider()
        st.subheader("🔍 Automatyczna wyszukiwarka nowości (EAN)")
        st.caption(
            "Wklej listę EANów z dostawy (po jednym w linii lub rozdzielone przecinkami). "
            "System oznaczy te, których nie ma w CP jako nowości w dostawie."
        )
        st.session_state.eany_input = st.text_area(
            "EANy z dostawy:", value=st.session_state.eany_input, height=100
        )
        if st.button("🔎 Sprawdź nowości", key="check_eans"):
            raw = st.session_state.eany_input.replace(",", "\n")
            eany_lista = [e.strip() for e in raw.splitlines() if e.strip()]
            eany_w_cp_set: set = set()  # <- placeholder: podłączyć z bazą CP
            nowe = znajdz_nowe_eany(eany_lista, eany_w_cp_set)
            st.session_state.nowe_eany_wykryte = nowe
            if nowe:
                st.session_state.nowosci_w_dostawie = True
                st.success(f"Wykryto **{len(nowe)}** nowych EANow \u2014 automatycznie zaznaczono 'Nowosci w dostawie: TAK'.")
                st.dataframe({"Nowe EANy (nie ma w CP)": nowe}, use_container_width=True)
            else:
                st.session_state.nowosci_w_dostawie = False
                st.info("Brak nowych EANów \u2014 wszystkie już istnieją w CP.")

    # KROK 3
    elif st.session_state.step == 2:
        st.subheader("📋 Podsumowanie zamówienia")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Rodzaj:** {st.session_state.rodzaj}")
            if st.session_state.rodzaj == "Magazyn":
                st.write(f"**Cel:** {st.session_state.cel}")
            st.write(f"**Dostawca:** {st.session_state.dostawca}")
            st.write(f"**Numer zamówienia:** {st.session_state.numer_zamowienia}")
        with col2:
            st.write(f"**Metoda:** {st.session_state.metoda}")
            st.write(f"**Status:** {st.session_state.status}")
            st.write(f"**Odpowiedzialny:** {st.session_state.odpowiedzialny}")
            st.write(f"**Liczba ticketów:** {st.session_state.liczba_ticketow}")
        if st.session_state.uwagi:
            st.write(f"**Uwagi:** {st.session_state.uwagi}")
        if st.session_state.nowe_eany_wykryte:
            st.info(
                f"Nowości w dostawie: **TAK** ({len(st.session_state.nowe_eany_wykryte)} nowych EANów)",
                icon="🆕",
            )

        st.divider()
        st.subheader("📦 Awizacja")
        st.session_state.awizacja_glowna = st.text_input(
            "Data/termin awizacji (główny ticket):",
            value=st.session_state.awizacja_glowna,
            help="Awizacja zostanie automatycznie skopiowana do ticketów podrzędnych.",
        )
        if st.session_state.liczba_ticketow > 1 or st.session_state.rodzaj == "Pre-order":
            st.caption("⚡ Awizacja zostanie automatycznie propagowana do wszystkich powiązanych ticketów podrzędnych.")

        st.divider()
        st.subheader("✂️ Częściowa realizacja (opcjonalnie)")
        rozdziel = st.checkbox(
            "Rozdziel ticket przy częściowej realizacji",
            help="Tworzy dodatkowy ticket podrzędny dla niezrealizowanej części zamówienia.",
        )
        if rozdziel:
            ilosc_czesciowa = st.number_input("Ile pozycji zostaje zrealizowanych?", min_value=1, value=1)
            st.info(
                f"Ticket zostanie rozdzielony: zrealizowana część ({ilosc_czesciowa} szt.) "
                f"+ pozostałość jako **{st.session_state.numer_zamowienia} cz.2**.",
                icon="✂️",
            )

        st.divider()
        st.success("✅ Zamówienie gotowe do dodania!")
        st.write("**Status po dodaniu:** W drodze (Awizacja)")

    # NAWIGACJA
    st.divider()
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.session_state.step > 0:
            if st.button("⬅️ Wróć", key="back_modal"):
                st.session_state.step -= 1
                st.rerun()
    with c_nav2:
        if st.session_state.step < 2:
            if st.button("Dalej ➡️", type="primary", key="next_modal"):
                st.session_state.step += 1
                st.rerun()
        else:
            if st.button("✅ Zakończ i Dodaj", type="primary", key="finish_modal"):
                st.session_state.step = 0
                st.rerun()


# --- WYSZUKIWARKA ---
def panel_wyszukiwarki(lista_ticketow: list) -> list:
    st.subheader("🔍 Wyszukiwarka ticketów")
    col_a, col_b = st.columns(2)
    with col_a:
        szukaj_tytul = st.text_input("Szukaj po tytule / numerze:", key="szukaj_tytul")
    with col_b:
        szukaj_tresc = st.text_input(
            "Szukaj po treści ticketu / załączniku:",
            key="szukaj_tresc",
            help="Przeszukuje treść zamówienia oraz tekst wyodrębnionych załączników.",
        )
    wyniki = lista_ticketow
    if szukaj_tytul:
        q = szukaj_tytul.lower()
        wyniki = [t for t in wyniki if q in t.get("tytul", "").lower()]
    if szukaj_tresc:
        q = szukaj_tresc.lower()
        wyniki = [
            t for t in wyniki
            if q in t.get("tresc", "").lower()
            or q in t.get("zalacznik_tekst", "").lower()
        ]
    return wyniki

# --- 6. PANEL BOCZNY ---
with st.sidebar:
    st.title("🚚 Logistyka App")
    st.write(f"Zalogowany: **{ZALOGOWANY_UZYTKOWNIK}**")
    st.divider()
    menu = sac.tree(items=[
        sac.TreeItem('Dashboard', icon='speedometer2'),
        sac.TreeItem('Zakupy', icon='box', children=[
            sac.TreeItem('Powiadomienia', icon='bell', tag=sac.Tag(str(len(alerty_uzytkownika)), color='red')),
            sac.TreeItem('Zamówienia', icon='ticket-perforated', children=[
                sac.TreeItem('Moje Dostawy', icon='person-check'),
                sac.TreeItem('Wszystkie Dostawy', icon='globe'),
                sac.TreeItem('Sekcja Odpraw', icon='globe'),
                sac.TreeItem('Sekcja Niezgodności', icon='globe'),
            ]),
            sac.TreeItem('Awizacja', icon='calendar-event', children=[
                sac.TreeItem('Moje Awizacje', icon='person-check'),
                sac.TreeItem('Sekcja Przyjęcia', icon='globe'),
                sac.TreeItem('Kalendarz', icon='calendar3'),
            ]),
            sac.TreeItem('Raporty', icon='file', children=[
                sac.TreeItem('Raporty Zakupy', icon='shopping-cart'),
                sac.TreeItem('Raporty Magazyn', icon='package'),
                sac.TreeItem('Raporty Awizacja', icon='barcode'),
            ]),
        ]),
    ], label='NAWIGACJA', open_all=True, size='sm')

# --- 7. WIDOKI ---
if menu == 'Powiadomienia':
    st.header(f"🔔 Alerty i Powiadomienia ({len(alerty_uzytkownika)})")
    if len(alerty_uzytkownika) > 0:
        for _, r in alerty_uzytkownika.iterrows():
            st.markdown(f"""
            <div class="alert-card">
                <span style="color: #ff4b4b; font-weight: bold;">⚠️ KONTROLA CENY</span> | Dostawca: <b>{r['Dostawca']}</b><br>
                Nr dostawy: {r['Nr dostawy']} | Opiekun: {r['Opiekun']}<br>
                <small>Zaktualizowano: {r['Aktualizacja']}</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Brak aktywnych powiadomień.")

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
    with st.container(border=True):
        c1, c2, c3 = st.columns([3, 1, 3])
        with c1:
            d_sel = st.selectbox("Dostawca:", ["Wszyscy"] + list(df_v["Dostawca"].unique()))
        with c2:
            with st.popover("📇 KARTA"):
                if d_sel != "Wszyscy":
                    st.subheader(f"Karta Dostawcy: {d_sel}")
                    st.divider()
                    col_k1, col_k2 = st.columns(2)
                    with col_k1:
                        st.write("**🔐 Dane B2B**")
                        st.text_input("URL Serwisu:", f"https://b2b.{d_sel.lower()}.pl")
                        st.text_input("Login:", "jan.kowalski")
                        st.text_input("Hasło:", "********", type="password")
                    with col_k2:
                        st.write("**👤 Kontakt**")
                        st.text_input("Opiekun (Firma):", "Aneta Nowak")
                        st.text_input("Tel:", "+48 123 456 789")
                        st.text_input("Email Price List:", "ceny@dostawca.pl")
                    st.divider()
                    st.write("**📋 Warunki i Logistyka**")
                    col_k3, col_k4 = st.columns(2)
                    col_k3.selectbox("Dzień dostawy:", ["Poniedziałek", "Wtorek", "Środa", "Czwartek", "Piątek"])
                    col_k4.text_input("Minimum logistyczne:", "1500 PLN")
                    st.text_area("Notatki operacyjne:", "Zawsze dzwonić przed awizacją.")
                    if st.button("💾 Zapisz zmiany w karcie"):
                        st.success("Zapisano dane kontrahenta!")
                else:
                    st.warning("Wybierz dostawcę z listy obok, aby zobaczyć jego kartę.")
        with c3:
            default_ops = [] if menu == 'Wszystkie Dostawy' else [ZALOGOWANY_UZYTKOWNIK]
            o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=default_ops)

        st.columns(4)[0].text_input("Ticket:", placeholder="Nr...")

        st.divider()
        st.write("**Akcje Szybkie:**")
        sa1, sa2, sa3, sa4, sa5, _ = st.columns([1.2, 1.2, 1.2, 1.2, 1.4, 4])
        with sa1:
            if st.button("✨ Nowa dostawa", type="primary", use_container_width=True):
                modal_kreatora()
        with sa2: st.button("➕ Dodaj Dostawcę", use_container_width=True)
        with sa3: st.button("🚛 Dodaj Przewoźnika", use_container_width=True)
        with sa4: st.button("🔄 Zamówienia Cykliczne", use_container_width=True)
        with sa5: st.button("🔄 Szablon Urlop", use_container_width=True)

    st.write("---")
    st.subheader("📊 Zarządzanie Tabelą")
    with st.container(border=True):
        cm1, cm2 = st.columns([3, 1])
        with cm1:
            def_cols = WSZYSTKIE_KOLUMNY if menu == 'Wszystkie Dostawy' else ["Lp.", "Dostawca", "Nr dostawy", "Status", "Cen", "Opiekun"]
            selected_cols = st.multiselect("Pokaż kolumny:", WSZYSTKIE_KOLUMNY, default=def_cols)
        with cm2:
            st.selectbox("Widok:", ["Standardowy", "Pełny"])

    f_df = df_v.copy()
    if d_sel != "Wszyscy": f_df = f_df[f_df["Dostawca"] == d_sel]
    if o_sel: f_df = f_df[f_df["Opiekun"].isin(o_sel)]

    st.dataframe(
        f_df[selected_cols].style.applymap(
            lambda x: 'background-color: #ffcccc' if x == "TAK" else '',
            subset=['Cen'] if 'Cen' in selected_cols else []
        ),
        use_container_width=True, hide_index=True
    )
