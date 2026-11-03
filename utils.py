import geopandas as gpd


def geojson_to_gdf(geojson_data: dict = {}):
    gdf = gpd.GeoDataFrame.from_features(geojson_data)
    gdf["longitude"] = gdf.centroid.x
    gdf["latitude"] = gdf.centroid.y
    return gdf


def geojson_to_gdf_wkt(geojson_data: dict = {}):
    """Keeps the full geometry (points, lines, polygons) and adds it as WKT text."""
    return gpd.GeoDataFrame.from_features(geojson_data, crs="EPSG:4326")
