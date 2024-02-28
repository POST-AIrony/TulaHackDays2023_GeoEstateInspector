import fiona
import pyproj
from shapely.geometry import Point, shape, Polygon, mapping
import rasterio


# Определение схемы для нового Shapefile
schema_parcel = {
    "geometry": "Polygon",
    "properties": [("id", "int"), ("Name", "str"), ("cadastral_", "str")],
}

schema_shp = {"geometry": "Polygon", "properties": [("id", "int"), ("Name", "str")]}


def match_buildings_to_parcels(
    buildings_shapefile_path, output_shapefile_path, path_to_land_map
):
    print(
        "Тут лог о том что мы ищем здания на фотке и кадастровый номер им притягиваем"
    )

    # Открытие файлов Shapefile для зданий и земельных участков
    parcels = fiona.open(path_to_land_map, "r")
    buildings = fiona.open(buildings_shapefile_path, "r")
    report = []

    # Получение CRS для земельных участков
    buildings_crs = pyproj.CRS.from_string(buildings.crs_wkt)
    parcels_crs = pyproj.CRS.from_string(parcels.crs_wkt)

    # Проверка наличия несоответствия CRS и создание трансформатора
    if buildings_crs != parcels_crs:
        transformer = pyproj.Transformer.from_crs(
            buildings_crs, parcels_crs, always_xy=True
        )
    else:
        transformer = None

    with fiona.open(
        output_shapefile_path,
        "w",
        driver="ESRI Shapefile",
        schema=schema_parcel,
        crs=buildings.crs,
    ) as output:
        for building in buildings:
            building_polygon = shape(building["geometry"])
            building_center = building_polygon.centroid

            # Преобразование координат, если CRS различаются
            if buildings_crs != parcels_crs:
                lon, lat = transformer.transform(building_center.x, building_center.y)
                building_center = Point(lon, lat)
            found = False

            # Поиск соответствующего земельного участка
            for i, parcel in enumerate(parcels.values()):
                parcel_polygon = shape(parcel["geometry"])
                if building_center.within(parcel_polygon):
                    found = True
                    cadastral = parcel["properties"]["cadastral_"]
                    report.append(
                        {
                            "building_id": building["properties"]["id"],
                            "building_type": building["properties"]["Name"],
                            "building_position": (lon, lat),
                            "parcel_id": i,
                            "cadastral_": parcel["properties"]["cadastral_"],
                        }
                    )

            # Обработка случая, если земельный участок не найден
            if not found:
                cadastral = "Not found"
                report.append(
                    {
                        "building_id": building["properties"]["id"],
                        "building_type": building["properties"]["Name"],
                        "building_position": (lon, lat),
                        "parcel_id": "Not found",
                        "cadastral_": "Not found",
                    }
                )

            # Обновление информации о здании в новом Shapefile
            updated_building = {
                "geometry": building["geometry"],
                "properties": {
                    "id": building["properties"]["id"],
                    "Name": building["properties"]["Name"],
                    "cadastral_": cadastral,
                },
            }
            output.write(updated_building)

    buildings.close()
    parcels.close()

    return report


def create_detection_shapefile(
    output_shapefile_path,
    track_results,
    names,
    transform,
    coordinates,
):
    features = []
    with fiona.open(
        output_shapefile_path,
        mode="w",
        driver="ESRI Shapefile",
        schema=schema_shp,
        crs=coordinates,
    ) as shp:

        # Обработка результатов детекции
        for r in track_results:
            for id, box in enumerate(r.boxes, start=1):
                b = box.xyxy[0]
                box_geo = [
                    transform * (b[0], b[1]),
                    transform * (b[0], b[3]),
                    transform * (b[2], b[3]),
                    transform * (b[2], b[1]),
                    transform * (b[0], b[1]),
                ]

                polygon = Polygon(box_geo)

                row_dict = {
                    "geometry": mapping(polygon),
                    "properties": {"id": id, "Name": names[int(box.cls)]},
                }
                features.append(row_dict)
        shp.writerecords(features)


def read_geospatial_metadata_from_tif(path_to_tif):
    with rasterio.open(path_to_tif) as src:
        transform = src.transform
        coordinates = src.crs

    return transform, coordinates
