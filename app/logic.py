import streamlit as st

from . import utils


def write_words(section_key):
    config = utils.load_config_file()
    for paragraph in config[section_key]:
        st.write(paragraph)


def step_one():
    section_key = "step one"
    st.header(section_key.title())