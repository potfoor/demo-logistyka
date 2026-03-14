import streamlit as st
import streamlit_antd_components as sac

with st.sidebar:
    st.title("Panel Sterowania")
    
    # Tworzymy drzewko
    selected_item = sac.tree(
        items=[
            sac.TreeItem('ZAMÓWIENIA', icon='box', children=[
                sac.TreeItem('Powiadomienia', icon='bell', children=[
                    sac.TreeItem('Wszystkie'),
                    sac.TreeItem('Aktywne'),
                    sac.TreeItem('Archiwum'),
                ]),
                sac.TreeItem('Ticket', icon='ticket', children=[
                    sac.TreeItem('Dodaj produkt'),
                    sac.TreeItem('Zestawy'),
                ]),
                sac.TreeItem('Awizacja', icon='calendar-event', children=[
                    sac.TreeItem('Ceny produktów'),
                    sac.TreeItem('Rodzaje cen'),
                ]),
            ]),
            sac.TreeItem('IMPORT DANYCH', icon='download', children=[
                sac.TreeItem('Excel'),
                sac.TreeItem('Kolejka'),
            ]),
        ],
        label='Menu nawigacyjne',
        index=0,
        open_all=False, # Zmienna na True, jeśli chcesz, by drzewko było od razu rozwinięte
        size='sm',
    )

# Wyświetlanie informacji o wybranym elemencie (dla testu)
st.write(f"Wybrano: **{selected_item}**")
