import osmnx as ox
import geopandas as gpd

from directories import DATA_DIR, SPATIAL_DATA


def load_community_area_boundaries():
    """
    Load and clean the community area boundaries geojson file provided by
    the city of Chicago.
    """
    filepath = DATA_DIR / "Boundaries - Community Areas (current).geojson"
    gdf = gpd.read_file(filepath)

    # Data Types
    non_numeric_columns = ["community", "geometry"]
    float_columns = ["shape_area", "shape_len"]
    columns_to_drop = ["area_num_1"]
    for col in gdf.columns:
        if col not in non_numeric_columns:
            # All columns loaded as strings
            if col in float_columns:
                gdf[col] = gdf[col].astype(float)
            else:
                gdf[col] = gdf[col].astype(int)

            # Many columns are all Zero
            if all(gdf[col] == 0):
                columns_to_drop.append(col)

    gdf.drop(columns=columns_to_drop, inplace=True)

    # Renames & Index
    gdf.rename(columns={"area_numbe": "area_number"}, inplace=True)
    gdf.set_index("area_number", inplace=True)
    gdf.sort_index(inplace=True)

    return gdf


def download_street_network_for_a_community_area(area_number=1):
    """
    Use OSMNX to download the drivable street network within a single community
    area.
    """
    gdf = load_community_area_boundaries()
    multipolygon = gdf.loc[area_number].geometry
    graph = ox.graph_from_polygon(multipolygon, network_type="drive")

    # Spatial files must be the expected coordinate system that will align
    # with google street view images
    assert(graph.graph["crs"] == "epsg:4326")

    # Save to shapefile (what treepedia accepts as input)
    drctry = SPATIAL_DATA / f"community_area_{area_number}"
    drctry.mkdir(parents=True, exist_ok=True)
    ox.save_graph_shapefile(graph, drctry)

    return graph



if __name__ == "__main__":
    # load_community_area_boundaries()
    download_street_network_for_a_community_area()