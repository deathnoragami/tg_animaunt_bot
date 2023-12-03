import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from database.request import BaseDB, AnimeDB
from database.psycopg2_connection import ENGINE

st.set_page_config(layout="wide")

def get_db():
    dbcon = ENGINE.connect()
    df = pd.read_sql("select * from \"Title\"", dbcon)
    pd.set_option('display.expand_frame_repr', False);    

    data = st.dataframe(df, use_container_width=True)
    return data


with st.sidebar:
    selected = option_menu(None, ["API запросы", "База данных"], 
    icons=["house", "database"], menu_icon="cast", default_index=0, orientation="vertical")

if selected == "API запросы":
    st.markdown(
    """
    <style>
        div[data-testid="stButton"]:nth-of-type(1)
        {
            text-align: end;
        } 
    </style>
    """,unsafe_allow_html=True
    )
    st.subheader('Добавить тайтл', divider="rainbow")  
    url = st.text_input(label="", placeholder="url")
    remote_path = st.text_input(label="", placeholder="name folder in SFTP")
    st.button(label="Добавить", on_click=AnimeDB.add_title, args=(url, remote_path))
    st.subheader('Обновить тайтл', divider="rainbow")

if selected == "База данных":
    st.subheader('Тайтлы', divider="rainbow")
    get_db()


