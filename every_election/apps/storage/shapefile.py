from django.contrib.gis.gdal.error import GDALException
from django.contrib.gis.geos import Polygon, MultiPolygon


def _remove_invalid_geometries(in_features):
    out_features = []
    for feature in in_features:
        try:
            feature.geom
            out_features.append(feature)
        except GDALException:
            pass
    return out_features


def _add_multipolygons(features):
    # 'enrich' feature objects with a handy .multipolygon property
    for feature in features:
        if isinstance(feature.geom.geos, Polygon):
            feature.multipolygon = MultiPolygon(feature.geom.geos)
        else:
           feature.multipolygon = feature.geom.geos
    return features


def _convert_multipolygons_to_latlong(features, srid):
    # ensure our .multipolygon property uses srid 4326
    for feature in features:
        if not feature.multipolygon.srid:
            feature.multipolygon.set_srid(srid)
        feature.multipolygon.transform(4326)
    return features


def pre_process_layer(layer, srid):
    """
    First convert our layer object to a list of feature objects
    Doing this means we lose some meta-data from the layer object,
    but a list of feature objects is easier to manipulate than a
    django.contrib.gis.gdal.layer.Layer (which is basically an
    abstraction over some C pointers).
    Given we mostly just want to iterate over the features,
    this is an OK compromise.
    """
    features = [f for f in layer]

    # then tidy it up
    features = _remove_invalid_geometries(features)
    features = _add_multipolygons(features)
    features = _convert_multipolygons_to_latlong(features, srid)
    return features
