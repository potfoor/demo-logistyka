import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
from datetime import datetime, date

# --- 1. KONFIGURACJA ---
st.set_page_config(layout="wide", page_title="System Logistyczny Pro", page_icon="🚚")

# --- 2. DANE ---
ZALOGOWANY_UZYTKOWNIK = "Jan Kowalski"
AKTUALNY_ROK = str(datetime.now().year)[-2:]

osoby_kolory = {
    "Jan Kowalski": "#333333",
    "Anna Nowak": "#8db600",
    "Piotr Zieliński": "#ff5722",
}

lista_firm = [
    "Samsung", "Toyota", "Coca-Cola", "Microsoft", "Nestlé",
    "Apple", "LG", "Sony", "Dell", "IKEA",
]

lista_uzytkownicy = list(osoby_kolory.keys()) + ["Marek Wiśniewski", "Katarzyna Dąbrowska"]

lista_przewoznicy = ["DHL", "DPD", "FedEx", "GLS", "InPost", "UPS", "Raben", "Inny"]

lista_marki_wlasne = ["Marka A", "Marka B", "Marka C", "Marka D"]

lista_statusow_ticket = [
    "Zamówione", "W trakcie", "Wstrzymany", "Pilny", "Zrealizowane",
]

lista_statusow_zakupow = [
    "Czekamy na fakturę", "Gotowy", "Opóźnienie", "W weryfikacji", "Zatwierdzony",
]

WSZYSTKIE_KOLUMNY = [
    "Lp.", "Dostawca", "Nr dostawy", "HWO", "Status", "Zakupy",
    "Cen", "Waga", "Pal", "Box", "Opiekun", "Aktualizacja",
]

raw_data = []
for i, firma in enumerate(lista_firm * 3):
    opiekun = list(osoby_kolory.keys())[i % 3]
    alert = "TAK" if (opiekun == ZALOGOWANY_UZYTKOWNIK and i % 4 == 0) else "Nie"
    raw_data.append({
        "Lp.": i + 1,
        "Dostawca": firma,
        "Nr dostawy": f"{100 + i}/26 🔗",
        "HWO": "12-03-2026",
        "Status": "Zamówione",
        "Cen": alert,
        "Waga": f"{100 + i}kg",
        "Pal": "1",
        "Box": "4",
        "Opiekun": opiekun,
        "Aktualizacja": "2026-03-14 22:45",
        "Zakupy": "OK",
    })
df = pd.DataFrame(raw_data)
alerty_uzytkownika = df[(df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK) & (df["Cen"] == "TAK")]

# Numery ticketów do symulacji pola "Ticket główny"
lista_ticketow_glownych = [
    {"numer": "45/26", "dostawca": "Samsung", "rodzaj": "Pre-order"},
    {"numer": "46/26", "dostawca": "Apple", "rodzaj": "Magazyn"},
    {"numer": "47/26", "dostawca": "Sony", "rodzaj": "Pre-order"},
    {"numer": "48/26", "dostawca": "LG", "rodzaj": "Magazyn"},
]

# --- 3. CSS ---
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
.priority-normal { color: #2196F3; font-weight: bold; }
.priority-high { color: #FF9800; font-weight: bold; }
.priority-urgent { color: #F44336; font-weight: bold; }
.inline-hint { font-size: 12px; color: #888; margin-top: -10px; margin-bottom: 10px; }
.section-header { background: #f8f9fa; padding: 8px 12px; border-radius: 6px; border-left: 4px solid #ff4b4b; margin-bottom: 12px; font-weight: 600; }
</style>
""", unsafe_allow_html=True)


# --- HELPERY ---
def generuj_numer_dostawy(dostawca: str, rok: str) -> str:
    """Generuje kolejny numer dostawy dla danego dostawcy."""
    # Symulacja: liczymy ile dostaw już ma ten dostawca
    ilosc = len([r for r in raw_data if r["Dostawca"] == dostawca])
    return f"{ilosc + 1}/{rok}"


def znajdz_nowe_eany(eany_z_dostawy: list, eany_w_cp: set) -> list:
    return [e for e in eany_z_dostawy if e not in eany_w_cp]


def init_kreator_state():
    defaults = {
        # Nawigacja
        "krok": 0,
        # Sekcja 1: Rodzaj
        "rodzaj": "Magazyn",
        "cel_zamowienia": "Bieżące",
        # Sekcja 2: Dostawca
        "dostawca": "",
        "numer_dostawy": "",
        # Sekcja 3: Informacje podstawowe
        "opiekun_dostawy": ZALOGOWANY_UZYTKOWNIK,
        "ticket_status": "Zamówione",
        # Sekcja 4: Informacje dostawy
        "priorytet": "Normalny",
        "awizacja_od": None,
        "awizacja_do": None,
        # Sekcja 5: Przesyłka
        "przewoznik": "",
        "nr_listu_przewozowego": "",
        "marki_wlasne": False,
        "status_zakupow": "",
        "odbior_osobisty": False,
        "kontener": False,
        "numer_kontenera": "",
        "ilosc_palet": 0,
        "ilosc_kartonow": 0,
        # Sekcja 6: Powiązania
        "ticket_glowny": "",
        # Sekcja 7: Uwagi
        "uwagi": "",
        # Sekcja 8: Liczba ticketów
        "liczba_ticketow": 1,
        # Krok 2
        "metoda": "Ręczna",
        "tresc_zamowienia": "",
        "eany_input": "",
        "nowe_eany_wykryte": [],
        "nowosci_w_dostawie": False,
        # Krok 3
        "awizacja_glowna": "",
        # Walidacja
        "step1_submitted": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def waliduj_krok1() -> list[str]:
    """Zwraca listę błędów walidacji kroku 1."""
    bledy = []
    if not st.session_state.get("rodzaj"):
        bledy.append("Rodzaj zamówienia jest wymagany.")
    if not st.session_state.get("cel_zamowienia"):
        bledy.append("Cel zamówienia jest wymagany.")
    if not st.session_state.get("dostawca"):
        bledy.append("Dostawca jest wymagany.")
    if not st.session_state.get("numer_dostawy"):
        bledy.append("Numer dostawy jest wymagany.")
    if not st.session_state.get("opiekun_dostawy"):
        bledy.append("Opiekun dostawy jest wymagany.")
    if not st.session_state.get("ticket_status"):
        bledy.append("Ticket Status jest wymagany.")
    if not st.session_state.get("priorytet"):
        bledy.append("Priorytet jest wymagany.")
    # Walidacja dat
    aod = st.session_state.get("awizacja_od")
    ado = st.session_state.get("awizacja_do")
    if aod and ado and ado < aod:
        bledy.append("'Awizacja do' musi być równa lub późniejsza niż 'Awizacja od'.")
    if st.session_state.get("liczba_ticketow", 1) < 1:
        bledy.append("Liczba ticketów musi wynosić co najmniej 1.")
    return bledy


# --- 5. MODAL KREATORA ---
@st.dialog("PROCES TWORZENIA NOWEGO ZAMÓWIENIA", width="large")
def modal_kreatora():
    init_kreator_state()

    sac.steps(
        items=[
            sac.StepsItem(title="Rodzaj / Dostawca / Info"),
            sac.StepsItem(title="Metoda zamówienia"),
            sac.StepsItem(title="Finalizacja"),
        ],
        index=st.session_state.krok,
        color="#ff4b4b",
    )
    st.divider()

    # ═══════════════════════════════════════════════
    # KROK 1 — pełna specyfikacja
    # ═══════════════════════════════════════════════
    if st.session_state.krok == 0:

        # ── Sekcja 1: Rodzaj zamówienia ──────────────
        st.markdown('<div class="section-header">📦 Sekcja 1: Rodzaj zamówienia</div>', unsafe_allow_html=True)
        col_r1, col_r2 = st.columns(2)
        with col_r1:
            rodzaj_opcje = ["Magazyn", "Pre-order", "Integracja"]
            idx_rodzaj = rodzaj_opcje.index(st.session_state.rodzaj) if st.session_state.rodzaj in rodzaj_opcje else 0
            st.session_state.rodzaj = st.radio(
                "Rodzaj *",
                rodzaj_opcje,
                index=idx_rodzaj,
                horizontal=True,
            )
        with col_r2:
            cel_opcje = ["Bieżące", "Zapas", "Integracja ręczna", "Special"]
            idx_cel = cel_opcje.index(st.session_state.cel_zamowienia) if st.session_state.cel_zamowienia in cel_opcje else 0
            st.session_state.cel_zamowienia = st.selectbox(
                "Cel zamówienia *",
                cel_opcje,
                index=idx_cel,
            )

        st.divider()

        # ── Sekcja 2: Dostawca ────────────────────────
        st.markdown('<div class="section-header">🏭 Sekcja 2: Dostawca</div>', unsafe_allow_html=True)
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            poprzedni_dostawca = st.session_state.dostawca
            idx_dost = lista_firm.index(st.session_state.dostawca) if st.session_state.dostawca in lista_firm else None
            wybrany_dostawca = st.selectbox(
                "Dostawca *",
                options=[""] + lista_firm,
                index=(idx_dost + 1) if idx_dost is not None else 0,
                placeholder="Wyszukaj dostawcę…",
                help="Wybierz dostawcę z listy. Po wyborze numer dostawy zostanie wygenerowany automatycznie.",
            )
            st.session_state.dostawca = wybrany_dostawca

            # Auto-uzupełnienie numeru dostawy po zmianie dostawcy
            if wybrany_dostawca and wybrany_dostawca != poprzedni_dostawca:
                st.session_state.numer_dostawy = generuj_numer_dostawy(wybrany_dostawca, AKTUALNY_ROK)

        with col_d2:
            numer_val = st.session_state.numer_dostawy
            if not numer_val and st.session_state.dostawca:
                numer_val = generuj_numer_dostawy(st.session_state.dostawca, AKTUALNY_ROK)
            st.session_state.numer_dostawy = st.text_input(
                "Numer dostawy *",
                value=numer_val,
                placeholder=f"np. 1/{AKTUALNY_ROK}",
                help=f"Format: [numer]/{AKTUALNY_ROK}. Generowany automatycznie, możliwa ręczna edycja.",
            )

        if st.session_state.rodzaj == "Pre-order" and st.session_state.numer_dostawy:
            st.info(
                f"ℹ️ Dostawy podrzędne będą numerowane: **{st.session_state.numer_dostawy} cz.1**, cz.2, cz.3…",
                icon="ℹ️",
            )

        st.divider()

        # ── Sekcja 3: Informacje podstawowe ──────────
        st.markdown('<div class="section-header">👤 Sekcja 3: Informacje podstawowe</div>', unsafe_allow_html=True)
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            # Autocomplete opiekuna (symulacja przez selectbox z wyszukiwaniem)
            idx_op = lista_uzytkownicy.index(st.session_state.opiekun_dostawy) if st.session_state.opiekun_dostawy in lista_uzytkownicy else 0
            st.session_state.opiekun_dostawy = st.selectbox(
                "Opiekun dostawy *",
                options=lista_uzytkownicy,
                index=idx_op,
                help="Domyślnie zalogowany użytkownik. Możesz zmienić na innego użytkownika systemu.",
            )
        with col_p2:
            idx_ts = lista_statusow_ticket.index(st.session_state.ticket_status) if st.session_state.ticket_status in lista_statusow_ticket else 0
            st.session_state.ticket_status = st.selectbox(
                "Ticket Status *",
                options=lista_statusow_ticket,
                index=idx_ts,
            )

        st.divider()

        # ── Sekcja 4: Informacje dostawy ─────────────
        st.markdown('<div class="section-header">📅 Sekcja 4: Informacje dostawy</div>', unsafe_allow_html=True)
        col_i1, col_i2, col_i3 = st.columns(3)
        with col_i1:
            priorytet_opcje = ["Normalny", "Wysoki", "Pilny"]
            priorytet_ikony = {"Normalny": "🔵 Normalny", "Wysoki": "🟠 Wysoki", "Pilny": "🔴 Pilny"}
            idx_pr = priorytet_opcje.index(st.session_state.priorytet) if st.session_state.priorytet in priorytet_opcje else 0
            wybr_prior = st.selectbox(
                "Priorytet *",
                options=priorytet_opcje,
                format_func=lambda x: priorytet_ikony[x],
                index=idx_pr,
            )
            st.session_state.priorytet = wybr_prior

        with col_i2:
            aod_val = st.session_state.awizacja_od
            st.session_state.awizacja_od = st.date_input(
                "Awizacja od (lub dokładna data)",
                value=aod_val,
                min_value=date.today(),
                format="DD.MM.YYYY",
                help="Dokładna data dostawy lub początek zakresu dat.",
            )

        with col_i3:
            ado_disabled = st.session_state.awizacja_od is None
            ado_min = st.session_state.awizacja_od if st.session_state.awizacja_od else date.today()
            if not ado_disabled:
                ado_val = st.session_state.awizacja_do if st.session_state.awizacja_do else None
                st.session_state.awizacja_do = st.date_input(
                    "Awizacja do",
                    value=ado_val,
                    min_value=ado_min,
                    format="DD.MM.YYYY",
                    help="Koniec zakresu dat dostawy. Zostaw puste dla dokładnej daty.",
                )
            else:
                st.date_input("Awizacja do", value=None, disabled=True)
                st.caption("⬅️ Najpierw wypełnij 'Awizacja od'")

        # Podpowiedź inline
        if st.session_state.awizacja_od:
            if st.session_state.awizacja_do:
                st.markdown(
                    f'<div class="inline-hint">📆 Zakres dat: <b>{st.session_state.awizacja_od.strftime("%d.%m.%Y")}</b> – <b>{st.session_state.awizacja_do.strftime("%d.%m.%Y")}</b></div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="inline-hint">📆 Dokładna data dostawy: <b>{st.session_state.awizacja_od.strftime("%d.%m.%Y")}</b></div>',
                    unsafe_allow_html=True,
                )
        else:
            st.markdown(
                '<div class="inline-hint">💡 Wypełnij oba pola jeśli dostawa ma zakres dat. Samo pole „od" oznacza dokładną datę.</div>',
                unsafe_allow_html=True,
            )

        st.divider()

        # ── Sekcja 5: Informacje o przesyłce ─────────
        st.markdown('<div class="section-header">🚛 Sekcja 5: Informacje o przesyłce</div>', unsafe_allow_html=True)

        col_pr1, col_pr2 = st.columns(2)
        with col_pr1:
            # Odbiór osobisty — toggle
            st.session_state.odbior_osobisty = st.toggle(
                "Odbiór osobisty",
                value=st.session_state.odbior_osobisty,
                help="Gdy włączone, pole Przewoźnik/Kurier staje się nieaktywne.",
            )
        with col_pr2:
            # Kontener — toggle + pole na numer
            st.session_state.kontener = st.toggle(
                "Kontener",
                value=st.session_state.kontener,
            )

        col_s1, col_s2 = st.columns(2)
        with col_s1:
            przewoznik_opcje = [""] + lista_przewoznicy
            idx_prz = przewoznik_opcje.index(st.session_state.przewoznik) if st.session_state.przewoznik in przewoznik_opcje else 0
            st.session_state.przewoznik = st.selectbox(
                "Przewoźnik / Kurier",
                options=przewoznik_opcje,
                index=idx_prz,
                disabled=st.session_state.odbior_osobisty,
                help="Nieaktywne gdy wybrany 'Odbiór osobisty'.",
            )
        with col_s2:
            przewoznik_wybrany = st.session_state.przewoznik and st.session_state.przewoznik != ""
            st.session_state.nr_listu_przewozowego = st.text_input(
                "Numer listu przewozowego",
                value=st.session_state.nr_listu_przewozowego,
                placeholder="Wpisz numer listu przewozowego",
                disabled=not przewoznik_wybrany or st.session_state.odbior_osobisty,
                help="Aktywne tylko gdy wybrany przewoźnik.",
            )

        if st.session_state.kontener:
            st.session_state.numer_kontenera = st.text_input(
                "Numer / opis kontenera",
                value=st.session_state.numer_kontenera,
                placeholder="Wpisz numer lub opis kontenera",
            )

        col_t1, col_t2, col_t3, col_t4 = st.columns(4)
        with col_t1:
            # Marki własne — TAK/NIE
            st.session_state.marki_wlasne = st.toggle(
                "Marki własne",
                value=st.session_state.marki_wlasne,
                help="Zaznacz jeśli dostawa zawiera marki własne.",
            )
        with col_t2:
            idx_sz = 0
            statusy_z_puste = [""] + lista_statusow_zakupow
            if st.session_state.status_zakupow in statusy_z_puste:
                idx_sz = statusy_z_puste.index(st.session_state.status_zakupow)
            st.session_state.status_zakupow = st.selectbox(
                "Status zakupów",
                options=statusy_z_puste,
                index=idx_sz,
            )
        with col_t3:
            st.session_state.ilosc_palet = st.number_input(
                "Ilość palet",
                min_value=0,
                value=st.session_state.ilosc_palet,
                step=1,
            )
        with col_t4:
            st.session_state.ilosc_kartonow = st.number_input(
                "Ilość kartonów",
                min_value=0,
                value=st.session_state.ilosc_kartonow,
                step=1,
            )

        st.divider()

        # ── Sekcja 6: Powiązania ──────────────────────
        st.markdown('<div class="section-header">🔗 Sekcja 6: Powiązania</div>', unsafe_allow_html=True)

        opcje_ticketow = [""] + [f"{t['numer']} — {t['dostawca']} ({t['rodzaj']})" for t in lista_ticketow_glownych]
        idx_tg = 0
        if st.session_state.ticket_glowny in opcje_ticketow:
            idx_tg = opcje_ticketow.index(st.session_state.ticket_glowny)

        st.session_state.ticket_glowny = st.selectbox(
            "Ticket główny (opcjonalnie)",
            options=opcje_ticketow,
            index=idx_tg,
            placeholder="Wyszukaj ticket główny…",
            help="Zostaw puste jeśli ticket jest samodzielny.",
        )

        if st.session_state.ticket_glowny:
            # Wyciągnij numer ticketu
            numer_tg = st.session_state.ticket_glowny.split(" — ")[0]
            rodzaj_tg = next((t["rodzaj"] for t in lista_ticketow_glownych if t["numer"] == numer_tg), "")
            st.info(
                f"ℹ️ Ten ticket zostanie powiązany jako dostawa podrzędna do **{numer_tg}**"
                + (f"  \n⚡ Ticket główny jest Pre-orderem — numeracja zostanie nadana automatycznie (cz.N)." if rodzaj_tg == "Pre-order" else ""),
            )

        st.divider()

        # ── Sekcja 7: Uwagi ───────────────────────────
        st.markdown('<div class="section-header">📝 Sekcja 7: Informacje dodatkowe</div>', unsafe_allow_html=True)
        uwagi_val = st.session_state.uwagi
        nowe_uwagi = st.text_area(
            "Uwagi",
            value=uwagi_val,
            height=100,
            placeholder="Opcjonalne uwagi do zamówienia…",
            help="Pole opcjonalne.",
        )
        st.session_state.uwagi = nowe_uwagi
        st.markdown(
            f'<div style="text-align:right; font-size:11px; color:#888; margin-top:-10px;">{len(nowe_uwagi)} znaków</div>',
            unsafe_allow_html=True,
        )

        st.divider()

        # ── Sekcja 8: Liczba ticketów ─────────────────
        st.markdown('<div class="section-header">🔢 Sekcja 8: Liczba ticketów</div>', unsafe_allow_html=True)
        st.session_state.liczba_ticketow = st.number_input(
            "Ile ticketów utworzyć naraz?",
            min_value=1,
            max_value=20,
            value=st.session_state.liczba_ticketow,
            help="Możesz jednocześnie założyć kilka identycznych ticketów dla tego samego dostawcy. Każdy ticket otrzyma odrębny numer.",
        )
        if st.session_state.liczba_ticketow > 1:
            st.warning(
                f"⚠️ Zostanie utworzonych **{st.session_state.liczba_ticketow}** ticketów. "
                f"Numery zostaną nadane kolejno.",
            )

        # Walidacja inline
        if st.session_state.step1_submitted:
            bledy = waliduj_krok1()
            if bledy:
                for b in bledy:
                    st.error(f"❌ {b}")

    # ═══════════════════════════════════════════════
    # KROK 2
    # ═══════════════════════════════════════════════
    elif st.session_state.krok == 1:
        st.subheader("Metoda zamówienia")
        metody = ["Ręczna", "Formatka", "Automatyczna"]
        st.session_state.metoda = sac.segmented(
            items=[sac.SegmentedItem(label=m) for m in metody],
            value=st.session_state.metoda,
            color="#ff4b4b",
            align="center",
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
            eany_w_cp_set: set = set()  # placeholder — podłączyć z bazą CP
            nowe = znajdz_nowe_eany(eany_lista, eany_w_cp_set)
            st.session_state.nowe_eany_wykryte = nowe
            if nowe:
                st.session_state.nowosci_w_dostawie = True
                st.success(f"Wykryto **{len(nowe)}** nowych EANów — automatycznie zaznaczono 'Nowości w dostawie: TAK'.")
                st.dataframe({"Nowe EANy (nie ma w CP)": nowe}, use_container_width=True)
            else:
                st.session_state.nowosci_w_dostawie = False
                st.info("Brak nowych EANów — wszystkie już istnieją w CP.")

    # ═══════════════════════════════════════════════
    # KROK 3
    # ═══════════════════════════════════════════════
    elif st.session_state.krok == 2:
        st.subheader("📋 Podsumowanie zamówienia")
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Rodzaj:** {st.session_state.rodzaj}")
            st.write(f"**Cel zamówienia:** {st.session_state.cel_zamowienia}")
            st.write(f"**Dostawca:** {st.session_state.dostawca}")
            st.write(f"**Numer dostawy:** {st.session_state.numer_dostawy}")
            st.write(f"**Ticket Status:** {st.session_state.ticket_status}")
            st.write(f"**Priorytet:** {st.session_state.priorytet}")
        with col2:
            st.write(f"**Metoda zamówienia:** {st.session_state.metoda}")
            st.write(f"**Opiekun dostawy:** {st.session_state.opiekun_dostawy}")
            st.write(f"**Liczba ticketów:** {st.session_state.liczba_ticketow}")
            if st.session_state.awizacja_od:
                aod_str = st.session_state.awizacja_od.strftime("%d.%m.%Y")
                ado_str = st.session_state.awizacja_do.strftime("%d.%m.%Y") if st.session_state.awizacja_do else "—"
                st.write(f"**Awizacja:** {aod_str}" + (f" – {ado_str}" if st.session_state.awizacja_do else " (dokładna data)"))
            if st.session_state.przewoznik:
                st.write(f"**Przewoźnik:** {st.session_state.przewoznik}")
            if st.session_state.nr_listu_przewozowego:
                st.write(f"**Nr listu przewozowego:** {st.session_state.nr_listu_przewozowego}")
            if st.session_state.ilosc_palet > 0:
                st.write(f"**Ilość palet:** {st.session_state.ilosc_palet}")
            if st.session_state.ilosc_kartonow > 0:
                st.write(f"**Ilość kartonów:** {st.session_state.ilosc_kartonow}")

        if st.session_state.ticket_glowny:
            st.info(f"🔗 Powiązano z ticketem głównym: **{st.session_state.ticket_glowny.split(' — ')[0]}**")
        if st.session_state.odbior_osobisty:
            st.info("🚶 Odbiór osobisty")
        if st.session_state.kontener:
            st.info(f"📦 Kontener: {st.session_state.numer_kontenera or 'TAK'}")
        if st.session_state.marki_wlasne:
            st.info("🏷️ Marki własne: TAK")
        if st.session_state.status_zakupow:
            st.write(f"**Status zakupów:** {st.session_state.status_zakupow}")
        if st.session_state.uwagi:
            st.write(f"**Uwagi:** {st.session_state.uwagi}")
        if st.session_state.nowe_eany_wykryte:
            st.info(
                f"🆕 Nowości w dostawie: **TAK** ({len(st.session_state.nowe_eany_wykryte)} nowych EANów)",
            )

        st.divider()
        st.subheader("📦 Awizacja (finalna)")
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
                f"+ pozostałość jako **{st.session_state.numer_dostawy} cz.2**.",
            )

        st.divider()
        st.success("✅ Zamówienie gotowe do dodania!")
        st.write("**Status po dodaniu:** W drodze (Awizacja)")

    # ═══════════════════════════════════════════════
    # NAWIGACJA
    # ═══════════════════════════════════════════════
    st.divider()
    c_nav1, c_nav2 = st.columns(2)
    with c_nav1:
        if st.session_state.krok > 0:
            if st.button("⬅️ Wróć", key="back_modal"):
                st.session_state.krok -= 1
                st.rerun()
    with c_nav2:
        if st.session_state.krok < 2:
            if st.button("Dalej ➡️", type="primary", key="next_modal"):
                if st.session_state.krok == 0:
                    st.session_state.step1_submitted = True
                    bledy = waliduj_krok1()
                    if bledy:
                        st.rerun()
                    else:
                        st.session_state.krok += 1
                        st.rerun()
                else:
                    st.session_state.krok += 1
                    st.rerun()
        else:
            if st.button("✅ Zakończ i Dodaj", type="primary", key="finish_modal"):
                st.session_state.krok = 0
                st.session_state.step1_submitted = False
                st.rerun()


# --- 6. PANEL BOCZNY ---
with st.sidebar:
    st.title("🚚 Logistyka App")
    st.write(f"Zalogowany: **{ZALOGOWANY_UZYTKOWNIK}**")
    st.divider()
    menu = sac.tree(
        items=[
            sac.TreeItem("Dashboard", icon="speedometer2"),
            sac.TreeItem("Zakupy", icon="box", children=[
                sac.TreeItem("Powiadomienia", icon="bell",
                             tag=sac.Tag(str(len(alerty_uzytkownika)), color="red")),
                sac.TreeItem("Zamówienia", icon="ticket-perforated", children=[
                    sac.TreeItem("Moje Dostawy", icon="person-check"),
                    sac.TreeItem("Wszystkie Dostawy", icon="globe"),
                    sac.TreeItem("Sekcja Odpraw", icon="globe"),
                    sac.TreeItem("Sekcja Niezgodności", icon="globe"),
                ]),
                sac.TreeItem("Awizacja", icon="calendar-event", children=[
                    sac.TreeItem("Moje Awizacje", icon="person-check"),
                    sac.TreeItem("Sekcja Przyjęcia", icon="globe"),
                    sac.TreeItem("Kalendarz", icon="calendar3"),
                ]),
                sac.TreeItem("Raporty", icon="file", children=[
                    sac.TreeItem("Raporty Zakupy", icon="shopping-cart"),
                    sac.TreeItem("Raporty Magazyn", icon="package"),
                    sac.TreeItem("Raporty Awizacja", icon="barcode"),
                ]),
            ]),
        ],
        label="NAWIGACJA",
        open_all=True,
        size="sm",
    )

# --- 7. WIDOKI ---
if menu == "Powiadomienia":
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
    if menu in ["Moje Dostawy", "Moje Awizacje"]:
        df_v = df[df["Opiekun"] == ZALOGOWANY_UZYTKOWNIK]

    st.write("**Aktywni Dostawcy:**")
    t_html = '<div class="tag-container">'
    for d_name in df_v["Dostawca"].unique():
        t_html += f'<span class="tag" style="background-color: {osoby_kolory.get(ZALOGOWANY_UZYTKOWNIK, "#333")};">{d_name}</span>'
    st.markdown(t_html + "</div>", unsafe_allow_html=True)

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
            default_ops = [] if menu == "Wszystkie Dostawy" else [ZALOGOWANY_UZYTKOWNIK]
            o_sel = st.multiselect("Odpowiedzialny:", list(osoby_kolory.keys()), default=default_ops)

        st.columns(4)[0].text_input("Ticket:", placeholder="Nr...")

        st.divider()
        st.write("**Akcje Szybkie:**")
        sa1, sa2, sa3, sa4, sa5, _ = st.columns([1.2, 1.2, 1.2, 1.2, 1.4, 4])
        with sa1:
            if st.button("✨ Nowa dostawa", type="primary", use_container_width=True):
                modal_kreatora()
        with sa2:
            st.button("➕ Dodaj Dostawcę", use_container_width=True)
        with sa3:
            st.button("🚛 Dodaj Przewoźnika", use_container_width=True)
        with sa4:
            st.button("🔄 Zamówienia Cykliczne", use_container_width=True)
        with sa5:
            st.button("🔄 Szablon Urlop", use_container_width=True)

    st.write("---")
    st.subheader("📊 Zarządzanie Tabelą")
    with st.container(border=True):
        cm1, cm2 = st.columns([3, 1])
        with cm1:
            def_cols = WSZYSTKIE_KOLUMNY if menu == "Wszystkie Dostawy" else ["Lp.", "Dostawca", "Nr dostawy", "Status", "Cen", "Opiekun"]
            selected_cols = st.multiselect("Pokaż kolumny:", WSZYSTKIE_KOLUMNY, default=def_cols)
        with cm2:
            st.selectbox("Widok:", ["Standardowy", "Pełny"])

    f_df = df_v.copy()
    if d_sel != "Wszyscy":
        f_df = f_df[f_df["Dostawca"] == d_sel]
    if o_sel:
        f_df = f_df[f_df["Opiekun"].isin(o_sel)]

    st.dataframe(
        f_df[selected_cols].style.applymap(
            lambda x: "background-color: #ffcccc" if x == "TAK" else "",
            subset=["Cen"] if "Cen" in selected_cols else [],
        ),
        use_container_width=True,
        hide_index=True,
    )
