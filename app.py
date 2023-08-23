import streamlit as st

from app import utils
from app import logic as lg


config = utils.load_config_file()
st.set_page_config(
    page_title=config["page title"],
    page_icon=config["favicon"],
    )


st.title(config["page title"])
lg.write_words("introduction")

st.write("")
lg.step_one()