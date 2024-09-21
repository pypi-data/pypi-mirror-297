"""
Parse GPS data to GeoJSON Features
"""
import geojson


class GeoJSONParser(object):
    """
    Create a GeoJSONParser object.
    
    """

    def __init__(self):
        self._collections_dict = {}

    def __iter__(self):
        """Return an iterator for `_collections_dict` items."""
        return iter(self._collections_dict.items())

    def add_feature(self, collection_title, lat, long, properties={}, collection_parent = None):
        """
        Add a `Feature' to `_collections_dict`.

        Parameters
        ----------
        collection_title : str
            The `FeatureCollection` title.
        lat : float
            The latitude of the 'Feature'.
        long : float
            The longitude of the 'Feature'.
        properties : dict
            The 'Feature' properties.
        collection_parent : str
            The `FeatureCollection` parent.
        """
        point = geojson.Point((long, lat))
        feature = geojson.Feature(
            geometry=point, 
            properties=properties
        )
        if collection_title not in self._collections_dict:
            feature_collection = geojson.FeatureCollection(
                title = collection_title,
                features = [feature]
            )
            if collection_parent: 
                feature_collection['properties'] = { 'parent': collection_parent }

            self._collections_dict[collection_title] = feature_collection
        else:
            self._collections_dict[collection_title]['features'].append(feature)
