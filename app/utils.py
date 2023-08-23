import yaml
from yaml.loader import SafeLoader

import streamlit as st

from .directories import APP_DIR


def load_config_file():
    filepath = APP_DIR / "text.yaml"
    config = load_yaml_file(filepath)
    return config


def load_yaml_file(filepath):
    with open(filepath) as file:
        obj = yaml.load(file, Loader=SafeLoader)
    return obj


def save_yaml_file(obj, filepath):
    with open(filepath, 'w') as file:
        yaml.dump(obj, file, default_flow_style=False)


def create_session_state_objects_if_they_dont_exist(objects):
    for key, value in objects.items():
        if key not in st.session_state:
            st.session_state[key] = value