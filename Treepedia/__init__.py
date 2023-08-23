from . import _create_directories, _create_points


class Treepedia(_create_directories.Mixin, 
                _create_points.Mixin):

    def __init__(self, shapefile_directory):
        self.create_directories(shapefile_directory)