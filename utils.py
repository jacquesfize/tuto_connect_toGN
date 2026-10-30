import geopandas as gpd


def geojson_to_gdf(geojson_data: dict = {}):
    gdf = gpd.GeoDataFrame.from_features(geojson_data)
    gdf["longitude"] = gdf.centroid.x
    gdf["latitude"] = gdf.centroid.y
    return gdf
