import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from database.request import BaseDB, AnimeDB
from database.psycopg2_connection import ENGINE

st.set_page_config(layout="wide")

def get_db(
        Title: bool = True,
        Search: bool = False,
        title_id: str = None,
        ):
    if Title:
        select_from = "Title"
    else:
        select_from = "Episode"
    if Search:
        sql_req = f"select * from \"{select_from}\" WHERE title_id = {title_id}"
    else:
        sql_req = f"select * from \"{select_from}\""
    dbcon = ENGINE.connect()
    pd.set_option('display.expand_frame_repr', False);  
    df = pd.read_sql(sql_req, dbcon)
    return df  



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
        div[data-testid="textInputRootElement"]:nth-of-type(0)
        {
            max-width: 500px;
        }

    </style>
    """,unsafe_allow_html=True
    )
    st.subheader('Добавить тайтл', divider="rainbow")  
    url = st.text_input(label="", placeholder="url")
    remote_path = st.text_input(label="", placeholder="name folder in SFTP")
    st.button(label="Добавить", on_click=AnimeDB.add_title, args=(url, remote_path))
    st.subheader('Обновить тайтл', divider="rainbow")
    st.text_input(label="", placeholder="id")

if selected == "База данных":
    st.subheader('DataBase', divider="rainbow")
    with st.expander(label="Тайтлы"):
        with st.spinner('Загружаю БД'):
            df = get_db()
            st.dataframe(df, hide_index=True, use_container_width=True, height=500)
    with st.expander(label="Эпизоды"):
        with st.spinner('Загружаю БД'):
            df = get_db(False)
            st.dataframe(df, hide_index=True, use_container_width=False, height=500, width=600)
    with st.expander(label="Поиск"):
        search_id = st.text_input(label="id", placeholder="Тайтл id", label_visibility="hidden")
        if st.button(label="Поиск", key="search_button"):
            df = get_db(False, True, search_id)
            if df.index.size == 0:
                st.error("Тайтл не найден")
            else:
                st.success("Тайтл найден")
                st.dataframe(df, hide_index=True, use_container_width=False, height=450, width=600)

    


