import streamlit as st
import osmnx as ox

from . import utils
from . import street_network


def write_words(section_key):
    config = utils.load_config_file()
    for paragraph in config[section_key]:
        st.write(paragraph)


def step_one():
    section_key = "step one"
    st.markdown("### 1: Download the Street Network")

    gdf = street_network.load_community_area_boundaries()
    slctn = select_a_community_area(gdf)
    graph_path, shapefile_dir = street_network.download_shapefile(gdf, slctn)
    plot_street_network(graph_path)
    return shapefile_dir

    
def select_a_community_area(gdf):
    label = "Select an Official Community Area"
    community_names = gdf["community"].values.tolist()
    options = sorted(community_names)
    slctn = st.selectbox(label, options)
    return slctn


def plot_street_network(graph_path):
    graph = utils.load_pickle_file(graph_path)
    fig, ax = ox.plot_graph(graph)
    # st.caption(f"Street Network")
    st.pyplot(fig)