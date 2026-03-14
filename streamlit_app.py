# 6. TABELA DANYCH "MOJE DOSTAWY"
st.subheader(f"MOJE DOSTAWY - Widok: {menu_selection}")

# Przykładowe dane
df_data = pd.DataFrame([
    {"Lp.": 1, "Dostawca": "ASG", "Nr dostawy": "14/23", "Status": "BR", "Zakupy": "Brak danych", "Kolor": "#f8d7da"},
    {"Lp.": 2, "Dostawca": "BARREL OPTICS", "Nr dostawy": "1/24-sampl", "Status": "Zamówiono", "Zakupy": "Brak danych", "Kolor": "#ffffff"},
    {"Lp.": 3, "Dostawca": "WYDAWNICTWO X", "Nr dostawy": "7/24", "Status": "SKŁAD", "Zakupy": "W przygotowaniu", "Kolor": "#d4edda"},
    {"Lp.": 4, "Dostawca": "Darek", "Nr dostawy": "1/24", "Status": "Zrealizowane", "Zakupy": "Brak danych", "Kolor": "#ffffff"},
    {"Lp.": 5, "Dostawca": "ZIRI", "Nr dostawy": "4/24", "Status": "SKŁAD", "Zakupy": "Gotowy", "Kolor": "#d4edda"},
])

# POPRAWIONA FUNKCJA STYLIZUJĄCA
def style_row(row):
    # Pobieramy kolor z kolumny 'Kolor' dla każdego wiersza
    color = row['Kolor']
    # Nakładamy ten kolor na wszystkie komórki w tym wierszu
    return [f'background-color: {color}' for _ in row]

# STYLIZUJEMY CAŁY DATAFRAME, A POTEM UKRYWAMY KOLUMNĘ 'Kolor'
styled_df = df_data.style.apply(style_row, axis=1)

# Wyświetlanie z ukryciem kolumny technicznej
st.dataframe(
    styled_df,
    column_config={
        "Kolor": None  # To sprawi, że kolumna 'Kolor' będzie niewidoczna dla użytkownika
    },
    use_container_width=True,
    hide_index=True
)
