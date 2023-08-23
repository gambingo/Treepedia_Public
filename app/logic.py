import streamlit as st
import osmnx as ox
import geopandas as gpd
import matplotlib.pyplot as plt

from . import utils
from . import street_network

from treepedia import Treepedia



def write_words(section_key):
    config = utils.load_config_file()
    for paragraph in config[section_key]:
        st.write(paragraph)


def download_street_network():
    st.write("")
    st.markdown("### Download the Street Network")

    gdf = street_network.load_community_area_boundaries()
    slctn = select_a_community_area(gdf)
    graph_path, shapefile_dir = street_network.download_shapefile(gdf, slctn)
    graph = plot_street_network(graph_path)
    return shapefile_dir, graph

    
def select_a_community_area(gdf):
    label = "Select an Official Community Area"
    community_names = gdf["community"].values.tolist()
    options = sorted(community_names)
    default = options.index("Oakland")
    slctn = st.selectbox(label, options, index=default)
    return slctn


def plot_street_network(graph_path):
    graph = utils.load_pickle_file(graph_path)
    fig, ax = ox.plot_graph(graph, node_size=0)
    ax.set_title("Street Network from Open Street Maps")
    st.pyplot(fig)
    return graph


def sample_points(shapefile_dir, graph):
    st.write("")
    st.markdown("### Sample Points Along the Network")

    label = "Minimum Sampling Distance"
    mini_dist = st.slider(label, value=20,
                          min_value=5, max_value=50,
                          format="%d meters")

    trees = Treepedia(shapefile_dir)
    points_dir = trees.create_points(mini_dist=mini_dist, recalculate=True)
    gdf = gpd.read_file(points_dir / "point-grids.shp")
    fig, ax = ox.plot_graph(graph, node_size=0)
    ax = gdf.plot(ax=ax, markersize=3)
    st.pyplot(fig)