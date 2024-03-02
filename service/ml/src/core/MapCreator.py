import fiona, pyproj, rasterio
from shapely.geometry import shape, Polygon, mapping
from typing import Any, List, Tuple, Dict, Union
from rtree import index


def process_detection_results(
    path_to_land_map: str,
    track_results: Any,
    names: List[str],
    transform: rasterio.transform.Affine,
    coordinates: str,
    start: int = 1,
) -> Union[List[Dict], List[None]]:
    buildings = []

    idx = index.Index()
    with fiona.open(path_to_land_map, "r") as parcels:
        for i, parcel in enumerate(parcels):
            idx.insert(i, shape(parcel["geometry"]).bounds)

        parcels_crs = pyproj.CRS.from_string(parcels.crs_wkt)
        buildings_crs = pyproj.CRS.from_string(coordinates)

        transformer = (
            pyproj.Transformer.from_crs(buildings_crs, parcels_crs, always_xy=True)
            if buildings_crs != parcels_crs
            else None
        )

        for r in track_results:
            for id, box in enumerate(r.boxes, start=start):
                b = box.xyxy[0]
                building_polygon = Polygon(
                    (
                        transform * (b[0], b[1]),
                        transform * (b[0], b[3]),
                        transform * (b[2], b[3]),
                        transform * (b[2], b[1]),
                        transform * (b[0], b[1]),
                    )
                )
                building_shape = shape(building_polygon)

                # Преобразование координат, если CRS различаются
                if transformer:
                    building_shape = Polygon(
                        transformer.transform(x, y)
                        for x, y in building_shape.exterior.coords
                    )

                max_intersection_area = 0
                max_intersection_cadastral = "Not found"
                for j in idx.intersection(building_shape.bounds):
                    parcel = parcels[j]
                    parcel_shape = shape(parcel["geometry"])

                    intersection = building_shape.intersection(parcel_shape)
                    if intersection.is_empty:
                        continue

                    intersection_area = intersection.area
                    if intersection_area > max_intersection_area:
                        max_intersection_area = intersection_area
                        max_intersection_cadastral = parcel["properties"]["cadastral_"]

                buildings.append(
                    {
                        "geometry": mapping(building_polygon),
                        "properties": {
                            "id": id,
                            "Name": names[int(box.cls)],
                            "cadastral_": max_intersection_cadastral,
                        },
                    }
                )

    return buildings


def read_geospatial_metadata_from_tif(
    path_to_tif: str,
) -> Tuple[rasterio.transform.Affine, str]:
    with rasterio.open(path_to_tif) as src:
        transform = src.transform
        coordinates = src.crs.to_proj4()

    return transform, coordinates


def create_buildings_shapefile(
    buildings: Union[List[Dict], List[None]],
    buildings_shapefile_path: str,
) -> None:
    with fiona.open(
        buildings_shapefile_path,
        "w",
        driver="ESRI Shapefile",
        schema={
            "geometry": "Polygon",
            "properties": [("id", "int"), ("Name", "str"), ("cadastral_", "str")],
        },
    ) as output:
        output.writerecords(buildings)
