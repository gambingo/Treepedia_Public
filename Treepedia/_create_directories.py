from pathlib import Path


class Mixin:
    def create_directories(self, shapefile_dir):
        """
        Create all the other directories needed for this process in the same 
        parent folder as the shapefile directory
        """
        if isinstance(shapefile_dir, str):
            shapefile_dir = Path(shapefile_dir)

        self.shapefile_dir = shapefile_dir
        self.point_grids_dir = shapefile_dir.parent / "point-grids"
        self.panoramas_dir = shapefile_dir.parent / "panorama-data"
        self.gvi_dir = shapefile_dir.parent / "greenview-index"

        self.point_grids_dir.mkdir(parents=True, exist_ok=True)
        self.panoramas_dir.mkdir(parents=True, exist_ok=True)
        self.gvi_dir.mkdir(parents=True, exist_ok=True)